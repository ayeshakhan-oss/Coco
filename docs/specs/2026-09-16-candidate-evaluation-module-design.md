# Candidate Evaluation module — design

**Date:** 2026-09-16 · **Status:** DRAFT, awaiting Ayesha's review
**Decision on record (Ayesha, 2026-09-15):** ship all six components; on the duplication
question, "1st and 2nd both" — extend Nugget's engine **and** build scoring in Coco.

---

## Goal

Turn the live app's `candidate-evaluation` tile from a `status: 'soon'` placeholder into a
working module, covering all six components of Skill 02.

Today the tile routes to `ComingSoonPage` via `/modules/:slug`
([App.tsx:26](../../frontend/src/App.tsx#L26)), and only `candidate-communication` is `'live'`
([modules.ts:15](../../frontend/src/lib/modules.ts#L15)).

## The six components

| # | Component | What it produces | Automatable? |
|---|---|---|---|
| 1 | `technical-screening` | Read Nugget's tiers, scores, strengths, gaps | **Already exists.** Display only. |
| 2 | `values-scorecard-scoring` | 6 values + GWC from a transcript, written to Markaz | Yes, with a hard approval gate |
| 3 | `case-study-scoring-rubric` | 6 weighted dimensions, flags, bands | Yes |
| 4 | `case-study-evaluation` | Retrieval + scoring + report | Retrieval is the hard part |
| 5 | `cv-screening` | Screening report, 4 stat boxes, ranked profiles | Yes, but see duplication |
| 6 | `kcd-evaluation` | Framework applied to a case study | Folds into #3/#4 |

---

## The decision that makes "both engines" safe

Running Coco's scoring alongside Nugget's risks two sets of numbers that disagree about the same
candidate. **One rubric format removes that risk.**

Coco adopts Nugget's rubric schema rather than inventing one:

- dimensions with a `key`, `label`, `weight`, `max: 5`, `core: bool`
- **`anchors` for all six values 0 to 5, with a real written zero**
- `look_for` and `common_gaps` per dimension
- `thresholds` with absolute bands **and per-tier `min_dimension` gates**
- `hard_filters` with `action` (`reject` / `flag`) and `on_unknown` (`pass` / `flag`)
- `manual_review_rules` (`min_resume_chars`, `min_resume_health`)

Two consequences worth stating plainly:

1. A Coco evaluation and a Nugget evaluation are **the same shape**, so one UI renders both and
   one report format serves both.
2. The real-zero anchor rule is inherited by construction. That is the direct fix for the defect
   that put all 25 RM case studies above the bar
   ([lesson_scoring_anchor_floor_inflation_2026_09_02.md](../../memory/lesson_scoring_anchor_floor_inflation_2026_09_02.md)),
   and it is enforced by a schema validator, not by discipline.

**Division of labour:** Nugget scores technical roles (and we ask Aymen to add non-technical
rubrics). Coco scores what Nugget does not cover, reads Nugget's results where they exist, and is
the reporting layer for both. `source` on every evaluation says which engine produced it, and
**the UI never silently mixes them.**

---

## Data model

🔒 **Every new table lives in the `coco` schema**, never `public`. Markaz's Replit deploys drop
Coco's public tables; this is already the pattern at
[models.py:271-274](../../webapp/models.py#L271-L274).

```
coco.eval_rubrics      id, job_id, version, status, kind, title, seniority, min_years,
                       jd_snapshot, dimensions(jsonb), max_score, thresholds(jsonb),
                       hard_filters(jsonb), manual_review_rules(jsonb),
                       system_prompt, system_prompt_hash, created_by, activated_at
coco.eval_runs         id, job_id, rubric_id, kind, status, model, cost_cap_usd,
                       planned/done/ok/unusable/failed counts, actual_cost_usd,
                       requested_by, created_at, finished_at
coco.evaluations       id, run_id, rubric_id, job_id, candidate_id, application_id,
                       source ('coco'|'nugget'), kind,
                       total_score, max_score, score_pct, dimension_scores(jsonb),
                       strengths(jsonb), gaps(jsonb), hard_filter_flags(jsonb),
                       verdict, confidence, tier, tier_reason,
                       evidence_health, evidence_chars, evidence_issues,
                       is_current, superseded_by, status, approved_by, approved_at,
                       model, cost_usd, evaluated_at
coco.eval_benchmarks   id, job_id, kind, body, created_by, created_at, qa_approved_at
```

Four things deliberately copied from Nugget because they solve problems we have already paid for:

- **`is_current` / `superseded_by`** — a re-mark retires the old score automatically. On the RM
  round this was done by hand and three artefacts were missed.
- **`cost_cap_usd` on the run** — a runaway batch stops itself.
- **`evidence_health`** separate from the score, so an unreadable document is never scored.
- **`kind`** (`cv` / `case_study` / `values` / `technical`) so one table serves all components.

**`coco.eval_benchmarks` exists to enforce Rule 17 in the schema:** a case-study run **cannot
start** unless a benchmark row for that job exists and is `qa_approved_at`. Benchmark before
submissions stops being a discipline and becomes a foreign key.

---

## Phases

Each phase leaves the app working. **Phases 1 and 2 ship together in one deploy** (Ayesha,
2026-09-16); phases 3 and 4 follow separately.

Within that push, Phase 1 still lands first and is independently revertable, so if Phase 2 slips
the tile is already live rather than the whole push being held.

### Phase 1 — Make the module live, read-only (smallest useful thing)

Covers component #1. No LLM calls, no new tables, no writes.

- `webapp/routers/evaluations.py` — `GET /api/evaluations/jobs`, `/jobs/{id}/summary`,
  `/jobs/{id}/candidates?tier=`, `/candidates/{app_id}`
- `webapp/services/nugget_reads.py` — the queries already proven in
  `scripts/screening/read_nugget_screening.py`, lifted into a service. **Read-only guard moves
  with them.**
- `frontend/src/pages/EvaluationPage.tsx` + a detail view; route added in `App.tsx`
- `modules.ts`: `candidate-evaluation` → `status: 'live'`
- Dockerfile + `.dockerignore`: add `.claude/skills/02_candidate-evaluation/`
  (the `!` negation must come **after** `.claude/skills/*`, and a `COPY` without it fails the
  build with `failed to compute cache key`)

**Non-negotiable in the UI:** `UNUSABLE` renders as "CV could not be read, needs a human", never
as a rejection or a zero score. Every figure is labelled with its source engine and rubric
version.

### Phase 2 — Values scorecard scoring

Covers #2. The highest-value automation because it runs on every candidate and currently costs
Ayesha a transcript read each time.

- Transcript in → 6 values scored with evidence quotes + GWC → **draft shown in full locked
  layout** → Ayesha approves → submit to Markaz.
- 🔒 **Two hard gates:** the draft is displayed in the locked Deep Dive / Curve Ball / Micro Case
  layout **before any DB write**, and the Markaz JSON must match
  `{date, host, candidateName, values[], finalComments, proceedToRightSeat}` exactly or it is
  invisible on Markaz's UI. Both are validated server-side, not trusted to the client.
- Pass/Out logic is computed and shown, never inferred by the model alone.

### Phase 3 — Case study evaluation + rubric + KCD

Covers #3, #4, #6.

- Benchmark editor writing `coco.eval_benchmarks`, with the QA gate described above.
- Six-dimension rubric from `case-study-scoring-rubric.md`, weighted
  Data 20 / Execution 25 / Stakeholder 20 / Commercial 15 / Discipline 10 / Signal 10.
- Retrieval is the real work and is **not** a single path: Markaz mirrors submissions to email as
  attachments, SMG submissions arrive as Drive links, `case_study_status` stays null after a real
  send, and `markaz.taleemabad.com/uploads/...` returns HTTP 200 with the SPA's index.html.
  Reuse `scripts/evals/fetch_submission_corpora.py` rather than writing a fourth retriever.
- 🔒 Quoted evidence is verified verbatim against the candidate's corpus before it can be saved.

### Phase 4 — CV screening

Covers #5. Last **on purpose**: it is the component that most overlaps Nugget, so it benefits
most from waiting to see whether Aymen's rubrics cover the roles we need.

- Rubric-driven scoring reusing `webapp/services/cv_text.py`, which already handles base64
  `resume_data`, refuses on unreadable input (`CVUnreadable`, `MIN_USABLE_CHARS`) and survived
  the pypdf letter-spacing defect.
- Report renders to the locked screening format: 4 stat boxes, hyperlinked Drive CVs, both total
  and relevant experience stated separately.

---

## What gets reused rather than rebuilt

| Need | Existing | Path |
|---|---|---|
| CV text from `resume_data` | `cv_text.py` (115 lines, refusal path built in) | `webapp/services/` |
| Candidate/application reads | `reads.py` (565 lines) | `webapp/services/` |
| Markaz scorecard normalising | `scorecard.py` | `webapp/services/` |
| Evidence assembly | `evidence.py` (253 lines) | `webapp/services/` |
| Anthropic call + review pass | `drafting.py` patterns | `webapp/services/` |
| Locked-module import surface | `reuse.py` | `webapp/` |
| Nugget queries | `read_nugget_screening.py` (verified working) | `scripts/screening/` |

## Risks

1. **Two engines disagreeing.** Mitigated by the shared rubric format, the `source` column, and
   never mixing engines in one ranking without labelling.
2. **Silent file loading.** `tone_rules.py`'s markdown readers are `@lru_cache`d and swallow
   `OSError`, so a missing skill file degrades output with no signal. Any Skill 02 reader must
   log loudly, and `/readyz` should assert the files exist.
3. **Scoring leniency.** A single unmoderated marker trends lenient. The schema validator
   rejecting anchor sets without a real zero is the mechanical guard; a second-read of anyone
   within ~8 points of a bar is the human one.
4. **Scope.** Four phases is genuinely multi-week. Phase 1 alone is small and delivers the tile.

## Decisions (Ayesha, 2026-09-16)

1. **Phases 1 and 2 ship together**, in one push and one review cycle. The tile goes live with
   the read-only view, and values scorecard scoring lands in the same deploy. Phases 3 and 4
   follow separately.
2. **Submitting a values scorecard to Markaz requires the `approver` role**, the same gate as
   sending a candidate email ([deps.py](../../webapp/deps.py), `require_approver`).
   *(Supersedes an earlier "any signed-in user" answer, given before the existing role model
   — `viewer < editor < approver < super_admin` — was on the table. Writing a permanent hiring
   record should not need less permission than sending an email.)*
   On top of the role gate: `approved_by` and `approved_at` are written on every submission, the
   Markaz payload is logged verbatim before it is sent, and there is **no auto-submit path** for
   any role.
3. **The request to Aymen for non-technical rubrics is drafted now**, so Phase 4 can shrink or be
   dropped if his engine covers those roles. Draft at
   [docs/request_aymen_non_technical_rubrics_2026_09_16.md](../request_aymen_non_technical_rubrics_2026_09_16.md).
