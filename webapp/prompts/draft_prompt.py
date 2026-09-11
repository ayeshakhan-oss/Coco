"""Build the per-candidate user prompt from the evidence for THIS email type.

IMPORTANT: the candidate's name comes from the candidates table (passed in),
NEVER from scorecard.candidateName — some scorecards contain a mismatched name
(confirmed: application 3364).

Evidence is sourced PER TYPE and never mixed (Ayesha, 2026-09-11):

  cv_rejection  -> the candidate's own application material: CV text, cover
                   letter, application answers. The values scorecard is NOT
                   passed: a CV-stage candidate was never assessed on values, so
                   values evidence here can only produce a fabricated letter.
  values_feedback / warm_bench -> the values scorecard.
  gwc_rejection -> the GWC scorecard.

If the evidence for the chosen type is missing or blank, this module raises
MissingEvidence. It must never fall back to "(no structured scorecard
available)" and let the model write 1000 words from nothing — that is exactly
how an empty scorecard produced an invented CV rejection on application 3867.
"""

from __future__ import annotations

import json
from typing import Optional

# A CV read below this is not a real read (Skill 01 asks for a full read, with
# 10,000 chars as its own reference point for a complete CV).
MIN_CV_CHARS = 400


class MissingEvidence(Exception):
    """No usable evidence exists for this email type on this application."""


def _values_evidence(sc: dict) -> str:
    lines = []
    if sc.get("proceed_to_right_seat"):
        lines.append(f"Overall recommendation to proceed: {sc['proceed_to_right_seat']}")
    if sc.get("final_comments"):
        lines.append(f"Interviewer final comments: {sc['final_comments']}")
    lines.append("Per-value observations:")
    for v in sc.get("values", []):
        rating = v.get("rating") or "(no rating)"
        bits = [f"- {v.get('name', '')} [{rating}]"]
        if v.get("deep_dive"):
            bits.append(f"deep dive: {v['deep_dive']}")
        if v.get("curve_ball"):
            bits.append(f"curveball: {v['curve_ball']}")
        if v.get("micro_case"):
            bits.append(f"micro-case: {v['micro_case']}")
        lines.append("  " + " | ".join(bits))
    return "\n".join(lines)


def _values_is_empty(sc: dict) -> bool:
    """A scorecard whose value rows are all blank carries the six value NAMES
    and nothing else. Saved-but-never-filled is common (application 3867), and
    the names alone are not evidence about a person."""
    for v in sc.get("values", []):
        if any(v.get(k) for k in ("rating", "deep_dive", "curve_ball", "micro_case")):
            return False
    return not sc.get("final_comments")


def _gwc_evidence(sc: dict) -> str:
    lines = []
    if sc.get("final_mark"):
        lines.append(f"Final mark: {sc['final_mark']}")
    if sc.get("additional_comments"):
        lines.append(f"Interviewer comments: {sc['additional_comments']}")
    lines.append("Competency scores:")
    for c in sc.get("competencies", []):
        lines.append(f"  - {c.get('name', '')}: score {c.get('score')} (weight {c.get('weight')})")
    return "\n".join(lines)


def _gwc_is_empty(sc: dict) -> bool:
    if sc.get("final_mark") or sc.get("additional_comments"):
        return False
    return not any(c.get("score") not in (None, "") for c in sc.get("competencies", []))


def _answers_block(raw) -> list[str]:
    """Markaz stores application answers as JSON (shape varies by job form)."""
    if not raw:
        return []
    data = raw
    if isinstance(raw, str):
        try:
            data = json.loads(raw)
        except ValueError:
            return [raw.strip()] if raw.strip() else []
    lines = []
    if isinstance(data, dict):
        # The live Markaz shape is {"<epoch id>": {"question": ..., "answer": ...}}
        # for all 4,502 non-null rows. Emitting the raw key/value put an epoch
        # timestamp and a dict repr into the prompt as if it were the candidate
        # answering a question.
        for key, value in data.items():
            if isinstance(value, dict):
                question = value.get("question") or value.get("label") or ""
                answer = value.get("answer", value.get("value"))
                if answer in (None, "", [], {}):
                    continue
                if isinstance(answer, list):
                    answer = ", ".join(str(a) for a in answer if a)
                lines.append(f"  - {question}: {answer}".strip() if question
                             else f"  - {answer}")
            elif value not in (None, "", [], {}):
                lines.append(f"  - {key}: {value}")
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                q = item.get("question") or item.get("label") or item.get("key") or ""
                a = item.get("answer") or item.get("value") or ""
                if a:
                    lines.append(f"  - {q}: {a}".strip())
            elif item:
                lines.append(f"  - {item}")
    return lines


def _cv_evidence(ev: dict) -> str:
    """The candidate's own words: CV text, cover letter, application answers."""
    cv = (ev.get("cv_text") or "").strip()
    if len(cv) < MIN_CV_CHARS:
        detail = ev.get("cv_error") or (
            f"only {len(cv)} characters of CV text (need {MIN_CV_CHARS}+)"
        )
        raise MissingEvidence(
            f"Cannot draft a CV-stage rejection: {detail}. A CV rejection must be "
            "grounded in the candidate's actual CV. Read the CV by hand, or fix "
            "the uploaded file, then try again."
        )

    parts = [f"CANDIDATE'S CV (verbatim text of {ev.get('cv_file_name') or 'the uploaded file'}):",
             cv]

    cover = (ev.get("cover_letter") or "").strip()
    if cover:
        parts += ["", "COVER LETTER (verbatim):", cover]

    answers = _answers_block(ev.get("custom_answers")) + _answers_block(ev.get("canned_answers"))
    if answers:
        parts += ["", "APPLICATION ANSWERS (verbatim):"] + answers

    links = [f"{k}: {ev[k]}" for k in ("linkedin_url", "portfolio_url") if ev.get(k)]
    if links:
        parts += ["", "LINKS THEY PROVIDED: " + " | ".join(links)]

    return "\n".join(parts)


_EVIDENCE_HEADER = {
    "cv_rejection": (
        "The candidate's own application material below is the ONLY evidence you "
        "have. Every strength and every gap you name must be traceable to a "
        "specific line in it. If the CV does not show something, you do not know "
        "it: say what the application did not make clear, never what the person "
        "is like. Do not name or allude to our internal values, scorecards or "
        "interview frameworks: this candidate was never assessed on them."
    ),
    "_scorecard": (
        "Scorecard evidence to ground the email in (do not quote ratings or "
        "internal labels verbatim; translate them into plain, specific "
        "observations):"
    ),
}


def build_user_prompt(
    *,
    scorecard: Optional[dict],
    first_name: str,
    role: str,
    email_type: str,
    cv_evidence: Optional[dict] = None,
) -> str:
    """Assemble the drafting prompt, or raise MissingEvidence.

    `cv_evidence` is reads.get_cv_evidence() output and is REQUIRED for
    cv_rejection. `scorecard` is the normalized values/GWC scorecard and is
    required for the interview-stage types.
    """
    if email_type == "cv_rejection":
        if cv_evidence is None:
            raise MissingEvidence(
                "Cannot draft a CV-stage rejection: no application material was "
                "loaded for this candidate."
            )
        evidence = _cv_evidence(cv_evidence)
        header = _EVIDENCE_HEADER["cv_rejection"]
    elif scorecard and scorecard.get("kind") == "values":
        if _values_is_empty(scorecard):
            raise MissingEvidence(
                "Cannot draft this email: the values scorecard for this candidate "
                "is empty. It carries the six value names but no ratings, no "
                "interview notes and no final comments, so there is nothing to "
                "write from. Fill in the scorecard, or pick an email type whose "
                "evidence exists."
            )
        evidence = _values_evidence(scorecard)
        header = _EVIDENCE_HEADER["_scorecard"]
    elif scorecard and scorecard.get("kind") == "gwc":
        if _gwc_is_empty(scorecard):
            raise MissingEvidence(
                "Cannot draft this email: the GWC scorecard for this candidate is "
                "empty (no final mark, no comments, no competency scores)."
            )
        evidence = _gwc_evidence(scorecard)
        header = _EVIDENCE_HEADER["_scorecard"]
    else:
        raise MissingEvidence(
            f"Cannot draft a {email_type.replace('_', ' ')}: no scorecard exists "
            "for this candidate, so there is no evidence to ground the email in."
        )

    intent = {
        "cv_rejection": "an application-stage update letting them know we will not be moving forward, with specific, useful reflection",
        "values_feedback": "warm, specific feedback after a values-based interview",
        "warm_bench": "a 'not a yes for now' message that keeps the door open and is honest about the gap",
        "gwc_rejection": "an honest, dignified decision that we will not be moving forward, grounded in the interview",
        "case_study_outcome": (
            "a decision email for a candidate who submitted the case study but did not "
            "meet the 70% benchmark, walking them through what their work showed and "
            "where it could have been stronger, so the feedback is useful to them"
        ),
    }.get(email_type, "candidate communication")

    return f"""Draft {intent}.

Candidate first name (use this EXACTLY for the greeting; ignore any name inside
the scorecard): {first_name}
Role applied for: {role}

{header}

{evidence}

Write the email per the system rules and the output contract. Return JSON only."""
