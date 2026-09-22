"""KCD evaluation: a case study scored on Knowledge / Capacity / Design.

`webapp/services/kcd_evaluation.py` holds the locked rules -- the 0-to-5 scale
in half steps with a real zero, the verdict bands, the 60% GWC threshold, the
two caps, the conditional rule and the incomplete-submission split. This router
is the only code that persists one.

WHAT THIS IS NOT. It is not a model score. The SOP's own prerequisites are to
read the assignment, open every dataset and read an ideal answer BEFORE opening
a submission, and the app has access to none of those. A model asked to score
without them would produce exactly the ungrounded output CLAUDE.md Rule 29
exists to prevent. `routers/case_studies.py` is the model-scored,
benchmark-anchored path and is a different thing. This router records a human's
evaluation and refuses to let the rules be broken while doing it.

Rules enforced here, verbatim rule -> mechanism:

  1. `require_editor` gates writing an evaluation; reading needs a signed-in
     user.
  2. The verdict, the total and the GWC decision are COMPUTED from the scores
     and are never accepted from the client, even if it sends them.
  3. Caps are applied before the total, mechanically, and a cap can only lower
     a score (memory/lesson_marking_cap_is_a_ceiling_2026_09_11.md).
  4. A CONDITIONAL verdict without its condition is refused with 422, and the
     database carries the same rule as a CHECK constraint.
  5. An incomplete submission is never ranked against a complete one; the
     cohort endpoint returns two lists, not one sorted list.
  6. Re-evaluating SUPERSEDES: the previous current row is retired in the same
     transaction (CLAUDE.md Rule 25).

🔒 "KCD" is internal. Anything leaving the team says "case study"
   (memory/feedback_terminology.md).
"""

from __future__ import annotations

import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import text
from sqlalchemy.orm import Session

from ..db import get_db
from ..deps import get_current_user, require_editor
from ..models import KCDEvaluation
from ..schemas import (
    KCDCohortOut,
    KCDCrossCheckOut,
    KCDDimensionOut,
    KCDEvaluationOut,
    KCDEvaluationRequest,
    KCDFrameworkOut,
)
from ..services import kcd_evaluation as kcd
from ..services import reads

log = logging.getLogger("webapp.routers.kcd_evaluations")

router = APIRouter(prefix="/api/kcd-evaluations", tags=["kcd-evaluations"])

_CURRENT_FOR_JOB_SQL = text(
    "SELECT * FROM coco.kcd_evaluations WHERE job_id = :job_id AND is_current "
    "ORDER BY total DESC"
)
_FOR_APPLICATION_SQL = text(
    "SELECT * FROM coco.kcd_evaluations WHERE application_id = :application_id "
    "ORDER BY created_at DESC"
)


def _dimensions_out() -> list[KCDDimensionOut]:
    return [KCDDimensionOut(**d) for d in kcd.DIMENSIONS]


def _evaluation_out(row) -> KCDEvaluationOut:
    get = (lambda k: getattr(row, k)) if isinstance(row, KCDEvaluation) else row.__getitem__
    total = get("total")
    second = get("second_total")
    return KCDEvaluationOut(
        id=get("id"),
        application_id=get("application_id"),
        job_id=get("job_id"),
        candidate_name=get("candidate_name"),
        role=get("role"),
        scores=get("scores"),
        evidence=get("evidence"),
        weights=get("weights"),
        caps_applied=get("caps_applied") or {},
        total=total,
        verdict=get("verdict"),
        condition=get("condition"),
        advances_to_gwc=get("advances_to_gwc"),
        incomplete=get("incomplete"),
        missing_parts=get("missing_parts") or [],
        integrity_flags=get("integrity_flags") or [],
        second_evaluator=get("second_evaluator"),
        second_total=second,
        cross_check=KCDCrossCheckOut(**kcd.cross_check(total, second)),
        is_current=get("is_current"),
        superseded_by=get("superseded_by"),
        created_by=get("created_by"),
        created_at=get("created_at"),
        dimensions=_dimensions_out(),
        # Rendered here, once, so every reader sees the same caveat rather
        # than a bare number that reads like a capability score.
        display_score=kcd.format_incomplete_score(total) if get("incomplete") else None,
    )


@router.get("/framework", response_model=KCDFrameworkOut)
def framework(user: dict = Depends(get_current_user)):
    """The rules the form renders from, straight off the service."""
    return KCDFrameworkOut(
        dimensions=_dimensions_out(),
        scores=list(kcd.SCORES),
        verdicts=list(kcd.VERDICTS),
        gwc_threshold=kcd.GWC_ADVANCEMENT_THRESHOLD,
        cap_insight_without_evidence=kcd.CAP_INSIGHT_WITHOUT_EVIDENCE,
        cap_evidence_without_interpretation=kcd.CAP_EVIDENCE_WITHOUT_INTERPRETATION,
    )


@router.get("/jobs/{job_id}/cohort", response_model=KCDCohortOut)
def cohort(
    job_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    """A job's current evaluations, split into ranked and incomplete.

    Two lists rather than one sorted list, because the SOP forbids ranking an
    incomplete submission above a complete one and a single list would break
    that the first time a strong partial outscored a weak complete.
    """
    rows = db.execute(_CURRENT_FOR_JOB_SQL, {"job_id": job_id}).mappings().all()
    evaluations = [_evaluation_out(r) for r in rows]
    split = kcd.rank_results(
        [{"total": e.total, "incomplete": e.incomplete, "_e": e} for e in evaluations]
    )
    return KCDCohortOut(
        job_id=job_id,
        ranked=[r["_e"] for r in split["ranked"]],
        incomplete=[r["_e"] for r in split["incomplete"]],
        note=split["note"],
        gwc_threshold=kcd.GWC_ADVANCEMENT_THRESHOLD,
        # Stated as a number so a report never has to restate the threshold in
        # prose and get it wrong.
        advancing=sum(1 for e in evaluations if e.advances_to_gwc and not e.incomplete),
    )


@router.get("/evaluations", response_model=list[KCDEvaluationOut])
def list_evaluations(
    application_id: int = Query(...),
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    """Every evaluation for an application, newest first. A re-evaluated
    candidate's history stays visible with `is_current` saying which is live."""
    rows = db.execute(
        _FOR_APPLICATION_SQL, {"application_id": application_id}
    ).mappings().all()
    return [_evaluation_out(r) for r in rows]


@router.post("/evaluations", response_model=KCDEvaluationOut)
def create_evaluation(
    body: KCDEvaluationRequest,
    db: Session = Depends(get_db),
    user: dict = Depends(require_editor),
):
    app_row = reads.get_application(db, body.application_id)
    if not app_row:
        raise HTTPException(404, "Application not found")
    job_id = app_row.get("job_pk")
    if job_id is None:
        raise HTTPException(422, f"Application {body.application_id} has no job on record")

    # Every score needs its evidence. The SOP's whole premise is that it
    # evaluates the honesty of the METHOD, which is unreadable from a number.
    missing = [d["key"] for d in kcd.DIMENSIONS if not (body.evidence.get(d["key"]) or "").strip()]
    if missing:
        raise HTTPException(
            422,
            f"every dimension needs evidence behind its score; blank for: {missing}",
        )

    try:
        capped = kcd.apply_caps(
            {k: float(v) for k, v in body.scores.items()},
            insight_without_evidence=body.caps.insight_without_evidence,
            evidence_without_interpretation=body.caps.evidence_without_interpretation,
        )
        weights = {k: float(v) for k, v in body.weights.items()} if body.weights else None
        total = kcd.weighted_total(capped, weights)
        decision = kcd.verdict(total)
        kcd.validate_conditional(decision, body.condition)
    except kcd.KCDEvaluationError as exc:
        raise HTTPException(422, str(exc)) from exc

    candidate_name = " ".join(
        p for p in (app_row.get("first_name"), app_row.get("last_name")) if p
    ).strip() or "the candidate"

    row = KCDEvaluation(
        application_id=body.application_id,
        job_id=job_id,
        candidate_name=candidate_name,
        role=(app_row.get("job_title") or "the role").strip(),
        scores=capped,
        evidence=body.evidence,
        weights=weights,
        caps_applied={
            "insight_without_evidence": list(body.caps.insight_without_evidence),
            "evidence_without_interpretation": list(
                body.caps.evidence_without_interpretation
            ),
        },
        total=total,
        verdict=decision,
        # Only kept where it means something: a condition on a HIRE is noise.
        condition=body.condition if decision == kcd.CONDITIONAL else None,
        advances_to_gwc=kcd.advances_to_gwc(total),
        incomplete=body.incomplete,
        missing_parts=body.missing_parts,
        integrity_flags=body.integrity_flags,
        second_evaluator=body.second_evaluator,
        second_total=body.second_total,
        is_current=True,
        created_by=user.get("id") or "",
    )
    db.add(row)
    db.flush()

    # Rule 25: retire the previous number in the same transaction that creates
    # its replacement, so there is never a moment with two current ones.
    db.execute(
        text(
            "UPDATE coco.kcd_evaluations SET is_current = false, superseded_by = :new_id "
            "WHERE application_id = :application_id AND is_current AND id <> :new_id"
        ),
        {"new_id": row.id, "application_id": body.application_id},
    )
    db.commit()
    db.refresh(row)
    return _evaluation_out(row)
