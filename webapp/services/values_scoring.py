"""The locked values-scoring rules.

Pure: no database, no model call. The pass/out rule and the Markaz payload shape are
non-negotiable, so they live here and are tested exhaustively rather than being trusted
to an LLM.

Schema note: the value names and the string "Yes"/"No" below are what all 219 existing
scorecards in public.applications.values_scorecard use, verified 2026-09-17. An earlier
version of the skill file documented shorter names and a boolean; those appear in 1 to 5
records each and are drift, not the standard.
"""

from __future__ import annotations

import datetime as dt
import logging
import re
from typing import Optional

log = logging.getLogger("webapp.values_scoring")

# Canonical order matters: Markaz renders the values in array order.
VALUE_NAMES = (
    "Don't Walk Away from Hard Things",
    "All for One & One for All",
    "Continuously Improve Our Craft",
    "Have Courageous Conversations",
    "Don't Hold On Too Tight",
    "Practice Joy",
)

RATINGS = ("+", "+/-", "-")

NOT_OBSERVED = "Not directly evident in interview."

_EVIDENCE_FIELDS = ("deepDive", "curveBall", "microCase")

# The exact key set a value object must have -- no more, no fewer. Verified
# 2026-09-17 against all 219 live public.applications.values_scorecard
# records: every nested value object across every record uses exactly these
# five keys, never an extra one. Without this, an editor's PATCH can smuggle
# an arbitrary extra key (e.g. an "internalNote") straight into Markaz's
# production table, since the top-level payload keys are whitelisted
# (MARKAZ_KEYS) but the nested ones previously were not.
VALUE_KEYS = frozenset({"name", "deepDive", "curveBall", "microCase", "rating"})


class ValuesScorecardError(ValueError):
    """The scorecard does not match the locked shape."""


class TranscriptTooShort(ValuesScorecardError):
    """The transcript is under MIN_TRANSCRIPT_CHARS characters.

    A real values interview transcript runs long. A short one almost always
    means the wrong text was pasted (a summary, a snippet, the wrong tab), so
    this refuses rather than scoring six values off a few sentences.
    """


# A real values interview runs 45-60+ minutes and transcribes to many
# thousands of characters. 2,000 is a floor well under any genuine interview,
# chosen to catch "wrong thing pasted" rather than to gate on interview length.
MIN_TRANSCRIPT_CHARS = 2000


def tally(ratings: list[str]) -> dict:
    return {
        "plus": ratings.count("+"),
        "plus_minus": ratings.count("+/-"),
        "minus": ratings.count("-"),
    }


def verdict(ratings: list[str]) -> str:
    """PASS = zero minuses AND at most two plus-minuses. Everything else is OUT."""
    t = tally(ratings)
    return "PASS" if (t["minus"] == 0 and t["plus_minus"] <= 2) else "OUT"


# Matches the "{PASS|OUT} - N(+) / N(+/-) / N(-)" prefix generate() writes,
# with an optional " - <narrative>" tail a human may have typed in PATCH.
_FINAL_COMMENTS_PREFIX_RE = re.compile(
    r"^(?:PASS|OUT) - \d+\(\+\) / \d+\(\+/-\) / \d+\(-\)\s*(?:-\s*)?"
)


def recompute_final_comments(ratings: list[str], existing_text: Optional[str] = "") -> str:
    """Rebuild the verdict/tally PREFIX of `final_comments` from the CURRENT
    ratings, keeping any narrative a human appended after that prefix.

    `final_comments` is a permanent Markaz field. A PATCH that changes
    ratings must never leave the old verdict/tally standing next to a
    contradicting `proceedToRightSeat` -- e.g. "PASS - 6(+) / 0(+/-) / 0(-)"
    beside "No". This is called both when the client left `final_comments`
    untouched (ratings changed under it) and when the client supplied fresh
    text (their narrative is kept, but the verdict/tally leading it is never
    trusted -- it is always the one computed here).
    """
    v = verdict(ratings)
    t = tally(ratings)
    prefix = f"{v} - {t['plus']}(+) / {t['plus_minus']}(+/-) / {t['minus']}(-)"
    remainder = _FINAL_COMMENTS_PREFIX_RE.sub("", existing_text or "", count=1).strip()
    return f"{prefix} - {remainder}" if remainder else prefix


def find_newer_duplicate(
    rows: list[tuple[int, Optional[dt.datetime]]],
    target_id: int,
    target_updated_at: Optional[dt.datetime],
) -> Optional[int]:
    """Given every `(id, updated_at)` for `public.applications` rows sharing
    the target's `(candidate_id, job_id)`, return the id of the one row that
    is genuinely newer than the target, or `None` if the target already is
    the newest.

    Deliberately NOT "sort everything by updated_at DESC and take the top
    row" -- in PostgreSQL that puts NULLs FIRST, so a duplicate that has
    never been touched (`updated_at IS NULL`) would look newer than every
    real timestamp and produce a permanent, unforceable false refusal. Here
    a NULL `updated_at` always sorts OLDER than any real timestamp, for
    both the target and the candidates. Exact timestamp ties (including two
    NULLs) are broken by the higher `id`. The target's own row is always
    excluded, so passing every row for the pair (target included) is safe.
    """

    def _key(updated_at, row_id):
        # (has_a_real_timestamp, timestamp, id): comparing two keys with
        # different first elements never touches the second, so a real
        # datetime is never compared against a bare `None`.
        return (updated_at is not None, updated_at, row_id)

    target_key = _key(target_updated_at, target_id)
    newest_id: Optional[int] = None
    newest_key = None
    for row_id, row_updated_at in rows:
        if row_id == target_id:
            continue
        row_key = _key(row_updated_at, row_id)
        if row_key > target_key and (newest_key is None or row_key > newest_key):
            newest_id = row_id
            newest_key = row_key
    return newest_id


def validate_values(values: list[dict]) -> None:
    if len(values) != len(VALUE_NAMES):
        raise ValuesScorecardError(
            f"expected {len(VALUE_NAMES)} values, got {len(values)}"
        )
    for i, (expected_name, v) in enumerate(zip(VALUE_NAMES, values)):
        extra_keys = set(v) - VALUE_KEYS
        missing_keys = VALUE_KEYS - set(v)
        if extra_keys or missing_keys:
            raise ValuesScorecardError(
                f"{expected_name}: value object keys must be exactly "
                f"{sorted(VALUE_KEYS)}, got {sorted(v)} "
                f"(extra={sorted(extra_keys)}, missing={sorted(missing_keys)}). "
                "No other key -- e.g. an internal note -- may ride along into "
                "Markaz's production record."
            )
        if v.get("name") != expected_name:
            raise ValuesScorecardError(
                f"value {i} must be {expected_name!r}, got {v.get('name')!r}. "
                "The canonical names are the ones Markaz already holds."
            )
        if v.get("rating") not in RATINGS:
            raise ValuesScorecardError(
                f"{expected_name}: rating must be one of {RATINGS}, got {v.get('rating')!r}"
            )
        for f in _EVIDENCE_FIELDS:
            if not str(v.get(f, "")).strip():
                raise ValuesScorecardError(
                    f"{expected_name}: {f} is blank. Use NOT_OBSERVED if it was not seen."
                )


MARKAZ_KEYS = frozenset(
    {"date", "host", "candidateName", "noteTaker", "values", "finalComments", "proceedToRightSeat"}
)


def format_markaz_date(d: dt.date) -> str:
    """Markaz stores the date as a human string, e.g. "Aug 14, 2026" -- but
    the day is NEVER zero-padded: "Nov 3, 2025", not "Nov 03, 2025".
    Verified 2026-09-17 against all 219 live `public.applications
    .values_scorecard` records with a date in this shape: 0 of them
    zero-pad the day. `dt.date.strftime("%b %d, %Y")` always zero-pads (its
    `%d` has no non-padded form on every platform), so it must not be used
    here.
    """
    return f"{d:%b} {d.day}, {d:%Y}"


# Maps the computed PASS/OUT verdict to the exact lowercase string Markaz's
# `applications.values_interview_result` column uses -- 101 live records
# read "pass", 23 read "fail", never "PASS"/"OUT". There is one legacy
# "strong_pass" (drift, not the standard); this must never produce it.
MARKAZ_RESULT_BY_VERDICT = {"PASS": "pass", "OUT": "fail"}


def markaz_result(computed_verdict: str) -> str:
    try:
        return MARKAZ_RESULT_BY_VERDICT[computed_verdict]
    except KeyError:
        raise ValuesScorecardError(
            f"verdict must be one of {sorted(MARKAZ_RESULT_BY_VERDICT)}, got {computed_verdict!r}"
        )


def build_markaz_payload(
    *,
    candidate_name: str,
    host: str,
    values: list[dict],
    final_comments: str,
    proceed: bool,
    date: Optional[str] = None,
    note_taker: str = "Coco (AI P&C Assistant)",
) -> dict:
    validate_values(values)
    payload = {
        "date": date or format_markaz_date(dt.date.today()),
        "host": host,
        "candidateName": candidate_name,
        "noteTaker": note_taker,
        "values": values,
        "finalComments": final_comments,
        # String, not boolean: 215 of the 219 live records are strings.
        "proceedToRightSeat": "Yes" if proceed else "No",
    }
    validate_markaz_payload(payload)
    return payload


def validate_markaz_payload(payload: dict) -> None:
    keys = set(payload)
    if keys != MARKAZ_KEYS:
        raise ValuesScorecardError(
            f"payload keys {sorted(keys)} != required {sorted(MARKAZ_KEYS)}"
        )
    prs = payload["proceedToRightSeat"]
    if not isinstance(prs, str) or prs not in ("Yes", "No"):
        raise ValuesScorecardError(
            f'proceedToRightSeat must be the string "Yes" or "No", got {prs!r}'
        )
    for field in ("date", "host", "candidateName", "noteTaker", "finalComments"):
        if not str(payload.get(field, "")).strip():
            raise ValuesScorecardError(f"{field} must not be blank")
    validate_values(payload["values"])


# --------------------------------------------------------------------------
# Model call: transcript -> scored values (+ GWC, when the computed verdict
# is PASS). The rules above never leave the model's hands; everything below
# runs its output back through them before anything is trusted.
# --------------------------------------------------------------------------

_GWC_KEYS = ("gets_it", "wants_it", "capacity")


def _validate_gwc(gwc: dict) -> None:
    """gwc must be exactly the three Get It / Want It / Capacity questions,
    each answered Yes or No. Never a boolean, never a longer sentence, never
    a fourth key."""
    if not isinstance(gwc, dict):
        raise ValuesScorecardError(f"gwc must be an object, got {type(gwc).__name__}")
    for key in _GWC_KEYS:
        val = gwc.get(key)
        if val not in ("Yes", "No"):
            raise ValuesScorecardError(
                f"gwc.{key} must be the string 'Yes' or 'No', got {val!r}"
            )


def _call_model(*, transcript: str, candidate_name: str, role: str) -> tuple:
    """One model call: transcript in, raw parsed JSON out.

    Module-level (not a method) so tests can monkeypatch it directly and never
    make a real Anthropic call. Reuses webapp.services.drafting.get_drafter(),
    the existing client with its model-fallback chain, rather than building a
    second client. Imported locally to avoid a module-level import cycle:
    drafting.py -> tone_rules.py -> reuse.py does not touch this module, but
    values_prompt.py (imported here) reads VALUE_NAMES/RATINGS/NOT_OBSERVED
    from this module, so the import has to happen after this module is fully
    defined.

    Returns (parsed_json, model_name). Raises whatever the drafter raises
    (DraftingUnavailable, an Anthropic SDK error, a JSON parse error from a
    non-JSON reply) -- none of that is swallowed here.
    """
    from . import drafting
    from ..prompts import values_prompt

    drafter = drafting.get_drafter()
    system = values_prompt.system_prompt()
    user = values_prompt.build_user_prompt(
        transcript=transcript, candidate_name=candidate_name, role=role
    )
    parsed = drafter.draft(
        system=system,
        user=user,
        email_type="values_scoring",
        first_name=candidate_name,
        role=role,
        prior_violations=None,
        attempt=0,
    )
    model_name = getattr(drafter, "model", None) or getattr(drafter, "name", "unknown")
    return parsed, model_name


def _score_ratings_from(values: list[dict]) -> list[str]:
    return [v["rating"] for v in values]


def score_transcript(*, transcript: str, candidate_name: str, role: str) -> dict:
    """Turn an interview transcript into a scored values scorecard.

    Refuses a transcript that is too short to be real (TranscriptTooShort).
    Calls the model, validates its response against the locked shape
    (validate_values), and NEVER repairs a malformed response: a response that
    fails validation -- including a response that is not even parseable JSON,
    which surfaces as a plain ValueError out of _call_model/drafting rather
    than a ValuesScorecardError -- is retried once with a fresh model call
    (not a repair of the old one), and if the second attempt is also
    malformed this raises ValuesScorecardError (never a bare ValueError)
    rather than coercing, guessing, or filling in a blank field.

    The verdict is always computed by verdict() from the model's six ratings,
    never taken from the model even if it volunteers one (the output contract
    tells it not to; this function does not trust that instruction either).
    GWC is only ever returned when the computed verdict is PASS -- a model
    that includes a gwc block on an OUT scorecard has that block dropped, not
    honoured, because GWC is not a back door around a failing values round.

    Returns {"values": [...], "gwc": {...} | None, "tally": {...},
    "verdict": "PASS"|"OUT", "model": str}.
    """
    if len(transcript) < MIN_TRANSCRIPT_CHARS:
        raise TranscriptTooShort(
            f"transcript is {len(transcript)} characters; a real values "
            f"interview transcript runs far longer than the "
            f"{MIN_TRANSCRIPT_CHARS}-character floor. This looks like the "
            "wrong text was pasted."
        )

    last_error: Optional[ValuesScorecardError] = None
    attempts = 2  # one retry, per the rule: malformed -> retry once -> raise
    for attempt in range(attempts):
        try:
            # The call itself is inside the try: a response that is not even
            # parseable JSON (a plain ValueError out of drafting._parse_json,
            # raised before this ever reaches ValuesScorecardError territory)
            # is exactly as "malformed" as a well-formed JSON object with the
            # wrong shape, and must be retried the same way.
            parsed, model_name = _call_model(
                transcript=transcript, candidate_name=candidate_name, role=role
            )
            if not isinstance(parsed, dict):
                raise ValuesScorecardError(
                    f"model response was not a JSON object, got {type(parsed).__name__}"
                )
            values = parsed.get("values")
            if not isinstance(values, list):
                raise ValuesScorecardError("model response has no 'values' list")
            validate_values(values)  # the ONLY place a malformed shape is caught

            ratings = _score_ratings_from(values)
            computed_verdict = verdict(ratings)

            gwc: Optional[dict] = None
            if computed_verdict == "PASS":
                gwc_raw = parsed.get("gwc")
                if gwc_raw is not None:
                    _validate_gwc(gwc_raw)
                    gwc = gwc_raw
                else:
                    log.warning(
                        "score_transcript: verdict is PASS but the model "
                        "returned no gwc block for %r.", candidate_name,
                    )
            elif parsed.get("gwc") is not None:
                log.warning(
                    "score_transcript: model returned a gwc block on an OUT "
                    "scorecard for %r; dropping it. GWC is never a back door "
                    "around a failing values round.", candidate_name,
                )
        except ValuesScorecardError as exc:
            last_error = exc
            log.warning(
                "score_transcript: malformed model response for %r "
                "(attempt %d/%d): %s", candidate_name, attempt + 1, attempts, exc,
            )
            continue
        except ValueError as exc:
            # ValuesScorecardError IS a ValueError, but that branch is caught
            # above, so anything landing here is a DIFFERENT ValueError: most
            # commonly drafting._parse_json's "LLM did not return parseable
            # JSON" when the model's text is not JSON at all. Wrap it so the
            # caller only ever has one exception type to handle, and keep the
            # original exception visible via __cause__ for debugging.
            wrapped = ValuesScorecardError(
                f"model response was not parseable JSON: {exc}"
            )
            wrapped.__cause__ = exc
            last_error = wrapped
            log.warning(
                "score_transcript: model call/parse failed for %r "
                "(attempt %d/%d): %s", candidate_name, attempt + 1, attempts, exc,
            )
            continue

        return {
            "values": values,
            "gwc": gwc,
            "tally": tally(ratings),
            "verdict": computed_verdict,
            "model": model_name,
        }

    # Both attempts were malformed. Never silently repair; raise the last
    # validation error so the caller sees exactly what was wrong.
    raise last_error
