"""Every SQL statement the evaluation and operations routers hold must run.

THE BUG THIS EXISTS FOR. `cv_screening._APPLICATIONS_FOR_JOB_SQL` and
`case_study_tracking._APPLICATIONS_SQL` both ordered by `a.created_at`.
`public.applications` has `applied_at`, not `created_at`, so both pages
returned a 500 on every request and the CV Screening page showed "Could not
load CV screening" in production. Ayesha found it, not the suite.

Nineteen router tests passed anyway, because they hand the route a fake session
whose `execute()` records the statement and returns canned rows. **A fake
session never sends the SQL to Postgres, so it cannot see a column that does
not exist.** That is the same class of defect as the earlier
`(:tier::text IS NULL ...)` bug, where SQLAlchemy bound no parameter at all and
two diff reviews passed it: SQL is only really checked by a database.

HOW THIS WORKS. Each statement is wrapped in `SELECT * FROM (...) _probe LIMIT
0` and executed. Postgres parses, plans and validates every column reference
without returning a row, so the check is cheap but complete. Named parameters
are substituted with harmless literals (-1, a string that matches nothing),
because the point is to validate the SQL's SHAPE, not to fetch data.

Skipped when the database is unreachable, like test_evaluations_api.py. That
means it does not protect an offline run -- run the suite with the database
reachable before shipping a router that touches SQL.

Run: python -m pytest webapp/tests/test_router_sql_executes.py -v
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


def _endpoint() -> str:
    # Neon's HTTPS SQL endpoint. Port 5432 from this machine is intermittent
    # (memory/lesson_tests_must_not_touch_production_2026_09_22.md), so a
    # direct psycopg connection makes this test flaky for no benefit.
    return f"https://{_DATABASE_URL.split('@')[1].split('/')[0]}/sql"


pytestmark = pytest.mark.skipif(
    not _DATABASE_URL, reason="needs DATABASE_URL to validate SQL against the real schema"
)

# Harmless literals. Every statement is run with LIMIT 0, so these only have to
# be type-correct, never to match anything.
_PARAM_LITERALS = {
    "job_id": "-1",
    "application_id": "-1",
    "benchmark_id": "'none'",
    "a": "-1",
    "i": "'none'",
    "new_id": "'none'",
    "name": "'none'",
    "tier": "'none'",
    "v": "'none'",
    "after": "-1",
    "limit": "1",
}

# A NEGATIVE LOOKBEHIND, because `lr.start_date::text` is a Postgres cast and
# not a parameter called :text. Without it this test reports a missing
# literal for every cast in every statement -- which is how it first
# failed on operations._LEAVE_SQL.
_PARAM = re.compile(r"(?<!:):([a-z_][a-z0-9_]*)", re.I)


def _statements():
    """Every module-level SQL constant on the evaluation routers, read from the
    modules themselves rather than copied -- a copy drifts and then guards a
    statement nobody runs."""
    from webapp.routers import candidates, case_studies, case_study_tracking
    from webapp.routers import cv_screening
    from webapp.routers import evaluations, kcd_evaluations, operations
    from webapp.routers import values_scorecards

    out = []
    for module in (
        cv_screening, case_study_tracking, kcd_evaluations,
        case_studies, evaluations, values_scorecards, operations, candidates,
    ):
        for attr in dir(module):
            if not attr.startswith("_") or not attr.isupper() and not attr[1:].isupper():
                continue
            value = getattr(module, attr)
            sql = getattr(value, "text", None)
            if isinstance(sql, str) and "select" in sql.lower():
                out.append((f"{module.__name__.rsplit('.', 1)[-1]}.{attr}", sql))
    return out


STATEMENTS = _statements()


def _run(sql: str) -> None:
    def literal(m):
        name = m.group(1)
        if name not in _PARAM_LITERALS:
            # Guessing a string for an unknown parameter turns an INTEGER
            # column into `a.id > 'none'` and reports a confusing type error
            # instead of the real problem, which is that this map is missing a
            # name. Say so.
            raise AssertionError(
                f"no test literal for parameter :{name}. Add it to "
                "_PARAM_LITERALS with the right type."
            )
        return _PARAM_LITERALS[name]

    probe = _PARAM.sub(literal, sql)
    r = requests.post(
        _endpoint(),
        headers={"Neon-Connection-String": _DATABASE_URL, "Content-Type": "application/json"},
        json={"query": f"SELECT * FROM ({probe.strip().rstrip(';')}) _probe LIMIT 0",
              "params": []},
        timeout=_TIMEOUT,
    )
    if not r.ok:
        raise AssertionError(r.text[:600])


def test_there_are_statements_to_check():
    """A collector that silently finds nothing would make every test below
    pass while checking no SQL at all."""
    assert len(STATEMENTS) >= 8, [n for n, _ in STATEMENTS]
    names = {n for n, _ in STATEMENTS}
    assert any("cv_screening" in n for n in names)
    assert any("case_study_tracking" in n for n in names)
    assert any("kcd_evaluations" in n for n in names)
    assert any("operations" in n for n in names)


@pytest.mark.parametrize("name,sql", STATEMENTS, ids=[n for n, _ in STATEMENTS])
def test_statement_runs_against_the_real_schema(name, sql):
    try:
        _run(sql)
    except requests.RequestException as exc:
        pytest.skip(f"database unreachable: {exc}")


def test_the_probe_catches_a_column_that_does_not_exist():
    """Proof this bites rather than only passes: the exact statement that was
    live in production must fail."""
    broken = (
        "SELECT a.id, a.created_at AS applied_at FROM applications a "
        "WHERE a.job_id = :job_id ORDER BY a.created_at DESC"
    )
    try:
        with pytest.raises(AssertionError, match="created_at"):
            _run(broken)
    except requests.RequestException as exc:
        pytest.skip(f"database unreachable: {exc}")


def test_applications_has_applied_at_and_not_created_at():
    """The specific fact both routers got wrong, asserted once and plainly."""
    try:
        _run("SELECT a.applied_at FROM applications a")
    except requests.RequestException as exc:
        pytest.skip(f"database unreachable: {exc}")


def test_a_postgres_cast_is_not_mistaken_for_a_parameter():
    """`lr.start_date::text` is a cast. Reading it as a parameter named :text
    made this test fail on a statement that was perfectly fine."""
    found = _PARAM.findall("SELECT lr.start_date::text FROM x WHERE id = :job_id")
    assert found == ["job_id"]
