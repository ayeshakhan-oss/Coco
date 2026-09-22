"""Case-study benchmark authoring, QA approval, and scoring against a QA'd benchmark.

`webapp/services/case_study_scoring.py` holds the locked scoring rules (weights, the
0-5 conversion, bands, flag overrides) and `score_submission`, which calls the model
and re-validates its response against those rules; `webapp/services/submissions.py`
retrieves a candidate's case-study text or refuses (`SubmissionUnreadable`). This
router is the only code in the app that persists a benchmark or a scored evaluation.

🔒 **Rule 0 of the rubric is the point of this router**: "Scoring calibrates to
whoever is read first. Build and QA the benchmark BEFORE opening any submission."
`POST /score` enforces this mechanically: it refuses with 409 unless an `approved`
`EvalBenchmark` row exists for the TARGET APPLICATION'S OWN job (read from the
database, never a client-supplied job id). A missing benchmark, a `draft` one, or a
`retired` one all 409 identically -- there is no code path here that can score
against anything else.

Rules enforced below, verbatim rule -> mechanism:

  1. `require_editor` gates benchmark creation and scoring; `require_approver` gates
     approval -- the same bar Ayesha set for submitting a values scorecard (Phase 2):
     turning a draft benchmark into the one a scoring run may use is a decision, not
     an edit, and needs a second person's sign-off.
  2. The benchmark never trusts client-supplied QA fields. `qa_approved_by`,
     `qa_approved_at` and `status` are set ONLY inside `approve_benchmark`, from the
     authenticated approver, and are never accepted on the create body
     (`CaseStudyBenchmarkCreateRequest` carries no such fields at all).
  3. `approve_benchmark` refuses (409) unless the benchmark is currently `draft` --
     an already-`approved` benchmark cannot be re-approved (no double-audit-trail
     confusion about who actually approved it) and a `retired` one cannot be revived
     by this endpoint.
  4. `score` looks up the target application's `job_id` from the database itself
     (`reads.get_application`), never from the request body -- so the Rule 0 gate can
     never be pointed at the wrong job's benchmark by a mistaken or malicious
     `job_id` in the score request.
  5. `score` re-derives `corpus_for(...)` fresh on every call (never cached) and lets
     `SubmissionUnreadable` surface as 422 -- an unreadable submission is refused,
     never scored as a weak one (Rule 26 / cv_text's refusal pattern).
  6. The persisted `CaseStudyEvaluation` row records the exact `benchmark_id` used
     (not just "the job's benchmark"), so "which answer key produced this total" is
     always answerable later even if a newer benchmark revision is approved
     afterwards, and every dimension's evidence citation is stored verbatim
     alongside the computed total/band -- nobody recomputes it differently on a
     later read (`GET /evaluations/{id}` returns exactly what was persisted).
  7. The total and band are never recomputed here: they are taken as-is from
     `score_submission`'s return value, which itself computes them with
     `weighted_total`/`band` rather than trusting the model (Task 5's own rule).
"""

from __future__ import annotations

import datetime as dt
import logging

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import text
from sqlalchemy.orm import Session

from ..db import get_db
from ..deps import require_approver, require_editor
from ..models import CaseStudyEvaluation, EvalBenchmark
from ..schemas import (
    CaseStudyBenchmarkCreateRequest,
    CaseStudyBenchmarkOut,
    CaseStudyEvaluationOut,
    CaseStudyScoreRequest,
)
from ..services import reads
from ..services.case_study_scoring import DIMENSIONS, CaseStudyScoringError, score_submission
from ..services.drafting import DraftingUnavailable
from ..services.submissions import SubmissionUnreadable, corpus_for

log = logging.getLogger("webapp.case_studies")

router = APIRouter(prefix="/api/case-studies", tags=["case-studies"])

# The most recently approved benchmark for a job wins (a job can carry more than
# one benchmark row over time: a draft, a retired prior version, a later
# revision). `qa_approved_at` -- not `created_at` -- orders these, since that is
# the moment Rule 0 actually cleared.
#
# `AND qa_approved_at IS NOT NULL` matches the plan's own wording for Rule 0:
# "a benchmark row with qa_approved_at set", not just status='approved' alone.
# `approve_benchmark` always sets both together, and migration 0011 backs this
# with a matching CHECK constraint on the table (ck_eval_benchmark_approved_
# has_qa_approved_at) so the two cannot diverge.
_APPROVED_BENCHMARK_FOR_JOB_SQL = text(
    "SELECT id, body FROM coco.eval_benchmarks "
    "WHERE job_id = :job_id AND status = 'approved' AND qa_approved_at IS NOT NULL "
    "ORDER BY qa_approved_at DESC NULLS LAST LIMIT 1"
)

# IMPORTANT 5a: lists EVERY benchmark for a job regardless of status, newest
# first, so the UI can recover "which one is approved" on mount/reload
# instead of depending on a benchmark id pasted in by hand. Column list is
# written to match CaseStudyBenchmarkOut's field names/order exactly, so the
# router below can return `dict(row)` straight off `.mappings()` with no
# ORM round-trip.
_LIST_BENCHMARKS_FOR_JOB_SQL = text(
    "SELECT id, job_id, kind, title, body, source_path, created_by, created_at, "
    "qa_approved_by, qa_approved_at, status "
    "FROM coco.eval_benchmarks "
    "WHERE job_id = :job_id "
    "ORDER BY created_at DESC"
)

# IMPORTANT 5b: lists every evaluation for an application, newest first, so a
# re-scored candidate's history is visible instead of only whichever row's id
# happens to be in hand. Same column-name-matches-the-schema trick as above.
# The UI (not this query) decides which row is "current" -- see
# CaseStudyPage.tsx: the first row here IS the newest by construction, so the
# frontend marks index 0 current and the rest superseded. No `is_current`
# column and no retirement workflow in this pass (Rule 25 full treatment is
# still outstanding -- see the report).
_LIST_EVALUATIONS_FOR_APPLICATION_SQL = text(
    "SELECT id, application_id, job_id, benchmark_id, candidate_name, role, "
    "scores, evidence, flags, total, band, model, sources, rubric_sha256, "
    "corpus_chars, created_by, created_at "
    "FROM coco.case_study_evaluations "
    "WHERE application_id = :application_id "
    "ORDER BY created_at DESC"
)


def _utcnow() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def _benchmark_or_404(db: Session, benchmark_id: str) -> EvalBenchmark:
    benchmark = db.get(EvalBenchmark, benchmark_id)
    if not benchmark:
        raise HTTPException(404, "Benchmark not found")
    return benchmark


def _benchmark_out(benchmark: EvalBenchmark) -> dict:
    return {
        "id": benchmark.id,
        "job_id": benchmark.job_id,
        "kind": benchmark.kind,
        "title": benchmark.title,
        "body": benchmark.body,
        "source_path": benchmark.source_path,
        "created_by": benchmark.created_by,
        "created_at": benchmark.created_at,
        "qa_approved_by": benchmark.qa_approved_by,
        "qa_approved_at": benchmark.qa_approved_at,
        "status": benchmark.status,
    }


def _dimensions_out() -> list[dict]:
    """IMPORTANT 4a: the rubric's dimension metadata (key/label/weight), taken
    straight from `case_study_scoring.DIMENSIONS` -- the single source of
    truth the frontend's now-deleted `CASE_STUDY_DIMENSIONS` used to mirror
    by hand. Every evaluation response carries this, so a weight or dimension
    change in Python is never silently stale on the page again."""
    return [dict(d) for d in DIMENSIONS]


def _evaluation_out(evaluation: CaseStudyEvaluation) -> dict:
    return {
        "id": evaluation.id,
        "application_id": evaluation.application_id,
        "job_id": evaluation.job_id,
        "benchmark_id": evaluation.benchmark_id,
        "candidate_name": evaluation.candidate_name,
        "role": evaluation.role,
        "scores": evaluation.scores,
        "evidence": evaluation.evidence,
        "flags": evaluation.flags,
        "total": evaluation.total,
        "band": evaluation.band,
        "model": evaluation.model_name,
        "sources": evaluation.sources,
        "rubric_sha256": evaluation.rubric_sha256,
        "corpus_chars": evaluation.corpus_chars,
        "created_by": evaluation.created_by,
        "created_at": evaluation.created_at,
        "dimensions": _dimensions_out(),
    }


@router.post("/benchmarks", response_model=CaseStudyBenchmarkOut)
def create_benchmark(
    body: CaseStudyBenchmarkCreateRequest,
    db: Session = Depends(get_db),
    user: dict = Depends(require_editor),
):
    """A new benchmark always starts `draft` -- there is no way for this
    endpoint to create one that is already `approved`; that transition only
    ever happens in `approve_benchmark`, by a different, more senior gate."""
    benchmark = EvalBenchmark(
        job_id=body.job_id,
        kind=body.kind,
        title=body.title,
        body=body.body,
        source_path=body.source_path,
        created_by=user.get("id") or "",
        status="draft",
    )
    db.add(benchmark)
    db.commit()
    db.refresh(benchmark)
    return _benchmark_out(benchmark)


@router.post("/benchmarks/{benchmark_id}/approve", response_model=CaseStudyBenchmarkOut)
def approve_benchmark(
    benchmark_id: str,
    db: Session = Depends(get_db),
    user: dict = Depends(require_approver),
):
    benchmark = _benchmark_or_404(db, benchmark_id)
    if benchmark.status != "draft":
        # Covers BOTH an already-approved benchmark (no silent re-approval,
        # no ambiguity about who actually approved it) and a retired one
        # (this endpoint is not how a retired benchmark comes back to life).
        raise HTTPException(
            409,
            f"Benchmark {benchmark_id} is '{benchmark.status}', not 'draft' -- "
            "only a draft benchmark can be approved.",
        )

    benchmark.status = "approved"
    # id + email, same as ValuesScorecardDraft.approved_by, so the audit trail
    # is readable directly in SQL with no join.
    benchmark.qa_approved_by = f"{user.get('id') or ''} {user.get('email') or ''}".strip()
    benchmark.qa_approved_at = _utcnow()
    db.commit()
    db.refresh(benchmark)
    return _benchmark_out(benchmark)


@router.get("/benchmarks", response_model=list[CaseStudyBenchmarkOut])
def list_benchmarks(
    job_id: int = Query(...),
    db: Session = Depends(get_db),
    user: dict = Depends(require_editor),
):
    """IMPORTANT 5a: every benchmark on record for `job_id`, newest first,
    with its `status` -- so the page can load the job's current benchmark on
    mount rather than depending on an id pasted in by hand."""
    rows = db.execute(_LIST_BENCHMARKS_FOR_JOB_SQL, {"job_id": job_id}).mappings().all()
    return [dict(r) for r in rows]


@router.post("/score", response_model=CaseStudyEvaluationOut)
def score(
    body: CaseStudyScoreRequest,
    db: Session = Depends(get_db),
    user: dict = Depends(require_editor),
):
    app_row = reads.get_application(db, body.application_id)
    if not app_row:
        raise HTTPException(404, "Application not found")

    job_id = app_row.get("job_pk")
    if job_id is None:
        raise HTTPException(422, f"Application {body.application_id} has no job on record")

    # --- RULE 0: refuse unless an APPROVED benchmark exists for this job.
    # A missing benchmark, a draft one, or a retired one all 409 identically
    # -- read straight from the database, not from anything the draft
    # benchmark object above might have cached.
    benchmark_row = db.execute(
        _APPROVED_BENCHMARK_FOR_JOB_SQL, {"job_id": job_id}
    ).mappings().first()
    if benchmark_row is None:
        raise HTTPException(
            409,
            f"No approved benchmark exists for job {job_id}. Rule 0: the benchmark "
            "must be written and QA'd before any submission is scored -- create one "
            "with POST /api/case-studies/benchmarks and approve it with "
            "POST /api/case-studies/benchmarks/{id}/approve first.",
        )

    candidate_name = " ".join(
        p for p in [app_row.get("first_name"), app_row.get("last_name")] if p
    ).strip() or "the candidate"
    role = (app_row.get("job_title") or "the role").strip()

    try:
        corpus = corpus_for(body.application_id, db=db)
    except SubmissionUnreadable as exc:
        raise HTTPException(422, str(exc)) from exc

    try:
        scored = score_submission(
            corpus=corpus["text"],
            benchmark_body=benchmark_row["body"],
            candidate_name=candidate_name,
            role=role,
        )
    except DraftingUnavailable as exc:
        raise HTTPException(503, f"Scoring unavailable: {exc}") from exc
    except CaseStudyScoringError as exc:
        raise HTTPException(422, f"Model returned a malformed scorecard: {exc}") from exc
    except Exception as exc:
        # An unexpected model/SDK failure (timeout, anthropic.APIError, ...) is
        # not a predictable input error -- surface it as 503, like
        # DraftingUnavailable, never as an uncaught 500 with a stack trace.
        # The exception detail is LOGGED, never handed to the caller: it can
        # carry SDK internals that have no business in a user-visible
        # response.
        log.exception(
            "score: unexpected scoring failure for application %s", body.application_id,
        )
        raise HTTPException(
            503,
            "Scoring unavailable due to an unexpected error. Try again, or check "
            "the server logs for detail.",
        ) from exc

    evaluation = CaseStudyEvaluation(
        application_id=body.application_id,
        job_id=job_id,
        benchmark_id=benchmark_row["id"],
        candidate_name=candidate_name,
        role=role,
        scores=scored["scores"],
        evidence=scored["evidence"],
        flags=scored["flags"],
        total=scored["total"],
        band=scored["band"],
        model_name=scored["model"],
        sources=corpus["sources"],
        rubric_sha256=scored["rubric_sha256"],
        corpus_chars=scored["corpus_chars"],
        created_by=user.get("id") or "",
    )
    db.add(evaluation)
    db.commit()
    db.refresh(evaluation)
    return _evaluation_out(evaluation)


@router.get("/evaluations", response_model=list[CaseStudyEvaluationOut])
def list_evaluations(
    application_id: int = Query(...),
    db: Session = Depends(get_db),
    user: dict = Depends(require_editor),
):
    """IMPORTANT 5b: every evaluation on record for `application_id`, newest
    first. A `/score` re-run is not idempotent, so an application can carry
    several `cse-` rows -- this makes that legible (newest = current) rather
    than inventing a retirement workflow in this pass."""
    rows = db.execute(
        _LIST_EVALUATIONS_FOR_APPLICATION_SQL, {"application_id": application_id}
    ).mappings().all()
    dimensions = _dimensions_out()
    return [{**dict(r), "dimensions": dimensions} for r in rows]


@router.get("/evaluations/{evaluation_id}", response_model=CaseStudyEvaluationOut)
def get_evaluation(
    evaluation_id: str,
    db: Session = Depends(get_db),
    # A persisted evaluation carries the candidate's name and quoted evidence
    # from their submission -- gated on require_editor, never a bare signed-in
    # viewer, same bar as reading a values-scorecard draft.
    _user: dict = Depends(require_editor),
):
    evaluation = db.get(CaseStudyEvaluation, evaluation_id)
    if not evaluation:
        raise HTTPException(404, "Evaluation not found")
    return _evaluation_out(evaluation)
