"""Filling a master: master bytes + values -> a finished .docx, in memory.

The document mechanics come from `scripts/utils/contract_builder.py`, which is
the same code the Claude Code build scripts use. This module adds nothing to
how a run is filled; it only does it in memory, against an uploaded master,
without touching disk.

🔴 THE MASTER IS NEVER MODIFIED. It is loaded from bytes into a fresh
   in-memory document every time, so there is no copy-then-edit step that
   could write back over an approved legal file.

🔴 THE COUNT IS ASSERTED. `fill_at` writes by field index, and every index must
   exist in the document being filled. A master re-issued with a different
   number of highlighted fields fails here rather than shifting every value
   one place along, which is the failure that produces a contract with a CNIC
   in the salary line and looks entirely normal until someone reads it.

🔴 NOTHING HERE CAN SEE A PAGE (CLAUDE.md Rule 14). The validator checks
   structure. Layout, spacing and page breaks are invisible to it, and the
   Muhammad Shayan package took four pilot rounds on exactly that. Every
   result carries the caveat, and it is not softened.
"""

from __future__ import annotations

import io
from typing import Optional

from . import contracts as spec


class BuildError(ValueError):
    """The document cannot be produced as asked."""


def _iter_field_paragraphs(doc):
    """Every paragraph that can hold a fill field, in the same order as
    `contracts.discover_fields` walks them: body first, then tables."""
    for paragraph in doc.paragraphs:
        yield paragraph
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    yield paragraph


def _replace_in_runs(paragraph, token: str, occurrence: int, value: str) -> bool:
    """Replace the nth occurrence of `token` in a paragraph's runs.

    🔴 REFUSES RATHER THAN MANGLES. If the token is split across runs, this
    returns False instead of rewriting the paragraph, because rebuilding runs
    destroys the bold, the underline and the highlighting that carry meaning
    in a contract. The caller turns that into a clear failure.
    """
    seen = 0
    lowered = token.lower()
    for run in paragraph.runs:
        text = run.text
        start = 0
        while True:
            at = text.lower().find(lowered, start)
            if at < 0:
                break
            if seen == occurrence:
                run.text = text[:at] + value + text[at + len(token):]
                return True
            seen += 1
            start = at + len(token)
    return False


def fill(data: bytes, values_by_index: dict[int, str],
         fields: Optional[list[dict]] = None) -> bytes:
    """Return the filled document as bytes.

    `values_by_index` maps the field positions produced by
    `contracts.discover_fields` to the text that replaces them. `fields` is
    that same list, needed to place the plain-text placeholders that carry no
    highlighting.
    """
    from docx import Document

    from scripts.utils.contract_builder import fill_segment, highlighted_segments

    doc = Document(io.BytesIO(data))

    index = 0
    filled = 0
    for paragraph in _iter_field_paragraphs(doc):
        for segment in highlighted_segments(paragraph):
            if index in values_by_index:
                fill_segment(segment, values_by_index[index])
                filled += 1
            index += 1

    # The placeholders nobody highlighted: the four salary lines and the
    # acceptance joining date. Located by paragraph ordinal across the WHOLE
    # document, headers included, which is how they are discovered.
    text_fields = [f for f in (fields or []) if f.get("text_token")]
    if text_fields:
        paragraphs = [par for par, _ in spec.all_paragraphs(doc)]
        refused = []
        for f in text_fields:
            if f["index"] not in values_by_index:
                continue
            ordinal = f.get("para_ordinal")
            if ordinal is None or ordinal >= len(paragraphs):
                refused.append(f["placeholder"])
                continue
            ok = _replace_in_runs(
                paragraphs[ordinal], f["text_token"], f.get("occurrence", 0),
                values_by_index[f["index"]],
            )
            if ok:
                filled += 1
            else:
                refused.append(f"{f['placeholder']} in {f['context'][:60]!r}")
        if refused:
            raise BuildError(
                "These placeholders could not be filled because the text is "
                "split across differently formatted pieces, and rewriting it "
                "would destroy the formatting: " + "; ".join(refused)
            )

    if index == 0:
        raise BuildError(
            "This master has no highlighted fill fields. Either the wrong file "
            "was uploaded, or the highlighting was lost when it was last saved."
        )
    # Every value must have landed. A value with nowhere to go means the master
    # changed under the field list, and the rest of the values are then
    # very likely in the wrong places too.
    text_indexes = {f["index"] for f in (fields or []) if f.get("text_token")}
    unplaced = sorted(i for i in values_by_index if i >= index and i not in text_indexes)
    if unplaced:
        raise BuildError(
            f"The master has {index} fill fields but values were given for "
            f"positions {unplaced}. It looks like this master was re-issued. "
            "Re-upload it and check the fields before building."
        )
    if filled != len(values_by_index):
        raise BuildError(
            f"Expected to fill {len(values_by_index)} fields but filled {filled}."
        )

    out = io.BytesIO()
    doc.save(out)
    return out.getvalue()


def validate(data: bytes, doc_type: str) -> dict:
    """Run the existing contract validator over the generated document.

    🔴 `contract_docx_eval.py --type` DEFAULTS TO `fellow`, and a project-based
       contract validated as a fellow one throws 11 FALSE hard blocks
       (CLAUDE.md Rule 19). The masters are near-identical, so the validator
       cannot infer the type. It is passed explicitly here, mapped from our own
       document type, and an unmapped type is a refusal rather than a default.
    """
    import tempfile
    from pathlib import Path

    kind = _VALIDATOR_TYPE.get(doc_type)
    if kind is None:
        raise BuildError(
            f"No validator profile for {doc_type!r}. Rather than validate it as "
            "the wrong kind of document, this refuses: the masters are "
            "near-identical and the wrong profile reports false failures."
        )

    try:
        from scripts.evals.contract_docx_eval import evaluate_contract
    except Exception as exc:  # pragma: no cover - the module ships with the image
        return {
            "ran": False,
            "passed": None,
            "findings": [],
            "note": f"The validator could not be loaded ({type(exc).__name__}), "
                    "so this document has not been checked.",
        }

    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "generated.docx"
        path.write_bytes(data)
        try:
            result = evaluate_contract(path, kind)
        except Exception as exc:
            return {
                "ran": False,
                "passed": None,
                "findings": [],
                "note": f"The validator errored ({type(exc).__name__}: {exc}), so "
                        "this document has not been checked.",
            }

    findings = _findings(result)

    # 🔴 A LEFTOVER PLACEHOLDER IS A HARD BLOCK HERE, whatever the shared
    #    validator calls it. On the first real build of a NIETE contract the
    #    validator reported the four unfilled salary lines as WARNINGs and this
    #    wrapper returned passed=True -- a document reading "Total Earnings PKR
    #    XYZ" would have been offered for download. An unfilled field is never
    #    a warning on a contract.
    for left in spec.unresolved_placeholders(data):
        findings.append({
            "severity": "HARD_BLOCK",
            "message": (
                f"{left['token']!r} is still in the document, in the "
                f"{left['where']}: {left['context'][:120]}"
            ),
        })

    hard = [f for f in findings if f.get("severity") == "HARD_BLOCK"]
    return {
        "ran": True,
        "passed": not hard,
        "findings": findings,
        "note": None,
    }


#: Our document type -> the validator's own `--type` value.
_VALIDATOR_TYPE = {
    spec.FELLOW_CONTRACT: "fellow",
    spec.FELLOW_NDA: "fellow",
    spec.PROJECT_CONTRACT: "project",
    spec.PERMANENT_CONTRACT: "project",
    spec.PERMANENT_NDA: "fellow",
    spec.ADDENDUM: "project",
}


def _findings(result) -> list[dict]:
    """Normalise whatever the validator returns into a list of findings.

    Written defensively on purpose: the validator is shared with the CLI and
    its return shape is not this module's to fix. An unrecognised shape is
    reported as one finding rather than crashing the build.
    """
    if result is None:
        return []
    if isinstance(result, dict):
        for key in ("violations", "findings", "failures", "issues"):
            if isinstance(result.get(key), list):
                return [_one(f) for f in result[key]]
        return []
    if isinstance(result, (list, tuple)):
        return [_one(f) for f in result]
    return [{"severity": "INFO", "message": str(result)[:400]}]


def _one(finding) -> dict:
    if isinstance(finding, dict):
        return {
            "severity": str(finding.get("severity") or finding.get("level") or "WARNING"),
            "message": str(
                finding.get("message") or finding.get("detail")
                or finding.get("rule") or finding
            )[:400],
        }
    return {"severity": "WARNING", "message": str(finding)[:400]}


#: Said on every build. Rule 14, not softened.
VISUAL_CAVEAT = (
    "These checks verify structure, never appearance. Nothing here can see a "
    "page, so open the document and look at it before it goes to anyone. The "
    "defects that have cost the most rounds were all invisible to a checker."
)


def filename_for(doc_type: str, person_name: str) -> str:
    """A predictable, human filename. No CNIC, no salary."""
    label = spec.DOC_TYPES.get(doc_type, doc_type).replace("/", "-")
    name = " ".join(str(person_name or "").split()) or "Unnamed"
    safe = "".join(ch for ch in f"{label} - {name}" if ch.isalnum() or ch in " -_.,()")
    return f"{safe.strip()}.docx"
