"""Every alembic revision id must fit `alembic_version.version_num`.

That column is `varchar(32)`. A longer id is not caught by anything at authoring
time: the migration imports fine, `alembic history` renders fine, and the failure
only appears when you actually try to stamp it against Postgres, with
`StringDataRightTruncation` from deep inside SQLAlchemy.

This happened on 2026-09-22 with `0011_eval_benchmark_qa_gate_and_rubric_provenance`
(49 characters), which could never have been applied. `0008_values_draft_interview_date`
is 32 characters exactly, so the margin was already gone.

Run: python -m pytest webapp/tests/test_migration_revision_ids.py
"""

from __future__ import annotations

import os
import re

VERSIONS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "alembic",
    "versions",
)

# alembic_version.version_num is varchar(32).
MAX_REVISION_ID = 32

_REVISION = re.compile(r'^revision\s*=\s*["\'](?P<id>[^"\']+)["\']', re.M)
_DOWN = re.compile(r'^down_revision\s*=\s*["\'](?P<id>[^"\']+)["\']', re.M)


def _migrations() -> list[tuple[str, str, str | None]]:
    out = []
    for name in sorted(os.listdir(VERSIONS_DIR)):
        if not name.endswith(".py") or name.startswith("__"):
            continue
        with open(os.path.join(VERSIONS_DIR, name), encoding="utf-8") as fh:
            text = fh.read()
        rev = _REVISION.search(text)
        assert rev, f"{name}: no revision id found"
        down = _DOWN.search(text)
        out.append((name, rev.group("id"), down.group("id") if down else None))
    return out


def test_every_revision_id_fits_the_version_column():
    too_long = [
        (name, rev, len(rev))
        for name, rev, _ in _migrations()
        if len(rev) > MAX_REVISION_ID
    ]
    assert not too_long, (
        "revision ids longer than the varchar(32) version_num column, so they can "
        f"never be stamped: {too_long}"
    )


def test_the_chain_is_linear_and_every_parent_exists():
    migrations = _migrations()
    ids = {rev for _, rev, _ in migrations}

    for name, _, down in migrations:
        if down is not None:
            assert down in ids, f"{name}: down_revision {down!r} is not any known revision"

    # Exactly one root (down_revision None) and no revision claimed by two children.
    roots = [rev for _, rev, down in migrations if down is None]
    assert len(roots) == 1, f"expected exactly one root migration, got {roots}"

    parents = [down for _, _, down in migrations if down is not None]
    assert len(parents) == len(set(parents)), (
        f"a revision is the parent of more than one migration (branched history): {parents}"
    )
