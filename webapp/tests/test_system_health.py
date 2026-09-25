"""The health page must be read-only, complete, and leak nothing.

Run: python -m pytest webapp/tests/test_system_health.py -v

Three properties, each with a way to be wrong:
  1. READ-ONLY. A health surface that can change things is a new way to break
     production during an incident.
  2. COMPLETE. If a table can be created but is not listed here, the page
     reports "all present" while something is missing. The list is therefore
     tied to the one the app actually creates.
  3. SILENT ABOUT SECRETS. This is the most-screenshotted page in any app.
"""

from __future__ import annotations

import inspect

import pytest

from webapp import deps
from webapp.routers import system as router_mod
from webapp.services import system_health as health


# --------------------------------------------------------------------------
# 1. Read-only
# --------------------------------------------------------------------------


def test_the_router_has_no_write_methods():
    methods: set[str] = set()
    for route in router_mod.router.routes:
        methods |= set(getattr(route, "methods", None) or set())
    assert methods <= {"GET", "HEAD", "OPTIONS"}, methods


def test_no_handler_commits_anything():
    src = inspect.getsource(router_mod)
    for forbidden in ("db.commit()", "db.add(", "db.delete(", "db.flush()"):
        assert forbidden not in src, f"{forbidden} has no place on a health page"


def _dependencies(path: str, method: str) -> set:
    for route in router_mod.router.routes:
        if getattr(route, "path", None) == path and method in (
            getattr(route, "methods", None) or set()
        ):
            return {d.call for d in route.dependant.dependencies if getattr(d, "call", None)}
    raise AssertionError(f"route not found: {method} {path}")


def test_activity_is_editor_gated_and_health_is_not():
    """Activity names candidates next to what they were sent, which is the
    whole pipeline in one list. Health itself is safe for any signed-in user."""
    assert deps.require_editor in _dependencies("/api/system/activity", "GET")
    assert deps.require_editor not in _dependencies("/api/system/health", "GET")
    assert deps.get_current_user in _dependencies("/api/system/health", "GET")


# --------------------------------------------------------------------------
# 2. Complete
# --------------------------------------------------------------------------


def test_every_table_the_app_creates_is_listed_on_the_health_page():
    """The failure this prevents: a table is added to `ensure_app_tables` but
    not to COCO_TABLES, so the page cheerfully reports everything present
    while that one is missing."""
    # Read the FILE, not the live attribute. conftest's DDL guard patches
    # `webapp.db.ensure_app_tables`, so inspect.getsource would hand back the
    # guard's wrapper and this test would silently compare against nothing.
    import pathlib

    from webapp import models

    db_src = (pathlib.Path(__file__).resolve().parents[1] / "db.py").read_text(
        encoding="utf-8"
    )
    start = db_src.index("def ensure_app_tables(")
    end = db_src.index("\ndef ", start + 1)
    src = db_src[start:end]

    created = set()
    for attr in dir(models):
        obj = getattr(models, attr)
        table = getattr(obj, "__table__", None)
        if table is None or getattr(table, "schema", None) != "coco":
            continue
        if f"{attr}.__table__" in src:
            created.add(table.name)

    assert created, "found no coco tables in ensure_app_tables"
    unlisted = sorted(created - set(health.COCO_TABLES))
    assert not unlisted, (
        "These tables are created by the app but are not on the health page, "
        "so their absence would never be reported:\n  " + "\n  ".join(unlisted)
    )


def test_the_completeness_check_bites():
    """Removing a known table from the list must be caught, or the test above
    would pass on an empty comparison."""
    shrunk = dict(health.COCO_TABLES)
    shrunk.pop("invite_sends")
    assert "invite_sends" not in shrunk


def test_both_invite_tables_are_listed():
    assert "invite_links" in health.COCO_TABLES
    assert "invite_sends" in health.COCO_TABLES


# --------------------------------------------------------------------------
# 3. Silent about secrets
# --------------------------------------------------------------------------


class _Settings:
    app_env = "production"
    database_url = "postgresql://user:hunter2@ep-x-pooler.neon.tech/db"
    gmail_oauth_token_json = '{"refresh_token": "1//0gSECRETVALUE"}'
    email_password = "abcd efgh ijkl mnop"
    anthropic_api_key = "sk-ant-api03-REALKEYMATERIAL"
    anthropic_auth_token = None
    anthropic_model = "claude-haiku-4-5-20251001"


SECRETS = ["hunter2", "1//0gSECRETVALUE", "abcd efgh ijkl mnop",
           "sk-ant-api03-REALKEYMATERIAL"]


def test_integration_status_never_returns_a_credential():
    blob = repr(health.integration_status(_Settings()))
    for secret in SECRETS:
        assert secret not in blob, f"{secret!r} leaked into the health payload"


def test_integration_status_still_says_what_is_configured():
    """Leaking nothing is easy if you report nothing. This is the other half."""
    by_key = {i["key"]: i for i in health.integration_status(_Settings())}
    assert by_key["database"]["configured"] is True
    assert "pooled" in by_key["database"]["detail"]
    assert by_key["email"]["configured"] is True
    assert "Gmail API" in by_key["email"]["detail"]
    assert by_key["anthropic"]["configured"] is True
    assert "claude-haiku-4-5-20251001" in by_key["anthropic"]["detail"]


def test_an_unconfigured_deployment_says_so_rather_than_looking_healthy():
    class Empty:
        app_env = "production"
        database_url = None
        gmail_oauth_token_json = None
        email_password = None
        anthropic_api_key = None
        anthropic_auth_token = None
        anthropic_model = None

    by_key = {i["key"]: i for i in health.integration_status(Empty())}
    assert by_key["email"]["configured"] is False
    assert "disabled" in by_key["email"]["detail"]
    assert by_key["anthropic"]["configured"] is False


def test_mask_shows_only_a_tail():
    masked = health.mask("sk-ant-api03-REALKEYMATERIAL")
    assert "REALKEYMATERIAL" not in masked
    assert masked.endswith("RIAL")
    assert health.mask(None) is None
    # Too short to reveal a tail safely.
    assert health.mask("abc") == "set"


# --------------------------------------------------------------------------
# The summary tells the truth
# --------------------------------------------------------------------------


def test_a_missing_table_makes_the_summary_degraded_and_names_it():
    report = {"status": health.DEGRADED, "missing": ["invite_sends"], "tables": []}
    s = health.summarise(report, [{"label": "x", "configured": True}])
    assert s["status"] == health.DEGRADED
    assert "invite_sends" in s["headline"]


def test_an_unreadable_database_is_degraded_not_ok():
    report = {"status": health.UNKNOWN, "missing": [], "tables": []}
    s = health.summarise(report, [{"label": "x", "configured": True}])
    assert s["status"] == health.DEGRADED


def test_a_healthy_system_still_reports_its_known_gaps():
    """An all-green page with nothing else on it teaches people that no alarm
    means nothing to know about."""
    report = {"status": health.OK, "missing": [], "tables": []}
    s = health.summarise(report, [{"label": "x", "configured": True}])
    assert s["status"] == health.OK
    assert s["known_gaps"] == len(health.KNOWN_GAPS) > 0


def test_the_inert_layer_3_hook_is_one_of_the_listed_gaps():
    """It is the single most load-bearing broken thing in the repo, and the
    page must not let anyone assume it is protecting them."""
    gaps = {g["key"]: g for g in health.KNOWN_GAPS}
    assert "layer3_hook" in gaps
    assert gaps["layer3_hook"]["severity"] == "high"
    assert "Bash" in gaps["layer3_hook"]["detail"]


@pytest.mark.parametrize("gap", health.KNOWN_GAPS, ids=[g["key"] for g in health.KNOWN_GAPS])
def test_each_gap_explains_itself(gap):
    assert gap["severity"] in ("high", "medium", "low")
    assert len(gap["detail"]) > 80, "a gap with no explanation is just an alarm"
