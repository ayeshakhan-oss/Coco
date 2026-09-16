# Candidate Evaluation Phase 1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the live app's `candidate-evaluation` module work read-only, surfacing Nugget's existing screening results (3 rubrics, 863 evaluations) so the tile stops being a placeholder.

**Architecture:** A new `nugget_reads` service issues SELECT-only queries against the `public.nugget_screening_*` tables that Nugget owns, a thin `evaluations` router exposes them, and a React page renders tiers and per-candidate detail. No new tables, no LLM calls, no writes. SQL and shaping are kept in separate functions so the shaping logic is unit-testable without a database.

**Tech Stack:** FastAPI, SQLAlchemy 2.x (`text()` queries, psycopg v3), Pydantic v2, React + TypeScript + Vite, pytest.

**Spec:** [docs/specs/2026-09-16-candidate-evaluation-module-design.md](../specs/2026-09-16-candidate-evaluation-module-design.md)

## Global Constraints

- 🔒 **READ ONLY.** These are Nugget's tables (owner: aymen.abid@taleemabad.com). No INSERT, UPDATE, DELETE, or DDL against `public.nugget_screening_*`, ever.
- 🔒 Always filter **`WHERE is_current`**. A superseded evaluation must never render as live.
- 🔒 `status` values are **`'scored'`** and **`'unusable'`**, never `'ok'`.
- 🔒 **`UNUSABLE` means the CV could not be read. It is NEVER a rejection and never a zero score.** It renders as its own state with a "needs a human" label.
- 🔒 Query the **`public`** schema. The `nugget_deg` schema holds the same 12 table names and is entirely empty.
- 🔒 Every figure shown in the UI is attributed to Nugget's engine and its rubric version.
- No em dashes in user-facing copy (Coco house style).
- Python: `from __future__ import annotations` at the top of every new module.

---

### Task 1: Read-only query guard and the screened-jobs list

**Files:**
- Create: `webapp/services/nugget_reads.py`
- Test: `webapp/tests/test_nugget_reads.py`

**Interfaces:**
- Consumes: `webapp.db.get_db` (existing FastAPI session dependency)
- Produces:
  - `READ_ONLY_PREFIXES: tuple[str, ...]`
  - `assert_read_only(sql: str) -> None` — raises `PermissionError` on anything but SELECT/WITH
  - `list_screened_jobs(db: Session) -> list[dict]` — keys: `job_id:int`, `job_title:str|None`, `rubric_version:int`, `rubric_status:str`, `seniority:str|None`, `scored:int`, `unusable:int`, `last_run_at:datetime|None`

- [ ] **Step 1: Write the failing test**

```python
"""Unit tests for the Nugget screening read layer.

These tables belong to Nugget (Aymen's agent). The guard below is the
mechanical reason Coco cannot write to them, so it is tested against
deliberately bad SQL rather than only against the happy path.

Run:  python -m pytest webapp/tests/test_nugget_reads.py
"""

from __future__ import annotations

import pytest

from webapp.services.nugget_reads import assert_read_only


def test_read_only_guard_blocks_writes():
    bad = [
        "UPDATE public.nugget_screening_evals SET tier='P1'",
        "DELETE FROM public.nugget_screening_runs",
        "INSERT INTO public.nugget_screening_rubrics (job_id) VALUES (1)",
        "DROP TABLE public.nugget_screening_evals",
        "  update  public.nugget_screening_evals SET tier='P1'",
        "\n\tTRUNCATE public.nugget_screening_evals",
    ]
    for sql in bad:
        with pytest.raises(PermissionError):
            assert_read_only(sql)


def test_read_only_guard_allows_reads():
    for sql in ("SELECT 1", "  select 1", "\nWITH x AS (SELECT 1) SELECT * FROM x"):
        assert_read_only(sql) is None
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest webapp/tests/test_nugget_reads.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'webapp.services.nugget_reads'`

- [ ] **Step 3: Write minimal implementation**

```python
"""Read-only access to Nugget's screening results.

Technical roles are screened by Nugget (Aymen Abid's agent), which owns the
`public.nugget_screening_*` tables. Coco reads them and never writes: rubric
changes, re-runs and tier changes go to Aymen.

See .claude/skills/02_candidate-evaluation/technical-screening.md.
"""

from __future__ import annotations

from typing import Any, Optional

from sqlalchemy import text
from sqlalchemy.orm import Session

# The `nugget_deg` schema holds the same table names and is EMPTY. Always public.
SCHEMA = "public"

READ_ONLY_PREFIXES = ("select", "with")


def assert_read_only(sql: str) -> None:
    """Raise unless `sql` is a plain read. These are not Coco's tables."""
    stripped = sql.lstrip().lower()
    if not stripped.startswith(READ_ONLY_PREFIXES):
        raise PermissionError(
            "nugget_reads is READ ONLY: public.nugget_screening_* belongs to Nugget."
        )


def _rows(db: Session, sql: str, **params: Any) -> list[dict]:
    assert_read_only(sql)
    result = db.execute(text(sql), params)
    return [dict(r) for r in result.mappings()]


def list_screened_jobs(db: Session) -> list[dict]:
    """Every job Nugget holds a rubric for, with current eval counts."""
    return _rows(
        db,
        f"""
        SELECT r.job_id,
               j.title AS job_title,
               r.version AS rubric_version,
               r.status  AS rubric_status,
               r.seniority,
               COUNT(*) FILTER (WHERE e.status = 'scored')   AS scored,
               COUNT(*) FILTER (WHERE e.status = 'unusable') AS unusable,
               MAX(e.evaluated_at) AS last_run_at
        FROM {SCHEMA}.nugget_screening_rubrics r
        LEFT JOIN {SCHEMA}.jobs j ON j.id = r.job_id
        LEFT JOIN {SCHEMA}.nugget_screening_evals e
               ON e.job_id = r.job_id AND e.is_current
        GROUP BY r.job_id, j.title, r.version, r.status, r.seniority
        ORDER BY scored DESC
        """,
    )
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest webapp/tests/test_nugget_reads.py -v`
Expected: PASS (2 tests)

- [ ] **Step 5: Commit**

```bash
git add webapp/services/nugget_reads.py webapp/tests/test_nugget_reads.py
git commit -m "feat(eval): read-only Nugget screening service + write guard"
```

---

### Task 2: Tier summary shaping (pure function, then the query)

**Files:**
- Modify: `webapp/services/nugget_reads.py`
- Test: `webapp/tests/test_nugget_reads.py`

**Interfaces:**
- Consumes: `_rows` from Task 1
- Produces:
  - `TIER_ORDER: tuple[str, ...]` = `("P1", "P2", "P3", "P4", "MANUAL_REVIEW", "UNUSABLE")`
  - `shape_summary(rows: list[dict]) -> dict` — pure. Returns keys `tiers:list[dict]`, `scored:int`, `unusable:int`, `total:int`. Each tier dict: `tier:str`, `status:str`, `n:int`, `avg_pct:float|None`, `min_pct:float|None`, `max_pct:float|None`, `is_unusable:bool`
  - `job_summary(db: Session, job_id: int) -> dict` — `shape_summary` applied to the query result

- [ ] **Step 1: Write the failing test**

```python
from webapp.services.nugget_reads import TIER_ORDER, shape_summary


def test_shape_summary_orders_tiers_and_separates_unusable():
    rows = [
        {"tier": "P4", "status": "scored", "n": 378, "avg_pct": 29.1, "min_pct": 0.0, "max_pct": 53.0},
        {"tier": "UNUSABLE", "status": "unusable", "n": 57, "avg_pct": 0.0, "min_pct": 0.0, "max_pct": 0.0},
        {"tier": "P1", "status": "scored", "n": 26, "avg_pct": 93.5, "min_pct": 85.0, "max_pct": 100.0},
    ]
    out = shape_summary(rows)

    # Tiers come back in published order, not query order.
    assert [t["tier"] for t in out["tiers"]] == ["P1", "P4", "UNUSABLE"]
    assert [t["tier"] for t in out["tiers"]] == [t for t in TIER_ORDER if t in {"P1", "P4", "UNUSABLE"}]

    # UNUSABLE is flagged so the UI can never render it as a rejection.
    unusable = [t for t in out["tiers"] if t["is_unusable"]]
    assert len(unusable) == 1 and unusable[0]["tier"] == "UNUSABLE"

    # UNUSABLE is excluded from the scored count but present in the total.
    assert out["scored"] == 404
    assert out["unusable"] == 57
    assert out["total"] == 461


def test_shape_summary_suppresses_meaningless_averages_for_unusable():
    rows = [{"tier": "UNUSABLE", "status": "unusable", "n": 6, "avg_pct": 0.0, "min_pct": 0.0, "max_pct": 0.0}]
    out = shape_summary(rows)
    # A 0.0 average on unreadable CVs is noise, not a score. Never show it.
    assert out["tiers"][0]["avg_pct"] is None
    assert out["tiers"][0]["min_pct"] is None
    assert out["tiers"][0]["max_pct"] is None


def test_shape_summary_handles_empty():
    assert shape_summary([]) == {"tiers": [], "scored": 0, "unusable": 0, "total": 0}
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest webapp/tests/test_nugget_reads.py -v`
Expected: FAIL with `ImportError: cannot import name 'TIER_ORDER'`

- [ ] **Step 3: Write minimal implementation**

Append to `webapp/services/nugget_reads.py`:

```python
# Published tier order. UNUSABLE is last and is NOT a ranking position: it means
# the CV could not be read, so it is never a rejection and never a zero score.
TIER_ORDER = ("P1", "P2", "P3", "P4", "MANUAL_REVIEW", "UNUSABLE")


def shape_summary(rows: list[dict]) -> dict:
    """Order tier buckets and separate unusable from scored. Pure."""
    by_tier = {r["tier"]: r for r in rows}
    tiers: list[dict] = []
    scored = 0
    unusable = 0

    for tier in TIER_ORDER:
        row = by_tier.get(tier)
        if row is None:
            continue
        is_unusable = row.get("status") == "unusable"
        n = int(row.get("n") or 0)
        if is_unusable:
            unusable += n
        else:
            scored += n
        tiers.append(
            {
                "tier": tier,
                "status": row.get("status"),
                "n": n,
                # An average over unreadable documents is noise, not a score.
                "avg_pct": None if is_unusable else row.get("avg_pct"),
                "min_pct": None if is_unusable else row.get("min_pct"),
                "max_pct": None if is_unusable else row.get("max_pct"),
                "is_unusable": is_unusable,
            }
        )

    return {"tiers": tiers, "scored": scored, "unusable": unusable, "total": scored + unusable}


def job_summary(db: Session, job_id: int) -> dict:
    rows = _rows(
        db,
        f"""
        SELECT tier, status, COUNT(*) AS n,
               ROUND(AVG(score_pct), 1) AS avg_pct,
               MIN(score_pct) AS min_pct,
               MAX(score_pct) AS max_pct
        FROM {SCHEMA}.nugget_screening_evals
        WHERE job_id = :job_id AND is_current
        GROUP BY tier, status
        """,
        job_id=job_id,
    )
    return shape_summary(rows)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest webapp/tests/test_nugget_reads.py -v`
Expected: PASS (5 tests)

- [ ] **Step 5: Commit**

```bash
git add webapp/services/nugget_reads.py webapp/tests/test_nugget_reads.py
git commit -m "feat(eval): tier summary shaping, unusable kept out of scores"
```

---

### Task 3: Candidate list and per-application detail

**Files:**
- Modify: `webapp/services/nugget_reads.py`
- Test: `webapp/tests/test_nugget_reads.py`

**Interfaces:**
- Consumes: `_rows`, `TIER_ORDER`
- Produces:
  - `candidates_for_job(db, job_id: int, tier: Optional[str] = None, limit: int = 100, offset: int = 0) -> list[dict]` — keys: `application_id`, `candidate_id`, `candidate_name`, `candidate_email`, `score_pct`, `tier`, `tier_reason`, `confidence`, `resume_health`, `is_unusable`
  - `evaluation_for_application(db, application_id: int) -> Optional[dict]` — the above plus `dimension_scores`, `strengths`, `gaps`, `hard_filter_flags`, `verdict`, `rubric_version`, `model`, `evaluated_at`
  - `is_valid_tier(tier: str) -> bool`

- [ ] **Step 1: Write the failing test**

```python
from webapp.services.nugget_reads import is_valid_tier


def test_is_valid_tier_accepts_published_tiers_only():
    for t in ("P1", "P2", "P3", "P4", "MANUAL_REVIEW", "UNUSABLE"):
        assert is_valid_tier(t) is True
    for t in ("p1", "OK", "", "P5", "DROP TABLE", None):
        assert is_valid_tier(t) is False
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest webapp/tests/test_nugget_reads.py::test_is_valid_tier_accepts_published_tiers_only -v`
Expected: FAIL with `ImportError: cannot import name 'is_valid_tier'`

- [ ] **Step 3: Write minimal implementation**

Append to `webapp/services/nugget_reads.py`:

```python
def is_valid_tier(tier: Any) -> bool:
    """Exact match against the published tiers. Case-sensitive on purpose: the
    value is interpolated nowhere, but an unknown tier should 400, not return []."""
    return isinstance(tier, str) and tier in TIER_ORDER


def candidates_for_job(
    db: Session,
    job_id: int,
    tier: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
) -> list[dict]:
    rows = _rows(
        db,
        f"""
        SELECT application_id, candidate_id, candidate_name, candidate_email,
               score_pct, tier, tier_reason, confidence, resume_health, status
        FROM {SCHEMA}.nugget_screening_evals
        WHERE job_id = :job_id AND is_current
          AND (:tier IS NULL OR tier = :tier)
        ORDER BY (status = 'unusable'), score_pct DESC NULLS LAST
        LIMIT :limit OFFSET :offset
        """,
        job_id=job_id,
        tier=tier,
        limit=limit,
        offset=offset,
    )
    for r in rows:
        r["is_unusable"] = r.pop("status") == "unusable"
        if r["is_unusable"]:
            r["score_pct"] = None  # never show 0.00 for a document nobody could read
    return rows


def evaluation_for_application(db: Session, application_id: int) -> Optional[dict]:
    rows = _rows(
        db,
        f"""
        SELECT e.application_id, e.candidate_id, e.candidate_name, e.candidate_email,
               e.score_pct, e.tier, e.tier_reason, e.confidence, e.resume_health,
               e.status, e.dimension_scores, e.strengths, e.gaps,
               e.hard_filter_flags, e.verdict, e.rubric_version, e.model, e.evaluated_at
        FROM {SCHEMA}.nugget_screening_evals e
        WHERE e.application_id = :application_id AND e.is_current
        LIMIT 1
        """,
        application_id=application_id,
    )
    if not rows:
        return None
    row = rows[0]
    row["is_unusable"] = row.pop("status") == "unusable"
    if row["is_unusable"]:
        row["score_pct"] = None
    return row
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest webapp/tests/test_nugget_reads.py -v`
Expected: PASS (6 tests)

- [ ] **Step 5: Commit**

```bash
git add webapp/services/nugget_reads.py webapp/tests/test_nugget_reads.py
git commit -m "feat(eval): candidate list + detail reads, unusable never scored"
```

---

### Task 4: Schemas, router, and mounting

**Files:**
- Modify: `webapp/schemas.py` (append)
- Create: `webapp/routers/evaluations.py`
- Modify: `webapp/main.py:173-178` (the `include_router` block)
- Test: `webapp/tests/test_nugget_reads.py`

**Interfaces:**
- Consumes: everything from Tasks 1 to 3
- Produces: `GET /api/evaluations/jobs`, `/api/evaluations/jobs/{job_id}/summary`, `/api/evaluations/jobs/{job_id}/candidates`, `/api/evaluations/applications/{application_id}`

- [ ] **Step 1: Write the failing test**

```python
def test_evaluations_router_is_mounted_and_read_only():
    from webapp.main import app

    paths = {r.path for r in app.routes}
    assert "/api/evaluations/jobs" in paths
    assert "/api/evaluations/jobs/{job_id}/summary" in paths
    assert "/api/evaluations/jobs/{job_id}/candidates" in paths
    assert "/api/evaluations/applications/{application_id}" in paths

    # Read-only surface: no POST/PUT/PATCH/DELETE anywhere under /api/evaluations.
    for r in app.routes:
        if getattr(r, "path", "").startswith("/api/evaluations"):
            assert set(getattr(r, "methods", set())) <= {"GET", "HEAD", "OPTIONS"}
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest webapp/tests/test_nugget_reads.py::test_evaluations_router_is_mounted_and_read_only -v`
Expected: FAIL on the first assert, `/api/evaluations/jobs` not in paths

- [ ] **Step 3: Write minimal implementation**

Append to `webapp/schemas.py`:

Note the existing file conventions: it imports `datetime as dt` and every schema
extends `_Base` (which sets `extra="ignore"` and `from_attributes=True`). Match both.

```python
class ScreenedJob(_Base):
    job_id: int
    job_title: Optional[str] = None
    rubric_version: int
    rubric_status: str
    seniority: Optional[str] = None
    scored: int
    unusable: int
    last_run_at: Optional[dt.datetime] = None


class TierBucket(_Base):
    tier: str
    status: Optional[str] = None
    n: int
    avg_pct: Optional[float] = None
    min_pct: Optional[float] = None
    max_pct: Optional[float] = None
    is_unusable: bool


class EvaluationSummary(_Base):
    tiers: list[TierBucket]
    scored: int
    unusable: int
    total: int


class EvaluationRow(_Base):
    application_id: Optional[int] = None
    candidate_id: Optional[int] = None
    candidate_name: Optional[str] = None
    candidate_email: Optional[str] = None
    score_pct: Optional[float] = None
    tier: Optional[str] = None
    tier_reason: Optional[str] = None
    confidence: Optional[str] = None
    resume_health: Optional[int] = None
    is_unusable: bool = False


class EvaluationDetail(EvaluationRow):
    dimension_scores: Optional[dict[str, Any]] = None
    strengths: Optional[list[Any]] = None
    gaps: Optional[list[Any]] = None
    hard_filter_flags: Optional[list[Any]] = None
    verdict: Optional[str] = None
    rubric_version: Optional[int] = None
    model: Optional[str] = None
    evaluated_at: Optional[dt.datetime] = None
```

`dt`, `Any` and `Optional` are already imported at the top of `schemas.py`. Add nothing.

Create `webapp/routers/evaluations.py`:

```python
"""Read-only endpoints over Nugget's screening results.

🔒 These tables belong to Nugget (Aymen Abid's agent). This router exposes GET
only; there is deliberately no write path. See
.claude/skills/02_candidate-evaluation/technical-screening.md.
"""

from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..db import get_db
from ..deps import get_current_user
from ..schemas import EvaluationDetail, EvaluationRow, EvaluationSummary, ScreenedJob
from ..services import nugget_reads

router = APIRouter(prefix="/api/evaluations", tags=["evaluations"])


@router.get("/jobs", response_model=list[ScreenedJob])
def screened_jobs(
    db: Session = Depends(get_db),
    _user: dict = Depends(get_current_user),
):
    return nugget_reads.list_screened_jobs(db)


@router.get("/jobs/{job_id}/summary", response_model=EvaluationSummary)
def job_summary(
    job_id: int,
    db: Session = Depends(get_db),
    _user: dict = Depends(get_current_user),
):
    return nugget_reads.job_summary(db, job_id)


@router.get("/jobs/{job_id}/candidates", response_model=list[EvaluationRow])
def job_candidates(
    job_id: int,
    tier: Optional[str] = Query(None),
    limit: int = Query(100, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    _user: dict = Depends(get_current_user),
):
    if tier is not None and not nugget_reads.is_valid_tier(tier):
        raise HTTPException(400, f"Invalid tier. One of: {list(nugget_reads.TIER_ORDER)}")
    return nugget_reads.candidates_for_job(db, job_id, tier=tier, limit=limit, offset=offset)


@router.get("/applications/{application_id}", response_model=EvaluationDetail)
def application_evaluation(
    application_id: int,
    db: Session = Depends(get_db),
    _user: dict = Depends(get_current_user),
):
    row = nugget_reads.evaluation_for_application(db, application_id)
    if not row:
        raise HTTPException(404, "No current screening evaluation for this application")
    return row
```

In `webapp/main.py`, add the import alongside the other routers and mount it after `candidates_router`:

```python
from .routers import evaluations as evaluations_router
...
app.include_router(evaluations_router.router)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest webapp/tests/test_nugget_reads.py -v`
Expected: PASS (7 tests)

- [ ] **Step 5: Commit**

```bash
git add webapp/schemas.py webapp/routers/evaluations.py webapp/main.py webapp/tests/test_nugget_reads.py
git commit -m "feat(eval): GET-only evaluations router"
```

---

### Task 5: Ship Skill 02 into the image

**Files:**
- Modify: `.dockerignore:24-27`
- Modify: `Dockerfile:47`
- Test: `webapp/tests/test_skill_files_shipped.py` (create)

**Interfaces:**
- Consumes: nothing
- Produces: `.claude/skills/02_candidate-evaluation/` present in the built image

**Why a test:** the dangerous ordering is a `.dockerignore` negation added without the matching `COPY`. That builds fine and the folder is simply absent at runtime, where readers swallow `OSError` and degrade silently. A static check catches it before deploy.

- [ ] **Step 1: Write the failing test**

```python
"""Guard: every skill folder the app expects is actually COPYed into the image.

The failure this prevents is silent. A .dockerignore negation without a matching
COPY builds clean, the folder is absent at runtime, and the readers in
tone_rules.py swallow the OSError and return "". The only symptom is worse output.
"""

from __future__ import annotations

import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

EXPECTED_SKILL_DIRS = [
    ".claude/skills/01_candidate-communication",
    ".claude/skills/02_candidate-evaluation",
]


def _read(rel: str) -> str:
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return fh.read()


def test_expected_skill_dirs_exist_on_disk():
    for d in EXPECTED_SKILL_DIRS:
        assert os.path.isdir(os.path.join(ROOT, d)), f"missing on disk: {d}"


def test_expected_skill_dirs_are_copied_into_the_image():
    dockerfile = _read("Dockerfile")
    for d in EXPECTED_SKILL_DIRS:
        assert f"COPY {d}/ {d}/" in dockerfile, f"no COPY line for {d}"


def test_expected_skill_dirs_are_reincluded_in_dockerignore():
    ignore = _read(".dockerignore")
    lines = [ln.strip() for ln in ignore.splitlines()]
    assert ".claude/skills/*" in lines, "the exclude line disappeared"
    star_at = lines.index(".claude/skills/*")
    for d in EXPECTED_SKILL_DIRS:
        negation = f"!{d}"
        assert negation in lines, f"no re-inclusion for {d}"
        # A negation BEFORE the exclude does nothing. Order is load-bearing.
        assert lines.index(negation) > star_at, f"{negation} must come after .claude/skills/*"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest webapp/tests/test_skill_files_shipped.py -v`
Expected: FAIL on `test_expected_skill_dirs_are_copied_into_the_image`, no COPY line for `.claude/skills/02_candidate-evaluation`

- [ ] **Step 3: Write minimal implementation**

In `.dockerignore`, immediately after the existing `!.claude/skills/01_candidate-communication` line, add:

```
!.claude/skills/02_candidate-evaluation
```

In `Dockerfile`, immediately after line 47, add:

```dockerfile
COPY .claude/skills/02_candidate-evaluation/ .claude/skills/02_candidate-evaluation/
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest webapp/tests/test_skill_files_shipped.py -v`
Expected: PASS (3 tests)

- [ ] **Step 5: Commit**

```bash
git add Dockerfile .dockerignore webapp/tests/test_skill_files_shipped.py
git commit -m "build: ship skill 02 into the image, with a guard against silent absence"
```

---

### Task 6: Frontend types and API client

**Files:**
- Modify: `frontend/src/lib/types.ts` (append)
- Modify: `frontend/src/lib/api.ts` (append to the exported api object)

**Interfaces:**
- Consumes: the four endpoints from Task 4
- Produces: `ScreenedJob`, `TierBucket`, `EvaluationSummary`, `EvaluationRow`, `EvaluationDetail` types; `api.evaluationJobs` / `evaluationSummary` / `evaluationCandidates` / `evaluationDetail`

- [ ] **Step 1: Add the types**

Append to `frontend/src/lib/types.ts`:

```ts
export interface ScreenedJob {
  job_id: number
  job_title: string | null
  rubric_version: number
  rubric_status: string
  seniority: string | null
  scored: number
  unusable: number
  last_run_at: string | null
}

export interface TierBucket {
  tier: string
  status: string | null
  n: number
  avg_pct: number | null
  min_pct: number | null
  max_pct: number | null
  is_unusable: boolean
}

export interface EvaluationSummary {
  tiers: TierBucket[]
  scored: number
  unusable: number
  total: number
}

export interface EvaluationRow {
  application_id: number | null
  candidate_id: number | null
  candidate_name: string | null
  candidate_email: string | null
  score_pct: number | null
  tier: string | null
  tier_reason: string | null
  confidence: string | null
  resume_health: number | null
  is_unusable: boolean
}

export interface EvaluationDetail extends EvaluationRow {
  dimension_scores: Record<string, unknown> | null
  strengths: string[] | null
  gaps: string[] | null
  hard_filter_flags: Array<Record<string, unknown>> | null
  verdict: string | null
  rubric_version: number | null
  model: string | null
  evaluated_at: string | null
}
```

- [ ] **Step 2: Add the API methods**

Add the imports to the existing `import type { ... } from './types'` block in `api.ts`: `EvaluationDetail`, `EvaluationRow`, `EvaluationSummary`, `ScreenedJob`.

Then add to the exported `api` object (declared at `api.ts:70`). The object is **flat**
(`api.candidates`, `api.scorecard`, `api.timeline`), so use flat names rather than a nested
`evaluations` sub-object. The typed GET helper is `get<T>(path)`, defined at `api.ts:59`.

```ts
  evaluationJobs: () => get<ScreenedJob[]>('/api/evaluations/jobs'),
  evaluationSummary: (jobId: number) =>
    get<EvaluationSummary>(`/api/evaluations/jobs/${jobId}/summary`),
  evaluationCandidates: (jobId: number, tier?: string) =>
    get<EvaluationRow[]>(
      `/api/evaluations/jobs/${jobId}/candidates` +
        (tier ? `?tier=${encodeURIComponent(tier)}` : ''),
    ),
  evaluationDetail: (applicationId: number) =>
    get<EvaluationDetail>(`/api/evaluations/applications/${applicationId}`),
```

- [ ] **Step 3: Verify it compiles**

Run: `cd frontend && npx tsc -b`
Expected: no errors

- [ ] **Step 4: Commit**

```bash
git add frontend/src/lib/types.ts frontend/src/lib/api.ts
git commit -m "feat(eval): frontend types + evaluations api client"
```

---

### Task 7: Evaluation page, route, and flip the module live

**Files:**
- Create: `frontend/src/pages/EvaluationPage.tsx`
- Modify: `frontend/src/App.tsx` (add the route above the `/modules/:slug` catch-all)
- Modify: `frontend/src/lib/modules.ts:16`

**Interfaces:**
- Consumes: `api.evaluationJobs`, `api.evaluationSummary`, `api.evaluationCandidates`, `api.evaluationDetail` from Task 6
- Produces: the `/evaluations` route; `candidate-evaluation` module `status: 'live'`

- [ ] **Step 1: Create the page**

```tsx
import { Fragment, useEffect, useState } from 'react'
import { api } from '../lib/api'
import type { EvaluationDetail, EvaluationRow, EvaluationSummary, ScreenedJob } from '../lib/types'

export function EvaluationPage() {
  const [jobs, setJobs] = useState<ScreenedJob[]>([])
  const [jobId, setJobId] = useState<number | null>(null)
  const [summary, setSummary] = useState<EvaluationSummary | null>(null)
  const [rows, setRows] = useState<EvaluationRow[]>([])
  const [tier, setTier] = useState<string | undefined>(undefined)
  const [openId, setOpenId] = useState<number | null>(null)
  const [detail, setDetail] = useState<EvaluationDetail | null>(null)

  const openRow = (applicationId: number | null) => {
    if (applicationId === null) return
    if (openId === applicationId) {
      setOpenId(null)
      setDetail(null)
      return
    }
    setOpenId(applicationId)
    setDetail(null)
    api.evaluationDetail(applicationId).then(setDetail)
  }

  useEffect(() => {
    api.evaluationJobs().then((j) => {
      setJobs(j)
      if (j.length && jobId === null) setJobId(j[0].job_id)
    })
  }, [])

  useEffect(() => {
    if (jobId === null) return
    api.evaluationSummary(jobId).then(setSummary)
    api.evaluationCandidates(jobId, tier).then(setRows)
  }, [jobId, tier])

  return (
    <div style={{ padding: 24 }}>
      <h1>Candidate Evaluation</h1>
      <p style={{ color: '#555' }}>
        Technical screening results produced by Nugget's screening engine. Read only.
      </p>

      <select
        value={jobId ?? ''}
        onChange={(e) => {
          setJobId(Number(e.target.value))
          setTier(undefined)
        }}
      >
        {jobs.map((j) => (
          <option key={j.job_id} value={j.job_id}>
            {j.job_title ?? `Job ${j.job_id}`} (rubric v{j.rubric_version})
          </option>
        ))}
      </select>

      {summary && (
        <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap', margin: '16px 0' }}>
          {summary.tiers.map((t) => (
            <button
              key={t.tier}
              onClick={() => setTier(tier === t.tier ? undefined : t.tier)}
              style={{
                padding: 12,
                minWidth: 140,
                textAlign: 'left',
                border: tier === t.tier ? '2px solid #2f4fa2' : '1px solid #ddd',
                background: t.is_unusable ? '#fff7ed' : '#fff',
                cursor: 'pointer',
              }}
            >
              <div style={{ fontWeight: 700 }}>{t.tier}</div>
              <div>{t.n}</div>
              {t.is_unusable ? (
                <div style={{ fontSize: 12, color: '#9a3412' }}>CV could not be read, needs a human</div>
              ) : (
                t.avg_pct !== null && <div style={{ fontSize: 12, color: '#555' }}>avg {t.avg_pct}%</div>
              )}
            </button>
          ))}
        </div>
      )}

      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr>
            <th style={{ textAlign: 'left' }}>Candidate</th>
            <th style={{ textAlign: 'left' }}>Tier</th>
            <th style={{ textAlign: 'left' }}>Score</th>
            <th style={{ textAlign: 'left' }}>Why</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((r) => (
            <Fragment key={r.application_id ?? r.candidate_email}>
              <tr
                onClick={() => openRow(r.application_id)}
                style={{ borderTop: '1px solid #eee', cursor: 'pointer' }}
              >
                <td>{r.candidate_name}</td>
                <td>{r.tier}</td>
                <td>{r.is_unusable ? 'Not scored' : `${r.score_pct}%`}</td>
                <td style={{ fontSize: 13, color: '#555' }}>{r.tier_reason}</td>
              </tr>
              {openId === r.application_id && (
                <tr>
                  <td colSpan={4} style={{ background: '#fafafa', padding: 16 }}>
                    {!detail ? (
                      <div>Loading...</div>
                    ) : (
                      <div>
                        <p style={{ marginTop: 0 }}>{detail.verdict}</p>
                        {detail.strengths && detail.strengths.length > 0 && (
                          <>
                            <strong>Strengths</strong>
                            <ul>
                              {detail.strengths.map((s, i) => (
                                <li key={i}>{String(s)}</li>
                              ))}
                            </ul>
                          </>
                        )}
                        {detail.gaps && detail.gaps.length > 0 && (
                          <>
                            <strong>Gaps</strong>
                            <ul>
                              {detail.gaps.map((g, i) => (
                                <li key={i}>{String(g)}</li>
                              ))}
                            </ul>
                          </>
                        )}
                        <p style={{ fontSize: 12, color: '#777' }}>
                          Screened by Nugget's engine, rubric v{detail.rubric_version}, model{' '}
                          {detail.model}.
                        </p>
                      </div>
                    )}
                  </td>
                </tr>
              )}
            </Fragment>
          ))}
        </tbody>
      </table>
    </div>
  )
}
```

- [ ] **Step 2: Wire the route**

In `frontend/src/App.tsx`, import the page and add the route **above** the `/modules/:slug` line so the live module is not captured by the Coming Soon catch-all:

```tsx
<Route path="/evaluations" element={<EvaluationPage />} />
```

- [ ] **Step 3: Flip the module live, and fix the single-live-module assumption**

⚠️ `modules.ts` assumes exactly one live module and `HomePage.tsx:86` hardcodes its
destination: `const isLive = skill.slug === ACTIVE_MODULE` then `to={isLive ? '/queue' : ...}`.
Flipping the status alone would send the Evaluation tile to the communication queue. Give each
module its own route.

In `frontend/src/lib/modules.ts`, add `route` to the interface, set it on both live modules, and
flip the status:

```ts
export interface ModuleDef {
  slug: string
  label: string
  icon: LucideIcon
  status: 'live' | 'soon'
  blurb: string
  route?: string
}
```

```ts
  { slug: 'candidate-communication', label: 'Candidate Communication', icon: Mail, status: 'live', route: '/queue', blurb: 'Draft, review, approve and send candidate rejection and feedback emails.' },
  { slug: 'candidate-evaluation', label: 'Candidate Evaluation', icon: FileSearch, status: 'live', route: '/evaluations', blurb: 'Screen CVs, score case studies and interview scorecards.' },
```

Keep `ACTIVE_MODULE` and `activeModule()` exactly as they are: other code imports them, and
removing them is out of scope for this task.

In `frontend/src/pages/HomePage.tsx`, change line 86 and line 90 to key off status and route:

```tsx
            const isLive = skill.status === 'live'
```

```tsx
                to={isLive && skill.route ? skill.route : `/modules/${skill.slug}`}
```

Update the import on line 8 if `ACTIVE_MODULE` becomes unused there: `import { MODULES } from '../lib/modules'`. TypeScript will flag it if it is still needed.

- [ ] **Step 4: Verify it builds and runs**

Run: `cd frontend && npm run build`
Expected: compiles clean.

Then run the API and click through:

```bash
python -m uvicorn webapp.main:app --reload --port 8000
```

Expected at `/evaluations`: the job picker lists AI Engineer Lead, Full Stack Developer and Lead Analytics Engineer. Selecting AI Engineer Lead shows P1 26, P2 77, P3 130, P4 378, MANUAL_REVIEW 1, UNUSABLE 57. The UNUSABLE tile reads "CV could not be read, needs a human" and shows no average. Clicking it lists candidates whose Score column reads "Not scored", never 0%.

- [ ] **Step 5: Commit**

```bash
git add frontend/src/pages/EvaluationPage.tsx frontend/src/App.tsx frontend/src/lib/modules.ts frontend/src/pages/HomePage.tsx
git commit -m "feat(eval): evaluation page, route, module live"
```

---

## Final verification before deploy

- [ ] `python -m pytest webapp/tests/ -q` passes
- [ ] `cd frontend && npm run build` compiles clean
- [ ] **Prove the read-only guard fires:** `python -m pytest webapp/tests/test_nugget_reads.py::test_read_only_guard_blocks_writes -v`
- [ ] **Prove nothing was written to Nugget's tables.** Before and after, the counts must be identical:

```sql
SELECT (SELECT COUNT(*) FROM public.nugget_screening_evals)   AS evals,
       (SELECT COUNT(*) FROM public.nugget_screening_rubrics) AS rubrics,
       (SELECT COUNT(*) FROM public.nugget_screening_runs)    AS runs;
```

Expected, unchanged: evals 863, rubrics 3, runs 6.

- [ ] Commit everything, then `bash scripts/deploy_webapp.sh`
- [ ] Poll `/healthz` until `"commit"` matches the deployed SHA. A `+dirty` suffix means what shipped is **not** that commit; `"unknown"` means the variable never landed.
- [ ] Confirm the bundle carries the new route:

```bash
curl -s https://coco-production-bcc8.up.railway.app/ | grep -o 'assets/index-[^"]*\.js'
curl -s https://coco-production-bcc8.up.railway.app/assets/index-XXXX.js | grep -c 'evaluations'
```
