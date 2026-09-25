"""Contract drafting (Skill 07): upload the masters, fill them, download.

`services/contracts.py` holds the routing and field rules, `contract_build.py`
does the fill and the validator pass, and this router is the only code that
stores a master or hands a finished document to anyone.

🔴 THE GENERATED DOCUMENT IS NEVER STORED. A filled contract carries a CNIC, a
   salary and sometimes an address. It is streamed straight back to whoever
   asked for it. `coco.contract_builds` records who built what for whom and
   whether the checks passed, which answers "was a contract issued for this
   person" without the database becoming a store of identity documents. The
   field VALUES are never written down, because the values are the PII.

🔴 A DOCUMENT THAT FAILS THE CHECKS IS NOT HANDED OVER. An unfilled
   placeholder is a HARD BLOCK, not a warning: on the first real build, four
   unfilled salary lines came back as warnings and the document would have
   been downloadable reading "Total Earnings PKR XYZ".

🔴 STRUCTURAL CHECKS ARE NOT VISUAL PROOF (CLAUDE.md Rule 14). Nothing here
   can see a page. Every response carries that caveat in its payload rather
   than relying on anyone to remember it.

🔴 UPLOADING A MASTER IS APPROVER-ONLY. These are approved legal documents and
   a wrong one silently changes every contract built afterwards.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import logging
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from ..db import get_db
from ..deps import get_current_user, require_approver, require_editor
from ..models import ContractBuild, ContractMaster
from ..services import contract_build as build
from ..services import contracts as spec

log = logging.getLogger("webapp.routers.contracts")

router = APIRouter(prefix="/api/contracts", tags=["contracts"])

#: A master is a Word document and nothing else. Guarding the size stops an
#: accidental upload of something enormous filling the database.
MAX_MASTER_BYTES = 10 * 1024 * 1024
DOCX_MIME = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"


def _utcnow() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


@router.get("/options")
def options(user: dict = Depends(get_current_user)):
    """Entities, engagements and document types, from the service.

    Served rather than duplicated in the frontend, so a document type cannot
    exist in the picker and not in the rules.
    """
    return {
        "entities": list(spec.ENTITIES),
        "engagements": [{"key": k, "label": v} for k, v in spec.ENGAGEMENTS.items()],
        "doc_types": [{"key": k, "label": v} for k, v in spec.DOC_TYPES.items()],
    }


@router.get("/masters")
def list_masters(db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    """Which masters have been uploaded, and which are still missing.

    The missing list is derived from the routing table rather than typed, so a
    master that exists in the rules but not in the database always shows up.
    """
    rows = {m.rel_path: m for m in db.query(ContractMaster).all()}
    needed = sorted({p for p in spec.MASTER_FOR.values() if p})
    return {
        "masters": [
            {
                "id": rows[p].id,
                "rel_path": p,
                "filename": rows[p].filename,
                "size_bytes": rows[p].size_bytes,
                "sha256": rows[p].sha256[:12],
                "field_count": rows[p].field_count,
                "uploaded_at": rows[p].uploaded_at,
            }
            for p in needed if p in rows
        ],
        "missing": [p for p in needed if p not in rows],
        "note": (
            "Masters are stored here rather than in the code, so no approved "
            "legal document enters the repository. Replacing one updates it in "
            "place: two versions of the same contract must never both be live."
        ),
    }


@router.post("/masters")
async def upload_master(
    rel_path: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: dict = Depends(require_approver),
):
    """Store or replace one approved master.

    Approver-only: a wrong file here silently changes every contract built
    afterwards, and nothing downstream would notice.
    """
    known = {p for p in spec.MASTER_FOR.values() if p}
    if rel_path not in known:
        raise HTTPException(
            400,
            f"{rel_path!r} is not a master this app knows about. Expected one "
            f"of: {sorted(known)}",
        )

    data = await file.read()
    if not data:
        raise HTTPException(400, "That file is empty.")
    if len(data) > MAX_MASTER_BYTES:
        raise HTTPException(400, "That file is larger than 10MB; it is not a master.")
    if not data.startswith(b"PK"):
        # .docx is a zip. A .doc or a PDF renamed does not become one.
        raise HTTPException(
            400,
            "That is not a .docx file. These masters must be Word documents; a "
            "renamed .doc or PDF cannot be filled.",
        )

    try:
        fields = spec.discover_fields(data)
    except Exception as exc:
        raise HTTPException(
            400,
            f"That file could not be read as a Word document ({type(exc).__name__}).",
        )
    if not fields:
        raise HTTPException(
            400,
            "That document has no fill fields at all. Either it is the wrong "
            "file, or its yellow highlighting was lost when it was last saved.",
        )

    digest = hashlib.sha256(data).hexdigest()
    row = db.query(ContractMaster).filter(ContractMaster.rel_path == rel_path).one_or_none()
    previous = row.field_count if row else None
    if row is None:
        row = ContractMaster(rel_path=rel_path)
        db.add(row)
    row.filename = file.filename or rel_path.rsplit("/", 1)[-1]
    row.content = data
    row.size_bytes = len(data)
    row.sha256 = digest
    row.field_count = len(fields)
    row.uploaded_at = _utcnow()
    row.uploaded_by = user.get("id") or ""
    db.commit()
    db.refresh(row)

    warning = None
    if previous is not None and previous != len(fields):
        # Rule 19's shape: a re-issued master shifts what every value means.
        warning = (
            f"This master previously had {previous} fill fields and now has "
            f"{len(fields)}. It has been re-issued. Check the fields before "
            "building anything from it."
        )
    log.info("contracts: master %s uploaded by %s", rel_path, user.get("email"))
    return {
        "rel_path": rel_path,
        "sha256": digest[:12],
        "field_count": len(fields),
        "warning": warning,
    }


@router.get("/plan")
def plan(
    engagement: str = Query(...),
    entity: str = Query(...),
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    """What would be built, what is missing, and what has to be filled in."""
    try:
        result = spec.plan(engagement, entity)
    except spec.ContractError as exc:
        raise HTTPException(400, str(exc))

    for item in result["documents"]:
        rel = item["master"]
        item["fields"] = []
        item["uploaded"] = False
        if not rel:
            continue
        row = db.query(ContractMaster).filter(ContractMaster.rel_path == rel).one_or_none()
        if row is None:
            result["blockers"].append(
                f"The master for {item['label']} has not been uploaded yet "
                f"({rel})."
            )
            continue
        item["uploaded"] = True
        fields = spec.discover_fields(row.content)
        item["fields"] = spec.group_fields(fields)
    return result


@router.post("/build")
def build_document(
    body: dict,
    db: Session = Depends(get_db),
    user: dict = Depends(require_editor),
):
    """Fill one document and stream it back. Nothing is stored.

    The response is the .docx itself, so the values never round-trip through
    the database. The checks run first, and a HARD BLOCK refuses the download.
    """
    entity = str(body.get("entity") or "")
    engagement = str(body.get("engagement") or "")
    doc_type = str(body.get("doc_type") or "")
    person = str(body.get("person_name") or "").strip()
    values = dict(body.get("values") or {})

    if not person:
        raise HTTPException(400, "A name is needed, for the file name if nothing else.")
    try:
        allowed = spec.documents_for(engagement, entity)
    except spec.ContractError as exc:
        raise HTTPException(400, str(exc))
    if doc_type not in allowed:
        # The volunteer-fellow rule lives here too: a contract simply is not
        # among the documents that engagement produces.
        raise HTTPException(
            400,
            f"A {spec.DOC_TYPES.get(doc_type, doc_type)} is not part of "
            f"{spec.ENGAGEMENTS.get(engagement, engagement)}. That engagement "
            f"produces: {', '.join(spec.DOC_TYPES[d] for d in allowed)}.",
        )

    rel = spec.master_for(entity, doc_type)
    if not rel:
        raise HTTPException(
            400,
            f"There is no approved master for a {spec.DOC_TYPES[doc_type]} at "
            f"{entity}. Ask Ayesha rather than using another entity's.",
        )
    row = db.query(ContractMaster).filter(ContractMaster.rel_path == rel).one_or_none()
    if row is None:
        raise HTTPException(400, f"The master {rel} has not been uploaded yet.")

    fields = spec.discover_fields(row.content)
    groups = spec.group_fields(fields)
    missing = spec.missing_values(groups, values)
    if missing:
        raise HTTPException(
            400,
            "These are still blank, and a contract never ships a blank: "
            + ", ".join(missing),
        )

    try:
        data = build.fill(row.content, spec.values_by_index(groups, values), fields=fields)
    except build.BuildError as exc:
        raise HTTPException(400, str(exc))

    report = build.validate(data, doc_type)
    record = ContractBuild(
        entity=entity, engagement=engagement, doc_type=doc_type,
        master_sha256=row.sha256, person_name=person,
        candidate_id=body.get("candidate_id"),
        application_id=body.get("application_id"),
        validator_passed=report.get("passed"),
        validator_report="; ".join(
            f"{f['severity']}: {f['message']}" for f in report.get("findings", [])
        )[:4000] or None,
        built_by=user.get("id") or "",
    )
    db.add(record)
    db.commit()

    if report.get("passed") is False:
        hard = [f["message"] for f in report["findings"] if f["severity"] == "HARD_BLOCK"]
        raise HTTPException(
            400,
            "This document did not pass its checks, so it has not been "
            "produced: " + "; ".join(hard[:6]),
        )

    filename = build.filename_for(doc_type, person)
    log.info("contracts: built %s for %s by %s", doc_type, person, user.get("email"))
    return StreamingResponse(
        iter([data]),
        media_type=DOCX_MIME,
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            # The file holds a CNIC and a salary. It must not sit in a cache.
            "Cache-Control": "private, no-store",
            "X-Coco-Visual-Check": "structure only, open and look at the page",
        },
    )


@router.get("/builds")
def recent_builds(
    limit: int = Query(50, ge=1, le=500),
    db: Session = Depends(get_db),
    user: dict = Depends(require_editor),
):
    """Which documents were produced, for whom. Never the documents."""
    rows = (
        db.query(ContractBuild)
        .order_by(ContractBuild.built_at.desc())
        .limit(limit)
        .all()
    )
    return [
        {
            "id": r.id,
            "entity": r.entity,
            "doc_type": r.doc_type,
            "label": spec.DOC_TYPES.get(r.doc_type, r.doc_type),
            "person_name": r.person_name,
            "validator_passed": r.validator_passed,
            "built_at": r.built_at,
        }
        for r in rows
    ]
