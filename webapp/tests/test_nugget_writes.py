"""The write guard on Nugget's tables.

Run: python -m pytest webapp/tests/test_nugget_writes.py -v

Coco was read-only against `public.nugget_screening_*` until 2026-09-25. The
rule was lifted so Coco can launch runs, and `nugget_writes` is the whole of
what replaced it. If this module's refusals stop working, the protection is
gone and nothing else in the app would notice.

Every test here feeds the guard something it MUST refuse. A guard exercised
only with valid input proves nothing (CLAUDE.md Rule 25).
"""

from __future__ import annotations

import pytest

from webapp.services import nugget_writes as nw


class _FakeSession:
    """Records what would have been executed. Never touches a database."""

    def __init__(self):
        self.executed = []

    def execute(self, stmt, params=None):
        self.executed.append((str(stmt), params))
        return None


# --------------------------------------------------------------------------
# The allowlist
# --------------------------------------------------------------------------


def test_an_unregistered_statement_is_refused():
    """The core guarantee: a caller cannot hand in SQL of its own."""
    db = _FakeSession()
    with pytest.raises(nw.NuggetWriteRefused) as exc:
        nw.execute(db, "UPDATE public.nugget_screening_evals SET tier = 'P1'")
    assert "allowlist" in str(exc.value)
    assert db.executed == [], "a refused statement must never reach the session"


def test_a_registered_statement_executes():
    sql = nw.register(
        "UPDATE public.nugget_screening_runs SET status = :status WHERE id = :id"
    )
    db = _FakeSession()
    nw.execute(db, sql, status="running", id="abc")
    assert len(db.executed) == 1


def test_whitespace_differences_do_not_break_the_match():
    """Constants are f-strings rendered across several lines; a registered
    statement must still match after reformatting."""
    sql = nw.register(
        "INSERT INTO public.nugget_screening_run_events (run_id, event) "
        "VALUES (:run_id, :event)"
    )
    reflowed = """
        INSERT INTO public.nugget_screening_run_events (run_id, event)
        VALUES (:run_id, :event)
    """
    assert nw._normalise(sql) == nw._normalise(reflowed)
    nw.execute(_FakeSession(), reflowed, run_id="r", event="planned")


def test_the_registry_is_not_empty():
    """A refactor that stopped registering anything would make every refusal
    test above pass while the feature silently stopped working."""
    import webapp.services.screening_runs  # noqa: F401  (registers its constants)

    assert nw.registered_count() > 0


# --------------------------------------------------------------------------
# The static shape checks — these apply even to registered statements
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "sql",
    [
        "DELETE FROM public.nugget_screening_evals WHERE id = :id",
        "DROP TABLE public.nugget_screening_evals",
        "TRUNCATE public.nugget_screening_evals",
        "ALTER TABLE public.nugget_screening_evals ADD COLUMN x int",
        "CREATE TABLE public.nugget_x (id int)",
        "GRANT ALL ON public.nugget_screening_evals TO PUBLIC",
    ],
)
def test_destructive_and_ddl_statements_are_refused(sql):
    """Nugget's history is superseded, never deleted. 863 evaluations and six
    runs live in these tables; a stray DELETE is unrecoverable."""
    with pytest.raises(nw.NuggetWriteRefused):
        nw.register(sql)
    with pytest.raises(nw.NuggetWriteRefused):
        nw.execute(_FakeSession(), sql)


def test_a_delete_hidden_inside_a_registered_looking_update_is_refused():
    """The keyword check runs over the whole statement, not just its first
    word, so a write cannot smuggle one in via a CTE."""
    sql = (
        "UPDATE public.nugget_screening_runs SET status = 'x' "
        "FROM (DELETE FROM public.nugget_screening_evals RETURNING id) d "
        "WHERE d.id = id"
    )
    with pytest.raises(nw.NuggetWriteRefused):
        nw.execute(_FakeSession(), sql)


def test_a_select_is_refused():
    """Reads go through nugget_reads, which has its own guard. This module
    should not become a second, weaker read path."""
    with pytest.raises(nw.NuggetWriteRefused):
        nw.execute(_FakeSession(), "SELECT * FROM public.nugget_screening_evals")


def test_multi_statement_sql_is_refused():
    with pytest.raises(nw.NuggetWriteRefused):
        nw.execute(
            _FakeSession(),
            "UPDATE public.nugget_screening_runs SET status='x'; "
            "DROP TABLE public.nugget_screening_evals",
        )


def test_a_comment_cannot_hide_a_forbidden_keyword():
    """Comments are stripped BEFORE the checks, so a keyword parked in one
    cannot produce a false pass, and a `;` in one cannot produce a false fail."""
    sql = (
        "UPDATE /* DELETE */ public.nugget_screening_runs "
        "SET status = :status WHERE id = :id"
    )
    nw.register(sql)  # the comment held the keyword, so this is legitimate
    nw.execute(_FakeSession(), sql, status="x", id="y")


def test_a_write_to_a_non_nugget_table_is_refused():
    """This module is not a general-purpose writer. Coco's own tables use the
    ORM; Markaz's tables are not Coco's to write at all."""
    with pytest.raises(nw.NuggetWriteRefused):
        nw.register("UPDATE public.applications SET status = 'rejected'")


# --------------------------------------------------------------------------
# The schema switch
# --------------------------------------------------------------------------


def test_schema_defaults_to_public(monkeypatch):
    monkeypatch.delenv(nw._SCHEMA_ENV, raising=False)
    assert nw.schema() == "public"


def test_schema_can_be_pointed_at_the_test_schema(monkeypatch):
    """Integration tests run against `nugget_worker_test`, which carries the
    same constraints and no evaluations."""
    monkeypatch.setenv(nw._SCHEMA_ENV, "nugget_worker_test")
    assert nw.schema() == "nugget_worker_test"


def test_a_schema_name_that_is_not_an_identifier_is_refused(monkeypatch):
    """The schema is interpolated into SQL because Postgres will not take an
    identifier as a bind parameter. That is precisely why it is validated."""
    monkeypatch.setenv(nw._SCHEMA_ENV, "public; DROP SCHEMA coco CASCADE")
    with pytest.raises(ValueError):
        nw.schema()


def test_the_read_module_still_cannot_write():
    """Lifting the read-only rule must not have loosened nugget_reads. It
    guards every existing read path and should be exactly as strict as before."""
    from webapp.services import nugget_reads

    with pytest.raises(PermissionError):
        nugget_reads.assert_read_only(
            "UPDATE public.nugget_screening_evals SET tier = 'P1'"
        )
    with pytest.raises(PermissionError):
        nugget_reads.assert_read_only(
            "WITH d AS (DELETE FROM public.nugget_screening_evals RETURNING id) "
            "SELECT * FROM d"
        )
