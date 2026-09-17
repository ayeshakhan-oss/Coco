# Candidate Evaluation Phase 2: Values Scorecard Scoring — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Score a values interview from its transcript into the locked 6-value scorecard, show it to a human in full, and submit it to Markaz only after an `approver` presses approve.

**Architecture:** Pure scoring logic (pass/out, canonical names, payload shape) is separated from the model call so the non-negotiable rules are unit-testable without an LLM or a database. A draft lands in a new `coco.values_scorecard_drafts` table, is rendered and editable in the UI, and is written to `public.applications.values_scorecard` only by an explicit approver action. There is no auto-submit path.

**Tech Stack:** FastAPI, SQLAlchemy 2.x, Pydantic v2, Anthropic SDK (via the existing `AnthropicDrafter`), React + TypeScript, pytest.

**Spec:** [docs/specs/2026-09-16-candidate-evaluation-module-design.md](../specs/2026-09-16-candidate-evaluation-module-design.md) (Phase 2)

## Global Constraints

- 🔒 **The canonical Markaz schema is what the 219 existing scorecards use, NOT what the skill file currently documents.** Verified live 2026-09-17. Value names, in order:
  1. `Don't Walk Away from Hard Things`
  2. `All for One & One for All`
  3. `Continuously Improve Our Craft`
  4. `Have Courageous Conversations`
  5. `Don't Hold On Too Tight`
  6. `Practice Joy`
- 🔒 `proceedToRightSeat` is the **string** `"Yes"` or `"No"`, not a boolean (215 of 219 records are strings).
- 🔒 Payload shape: `{date, host, candidateName, noteTaker, values[], finalComments, proceedToRightSeat}`; each value carries `{name, deepDive, curveBall, microCase, rating}`.
- 🔒 **Ratings are exactly `+`, `+/-`, `-`.** No other token is valid.
- 🔒 **PASS = zero minuses AND at most 2 plus-minuses. Everything else is OUT.** Non-negotiable, computed in code, never left to the model.
- 🔒 **GWC is assessed only for candidates who PASS.**
- 🔒 **Never leave an evidence field blank.** If a value was not observed, the text is `Not directly evident in interview.`
- 🔒 **Submitting to Markaz requires the `approver` role** (Ayesha, 2026-09-16), the same gate as sending a candidate email. `require_approver` already exists in `webapp/deps.py`.
- 🔒 **No auto-submit for any role.** A human presses approve, every time.
- 🔒 Coco's own tables live in the **`coco`** schema, never `public` (Markaz's Replit deploys drop Coco's public tables).
- `from __future__ import annotations` at the top of every new module. No em dashes in user-facing copy.

---

### Task 1: Correct the locked skill file to match reality

**Files:**
- Modify: `.claude/skills/02_candidate-evaluation/values-scorecard-scoring.md`

**Interfaces:**
- Consumes: nothing
- Produces: a skill file whose documented schema matches the 219 live records

**Why first:** the file calls its schema NON-NEGOTIABLE and warns that a wrong schema makes data invisible on Markaz, while documenting names that appear 1-5 times against canonical names that appear 212-219 times. Every later task reads this file. Ayesha approved this correction on 2026-09-17.

- [ ] **Step 1: Replace the schema block**

In the `## The Markaz JSON Schema (NON-NEGOTIABLE)` section, replace the example with:

```json
{
  "date": "Aug 14, 2026",
  "host": "Ayesha Khan",
  "candidateName": "Muhammad Junaid",
  "noteTaker": "Coco (AI P&C Assistant)",
  "values": [
    {
      "name": "Don't Walk Away from Hard Things",
      "deepDive": "...",
      "curveBall": "...",
      "microCase": "...",
      "rating": "+"
    }
  ],
  "finalComments": "PASS - 4(+) / 2(+/-) / 0(-) ...",
  "proceedToRightSeat": "Yes"
}
```

- [ ] **Step 2: Add the verification note**

Immediately under that block, add:

```markdown
🔒 **VERIFIED AGAINST LIVE DATA (2026-09-17).** These names and types are what all 219
existing scorecards in `public.applications.values_scorecard` use. Counts at the time of
checking: `Don't Walk Away from Hard Things` 219, `All for One & One for All` 213,
`Continuously Improve Our Craft` 212, `Have Courageous Conversations` 214,
`Don't Hold On Too Tight` 219, `Practice Joy` 219.

`proceedToRightSeat` is a **string** `"Yes"` / `"No"` (215 of 219), not a boolean.

⚠️ This file previously documented shorter names (`Don't Walk Away`, `All for One`,
`Continuously Improve`, `Courageous Conversations`) and a boolean. Those spellings exist in
only 1 to 5 records each and are drift from hand-written submissions, not the standard.
Do not reintroduce them.
```

- [ ] **Step 3: Update the 6-values list**

In `## The 6 Values to Assess`, change each heading to the canonical name while keeping its existing description text unchanged. Do not alter the rating system, the pass/out logic, the GWC section or the 7 steps.

- [ ] **Step 4: Verify nothing else drifted**

Run: `grep -nE "Don't Walk Away|All for One|Continuously Improv|Courageous Conversations|Hold On Too Tight|Practice Joy" .claude/skills/02_candidate-evaluation/values-scorecard-scoring.md`
Expected: every occurrence is a canonical name, except inside the new warning paragraph.

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/02_candidate-evaluation/values-scorecard-scoring.md
git commit -m "docs(skill02): correct the Markaz values schema to match all 219 live records"
```

---

### Task 2: Pure scoring rules

**Files:**
- Create: `webapp/services/values_scoring.py`
- Test: `webapp/tests/test_values_scoring.py`

**Interfaces:**
- Consumes: nothing (pure module, no DB, no network)
- Produces:
  - `VALUE_NAMES: tuple[str, ...]` — the six canonical names in order
  - `RATINGS: tuple[str, ...]` = `("+", "+/-", "-")`
  - `NOT_OBSERVED: str` = `"Not directly evident in interview."`
  - `verdict(ratings: list[str]) -> str` — `"PASS"` or `"OUT"`
  - `tally(ratings: list[str]) -> dict` — `{"plus": int, "plus_minus": int, "minus": int}`
  - `ValuesScorecardError(Exception)`
  - `validate_values(values: list[dict]) -> None` — raises on wrong count, wrong/duplicate names, wrong order, invalid rating, or a blank evidence field

- [ ] **Step 1: Write the failing test**

```python
"""The non-negotiable values-scoring rules, tested without an LLM or a database.

PASS is zero minuses AND at most two plus-minuses. Everything else is OUT. This is
computed in code and never left to a model, so it is tested exhaustively here.
"""

from __future__ import annotations

import itertools

import pytest

from webapp.services.values_scoring import (
    NOT_OBSERVED,
    RATINGS,
    VALUE_NAMES,
    ValuesScorecardError,
    tally,
    validate_values,
    verdict,
)


def _values(ratings):
    return [
        {"name": n, "deepDive": "d", "curveBall": "c", "microCase": "m", "rating": r}
        for n, r in zip(VALUE_NAMES, ratings)
    ]


def test_canonical_names_and_ratings():
    assert VALUE_NAMES == (
        "Don't Walk Away from Hard Things",
        "All for One & One for All",
        "Continuously Improve Our Craft",
        "Have Courageous Conversations",
        "Don't Hold On Too Tight",
        "Practice Joy",
    )
    assert RATINGS == ("+", "+/-", "-")


def test_verdict_exhaustively_over_every_possible_scorecard():
    # All 3^6 = 729 combinations. The rule must hold for every one.
    for combo in itertools.product(RATINGS, repeat=6):
        got = verdict(list(combo))
        minuses = combo.count("-")
        plus_minuses = combo.count("+/-")
        expected = "PASS" if (minuses == 0 and plus_minuses <= 2) else "OUT"
        assert got == expected, f"{combo}: got {got}, expected {expected}"


def test_verdict_named_cases():
    assert verdict(["+"] * 6) == "PASS"
    assert verdict(["+", "+", "+", "+", "+", "+/-"]) == "PASS"
    assert verdict(["+", "+", "+", "+", "+/-", "+/-"]) == "PASS"
    # Three plus-minuses is OUT even with no minus.
    assert verdict(["+", "+", "+", "+/-", "+/-", "+/-"]) == "OUT"
    # A single minus is OUT regardless of everything else.
    assert verdict(["+", "+", "+", "+", "+", "-"]) == "OUT"


def test_tally():
    assert tally(["+", "+", "+/-", "-", "+", "+/-"]) == {"plus": 3, "plus_minus": 2, "minus": 1}


def test_validate_rejects_wrong_shape():
    with pytest.raises(ValuesScorecardError):
        validate_values(_values(["+"] * 5)[:5])            # only five values
    with pytest.raises(ValuesScorecardError):
        bad = _values(["+"] * 6); bad[0]["name"] = "Don't Walk Away"
        validate_values(bad)                                # the OLD skill-file name
    with pytest.raises(ValuesScorecardError):
        bad = _values(["+"] * 6); bad[2], bad[3] = bad[3], bad[2]
        validate_values(bad)                                # out of canonical order
    with pytest.raises(ValuesScorecardError):
        bad = _values(["+"] * 6); bad[1]["rating"] = "++"
        validate_values(bad)                                # invalid rating token
    with pytest.raises(ValuesScorecardError):
        bad = _values(["+"] * 6); bad[4]["curveBall"] = "   "
        validate_values(bad)                                # blank evidence


def test_validate_accepts_the_not_observed_sentinel():
    ok = _values(["+"] * 6)
    ok[3]["curveBall"] = NOT_OBSERVED
    validate_values(ok)  # must not raise
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest webapp/tests/test_values_scoring.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'webapp.services.values_scoring'`

- [ ] **Step 3: Write minimal implementation**

```python
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


class ValuesScorecardError(ValueError):
    """The scorecard does not match the locked shape."""


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


def validate_values(values: list[dict]) -> None:
    if len(values) != len(VALUE_NAMES):
        raise ValuesScorecardError(
            f"expected {len(VALUE_NAMES)} values, got {len(values)}"
        )
    for i, (expected_name, v) in enumerate(zip(VALUE_NAMES, values)):
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest webapp/tests/test_values_scoring.py -v`
Expected: PASS (6 tests, one of which covers all 729 rating combinations)

- [ ] **Step 5: Commit**

```bash
git add webapp/services/values_scoring.py webapp/tests/test_values_scoring.py
git commit -m "feat(values): locked scoring rules, pass/out tested over all 729 combinations"
```

---

### Task 3: The Markaz payload builder, checked against a real record

**Files:**
- Modify: `webapp/services/values_scoring.py`
- Test: `webapp/tests/test_values_scoring.py`

**Interfaces:**
- Consumes: `VALUE_NAMES`, `validate_values`, `verdict`, `tally`
- Produces:
  - `build_markaz_payload(*, candidate_name: str, host: str, values: list[dict], final_comments: str, proceed: bool, date: Optional[str] = None, note_taker: str = "Coco (AI P&C Assistant)") -> dict`
  - `MARKAZ_KEYS: frozenset[str]`
  - `validate_markaz_payload(payload: dict) -> None`

- [ ] **Step 1: Write the failing test**

```python
from webapp.services.values_scoring import (
    MARKAZ_KEYS,
    build_markaz_payload,
    validate_markaz_payload,
)


def _ok_values():
    return [
        {"name": n, "deepDive": "d", "curveBall": "c", "microCase": "m", "rating": "+"}
        for n in VALUE_NAMES
    ]


def test_payload_shape_matches_the_live_records():
    p = build_markaz_payload(
        candidate_name="Muhammad Junaid",
        host="Ayesha Khan",
        values=_ok_values(),
        final_comments="PASS - 6(+) / 0(+/-) / 0(-)",
        proceed=True,
        date="Aug 14, 2026",
    )
    assert set(p) == MARKAZ_KEYS
    assert p["candidateName"] == "Muhammad Junaid"
    assert p["noteTaker"] == "Coco (AI P&C Assistant)"
    assert p["date"] == "Aug 14, 2026"
    # The live records store a STRING, not a boolean. 215 of 219.
    assert p["proceedToRightSeat"] == "Yes"
    assert isinstance(p["proceedToRightSeat"], str)
    assert [v["name"] for v in p["values"]] == list(VALUE_NAMES)


def test_proceed_false_is_the_string_no():
    p = build_markaz_payload(
        candidate_name="X", host="Ayesha Khan", values=_ok_values(),
        final_comments="OUT", proceed=False,
    )
    assert p["proceedToRightSeat"] == "No"


def test_payload_rejects_a_boolean_proceed_value():
    p = build_markaz_payload(
        candidate_name="X", host="Ayesha Khan", values=_ok_values(),
        final_comments="PASS", proceed=True,
    )
    p["proceedToRightSeat"] = True          # the shape the old skill file documented
    with pytest.raises(ValuesScorecardError):
        validate_markaz_payload(p)


def test_payload_rejects_extra_or_missing_keys():
    p = build_markaz_payload(
        candidate_name="X", host="Ayesha Khan", values=_ok_values(),
        final_comments="PASS", proceed=True,
    )
    with pytest.raises(ValuesScorecardError):
        validate_markaz_payload({**p, "extra": 1})
    with pytest.raises(ValuesScorecardError):
        validate_markaz_payload({k: v for k, v in p.items() if k != "noteTaker"})
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest webapp/tests/test_values_scoring.py -v`
Expected: FAIL with `ImportError: cannot import name 'MARKAZ_KEYS'`

- [ ] **Step 3: Write minimal implementation**

Append to `webapp/services/values_scoring.py`:

```python
import datetime as dt
from typing import Optional

MARKAZ_KEYS = frozenset(
    {"date", "host", "candidateName", "noteTaker", "values", "finalComments", "proceedToRightSeat"}
)

# Markaz stores the date as a human string, e.g. "Aug 14, 2026".
_DATE_FMT = "%b %d, %Y"


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
        "date": date or dt.date.today().strftime(_DATE_FMT),
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest webapp/tests/test_values_scoring.py -v`
Expected: PASS (10 tests)

- [ ] **Step 5: Add a round-trip test against a REAL record**

This is the test that proves we match Markaz rather than our own idea of Markaz. Add to `webapp/tests/test_evaluations_api.py` (which already skips without `DATABASE_URL`):

```python
def test_our_payload_shape_matches_a_real_markaz_scorecard(db_session):
    """Pull a real scorecard and assert our validator accepts it unchanged.

    If Markaz's shape ever drifts, this fails and tells us before we write a
    scorecard nobody can see.
    """
    from sqlalchemy import text
    from webapp.services.values_scoring import validate_markaz_payload

    row = db_session.execute(
        text(
            "SELECT values_scorecard FROM public.applications "
            "WHERE jsonb_typeof(values_scorecard) = 'object' "
            "AND jsonb_typeof(values_scorecard->'values') = 'array' "
            "AND jsonb_array_length(values_scorecard->'values') = 6 "
            "AND jsonb_typeof(values_scorecard->'proceedToRightSeat') = 'string' "
            "ORDER BY id DESC LIMIT 1"
        )
    ).scalar()
    assert row, "no real scorecard found to compare against"
    validate_markaz_payload(row)
```

- [ ] **Step 6: Commit**

```bash
git add webapp/services/values_scoring.py webapp/tests/test_values_scoring.py webapp/tests/test_evaluations_api.py
git commit -m "feat(values): Markaz payload builder, round-tripped against a real record"
```

---

### Task 4: Draft storage in the `coco` schema

**Files:**
- Modify: `webapp/models.py`
- Modify: `webapp/db.py` (add the new table to `ensure_app_tables`)
- Create: `alembic/versions/0006_values_scorecard_drafts.py`
- Test: `webapp/tests/test_values_scoring.py`

**Interfaces:**
- Consumes: nothing
- Produces: `ValuesScorecardDraft` model, table `coco.values_scorecard_drafts`

🔒 The table MUST declare `{"schema": "coco"}` in `__table_args__`. `public` is inside Markaz's Replit schema-push blast radius and Coco has lost tables there before. Follow the existing `CommEvidence` model exactly.

Columns: `id` (uuid pk), `application_id` (int, indexed), `candidate_name` (text), `host` (text), `transcript_sha256` (text), `values` (jsonb), `final_comments` (text), `proceed` (bool), `gwc` (jsonb, nullable), `status` (text: `draft` / `submitted`), `model` (text), `created_by` (text), `created_at`, `approved_by` (text, nullable), `approved_at` (nullable), `submitted_at` (nullable), `markaz_payload` (jsonb, nullable).

**Why store the transcript hash and not the transcript:** the transcript is interview content about a named person. The hash is enough to tell whether a re-score used the same input, without keeping the text in a second place.

- [ ] **Step 1: Write the failing test**

```python
def test_draft_table_lives_in_the_coco_schema():
    """public is inside Markaz's Replit schema-push blast radius; coco is not."""
    from webapp.models import ValuesScorecardDraft

    assert ValuesScorecardDraft.__table__.schema == "coco"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest webapp/tests/test_values_scoring.py::test_draft_table_lives_in_the_coco_schema -v`
Expected: FAIL with `ImportError: cannot import name 'ValuesScorecardDraft'`

- [ ] **Step 3: Write the model, the migration, and the self-heal entry**

Add `ValuesScorecardDraft` to `webapp/models.py` following `CommEvidence`'s structure and its `{"schema": "coco"}` table arg. Add it to the `tables=[...]` list in `db.ensure_app_tables` so a schema reset self-heals it, exactly as `CommEvidence` and `GmailSyncRun` are handled. Write `alembic/versions/0006_values_scorecard_drafts.py` creating the table in the `coco` schema (`op.execute("CREATE SCHEMA IF NOT EXISTS coco")` first).

⚠️ `Dockerfile` deliberately does NOT run migrations on boot. The migration must be applied by hand before or with the deploy: `railway run --service elegant-benevolence alembic upgrade head`.

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest webapp/tests/test_values_scoring.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add webapp/models.py webapp/db.py alembic/versions/0006_values_scorecard_drafts.py webapp/tests/test_values_scoring.py
git commit -m "feat(values): draft storage in the coco schema"
```

---

### Task 5: The scoring service (model call)

**Files:**
- Modify: `webapp/services/values_scoring.py`
- Create: `webapp/prompts/values_prompt.py`
- Test: `webapp/tests/test_values_scoring.py`

**Interfaces:**
- Consumes: `webapp.services.drafting.get_drafter` (existing Anthropic client with its model-fallback chain), `VALUE_NAMES`, `validate_values`, `verdict`
- Produces:
  - `system_prompt() -> str`
  - `build_user_prompt(*, transcript: str, candidate_name: str, role: str) -> str`
  - `score_transcript(*, transcript: str, candidate_name: str, role: str) -> dict` — returns `{"values": [...], "gwc": {...} | None, "tally": {...}, "verdict": "PASS"|"OUT", "model": str}`
  - `TranscriptTooShort(ValuesScorecardError)`

**Rules the prompt must carry, and the code must enforce after the call:**
- The model returns the six values in canonical order with all three evidence fields populated and a rating token from `RATINGS`. `validate_values` runs on the response; a malformed response is a retry, then an error. **Never repair a malformed response silently.**
- **The verdict is computed by `verdict()`, never taken from the model.** If the model volunteers one, ignore it.
- **GWC is only produced when the computed verdict is PASS.** If the verdict is OUT, `gwc` is `None`.
- Evidence must quote the transcript. An empty observation uses `NOT_OBSERVED`, never an invention.
- `TranscriptTooShort` if the transcript is under 2,000 characters: a values interview transcript is long, and a short one means the wrong thing was pasted.

- [ ] **Step 1: Write the failing test**

```python
def test_verdict_is_computed_not_taken_from_the_model(monkeypatch):
    """A model that claims PASS on a scorecard containing a minus must not win."""
    from webapp.services import values_scoring as vs

    payload = {
        "values": [
            {"name": n, "deepDive": "d", "curveBall": "c", "microCase": "m", "rating": r}
            for n, r in zip(vs.VALUE_NAMES, ["+", "+", "+", "+", "+", "-"])
        ],
        "verdict": "PASS",          # the model lying
        "gwc": {"gets_it": "Yes", "wants_it": "Yes", "capacity": "Yes"},
    }
    monkeypatch.setattr(vs, "_call_model", lambda **kw: (payload, "test-model"))

    out = vs.score_transcript(transcript="x" * 3000, candidate_name="A", role="R")
    assert out["verdict"] == "OUT"      # computed from the ratings
    assert out["gwc"] is None           # GWC only for a PASS


def test_short_transcript_is_refused():
    from webapp.services.values_scoring import TranscriptTooShort, score_transcript

    with pytest.raises(TranscriptTooShort):
        score_transcript(transcript="too short", candidate_name="A", role="R")


def test_malformed_model_response_is_not_silently_repaired(monkeypatch):
    from webapp.services import values_scoring as vs

    bad = {"values": [{"name": "Don't Walk Away", "deepDive": "d",
                       "curveBall": "c", "microCase": "m", "rating": "+"}]}
    monkeypatch.setattr(vs, "_call_model", lambda **kw: (bad, "test-model"))
    with pytest.raises(vs.ValuesScorecardError):
        vs.score_transcript(transcript="x" * 3000, candidate_name="A", role="R")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest webapp/tests/test_values_scoring.py -v`
Expected: FAIL with `AttributeError: module ... has no attribute '_call_model'`

- [ ] **Step 3: Write the implementation**

Create `webapp/prompts/values_prompt.py` holding `system_prompt()` and `build_user_prompt()`. The system prompt states the six canonical values with their definitions (read them from `.claude/skills/02_candidate-evaluation/values-scorecard-scoring.md` at import, the way `tone_rules.py` reads its SOPs, and **log at ERROR if the file is missing rather than silently returning an empty string** — that silent-degradation failure is recorded in the repo's history). It must instruct: evidence quoted from the transcript, all three evidence fields per value, `NOT_OBSERVED` when unseen, a rating token, and **no verdict** since the code computes it.

In `values_scoring.py` add `_call_model(...)` wrapping `get_drafter()`, requesting JSON, and `score_transcript(...)` which refuses a short transcript, calls the model, runs `validate_values`, computes `tally`/`verdict`, and drops GWC when the verdict is OUT.

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest webapp/tests/test_values_scoring.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add webapp/services/values_scoring.py webapp/prompts/values_prompt.py webapp/tests/test_values_scoring.py
git commit -m "feat(values): transcript scoring, verdict computed in code not by the model"
```

---

### Task 6: Router, with the approver gate on submission

**Files:**
- Create: `webapp/routers/values_scorecards.py`
- Modify: `webapp/schemas.py`, `webapp/main.py`
- Test: `webapp/tests/test_values_scoring.py`

**Interfaces:**
- Consumes: `values_scoring`, `ValuesScorecardDraft`, `require_editor` and `require_approver` from `webapp/deps.py`
- Produces:
  - `POST /api/values-scorecards/generate` — **editor**; body `{application_id, transcript, host}`; scores and stores a draft
  - `GET /api/values-scorecards/{draft_id}` — signed in
  - `PATCH /api/values-scorecards/{draft_id}` — **editor**; edit evidence text and ratings; recomputes the verdict; refuses if already submitted
  - `POST /api/values-scorecards/{draft_id}/submit` — **approver**; writes `public.applications.values_scorecard` and marks the draft submitted

🔒 Submission rules, all enforced server-side:
- `require_approver`. Never `get_current_user`.
- Re-run `validate_markaz_payload` immediately before the write. Never trust a stored draft.
- Refuse if the draft is already `submitted` (409), so a double-click cannot overwrite a live record twice.
- Write `approved_by`, `approved_at`, `submitted_at` and the exact `markaz_payload` sent.
- **Log the payload verbatim before the write.**
- The UPDATE targets one `application_id` and must assert exactly one row was affected.

- [ ] **Step 1: Write the failing test**

```python
def test_submit_requires_approver_and_generate_requires_editor():
    from webapp.main import app

    def _routes():
        out = []
        def walk(rs):
            for r in rs:
                if hasattr(r, "path"):
                    out.append(r)
                elif hasattr(r, "original_router"):
                    walk(r.original_router.routes)
        walk(app.routes)
        return out

    paths = {r.path for r in _routes()}
    assert "/api/values-scorecards/generate" in paths
    assert "/api/values-scorecards/{draft_id}/submit" in paths

    import webapp.routers.values_scorecards as m
    src = open(m.__file__, encoding="utf-8").read()
    # The submit endpoint must be gated on approver, not on any signed-in user.
    assert "require_approver" in src
    submit_block = src.split("def submit")[1]
    assert "get_current_user" not in submit_block
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest webapp/tests/test_values_scoring.py -v`
Expected: FAIL, `/api/values-scorecards/generate` not in paths

- [ ] **Step 3: Write the router, schemas and mounting**

Model it on `webapp/routers/evaluations.py` for style and on `webapp/routers/communications.py` for the draft/approve lifecycle. Mount it in `webapp/main.py` beside the other routers.

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest webapp/tests/ -q`
Expected: all pass

- [ ] **Step 5: Commit**

```bash
git add webapp/routers/values_scorecards.py webapp/schemas.py webapp/main.py webapp/tests/test_values_scoring.py
git commit -m "feat(values): scorecard router, approver-gated Markaz submission"
```

---

### Task 7: The UI

**Files:**
- Create: `frontend/src/pages/ValuesScorecardPage.tsx`
- Modify: `frontend/src/lib/types.ts`, `frontend/src/lib/api.ts`, `frontend/src/App.tsx`, `frontend/src/lib/modules.ts` (add the sub-page to the Candidate Evaluation module)

**Interfaces:**
- Consumes: the four endpoints from Task 6
- Produces: the `/values-scorecards` route

Flow: pick an application, paste the transcript, generate, then the draft renders **in full** in the locked layout (per value: Deep Dive, Curve Ball, Micro Case, Rating), with the tally and the computed verdict shown, GWC shown only on a PASS. Evidence and ratings are editable; editing recomputes the verdict live. A single **Submit to Markaz** button, visible only to an approver, with a confirmation naming the candidate and the application id.

🔒 The draft must be shown in full before any write is possible. That is the locked process rule and the reason this screen exists.

- [ ] **Step 1: Build the page** following `QueuePage.tsx` and `ReviewInboxPage.tsx` for the app's token classes. Reuse the paging, error-state and request-token patterns from `EvaluationPage.tsx`; do not reinvent them.
- [ ] **Step 2: Add the route above the `/modules/:slug` catch-all** in `App.tsx`, and add a `Values Scorecards` entry to the Candidate Evaluation module's sub-pages in `modules.ts` so it appears in the sidebar.
- [ ] **Step 3: Verify**

```bash
cd frontend && npm run build
```
Then run the API and click through: generate a draft from a real transcript, confirm all six values render with three evidence fields each, confirm the verdict matches the ratings, edit a rating to a minus and confirm the verdict flips to OUT and GWC disappears.

- [ ] **Step 4: Commit**

```bash
git add frontend/
git commit -m "feat(values): scorecard drafting UI, full draft shown before any submission"
```

---

## Final verification before deploy

- [ ] `python -m pytest webapp/tests/ -q` passes
- [ ] `cd frontend && npm run build` compiles clean
- [ ] **Prove the approver gate fires.** Call submit as a non-approver and confirm 403. A gate that has only ever passed proves nothing.
- [ ] **Prove the verdict cannot be overridden by the model** (the Task 5 test) and that a `-` anywhere forces OUT.
- [ ] **Submit exactly one scorecard end to end against a real application, chosen by Ayesha**, then read `public.applications.values_scorecard` back and confirm it matches the payload logged at submit time, byte for byte.
- [ ] Confirm in Markaz's own UI that the submitted scorecard renders. This is the only check that catches a schema problem, and it cannot be done from here: **ask Ayesha to look.**
- [ ] Apply the migration: `railway run --service elegant-benevolence alembic upgrade head`
- [ ] Deploy with `scripts/deploy_webapp.sh`, then poll `/healthz` until the SHA matches. A `+dirty` suffix means what shipped is not that commit.
