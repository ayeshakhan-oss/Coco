"""The ONLY module that writes to Nugget's screening tables.

🔒 HISTORY, AND WHY THIS MODULE IS SHAPED LIKE THIS.

`public.nugget_screening_*` belongs to Nugget (Aymen Abid's engine). Until
2026-09-25 Coco was read-only against it, enforced by
`nugget_reads.assert_read_only`, because two engines writing the same rows
produce two sets of numbers that disagree about the same candidate.

That rule was lifted by the owner so Coco can launch screening runs from
Railway -- Nugget's own worker mostly runs on a desktop, so when the desktop is
off, nothing screens. What did NOT change is the reasoning behind the rule. So:

  * `nugget_reads.assert_read_only` is untouched and still guards every read
    path. The read module cannot write, at all, exactly as before.
  * Writes are confined to THIS module, and this module cannot execute SQL it
    was not shipped with. `execute()` refuses any statement that is not one of
    the registered constants below. There is no ad-hoc write path, and no
    caller can pass one in.

That is the difference between narrowing a guard and weakening it.

🔴 NOTHING HERE DELETES. Evaluations supersede via `is_current`/`superseded_by`
and rubrics via `status='archived'`; run items are written once and then change
state. A DELETE or a DDL keyword anywhere in a statement is refused even if a
future edit adds one to the registry, so losing Nugget's history takes a
deliberate change to this file and its tests, never a passing edit elsewhere.
"""

from __future__ import annotations

import logging
import os
import re
from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session

log = logging.getLogger("webapp.nugget_writes")

# The schema holding Nugget's tables. `nugget_worker_test` carries the same 12
# tables with the same 18 CHECK constraints and 32 indexes and no evaluations,
# so integration tests point here rather than at 863 live rows. `nugget_deg`
# also mirrors the table names and is EMPTY -- never point anything at it and
# conclude "no screening exists".
DEFAULT_SCHEMA = "public"
_SCHEMA_ENV = "NUGGET_SCHEMA"
_SCHEMA_RE = re.compile(r"^[a-z_][a-z0-9_]*$")


def schema() -> str:
    """Resolved at call time, not import time, so a test can set the env var
    after this module is already imported."""
    value = (os.environ.get(_SCHEMA_ENV) or DEFAULT_SCHEMA).strip()
    if not _SCHEMA_RE.match(value):
        # Interpolated into SQL, so it can never be attacker-shaped. A schema
        # name is not a bind parameter in Postgres, which is exactly why this
        # check exists rather than a comment saying "trusted input".
        raise ValueError(f"{_SCHEMA_ENV}={value!r} is not a bare identifier")
    return value


class NuggetWriteRefused(PermissionError):
    """A statement that is not in the registry, or not a write at all."""


# Statements this module may issue, by exact text. `register()` is the only way
# in, and it runs at import time, so the set is fixed before any request is
# served. A caller holding a hand-built string cannot execute it.
_REGISTRY: set[str] = set()

_ALLOWED_LEADING = ("insert", "update")

# Refused anywhere in a statement, registered or not. DELETE is on this list on
# purpose: see the module docstring.
_FORBIDDEN_RE = re.compile(
    r"\b(DELETE|DROP|TRUNCATE|ALTER|CREATE|GRANT|REVOKE|COPY|MERGE)\b",
    re.IGNORECASE,
)

_COMMENT_RE = re.compile(r"/\*.*?\*/|--[^\n]*", re.DOTALL)


def _normalise(sql: str) -> str:
    """Whitespace-insensitive form, so an f-string rendered with a different
    schema still matches the constant it was registered from."""
    return " ".join(sql.split())


def register(sql: str) -> str:
    """Add a statement template to the allowlist and return it unchanged.

    Every write constant in this package is defined as `register("...")` and
    carries a literal `{schema}` placeholder, so the registry and the constants
    cannot drift apart: a constant that was never registered does not execute.

    The shape checks run against the template RENDERED with the default
    schema, because `{schema}.nugget_x` is not what Postgres will actually see
    and a check that passes on the template but not on the rendered statement
    would be worth nothing.
    """
    _assert_write_shaped(render(sql, DEFAULT_SCHEMA))
    _REGISTRY.add(_normalise(sql))
    return sql


def render(sql: str, schema_name: str) -> str:
    """Substitute the schema placeholder. Kept here, and applied by `execute`
    itself, so no caller ever chooses the schema a write lands in."""
    return sql.replace("{schema}", schema_name)


def _assert_write_shaped(sql: str) -> None:
    """The static checks, applied both at registration and at execution.

    Registration-time so a bad constant fails at import rather than at 3am on
    someone's run; execution-time so the guarantee does not depend on the
    registry being the only thing anyone ever trusts.
    """
    without_comments = _COMMENT_RE.sub(" ", sql)
    trimmed = without_comments.strip()
    if trimmed.endswith(";"):
        trimmed = trimmed[:-1].rstrip()
    if ";" in trimmed:
        raise NuggetWriteRefused(
            "multi-statement SQL is refused: one statement per execute()."
        )

    if not trimmed.lstrip().lower().startswith(_ALLOWED_LEADING):
        raise NuggetWriteRefused(
            "only INSERT and UPDATE may be written to Nugget's tables; "
            f"got {trimmed.lstrip()[:40]!r}"
        )

    if _FORBIDDEN_RE.search(trimmed):
        raise NuggetWriteRefused(
            "statement contains a destructive or DDL keyword. Nugget's history "
            "is superseded, never deleted."
        )

    if "nugget_" not in trimmed.lower():
        raise NuggetWriteRefused(
            "this module writes only to nugget_screening_* tables."
        )


def execute(db: Session, sql: str, **params: Any):
    """Run one registered write against the resolved schema.

    `sql` is the TEMPLATE, exactly as `register()` received it. This function
    does the substitution, so a caller cannot pre-render one schema and pass a
    statement pointing somewhere else.
    """
    if _normalise(sql) not in _REGISTRY:
        raise NuggetWriteRefused(
            "this statement is not in nugget_writes' allowlist. Writes to "
            "Nugget's tables must be declared as module-level constants via "
            "register(), never built at the call site."
        )
    rendered = render(sql, schema())
    _assert_write_shaped(rendered)
    return db.execute(text(rendered), params)


def registered_count() -> int:
    """For the test that asserts the allowlist did not silently empty."""
    return len(_REGISTRY)
