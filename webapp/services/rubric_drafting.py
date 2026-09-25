"""Draft a screening rubric from a job description, in Nugget's own shape.

Two things happen here. `draft_rubric` asks the model for the dimensions,
filters and thresholds. `compose_system_prompt` then renders those into the
SCORING prompt that gets stored on the rubric row, in the same layout Nugget's
own rubrics use, because that stored prompt is the entire scoring contract: the
engine reads it back per candidate and never reconstructs it.

🔴 NOTHING IS PUBLISHED FROM HERE. `draft_rubric` returns an unsaved draft. A
person reads it and publishes it (`screening_runs.publish_rubric`). A rubric
decides how every applicant to a role is judged, and a structural check that it
has five dimensions whose weights sum to something sensible verifies shape,
never judgement.
"""

from __future__ import annotations

import logging
from typing import Any, Optional

from ..prompts import rubric_drafting_prompt

log = logging.getLogger("webapp.rubric_drafting")

SENIORITIES = ("junior", "mid", "senior", "lead", "exec")
REQUIRED_ANCHORS = ("0", "1", "2", "3", "4", "5")
MIN_DIMENSIONS = 3
MAX_DIMENSIONS = 8


class RubricDraftError(ValueError):
    """The model's draft does not satisfy the rubric contract."""


def _call_model(*, system: str, user: str) -> tuple[dict, str]:
    """Module-level so tests monkeypatch it and never make a real call."""
    from . import drafting

    drafter = drafting.get_drafter()
    if isinstance(drafter, drafting.StubDrafter):
        raise drafting.DraftingUnavailable(
            "No Anthropic credential configured: get_drafter() returned the "
            "offline StubDrafter, whose output is an email-shaped placeholder, "
            "never a rubric."
        )
    parsed = drafter.draft(
        system=system, user=user, email_type="rubric_drafting",
        first_name="", role="", prior_violations=None, attempt=0,
    )
    return parsed, (getattr(drafter, "model", None) or "unknown")


def validate_draft(draft: Any) -> dict:
    """Reject a draft that would be unsafe or unusable. Raises, never repairs.

    🔴 A MISSING 0 ANCHOR IS THE ONE THIS EXISTS FOR. Scoring anchors that
    start at 1 put a floor of a fifth of every weight under every candidate,
    and that floor is what put all 25 RM case studies above a published 70%
    bar. It is invisible in a rendered rubric and obvious here.
    """
    if not isinstance(draft, dict):
        raise RubricDraftError("the draft is not an object")

    title = (draft.get("title") or "").strip()
    if not title:
        raise RubricDraftError("the draft has no title")

    seniority = (draft.get("seniority") or "").strip().lower()
    if seniority not in SENIORITIES:
        raise RubricDraftError(
            f"seniority {seniority!r} is not one of {list(SENIORITIES)}"
        )

    dims = draft.get("dimensions")
    if not isinstance(dims, list) or not MIN_DIMENSIONS <= len(dims) <= MAX_DIMENSIONS:
        raise RubricDraftError(
            f"expected {MIN_DIMENSIONS} to {MAX_DIMENSIONS} dimensions, "
            f"got {len(dims) if isinstance(dims, list) else 'none'}"
        )

    seen: set[str] = set()
    cleaned_dims = []
    for dim in dims:
        key = (dim.get("key") or "").strip()
        if not key or key in seen:
            raise RubricDraftError(f"dimension key {key!r} is missing or repeated")
        seen.add(key)
        try:
            weight = int(dim.get("weight"))
        except (TypeError, ValueError) as exc:
            raise RubricDraftError(f"dimension {key!r} has no numeric weight") from exc
        if weight < 1:
            raise RubricDraftError(f"dimension {key!r} has weight {weight}")

        anchors = dim.get("anchors") or {}
        anchors = {str(k): v for k, v in anchors.items()}
        missing = [a for a in REQUIRED_ANCHORS if not (anchors.get(a) or "").strip()]
        if missing:
            raise RubricDraftError(
                f"dimension {key!r} is missing anchors {missing}. Every "
                "dimension needs all six, and the 0 anchor must describe "
                "absence: anchoring the bottom of the scale at 1 floors every "
                "candidate at a fifth of the weight."
            )
        cleaned_dims.append({
            "key": key,
            "label": (dim.get("label") or key.replace("_", " ").capitalize()),
            "weight": weight,
            "core": bool(dim.get("core")),
            "max": 5,
            "anchors": {a: anchors[a].strip() for a in REQUIRED_ANCHORS},
            "look_for": [str(x) for x in (dim.get("look_for") or [])][:6],
            "common_gaps": [str(x) for x in (dim.get("common_gaps") or [])][:6],
        })

    if not any(d["core"] for d in cleaned_dims):
        raise RubricDraftError("no dimension is marked core, so no gate can be set")

    filters = []
    for f in (draft.get("hard_filters") or []):
        key = (f.get("key") or "").strip()
        if not key:
            continue
        action = (f.get("action") or "flag").strip().lower()
        if action not in ("reject", "flag"):
            action = "flag"
        rule = (f.get("rule") or "").strip()
        if not rule:
            raise RubricDraftError(f"hard filter {key!r} has no rule text")
        # University or education filters must never reject. The SOP is
        # explicit: "Never fail on this. It is a tie-breaker between comparable
        # candidates and nothing more."
        if action == "reject" and any(
            word in key.lower() for word in ("university", "college", "school", "degree_tier")
        ):
            action = "flag"
        filters.append({
            "key": key,
            "label": f.get("label") or key.replace("_", " ").capitalize(),
            "rule": rule,
            "action": action,
            "on_unknown": (f.get("on_unknown") or "flag").strip().lower(),
        })

    thresholds = draft.get("thresholds") or {}
    for tier in ("p1", "p2", "p3"):
        if thresholds.get(tier) is None:
            raise RubricDraftError(f"thresholds is missing {tier}")
    if not (
        float(thresholds["p1"]) > float(thresholds["p2"]) > float(thresholds["p3"])
    ):
        raise RubricDraftError("thresholds must descend p1 > p2 > p3")
    thresholds.setdefault("basis", "absolute")

    gates = thresholds.get("gates") or {}
    core_keys = {d["key"] for d in cleaned_dims if d["core"]}
    for tier, gate in list(gates.items()):
        for key in list((gate or {}).get("min_dimension") or {}):
            if key not in core_keys:
                # A gate naming a dimension that is not core, or not present at
                # all, silently never fires. Drop it rather than ship a gate
                # that looks like a safeguard and is not one.
                del gates[tier]["min_dimension"][key]
    thresholds["gates"] = gates

    min_years = draft.get("min_years")
    try:
        min_years = float(min_years) if min_years is not None else None
    except (TypeError, ValueError):
        min_years = None

    return {
        "title": title,
        "seniority": seniority,
        "min_years": min_years,
        "dimensions": cleaned_dims,
        "hard_filters": filters,
        "thresholds": thresholds,
        "max_score": 100,
        "manual_review_rules": {"min_resume_chars": 500, "min_resume_health": 60},
    }


def compose_system_prompt(
    *, draft: dict, job_title: str, department: Optional[str],
    location: Optional[str], job_description: str,
) -> str:
    """Render the SCORING prompt stored on the rubric row.

    Laid out the way Nugget's own stored prompts are, because a rubric is read
    back and executed from this text alone: dimension header, six anchors
    descending, look-for cues, common gaps. Keeping the layout identical means
    a rubric Coco publishes and one Nugget published are scored the same way.
    """
    lines: list[str] = []
    lines.append(
        "You are screening candidates for one role at Taleemabad, an education "
        "non-profit in Pakistan."
    )
    lines.append("")
    lines.append(f"ROLE: {job_title}")
    lines.append(f"DEPARTMENT: {department or 'not stated'}")
    lines.append(f"LOCATION: {location or 'not stated'}")
    lines.append("")
    lines.append("--- JOB DESCRIPTION ---")
    lines.append(job_description.strip())
    lines.append("--- END JOB DESCRIPTION ---")
    lines.append("")
    lines.append("# How to score")
    lines.append("")
    lines.append(
        "Score each dimension 0 to 5 against the anchors below. An absent skill "
        "scores 0, not a middling guess. Quote your evidence from the CV rather "
        "than summarising it, and quote nothing that is not there."
    )
    lines.append("")

    for dim in draft["dimensions"]:
        core = " - CORE" if dim["core"] else ""
        lines.append(
            f"{dim['label']} [key: {dim['key']}] - 0 to 5, weighted x{dim['weight']}{core}"
        )
        for score in ("5", "4", "3", "2", "1", "0"):
            lines.append(f"  {score}: {dim['anchors'][score]}")
        if dim["look_for"]:
            lines.append("  Look for: " + "; ".join(dim["look_for"]))
        if dim["common_gaps"]:
            lines.append("  Common gaps: " + "; ".join(dim["common_gaps"]))
        lines.append("")

    if draft["hard_filters"]:
        lines.append("# Hard filters")
        lines.append("")
        lines.append(
            "Report each as pass, fail or unknown. Report a hard filter as "
            "unknown when the CV is silent. Silence is not a refusal, and it "
            "must never read as one."
        )
        lines.append("")
        for f in draft["hard_filters"]:
            lines.append(f"{f['label']} [key: {f['key']}] - action: {f['action']}")
            lines.append(f"  {f['rule']}")
        lines.append("")

    lines.append("# Fairness")
    lines.append("")
    lines.append(
        "You are scoring a document, not ranking a person. Do not speculate "
        "about gender, age, ethnicity, religion, marital status or nationality, "
        "and do not let a name, a photograph, or a university influence any "
        "score. Never infer a candidate's gender; write they."
    )
    lines.append("")
    lines.append("# Output contract")
    lines.append("")
    lines.append(
        "Reply with ONE JSON object and nothing else. No prose before or after, "
        "no markdown fence. No em dashes anywhere in what you write."
    )
    lines.append("")
    keys = ", ".join(f'"{d["key"]}"' for d in draft["dimensions"])
    lines.append("{")
    lines.append(f'  "dimensions": {{ each of {keys} as '
                 '{"raw": <int 0-5>, "evidence": ["<quoted from the CV>"]} }},')
    lines.append('  "extracted": {"years_total_experience": <number>, '
                 '"experience_confidence": "high"|"medium"|"low", '
                 '"current_title": <string|null>, "technologies": ["..."]},')
    lines.append('  "strengths": ["<2 to 4 items>"],')
    lines.append('  "gaps": ["<2 to 4 items>"],')
    lines.append('  "hard_filters": { "<key>": "pass"|"fail"|"unknown" },')
    lines.append('  "verdict": "<under 400 characters>",')
    lines.append('  "confidence": "high"|"medium"|"low"')
    lines.append("}")
    lines.append("")
    lines.append(
        "Do NOT include a total, a percentage, a tier or a recommendation. "
        "Those are computed from your dimension scores by code you do not "
        "control, and any you volunteer is discarded."
    )
    return "\n".join(lines)


def _strict(node):
    """Recursively set `additionalProperties: false` on every object node.

    Delegates to the drafter's implementation so the send-time normaliser and
    the generator can never disagree about what "strict" means.
    """
    from .drafting import AnthropicDrafter

    return AnthropicDrafter._strict_schema(node)


def output_schema(draft: dict) -> dict:
    """The JSON schema stored alongside the prompt, matching the contract.

    🔴 EVERY `object` CARRIES `additionalProperties: false`. The API refuses a
    tool schema without it -- "For 'object' type, 'additionalProperties' must
    be explicitly set to false" -- on every nested object, not just the root.
    A rubric drafted without it dies on every candidate with a 400: run
    4b3a144f lost 66 of 76 that way, and the rubric that broke was the first
    one a model had written, because the hand-edited ones already had the flag.

    `drafting.AnthropicDrafter._strict_schema` also applies this at send time,
    so rubrics already published stay screenable without a migration. Both
    exist on purpose: this one makes new rubrics correct at birth, that one
    makes old ones safe. Neither is sufficient alone.
    """
    keys = [d["key"] for d in draft["dimensions"]]
    return _strict({
        "type": "object",
        "required": ["dimensions", "extracted", "strengths", "gaps",
                     "hard_filters", "verdict", "confidence"],
        "properties": {
            "dimensions": {
                "type": "object",
                "required": keys,
                "properties": {
                    k: {
                        "type": "object",
                        "required": ["raw"],
                        "properties": {
                            "raw": {"type": "integer", "minimum": 0, "maximum": 5},
                            "evidence": {"type": "array",
                                         "items": {"type": "string"}, "maxItems": 6},
                        },
                    }
                    for k in keys
                },
            },
            "extracted": {"type": "object"},
            "strengths": {"type": "array", "items": {"type": "string"}, "maxItems": 4},
            "gaps": {"type": "array", "items": {"type": "string"}, "maxItems": 4},
            "hard_filters": {"type": "object"},
            "verdict": {"type": "string", "maxLength": 400},
            "confidence": {"enum": ["high", "medium", "low"]},
        },
    })


def draft_rubric(
    *, job_title: str, department: Optional[str], location: Optional[str],
    job_description: str,
) -> dict:
    """Draft a complete, unsaved rubric. The caller shows it to a person."""
    parsed, model = _call_model(
        system=rubric_drafting_prompt.system_prompt(),
        user=rubric_drafting_prompt.build_user_prompt(
            job_title=job_title, department=department, location=location,
            job_description=job_description,
        ),
    )
    draft = validate_draft(parsed)
    draft["system_prompt"] = compose_system_prompt(
        draft=draft, job_title=job_title, department=department,
        location=location, job_description=job_description,
    )
    draft["output_schema"] = output_schema(draft)
    draft["jd_snapshot"] = job_description
    draft["jd_source"] = "neon_description"
    draft["drafted_by_model"] = model
    draft["source"] = "llm_drafted"
    draft["sop_sha256"] = rubric_drafting_prompt.sop_sha256()
    return draft
