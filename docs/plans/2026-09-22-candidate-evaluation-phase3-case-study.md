# Candidate Evaluation Phase 3: Case Study Evaluation — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Score a case-study submission against a QA'd benchmark on six weighted dimensions, show the evaluation in full, and produce the locked report. Covers Skill 02 components #3 (scoring rubric), #4 (case study evaluation) and #6 (KCD, which folds into the rubric).

**Architecture:** The same shape that worked in Phase 2. Pure scoring rules first (weights, bands, flags, the 0-5 conversion) with no model and no database, so the non-negotiables are exhaustively testable. Benchmarks live in `coco.eval_benchmarks` and a run **cannot start** without a QA'd benchmark for that job, which turns Rule 17 from a discipline into a foreign key. Retrieval reuses the existing `scripts/evals/fetch_submission_corpora.py` rather than becoming a fourth retriever.

**Tech Stack:** FastAPI, SQLAlchemy 2.x, Pydantic v2, Anthropic SDK via the existing `AnthropicDrafter`, React + TypeScript, pytest.

**Spec:** [docs/specs/2026-09-16-candidate-evaluation-module-design.md](../specs/2026-09-16-candidate-evaluation-module-design.md) (Phase 3)

## Global Constraints

- 🔒 **Rule 0, benchmark before submissions.** The benchmark is written and QA'd BEFORE any submission is opened. Scoring calibrates to whoever is read first. Enforced in the schema: a run requires a benchmark row with `qa_approved_at` set.
- 🔒 **The benchmark carries NO candidate names or responses** (CLAUDE.md Rule 17). It must calibrate against the case, not against this cohort, or it stops being reusable.
- 🔒 **Six dimensions, weighted to 100:** Data judgment 20, Execution specificity 25, Stakeholder craft 20, Commercial honesty 15, Decision discipline 10, Signal & self-awareness 10.
- 🔒 **Scored 0-5 with a REAL ZERO** (Ayesha, 2026-09-22). The rubric's current 5/3/1 anchors create the ~20% floor that put all 25 RM case studies above the bar (CLAUDE.md Rule 27). Conversion: 5→100%, 4→80%, 3→60%, 2→40%, 1→20%, 0→0.
- 🔒 **Bands are UNCHANGED** (Ayesha, 2026-09-22): 80+ strong yes, 65-79 yes, 50-64 borderline, <50 no. The bar genuinely rises with the zero. That is the intent.
- 🔒 **Flags override the score.** Fabricated data is disqualifying regardless of total.
- 🔒 **Never force a fixed shortlist size.** If three clear the bar, recommend three.
- 🔒 **Every score cites evidence** — a quoted line, slide number or figure. A score without a citation is an impression.
- 🔒 **Score reasoning, not agreement.** A candidate who disagrees with the benchmark with a real argument scores as high as one who matches it.
- 🔒 Coco's tables live in the **`coco`** schema, never `public`.
- `from __future__ import annotations` in every new module. No em dashes in user-facing copy.

---

### Task 1: Give the rubric a real zero

**Files:**
- Modify: `.claude/skills/02_candidate-evaluation/case-study-scoring-rubric.md`

**Why first:** Task 3's scoring logic encodes these anchors, and Task 5's prompt reads this file. Ayesha approved the change on 2026-09-22 after seeing that the file's 5/3/1 anchors are the exact defect CLAUDE.md Rule 27 records.

- [ ] **Step 1: Add a 0 anchor to each of the six dimensions**

Keep every existing 5/3/1 anchor's wording unchanged. Add a `0` beneath each, in the file's existing terse voice:

| Dimension | New 0 anchor |
|---|---|
| 1. Data judgment | **0** — The dataset is not engaged. No figures cited, or the analysis answers a different question than the one asked. |
| 2. Execution specificity | **0** — No plan submitted, or a document with no actions in it at all. |
| 3. Stakeholder craft | **0** — No email submitted, or it does not address the situation described. |
| 4. Commercial honesty | **0** — No internal update, or it contains neither a likelihood nor an ask. |
| 5. Decision discipline | **0** — Absent entirely. |
| 6. Signal & self-awareness | **0** — No reflection submitted. |

⚠️ Dimension 5's existing **1** anchor reads "Absent, or success metrics with no failure condition" and conflates absent with weak. Split it: `0` takes "absent entirely", and `1` becomes "Success metrics with no failure condition." Do not change 3 or 5.

- [ ] **Step 2: Replace the scale line and record why**

Change "Each scored 1–5. Weighted total out of 100." to:

```markdown
Each scored **0–5, with a real zero**. Weighted total out of 100.
Conversion: 5→100%, 4→80%, 3→60%, 2→40%, 1→20%, 0→0.

🔒 **The zero is not decorative (Ayesha, 2026-09-22).** This rubric previously anchored at
5/3/1 with no zero, which floors every dimension at 20% of its weight: a submission answering
the wrong question still banked 20 points. That is the defect recorded in CLAUDE.md Rule 27,
which put all 25 RM case studies above the published bar and required a strict re-mark that
moved the mean from 88.3 to 75.0. An absent or wholly wrong answer scores 0, not a middling guess.

**The bands below are unchanged.** Totals therefore fall, and the bar genuinely rises. That is
the intent, not a side effect to be corrected by rescaling.
```

- [ ] **Step 3: Clear the DRAFT status**

The header says `**Status:** DRAFT — pending Ayesha's QA (2026-08-16)`. Replace with
`**Status:** Anchors and bands approved by Ayesha 2026-09-22. Report spec still as drafted 2026-08-16.`
Do not claim more approval than was given: she approved the 0-5 anchors and keeping the bands.

- [ ] **Step 4: Verify**

Run: `grep -c '^- \*\*0\*\*' .claude/skills/02_candidate-evaluation/case-study-scoring-rubric.md`
Expected: `6`. Confirm the flags table, the bands table and the report spec are untouched.

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/02_candidate-evaluation/case-study-scoring-rubric.md
git commit -m "docs(rubric): a real zero anchor, removing the 20 percent floor"
```

---

### Task 2: Pure scoring rules

**Files:**
- Create: `webapp/services/case_study_scoring.py`
- Test: `webapp/tests/test_case_study_scoring.py`

**Interfaces:**
- Consumes: nothing (pure)
- Produces:
  - `DIMENSIONS: tuple[dict, ...]` — six entries `{key, label, weight}`, weights 20/25/20/15/10/10
  - `SCORES: tuple[int, ...]` = `(0, 1, 2, 3, 4, 5)`
  - `FLAGS: dict[str, str]` — flag key to severity (`disqualifying` / `serious` / `note`)
  - `weighted_total(scores: dict[str, int]) -> float`
  - `band(total: float, flags: list[str]) -> str` — `"strong_yes" | "yes" | "borderline" | "no" | "disqualified"`
  - `CaseStudyScoringError(Exception)`
  - `validate_scores(scores: dict) -> None`

- [ ] **Step 1: Write the failing test**

```python
"""The locked case-study scoring rules, tested without a model or a database.

The zero is the point: anchoring at 1 floors every dimension at 20% of its weight,
which is the defect that put all 25 RM case studies above the bar (CLAUDE.md Rule 27).
"""

from __future__ import annotations

import pytest

from webapp.services.case_study_scoring import (
    DIMENSIONS,
    SCORES,
    CaseStudyScoringError,
    band,
    validate_scores,
    weighted_total,
)


def _all(n):
    return {d["key"]: n for d in DIMENSIONS}


def test_weights_are_the_locked_six_and_sum_to_100():
    assert [d["weight"] for d in DIMENSIONS] == [20, 25, 20, 15, 10, 10]
    assert sum(d["weight"] for d in DIMENSIONS) == 100
    assert len(DIMENSIONS) == 6


def test_the_scale_has_a_real_zero():
    assert SCORES == (0, 1, 2, 3, 4, 5)
    # THE defect this rubric change exists to remove: all-minimum must be 0, not 20.
    assert weighted_total(_all(0)) == 0.0


def test_conversion_is_linear_on_the_full_scale():
    assert weighted_total(_all(5)) == 100.0
    assert weighted_total(_all(4)) == 80.0
    assert weighted_total(_all(3)) == 60.0
    assert weighted_total(_all(2)) == 40.0
    assert weighted_total(_all(1)) == 20.0


def test_weighting_is_per_dimension_not_flat():
    # Only Execution specificity (weight 25) at full marks.
    scores = _all(0)
    scores["execution_specificity"] = 5
    assert weighted_total(scores) == 25.0


def test_bands_match_the_locked_thresholds():
    assert band(80.0, []) == "strong_yes"
    assert band(95.0, []) == "strong_yes"
    assert band(79.9, []) == "yes"
    assert band(65.0, []) == "yes"
    assert band(64.9, []) == "borderline"
    assert band(50.0, []) == "borderline"
    assert band(49.9, []) == "no"
    assert band(0.0, []) == "no"


def test_fabricated_data_disqualifies_regardless_of_total():
    assert band(100.0, ["fabricated_data"]) == "disqualified"
    assert band(92.0, ["fabricated_data", "undisclosed_ai"]) == "disqualified"
    # A serious-but-not-disqualifying flag does NOT override the band.
    assert band(92.0, ["undisclosed_ai"]) == "strong_yes"


def test_validate_rejects_a_bad_score_set():
    with pytest.raises(CaseStudyScoringError):
        validate_scores({d["key"]: 3 for d in DIMENSIONS[:5]})     # missing one
    with pytest.raises(CaseStudyScoringError):
        bad = _all(3); bad["data_judgment"] = 6
        validate_scores(bad)                                        # out of range
    with pytest.raises(CaseStudyScoringError):
        bad = _all(3); bad["not_a_dimension"] = 3
        validate_scores(bad)                                        # unknown key
    with pytest.raises(CaseStudyScoringError):
        bad = _all(3); bad["data_judgment"] = 2.5
        validate_scores(bad)                                        # not an integer
    validate_scores(_all(0))                                        # zero is VALID
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest webapp/tests/test_case_study_scoring.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'webapp.services.case_study_scoring'`

- [ ] **Step 3: Write minimal implementation**

```python
"""The locked case-study scoring rules.

Pure: no model, no database. Weights, the 0-5 conversion, the bands and the flag
overrides are non-negotiable, so they live here and are tested directly.

🔒 The scale runs 0-5 WITH A REAL ZERO (Ayesha, 2026-09-22). Anchoring at 1 floors
every dimension at 20% of its weight, which is the defect recorded in CLAUDE.md
Rule 27: it put all 25 RM case studies above the published bar. An absent or wholly
wrong answer scores 0, not a middling guess. The bands are deliberately unchanged,
so totals fall and the bar rises.
"""

from __future__ import annotations

DIMENSIONS = (
    {"key": "data_judgment", "label": "Data judgment", "weight": 20},
    {"key": "execution_specificity", "label": "Execution specificity", "weight": 25},
    {"key": "stakeholder_craft", "label": "Stakeholder craft", "weight": 20},
    {"key": "commercial_honesty", "label": "Commercial honesty", "weight": 15},
    {"key": "decision_discipline", "label": "Decision discipline", "weight": 10},
    {"key": "signal_self_awareness", "label": "Signal & self-awareness", "weight": 10},
)

SCORES = (0, 1, 2, 3, 4, 5)
_MAX = 5

# A flag can outrank a high total. Only `disqualifying` changes the band.
FLAGS = {
    "fabricated_data": "disqualifying",
    "undisclosed_ai": "serious",
    "materially_incomplete": "serious",
    "instruction_breach": "note",
    "consent_blindness": "note",
}

_KEYS = {d["key"] for d in DIMENSIONS}


class CaseStudyScoringError(ValueError):
    """The score set does not match the locked shape."""


def validate_scores(scores: dict) -> None:
    keys = set(scores)
    if keys != _KEYS:
        missing, extra = sorted(_KEYS - keys), sorted(keys - _KEYS)
        raise CaseStudyScoringError(f"missing {missing}, unexpected {extra}")
    for k, v in scores.items():
        # bool is an int subclass; reject it explicitly.
        if isinstance(v, bool) or not isinstance(v, int) or v not in SCORES:
            raise CaseStudyScoringError(f"{k}: score must be an integer in {SCORES}, got {v!r}")


def weighted_total(scores: dict) -> float:
    validate_scores(scores)
    total = sum(scores[d["key"]] / _MAX * d["weight"] for d in DIMENSIONS)
    return round(total, 2)


def band(total: float, flags: list[str]) -> str:
    if any(FLAGS.get(f) == "disqualifying" for f in flags):
        return "disqualified"
    if total >= 80:
        return "strong_yes"
    if total >= 65:
        return "yes"
    if total >= 50:
        return "borderline"
    return "no"
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest webapp/tests/test_case_study_scoring.py -v`
Expected: PASS (7 tests)

- [ ] **Step 5: Commit**

```bash
git add webapp/services/case_study_scoring.py webapp/tests/test_case_study_scoring.py
git commit -m "feat(case-study): scoring rules on a 0-5 scale with a real zero"
```

---

### Task 3: Benchmark storage, with Rule 0 as a foreign key

**Files:**
- Modify: `webapp/models.py`, `webapp/db.py`
- Create: `alembic/versions/0009_eval_benchmarks.py`
- Test: `webapp/tests/test_case_study_scoring.py`

**Interfaces:**
- Produces: `EvalBenchmark` model, table `coco.eval_benchmarks`

🔒 Schema `coco`, following `ValuesScorecardDraft` exactly. Columns: `id` (str pk), `job_id` (int, indexed), `kind` (text, e.g. `case_study`), `title` (text), `body` (text), `source_path` (text, nullable), `created_by` (text), `created_at` (timestamptz), `qa_approved_by` (text, nullable), `qa_approved_at` (timestamptz, nullable), `status` (text: `draft` / `approved` / `retired`).

**Why this table is the whole point:** Rule 0 says the benchmark is written and QA'd before any submission is read, because scoring calibrates to whoever is read first. A run that requires `qa_approved_at` cannot start early. That is discipline made mechanical.

- [ ] **Step 1: Write the failing test**

```python
def test_benchmark_table_is_in_the_coco_schema():
    from webapp.models import EvalBenchmark
    assert EvalBenchmark.__table__.schema == "coco"


def test_benchmark_carries_a_qa_gate():
    from webapp.models import EvalBenchmark
    cols = {c.name for c in EvalBenchmark.__table__.columns}
    # Rule 0 is enforced by requiring these before a run may start.
    assert {"qa_approved_at", "qa_approved_by", "status"} <= cols
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest webapp/tests/test_case_study_scoring.py -v`
Expected: FAIL with `ImportError: cannot import name 'EvalBenchmark'`

- [ ] **Step 3: Write the model, self-heal entry and migration**

Add `EvalBenchmark` to `webapp/models.py` following `ValuesScorecardDraft`'s structure and its `{"schema": "coco"}` table arg. Add it to the `tables=[...]` list in `db.ensure_app_tables`. Write `alembic/versions/0009_eval_benchmarks.py` with `CREATE SCHEMA IF NOT EXISTS coco` first; read `alembic/versions/0008_*.py` for the correct `down_revision` and style.

⚠️ Do NOT run the migration. Production is applied by hand and **port 5432 is blocked from this machine**, so local alembic cannot connect; `railway run --service elegant-benevolence alembic upgrade head` is the only working path and takes a few minutes per invocation. Verify the file by importing it.

⚠️ Also add `"eval_benchmarks"` to `MANAGED_TABLES` in `alembic/env.py`, or autogenerate will ignore the table and never detect drift on it (this was missed for `values_scorecard_drafts` and had to be fixed later).

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest webapp/tests/ -q`
Expected: all pass

- [ ] **Step 5: Commit**

```bash
git add webapp/models.py webapp/db.py alembic/versions/0009_eval_benchmarks.py alembic/env.py webapp/tests/test_case_study_scoring.py
git commit -m "feat(case-study): benchmark storage with the Rule 0 QA gate"
```

---

### Task 4: Submission retrieval

**Files:**
- Create: `webapp/services/submissions.py`
- Test: `webapp/tests/test_case_study_scoring.py`

**Interfaces:**
- Consumes: `scripts/evals/fetch_submission_corpora.py` (151 lines, already extracts docx text boxes and tables, pptx notes, xlsx values and formulas, and PDF via PyMuPDF). **Reuse it. Do not write a fourth retriever.**
- Produces: `corpus_for(application_id) -> dict` with `{text, sources: list[str], chars, usable: bool}`, and `SubmissionUnreadable(Exception)`

**Why this is the hard part.** Retrieval is not one path, and the repo has paid for each lesson:
- Markaz mirrors every document submission to email as an attachment, so **the mailbox is the first place to look, not the last** (Rule 18).
- SMG submissions arrive as **Markaz Drive links, not attachments** (Rule 26).
- `/api/case-study-file/<app>/<word|excel>` returns **401** to automation and is not a blocker.
- `markaz.taleemabad.com/uploads/...` returns **HTTP 200 with the SPA's index.html** — check `content_type`, not status.
- Markaz subject lines contain **double spaces** ("Growth  Manager") which break naive keyword search.
- `case_study_status` stays null even when Markaz sent a case study, so it proves nothing.

- [ ] **Step 1** — Write a test asserting `corpus_for` refuses rather than returns empty text: a source that yields under a usable threshold raises `SubmissionUnreadable`, mirroring `cv_text.CVUnreadable`. An unreadable submission must never be scored as a weak one. Follow `webapp/services/cv_text.py` for the refusal pattern and reuse its `MIN_USABLE_CHARS` thinking.
- [ ] **Step 2** — Run it and watch it fail.
- [ ] **Step 3** — Implement, delegating extraction to `fetch_submission_corpora`. Record every source actually read in `sources` so the report's method note can say what was verified and what could not be accessed.
- [ ] **Step 4** — Run the tests.
- [ ] **Step 5** — Commit: `feat(case-study): submission retrieval that refuses rather than returns empty`

---

### Task 5: The scoring service

**Files:**
- Create: `webapp/prompts/case_study_prompt.py`
- Modify: `webapp/services/case_study_scoring.py`
- Test: `webapp/tests/test_case_study_scoring.py`

**Interfaces:**
- Consumes: `get_drafter()`, `DIMENSIONS`, `validate_scores`, `weighted_total`, `band`, the benchmark body, the submission corpus
- Produces: `score_submission(*, corpus, benchmark_body, candidate_name, role) -> dict` returning `{scores, evidence, flags, total, band, model}`

🔒 Rules the code enforces after the call, not the prompt:
- **The total and the band are computed by `weighted_total` and `band`, never taken from the model.**
- `validate_scores` runs on the response; malformed is retried once then raises. Never repaired.
- **Every dimension must carry an evidence citation.** A score with an empty citation is rejected, per Rule 1.
- A `fabricated_data` flag forces `disqualified` regardless of total.
- The prompt reads the rubric file at import and **logs at ERROR and raises if it is missing** — do NOT copy `tone_rules.py`'s silent `except OSError: return ""`.
- The prompt must carry Rule 3 explicitly: a candidate who disagrees with the benchmark with a real argument scores as high as one who matches it.

- [ ] **Step 1** — Test that a model returning `total: 95` on a score set worth 40 is overruled to 40, that a `fabricated_data` flag forces `disqualified` even at 100, and that a dimension with an empty evidence citation is rejected. Monkeypatch `_call_model`; no network.
- [ ] **Step 2** — Run and watch fail.
- [ ] **Step 3** — Implement.
- [ ] **Step 4** — Run the tests.
- [ ] **Step 5** — Commit: `feat(case-study): scoring service, total and band computed in code`

---

### Task 6: Router

**Files:**
- Create: `webapp/routers/case_studies.py`
- Modify: `webapp/schemas.py`, `webapp/main.py`
- Test: `webapp/tests/test_case_study_scoring.py`

Endpoints, gates matching Phase 2's pattern:
- `POST /api/case-studies/benchmarks` — **require_editor** — create a benchmark (status `draft`)
- `POST /api/case-studies/benchmarks/{id}/approve` — **require_approver** — sets `qa_approved_by/at`, status `approved`
- `POST /api/case-studies/score` — **require_editor** — 🔒 **409 unless an `approved` benchmark exists for that job.** This is Rule 0.
- `GET /api/case-studies/evaluations/{id}` — **require_editor**

🔒 Assert the gates on `route.dependant.dependencies`, not on source text. A source-text assertion matches the module docstring and passes with the wrong dependency — that exact mistake shipped in Phase 2 and was only caught in review. Prove the test bites by flipping a gate and watching it fail.

- [ ] Steps 1-5 as in Phase 2's Task 6, including the dependency-identity test and a `TestClient` + `dependency_overrides` test asserting a real 403 per role.

---

### Task 7: UI

**Files:**
- Create: `frontend/src/pages/CaseStudyPage.tsx`
- Modify: `frontend/src/lib/types.ts`, `api.ts`, `App.tsx`, `modules.ts`, `components/AppLayout.tsx`

Flow: write or paste a benchmark, an approver approves it, then score submissions against it. The evaluation renders in full: six dimensions with score, weight and the quoted evidence, the computed total and band, and any flags shown prominently since a disqualifying flag outranks the total.

🔒 **Scoring is blocked in the UI until the benchmark is approved**, with the reason stated plainly, so Rule 0 is visible rather than a surprise 409.
🔒 The total and band come from the server. Do not recompute in the browser.
🔒 Follow `QueuePage.tsx` / `ReviewInboxPage.tsx` for token classes. Reuse `EvaluationPage.tsx`'s request-token and error-state patterns.

- [ ] Steps as in Phase 2's Task 7, ending with `npm run build` clean and a click-through.

---

## Final verification before deploy

- [ ] `python -m pytest webapp/tests/ -q` passes
- [ ] `cd frontend && npm run build` compiles clean
- [ ] **Prove the Rule 0 gate fires:** attempt to score against an unapproved benchmark and confirm 409.
- [ ] **Prove the zero is real:** an all-zero score set totals 0, not 20.
- [ ] **Prove a disqualifying flag outranks a high total.**
- [ ] **Prove the auth gates bite** by flipping one and watching the test fail.
- [ ] Score one real submission end to end against a QA'd benchmark, and read the evidence citations against the actual document.
- [ ] Apply migration 0009: `railway run --service elegant-benevolence alembic upgrade head`
  (⚠️ port 5432 is blocked locally; `railway run` is the only path and takes minutes per call)
- [ ] Deploy, then poll `/healthz` until the SHA matches. `+dirty` means what shipped is not that commit.
