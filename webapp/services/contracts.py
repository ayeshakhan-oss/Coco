"""Contract drafting (Skill 07): which master, which documents, which fields.

SOURCE OF TRUTH: .claude/skills/07_contract-drafting/SKILL.md and TEMPLATE_MAP.md,
and CLAUDE.md Rules 14, 19 and 21.

🔴 MASTERS ARE NEVER COMMITTED. `Contracts\\` is gitignored and stays that way:
   these are approved legal documents, and putting them in git history is
   permanent. They are uploaded once through the app and stored in the
   database, so nothing confidential enters the repository.

🔴 THE FIELDS ARE READ FROM THE MASTER, NOT HARDCODED. Every fill field in
   these documents is a yellow-highlighted run, and the highlighted text is
   usually its own label ("EMPLOYEE NAME", "JOINING DATE", "CURRENT DATE").
   Discovering them means a master that changes shows a changed field list
   instead of silently filling the wrong place.

   ⚠️ Some placeholders are bare ("XYZ", "xyz", "X Y Z") and say nothing about
   what belongs there. Those are NOT guessed and NOT grouped: each is shown
   with the sentence it sits in, and a person decides. TEMPLATE_MAP records
   what they were on 2026-08-12, but a master can be re-issued, and a wrong
   guess here puts a CNIC where a salary goes.

🔴 A VOLUNTEER FELLOW NEVER RECEIVES A CONTRACT (Skill 07, Rule 8). That is a
   package rule, enforced in `documents_for()`, not a thing to remember.

🔴 STRUCTURAL CHECKS ARE NOT VISUAL PROOF (Rule 14). Nothing here can see a
   page. Every build says so, and asks for a human to look before it goes out.
"""

from __future__ import annotations

import io
import re
from typing import Optional

# --------------------------------------------------------------------------
# Entities and document types
# --------------------------------------------------------------------------

OPL, OWT, INC, NIETE = "OPL", "OWT", "Inc.", "NIETE"
ENTITIES = (OPL, OWT, INC, NIETE)

PERMANENT_CONTRACT = "permanent_contract"
PROJECT_CONTRACT = "project_contract"
FELLOW_CONTRACT = "fellow_contract"
PERMANENT_NDA = "permanent_nda"
FELLOW_NDA = "fellow_nda"
ADDENDUM = "addendum"

DOC_TYPES = {
    PERMANENT_CONTRACT: "Permanent Full-Time Contract",
    PROJECT_CONTRACT: "Project-Based Contract",
    FELLOW_CONTRACT: "Fellow / Internship Contract",
    PERMANENT_NDA: "Permanent Employee NDA",
    FELLOW_NDA: "Fellow NDA",
    ADDENDUM: "Addendum (promotion, same team)",
}

#: Which master file backs each (entity, doc_type), from TEMPLATE_MAP.md.
#: `None` means no approved master exists — ask Ayesha, never substitute one.
#: The NDAs and the addendum are single Orenda masters serving all entities.
MASTER_FOR: dict[tuple[str, str], Optional[str]] = {
    (OPL, PERMANENT_CONTRACT): "OPL/Template Full Time - OPL Contract.docx",
    (OWT, PERMANENT_CONTRACT): "OWT/Template Full Time Employment  OWT - Contract.docx",
    (INC, PERMANENT_CONTRACT): "INC/Template - Contract Taleemabad Inc.  .docx",
    (NIETE, PERMANENT_CONTRACT): None,   # only project-based exists

    (NIETE, PROJECT_CONTRACT): "NIETE/NIETE - Project-based Employment Contract.docx",
    # OPL project-based intentionally uses the same master (OPL letterhead).
    (OPL, PROJECT_CONTRACT): "Fellow/Template - Project-based Employment Contract.docx",
    (OWT, PROJECT_CONTRACT): None,       # "There's only OWT full time"
    (INC, PROJECT_CONTRACT): None,

    (OPL, FELLOW_CONTRACT): "Fellow/Template - Project-based Employment Contract.docx",
    (OWT, FELLOW_CONTRACT): "Fellow/Template - Project-based Employment Contract.docx",
    (INC, FELLOW_CONTRACT): "Fellow/Template - Project-based Employment Contract.docx",
    (NIETE, FELLOW_CONTRACT): "Fellow/Template - Project-based Employment Contract.docx",
}
for _e in ENTITIES:
    MASTER_FOR[(_e, PERMANENT_NDA)] = "Promotion/Template - NDA Full Time Permanent Employee.docx"
    MASTER_FOR[(_e, FELLOW_NDA)] = "Fellow/Template - NDA Fellow Employee.docx"
    MASTER_FOR[(_e, ADDENDUM)] = "Addendum/Template  - Addendum Orenda.docx"


class ContractError(ValueError):
    """The package cannot be built as described."""


def master_for(entity: str, doc_type: str) -> Optional[str]:
    if entity not in ENTITIES:
        raise ContractError(f"unknown entity {entity!r}; must be one of {list(ENTITIES)}")
    if doc_type not in DOC_TYPES:
        raise ContractError(f"unknown document type {doc_type!r}")
    return MASTER_FOR.get((entity, doc_type))


# --------------------------------------------------------------------------
# What a given engagement actually needs
# --------------------------------------------------------------------------

PAID_FELLOW = "paid_fellow"
VOLUNTEER_FELLOW = "volunteer_fellow"
FELLOW_TO_PAID = "fellow_to_paid"
PERMANENT_HIRE = "permanent_hire"
PROJECT_HIRE = "project_hire"
PROMOTION_SAME_TEAM = "promotion_same_team"
TEAM_MOVE = "team_move"

ENGAGEMENTS = {
    PAID_FELLOW: "Fellow, paid",
    VOLUNTEER_FELLOW: "Fellow, volunteer or unpaid",
    FELLOW_TO_PAID: "Fellow moving from unpaid to paid",
    PERMANENT_HIRE: "New permanent full-time hire",
    PROJECT_HIRE: "New project-based hire",
    PROMOTION_SAME_TEAM: "Promotion within the same team",
    TEAM_MOVE: "Move to a different team",
}


def documents_for(engagement: str, entity: str) -> list[str]:
    """The documents this engagement needs, in order.

    🔴 A VOLUNTEER FELLOW GETS AN NDA AND NOTHING ELSE. Skill 07 Rule 8, and
       the one that would do real harm if forgotten: sending an unpaid person
       an employment contract creates an obligation nobody agreed to.

    🔴 An unpaid-to-paid transition gets the CONTRACT ONLY. The NDA was signed
       when they started, and a second one implies the first did not count.
    """
    if engagement not in ENGAGEMENTS:
        raise ContractError(f"unknown engagement {engagement!r}")
    if entity not in ENTITIES:
        raise ContractError(f"unknown entity {entity!r}")

    if engagement == VOLUNTEER_FELLOW:
        return [FELLOW_NDA]
    if engagement == PAID_FELLOW:
        return [FELLOW_CONTRACT, FELLOW_NDA]
    if engagement == FELLOW_TO_PAID:
        return [FELLOW_CONTRACT]
    if engagement == PERMANENT_HIRE:
        return [PERMANENT_CONTRACT, PERMANENT_NDA]
    if engagement == PROJECT_HIRE:
        return [PROJECT_CONTRACT, PERMANENT_NDA]
    if engagement == PROMOTION_SAME_TEAM:
        return [ADDENDUM]
    if engagement == TEAM_MOVE:
        # A move to another team is a NEW contract, not an addendum.
        return [PERMANENT_CONTRACT]
    raise ContractError(f"no document rule for {engagement!r}")


def plan(engagement: str, entity: str) -> dict:
    """What would be built, and what is missing, before anything is built."""
    docs = documents_for(engagement, entity)
    items, blockers = [], []
    for doc_type in docs:
        rel = master_for(entity, doc_type)
        items.append({
            "doc_type": doc_type,
            "label": DOC_TYPES[doc_type],
            "master": rel,
        })
        if rel is None:
            blockers.append(
                f"There is no approved master for a {DOC_TYPES[doc_type]} at "
                f"{entity}. Ask Ayesha rather than substituting another entity's."
            )
    return {
        "engagement": engagement,
        "engagement_label": ENGAGEMENTS[engagement],
        "entity": entity,
        "documents": items,
        "blockers": blockers,
        # Rule 14, stated on every plan rather than remembered.
        "caveat": (
            "Nothing here can see a page. The checks verify structure, never "
            "appearance, so every generated document still has to be opened "
            "and looked at before it goes to anyone."
        ),
    }


# --------------------------------------------------------------------------
# Reading the fill fields out of a master
# --------------------------------------------------------------------------

#: Placeholders that say nothing about what belongs in them. These are never
#: grouped with each other and never auto-labelled: "XYZ" is a duration in one
#: place and a CNIC in another, and a wrong guess puts a national ID number
#: where a salary goes.
_OPAQUE = re.compile(r"^[\sxyz.,/-]*$", re.I)

_WS = re.compile(r"\s+")


def _norm(text: str) -> str:
    return _WS.sub(" ", (text or "").replace("’", "'")).strip()


def is_opaque(placeholder: str) -> bool:
    """True when the placeholder text does not name its own field."""
    return bool(_OPAQUE.match(_norm(placeholder)))


def _segments(paragraph):
    from scripts.utils.contract_builder import highlighted_segments

    return highlighted_segments(paragraph)


#: Placeholder strings that appear in these masters WITHOUT highlighting.
#: Discovered on the NIETE compensation cell, which reads "Total Earnings PKR
#: XYZ / Base Salary: PKR XYZ / Medical: PKR XYZ / Others: PKR XYZ" with only
#: ONE of the four highlighted. Filling the highlighted runs alone leaves
#: "PKR XYZ" printed on a real contract, in the salary line.
#: Ordered longest-first so "X Y Z" is matched before "XYZ".
TEXT_PLACEHOLDERS = (
    "EMPLOYEE'S NAME", "EMPLOYEE'S CNIC", "EMPLOYEE NAME", "EMPLOYER NAME",
    "EFFECTIVE DATE OF JOINING", "JOINING DATE", "CURRENT DATE",
    "DATE, MONTH, YEAR", "FELLOW NAME", "X Y Z", "XYZ",
)


def _placeholder_hits(text: str) -> list[str]:
    """Which placeholder strings are still literally present in `text`.

    Longest-first with the matched span blanked out, so "X Y Z" is not also
    reported as "XYZ" and one occurrence is never counted twice.
    """
    remaining = text or ""
    hits = []
    for token in TEXT_PLACEHOLDERS:
        while True:
            at = remaining.upper().find(token.upper())
            if at < 0:
                break
            hits.append(token)
            remaining = remaining[:at] + (" " * len(token)) + remaining[at + len(token):]
    return hits


def all_paragraphs(doc):
    """Every paragraph in the document, including headers and footers.

    `discover_fields` walks body then tables to match the fill order. This one
    is for CHECKING, where missing a header would mean shipping a contract
    with a placeholder printed at the top of every page.
    """
    for paragraph in doc.paragraphs:
        yield paragraph, "body"
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    yield paragraph, "table"
    for section in doc.sections:
        for part, label in ((section.header, "header"), (section.footer, "footer")):
            for paragraph in part.paragraphs:
                yield paragraph, label
            for table in part.tables:
                for row in table.rows:
                    for cell in row.cells:
                        for paragraph in cell.paragraphs:
                            yield paragraph, label


def unresolved_placeholders(data: bytes) -> list[dict]:
    """Placeholder text still present in a document, anywhere.

    This is the check that a fill actually finished. It looks at headers and
    footers too, which the fill walk deliberately does not.
    """
    from docx import Document

    out = []
    doc = Document(io.BytesIO(data))
    for paragraph, where in all_paragraphs(doc):
        for token in _placeholder_hits(paragraph.text):
            out.append({
                "token": token,
                "where": where,
                "context": _norm(paragraph.text)[:240],
            })
    return out


def discover_fields(data: bytes) -> list[dict]:
    """Every fill field in a master, in document order.

    A fill field is a contiguous run of yellow-highlighted text. Reading them
    from the document means a re-issued master presents a changed field list
    rather than quietly filling values into the wrong places.
    """
    from docx import Document

    doc = Document(io.BytesIO(data))
    fields: list[dict] = []

    def take(paragraph, where: str):
        for seg in _segments(paragraph):
            placeholder = "".join(r.text for r in seg)
            fields.append({
                "index": len(fields),
                "placeholder": _norm(placeholder),
                "context": _norm(paragraph.text)[:240],
                "location": where,
                "opaque": is_opaque(placeholder),
            })

    for paragraph in doc.paragraphs:
        take(paragraph, "body")
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    take(paragraph, "table")

    # 🔴 AND THE ONES NOBODY HIGHLIGHTED. The NIETE compensation cell reads
    # "Total Earnings PKR XYZ / Base Salary: PKR XYZ / Medical: PKR XYZ /
    # Others: PKR XYZ" with only ONE of the four highlighted, and the
    # acceptance line carries an unhighlighted JOINING DATE. Filling only the
    # highlighted runs leaves "PKR XYZ" printed in the salary line of a real
    # contract. These are appended AFTER the highlighted fields so the
    # highlighted indexes stay stable.
    fields.extend(_text_fields(doc, start=len(fields)))
    return fields


def _highlighted_tokens(paragraph) -> list[str]:
    """Which placeholder tokens the highlighted runs of this paragraph cover."""
    covered: list[str] = []
    for segment in _segments(paragraph):
        covered.extend(_placeholder_hits("".join(r.text for r in segment)))
    return covered


def _text_fields(doc, start: int) -> list[dict]:
    """Placeholder strings present as plain text rather than highlighting.

    🔴 OCCURRENCES ALREADY COVERED BY HIGHLIGHTING ARE SUBTRACTED. "EMPLOYEE
    NAME" in the parties clause is highlighted and is already field 4; listing
    it again here would ask for the same value twice and make the field count
    meaningless. Only the SURPLUS occurrences in a paragraph are new fields.
    """
    out: list[dict] = []
    for ordinal, (paragraph, where) in enumerate(all_paragraphs(doc)):
        seen: dict[str, int] = {}
        already = _highlighted_tokens(paragraph)
        skip: dict[str, int] = {}
        for token in already:
            skip[token] = skip.get(token, 0) + 1
        for token in _placeholder_hits(paragraph.text):
            if skip.get(token):
                # This occurrence is the highlighted one; it is filled already.
                skip[token] -= 1
                seen[token] = seen.get(token, 0) + 1
                continue
            occurrence = seen.get(token, 0)
            seen[token] = occurrence + 1
            out.append({
                "index": start + len(out),
                "placeholder": token,
                "context": _norm(paragraph.text)[:240],
                "location": f"{where} (not highlighted)",
                "opaque": is_opaque(token),
                # How the filler finds this exact spot again.
                "para_ordinal": ordinal,
                "occurrence": occurrence,
                "text_token": token,
            })
    return out


def group_fields(fields: list[dict]) -> list[dict]:
    """One input per distinct named placeholder; opaque ones stay separate.

    "EMPLOYEE NAME" appears twice in the NDA and means the same person both
    times, so it is typed once. "XYZ" appears three times in the project
    contract meaning three different things, so it is never merged.

    ⚠️ A merged group is FLAGGED when its occurrences sit in different
    sentences (`spans_contexts`). Identical placeholder text does not
    guarantee an identical value: a master with "DATE, MONTH, YEAR" twice
    could mean the start AND the end of a term, and filling one value into
    both would silently produce a contract that begins and ends on the same
    day. The UI shows every context so a person can see what they are filling.
    """
    groups: list[dict] = []
    by_name: dict[str, dict] = {}
    for f in fields:
        key = f["placeholder"].upper()
        if f["opaque"] or key not in by_name:
            group = {
                "key": f"f{f['index']}" if f["opaque"] else key,
                "placeholder": f["placeholder"],
                "label": f["placeholder"] if not f["opaque"] else "",
                "contexts": [f["context"]],
                "indexes": [f["index"]],
                "opaque": f["opaque"],
            }
            groups.append(group)
            if not f["opaque"]:
                by_name[key] = group
        else:
            by_name[key]["indexes"].append(f["index"])
            if f["context"] not in by_name[key]["contexts"]:
                by_name[key]["contexts"].append(f["context"])
    for g in groups:
        # One value will be written into several different sentences. Say so.
        g["spans_contexts"] = len(g["indexes"]) > 1 and len(g["contexts"]) > 1
    return groups


def missing_values(groups: list[dict], values: dict) -> list[str]:
    """Which inputs have not been filled. A contract never ships a blank.

    Skill 07 Rule 6: never invent a field. Leave it visibly open and ask.
    """
    return [g["key"] for g in groups if not str(values.get(g["key"]) or "").strip()]


def values_by_index(groups: list[dict], values: dict) -> dict[int, str]:
    """Flatten {input key: text} onto {field index: text} for the builder."""
    out: dict[int, str] = {}
    for g in groups:
        text = str(values.get(g["key"]) or "")
        for i in g["indexes"]:
            out[i] = text
    return out
