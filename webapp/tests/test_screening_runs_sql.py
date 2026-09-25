"""Every SQL statement the technical-screening engine holds must run.

Run: python -m pytest webapp/tests/test_screening_runs_sql.py -v

WHY THIS IS THE FIRST TEST WRITTEN FOR THIS MODULE. `applications.created_at`
does not exist -- the column is `applied_at` -- and two routers shipped to
production ordering by it. Nineteen router tests passed, because a fake session
records the statement and never sends it to Postgres, so it cannot see a column
that is not there (CLAUDE.md Rule 32). Screening writes into tables holding 863
live evaluations; a column or type error found by a candidate's run is found too
late.

Reads are wrapped in `SELECT * FROM (...) _probe LIMIT 0`. Writes are run under
`EXPLAIN`, which makes Postgres parse, plan and type-check the whole statement
-- every column, every cast, every ON CONFLICT target -- while executing
nothing and touching no row.

Skipped when the database is unreachable, so an offline run proves nothing here.
"""

from __future__ import annotations

import os
import re

import pytest
import requests
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

_DATABASE_URL = os.environ.get("DATABASE_URL")
_TIMEOUT = float(os.environ.get("COCO_SQL_PROBE_TIMEOUT", "180"))

pytestmark = pytest.mark.skipif(
    not _DATABASE_URL, reason="needs DATABASE_URL to validate SQL against the real schema"
)

_UUID = "'00000000-0000-0000-0000-000000000000'::uuid"

# Type-correct and harmless. Reads run with LIMIT 0 and writes only under
# EXPLAIN, so none of these ever has to match or insert anything.
_LIT = {
    # identity / keys
    "run_id": _UUID, "item_id": _UUID, "eval_id": _UUID, "new_id": _UUID,
    "rubric_id": _UUID, "rid": _UUID, "ids": "ARRAY[]::uuid[]",
    "job_id": "-1", "candidate_id": "-1", "application_id": "-1", "cid": "-1",
    # run shape
    "mode": "'new_only'", "status": "'scored'", "state": "'pending'",
    "model": "'claude-haiku-4-5'", "effort": "'medium'", "worker": "'test'",
    "pause_reason": "NULL", "terminal": "false", "concurrency": "4",
    "use_batch": "false", "requested_by": "'test'", "cancel_requested": "false",
    # windows and counts
    "since": "NULL", "until": "NULL", "cutoff": "now()", "max_attempts": "3",
    "limit": "1", "priority": "0", "since_days": "NULL",
    "max_candidates": "NULL", "window_from": "NULL", "window_to": "NULL",
    "planned_count": "0", "total_items": "0",
    "done": "0", "ok": "0", "unusable": "0", "failed": "0", "skipped": "0",
    # money and tokens
    "est_input_tokens": "0", "est_cached_tokens": "0", "est_output_tokens": "0",
    "est_cost_usd": "0", "cost_cap_usd": "NULL", "cost_usd": "0",
    "input_tokens": "0", "cache_read_tokens": "0",
    "cache_creation_tokens": "0", "output_tokens": "0", "latency_ms": "0",
    # rubric
    "version": "1", "title": "'t'", "seniority": "'mid'", "min_years": "0",
    "jd_source": "'neon_description'", "jd_snapshot": "'jd'",
    "custom_questions": "'[]'", "dimensions": "'[]'", "max_score": "100",
    "hard_filters": "'[]'", "thresholds": "'{}'", "manual_review_rules": "'{}'",
    "system_prompt": "'p'", "system_prompt_hash": "'h'", "output_schema": "'{}'",
    "drafted_by_model": "'m'", "source": "'llm_drafted'", "created_by": "'x'",
    "notes": "NULL", "selection": "'{}'",
    # evaluation
    "dedup_key": "'1:2'", "applied_at": "now()", "total_score": "0",
    "score_pct": "0", "dimension_scores": "'{}'", "extracted": "'{}'",
    "strengths": "'[]'", "gaps": "'[]'", "hard_filter_flags": "'[]'",
    "verdict": "'v'", "confidence": "'medium'", "tier": "'P1'",
    "tier_reason": "'r'", "tiered_thresholds": "'{}'",
    "candidate_email": "'a@b.c'", "candidate_name": "'n'",
    "skip_reason": "NULL", "error": "NULL",
    # run events
    "level": "'info'", "event": "'planned'", "detail": "'{}'",
    # resume cache
    "source_hash": "'h'", "text": "'t'", "chars": "0", "truncated": "false",
    "parse_type": "'pdf'", "parse_success": "true", "parse_error": "NULL",
    "health": "0", "issues": "ARRAY[]::text[]",
    "resume_health": "0", "resume_issues": "ARRAY[]::text[]",
    "resume_chars": "0", "resume_type": "'pdf'", "resume_truncated": "false",
    "rubric_version": "1",
    "h": "'h'",
}

# Negative lookbehind so a Postgres `::text` cast is not read as a parameter
# named :text -- the trap that made the sibling test fail on good SQL.
_PARAM = re.compile(r"(?<!:):([a-z_][a-z0-9_]*)", re.I)


def _endpoint() -> str:
    return f"https://{_DATABASE_URL.split('@')[1].split('/')[0]}/sql"


def _substitute(sql: str) -> str:
    def literal(m):
        name = m.group(1)
        if name not in _LIT:
            raise AssertionError(
                f"no test literal for parameter :{name}. Add it to _LIT with "
                "the right type rather than letting the probe guess."
            )
        return _LIT[name]

    return _PARAM.sub(literal, sql)


def _post(query: str) -> None:
    r = requests.post(
        _endpoint(),
        headers={"Neon-Connection-String": _DATABASE_URL,
                 "Content-Type": "application/json"},
        json={"query": query, "params": []},
        timeout=_TIMEOUT,
    )
    if not r.ok:
        raise AssertionError(r.text[:700])


def _probe_read(sql: str) -> None:
    _post(f"SELECT * FROM ({_substitute(sql).strip().rstrip(';')}) _probe LIMIT 0")


def _probe_write(sql: str) -> None:
    """EXPLAIN parses, plans and type-checks without executing or locking."""
    _post(f"EXPLAIN {_substitute(sql).strip().rstrip(';')}")


def _writes():
    """Every registered write template, rendered against the live schema.

    Read off the module rather than pasted, so a statement added later is
    covered without anyone remembering to add it here.
    """
    from webapp.services import nugget_writes, screening_runs

    out = []
    for attr in dir(screening_runs):
        if not attr.isupper() and not (attr.startswith("_") and attr[1:].isupper()):
            continue
        value = getattr(screening_runs, attr)
        if isinstance(value, str) and "{schema}" in value:
            out.append((attr, nugget_writes.render(value, "public")))
    return out


def _reads():
    from webapp.services import screening_runs as sr

    return [
        ("_POOL_SQL", sr._POOL_SQL.format(schema="public")),
        ("_CANDIDATE_SQL", sr._CANDIDATE_SQL),
    ]


WRITES = _writes()
READS = _reads()


def test_the_collectors_found_something():
    """A collector that silently finds nothing makes every test below pass
    while checking no SQL at all."""
    assert len(WRITES) >= 15, [n for n, _ in WRITES]
    assert len(READS) == 2
    names = {n for n, _ in WRITES}
    for expected in ("_INSERT_EVAL", "_CLAIM_ITEMS", "_REAP_STUCK", "_INSERT_RUN"):
        assert expected in names, f"{expected} missing from {sorted(names)}"


@pytest.mark.parametrize("name,sql", WRITES, ids=[n for n, _ in WRITES])
def test_write_statement_type_checks(name, sql):
    try:
        _probe_write(sql)
    except requests.RequestException as exc:
        pytest.skip(f"database unreachable: {exc}")


@pytest.mark.parametrize("name,sql", READS, ids=[n for n, _ in READS])
def test_read_statement_runs(name, sql):
    try:
        _probe_read(sql)
    except requests.RequestException as exc:
        pytest.skip(f"database unreachable: {exc}")


def test_the_probe_catches_a_column_that_does_not_exist():
    """Proof the probe bites rather than only passes. `applications.created_at`
    is the exact column that shipped broken to production."""
    try:
        with pytest.raises(AssertionError, match="created_at"):
            _probe_read(
                "SELECT a.created_at FROM public.applications a WHERE a.job_id = :job_id"
            )
    except requests.RequestException as exc:
        pytest.skip(f"database unreachable: {exc}")


def test_the_write_probe_catches_a_bad_column():
    """EXPLAIN must reject a write naming a column that is not there, or it is
    checking nothing."""
    try:
        with pytest.raises(AssertionError):
            _probe_write(
                "UPDATE public.nugget_screening_runs SET no_such_column = 1 "
                "WHERE id = :run_id"
            )
    except requests.RequestException as exc:
        pytest.skip(f"database unreachable: {exc}")


def test_markaz_tables_are_never_qualified_with_the_nugget_schema():
    """`nugget_worker_test` holds the eight nugget tables and NO jobs,
    applications or candidates. Qualifying a Markaz table with the switchable
    schema works in production and breaks every integration run."""
    from webapp.services import screening_runs as sr

    for name, sql in _reads() + [("get_run", sr.get_run.__doc__ or "")]:
        assert "{schema}.jobs" not in sql
        assert "{schema}.applications" not in sql
        assert "{schema}.candidates" not in sql
    assert sr.MARKAZ_SCHEMA == "public"
