---
name: Case Study Evaluation — Phase 3 Built (2026-09-22)
description: Coco can score a case study against a QA'd benchmark on six weighted dimensions, with a real zero anchor. Records the two Criticals that a green test suite could not catch (a missing Dockerfile COPY that would have bricked the whole app, and failed extractions being scored as candidate work), and why the frontend has failed review three times.
type: project
---

# Case study evaluation, Phase 3 (2026-09-22)

**Branch:** `feat/candidate-evaluation`, 45 commits, **not merged, not deployed.**
**Plan:** [docs/plans/2026-09-22-candidate-evaluation-phase3-case-study.md](../docs/plans/2026-09-22-candidate-evaluation-phase3-case-study.md)

Write a benchmark, an approver QAs it, then submissions score against it on six weighted
dimensions. 379 tests pass (0 skipped when the DB is reachable). Markaz's 219 scorecards and
Nugget's 863 evaluations were untouched throughout.

---

## 🔴 The rubric now has a real zero

It anchored at 5/3/1 with no zero, flooring every dimension at 20% of its weight: a submission
answering the wrong question banked 20 of 100 automatically. That is the defect in CLAUDE.md
Rule 27 which put **all 25 RM case studies above the published bar** and needed a strict re-mark
(mean 88.3 → 75.0).

Now 0-5 with a written zero per dimension. Measured: all-zero totals **0.0** (was 20), all-ones
20.0, all-fives 100.0. **Ayesha kept the bands (80/65/50)**, so totals fall and the bar genuinely
rises. That was the explicit choice over rescaling.

⚠️ Dimension 5's old "1" anchor conflated *absent* with *weak* ("Absent, or success metrics with
no failure condition"). Under a real zero those split: 0 is absent, 1 is present-but-soft.

## 🔴 Two Criticals a green test suite could not catch

Both found only by the whole-branch review, after seven clean task reviews and 339 passing tests.

**1. A deploy would have bricked the ENTIRE app.** `webapp/services/submissions.py` imports
`scripts.evals.fetch_submission_corpora` at module scope; the router imports submissions;
`main.py` imports the router. The Dockerfile copies seven named `scripts/` files and that was not
one of them. On Railway: `ModuleNotFoundError` during app import, uvicorn never binds, `/healthz`
never answers, and the candidate queue, drafting and values scorecards all go down with it.
**Invisible locally because the repo checkout has the file.**
🔑 Fixed, plus `webapp/tests/test_scripts_modules_shipped.py` now AST-scans every module-scope
`scripts.*` import under `webapp/` and asserts a matching Dockerfile COPY. Proven to fail when
the COPY is removed.

**2. A failed extraction was scored as the candidate's work.** `extract()` returns the *string*
`"[EXTRACT FAILED …]"`, which is truthy, so it entered the corpus, counted toward the readability
floor, and was listed in `sources` as a verified origin. And `requirements.txt` had python-docx
but **no python-pptx, openpyxl or PyMuPDF** — so in production every deck, spreadsheet and PDF
produced that string. A candidate submitting a doc plus a deck plus a model would have been scored
on the doc alone. **Invisible locally because those libraries are installed in `.venv`.**

🔑 **The lesson: "N tests green" says nothing about whether the app boots in production.** Both
defects existed only inside the container. Check what the image actually contains.

## 🔴 Rule 0 is now a foreign key, and its SQL is finally tested

`coco.eval_benchmarks.qa_approved_at` gates scoring: 409 unless the job has an approved,
QA'd benchmark. Scoring calibrates to whoever is read first, so this makes Rule 0 mechanical.

⚠️ The gate's SQL was **never executed by any test** — the fake session matched a substring and
re-implemented the predicate in Python, so the gate could have been opened entirely with every
test still green. Now the real imported statement runs against in-memory SQLite
(`ATTACH DATABASE ':memory:' AS coco`), covering: no row, draft, retired, approved-but-null, and
a genuine approval. The SQL also now requires `qa_approved_at IS NOT NULL`, backed by a CHECK
constraint so model and SQL cannot diverge.

## Why the frontend has failed review three times

**The repo has no frontend test framework at all** — no vitest, no jest, no testing-library, no
`*.test.*` files. Ruling "the UI ships with manual verification only" was made in all three
phases and failed all three times, but it was never a lapse: there is no way to test the UI.
Phase 1 lost a table behind a stale error, Phase 2 could submit unsaved edits, Phase 3 duplicated
the rubric dimensions into TypeScript where a renamed key would silently stop rendering.
🔑 **Any future "manual verification only" ruling is a restatement of this gap, not a decision.**

## Other things worth keeping

- **Retrieval is three channels, all fragile.** Markaz mirrors submissions to email; SMG arrives as
  Drive links; the file API 401s (expected, not a blocker); `uploads/...` returns **200 with the
  SPA's index.html** so `content_type` must be checked, not status; Markaz subjects carry double
  spaces. An unreadable submission is **refused**, never scored as weak.
- **Provenance:** `rubric_sha256` and `corpus_chars` are stored per evaluation, so a score can be
  tied to the rubric text that produced it. Without it, rows scored before and after an anchor
  edit are indistinguishable.
- `socket.timeout` does not bound DNS resolution. "DATABASE_URL is set" is not "the DB is
  reachable" — that confusion made the suite take 414s instead of 5s.

## Outstanding

1. **Migrations 0009, 0010 and 0011 are unapplied** (production is at 0008).
   `railway run --service elegant-benevolence alembic upgrade head`. ⚠️ Port 5432 is blocked
   locally, so `railway run` is the only path and takes minutes per invocation.
2. **Rule 25 has no real support.** `/score` is not idempotent; re-scoring leaves several rows.
   The UI marks the newest "Current" and older ones "Superseded", which makes it legible but
   retires nothing in the database. A retirement workflow is unscoped.
3. **Phase 4 (CV screening) is not started**, and whether it is needed at all depends on Aymen's
   answer about extending Nugget's rubrics to non-technical roles.
4. Production runs `cfd3715+dirty` with 45 commits unmerged to main.
