"""System health: what is configured, what is connected, what is broken.

Skill 04 (Data and Systems) is infrastructure, not a candidate workflow. It is
about how the database is reached, how mail is sent, how tokens are managed
and what gets audited. So "live" for it means a page that answers one
question honestly: is Coco healthy, and if not, where.

🔴 NO SECRET VALUE IS EVER RETURNED. Every credential is reported as a
   boolean, a length, or a masked tail. A health page is the most-screenshotted
   page in any app, and a token that reaches a screenshot is a token that has
   to be re-minted. `mask()` is the only way a credential is allowed to appear.

🔴 A MISSING COCO TABLE IS A FIRST-CLASS ALARM, not a 500 somewhere else. The
   Markaz/Replit schema push has dropped Coco's tables before, which is why
   they live in the `coco` schema at all
   (memory/root_cause_markaz_replit_drops_coco_tables_2026_06_30.md). This
   checks for their presence directly rather than waiting for a page to fail.

🔴 KNOWN-BROKEN THINGS ARE LISTED, NOT HIDDEN. A health page that only shows
   green is worse than none, because it teaches people the absence of an alarm
   means everything works. The Layer 3 send hook is inert, Calendar OAuth is
   dead, and migrations do not run on boot. Those are stated.
"""

from __future__ import annotations

import datetime as dt
from typing import Optional

from sqlalchemy import text
from sqlalchemy.orm import Session

OK = "ok"
DEGRADED = "degraded"
MISSING = "missing"
UNKNOWN = "unknown"

#: Every table the app owns in the `coco` schema, with what it holds. The list
#: is explicit rather than derived from the metadata, so a table that is
#: quietly dropped from the models still shows up here as an absence.
COCO_TABLES = {
    "comm_evidence": "Gmail evidence behind each candidate's history",
    "gmail_sync_runs": "when the mailbox was last read",
    "values_scorecard_drafts": "values scorecards awaiting submission",
    "eval_benchmarks": "case study answer keys",
    "case_study_evaluations": "scored case study submissions",
    "cv_screens": "CV screening results",
    "cv_screen_skips": "CVs that could not be read, and why",
    "case_study_probes": "case study send and submission evidence",
    "kcd_evaluations": "Knowledge / Capacity / Design scores",
    "sourced_candidates": "the passive sourcing pool and outreach state",
    "invite_links": "booking links and the page titles they were proved against",
    "invite_sends": "every invite that actually left, pilot and live",
    "contract_masters": "the approved contract and NDA masters, kept out of git",
    # Deliberately holds no document and no field values: the values are the
    # PII. It records that a document was issued, and for whom.
    "contract_builds": "which contracts were generated, for whom, and whether they passed",
}

_TABLES_SQL = text(
    """
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = 'coco'
    """
)

_COUNT_SQL = "SELECT count(*) AS n FROM coco.{table}"

_APP_TABLES_SQL = text(
    """
    SELECT
      (SELECT count(*) FROM communications)                   AS communications,
      (SELECT count(*) FROM communications WHERE status = 'sent')  AS sent,
      (SELECT count(*) FROM app_users)                        AS users
    """
)


def mask(value: Optional[str]) -> Optional[str]:
    """The only way a credential may appear anywhere in this module.

    Returns the last four characters and nothing else, so two people can agree
    they are looking at the same token without either of them learning it.
    """
    if not value:
        return None
    tail = value[-4:] if len(value) > 8 else ""
    return f"set, {len(value)} chars, ending {tail}" if tail else "set"


def table_health(db: Session) -> dict:
    """Which coco tables exist, and how much is in them.

    A count that fails is reported against that table rather than aborting the
    whole page: one unreadable table must not hide the other eleven.
    """
    try:
        present = {r[0] for r in db.execute(_TABLES_SQL).all()}
    except Exception as exc:  # the schema itself is unreachable
        return {
            "status": UNKNOWN,
            "error": f"could not read the coco schema: {type(exc).__name__}",
            "tables": [],
            "missing": [],
        }

    rows, missing = [], []
    for name, purpose in COCO_TABLES.items():
        if name not in present:
            missing.append(name)
            rows.append({"name": name, "purpose": purpose, "exists": False,
                         "rows": None})
            continue
        count: Optional[int] = None
        try:
            # The table name comes from the constant above, never from input.
            count = db.execute(text(_COUNT_SQL.format(table=name))).scalar()
        except Exception:
            count = None
        rows.append({"name": name, "purpose": purpose, "exists": True,
                     "rows": count})

    return {
        "status": OK if not missing else DEGRADED,
        "error": None,
        "tables": rows,
        "missing": missing,
        # Said plainly, because the last time this happened nobody knew why a
        # page had started returning 500.
        "note": (
            "These tables live in the `coco` schema on purpose. Markaz's Replit "
            "schema push has dropped Coco tables out of `public` before, so a "
            "missing table here usually means a reset, not a bug in a page."
            if missing else
            "All app-owned tables are present in the `coco` schema."
        ),
    }


def integration_status(settings) -> list[dict]:
    """What is configured, without revealing any of it.

    `configured` answers whether the app could use it at all. It is not a
    liveness check: a token can be present and expired, and saying otherwise
    would be the kind of green light this module exists to avoid.
    """
    out = []

    out.append({
        "key": "database",
        "label": "Neon Postgres",
        "configured": bool(settings.database_url),
        "detail": (
            "pooled connection" if settings.database_url
            and "-pooler" in settings.database_url
            else "direct connection (prefer the -pooler host)"
            if settings.database_url else "DATABASE_URL is not set"
        ),
    })

    # Which transport a send would actually use, resolved the same way
    # `sending.get_transport()` resolves it, so the page cannot disagree with
    # the code.
    if settings.gmail_oauth_token_json:
        transport = "Gmail API over HTTPS (Railway blocks outbound SMTP)"
        configured = True
    elif settings.email_password:
        transport = "SMTP (local development)"
        configured = True
    else:
        transport = "nothing configured, so sending is disabled"
        configured = False
    out.append({
        "key": "email",
        "label": "Outbound email",
        "configured": configured,
        "detail": transport,
    })

    model = getattr(settings, "anthropic_model", None)
    has_key = bool(getattr(settings, "anthropic_api_key", None))
    has_oauth = bool(getattr(settings, "anthropic_auth_token", None))
    out.append({
        "key": "anthropic",
        "label": "Claude (drafting)",
        "configured": has_key or has_oauth,
        "detail": (
            f"model {model}"
            + (", Console API key" if has_key else
               ", OAuth token" if has_oauth else "")
            # Rule 30's lesson: an env var silently overriding the code default
            # is invisible until a letter comes out wrong.
            + ". Check `railway variables` before trusting a code default."
        ) if (has_key or has_oauth) else "no credential set, drafting is disabled",
    })

    out.append({
        "key": "deployment",
        "label": "Deployment",
        "configured": True,
        "detail": f"environment {settings.app_env}",
    })
    return out


#: Things that are known to be broken or absent. Listed so nobody rediscovers
#: them during an incident.
KNOWN_GAPS = [
    {
        "key": "layer3_hook",
        "severity": "high",
        "title": "The Layer 3 send-time hook validates nothing",
        "detail": (
            "scripts/hooks/pre_send_validation_hook.py early-returns unless "
            "`tool_name` contains 'send', but it is registered under a 'Bash' "
            "matcher, so tool_name is always literally 'Bash'. It returns 0 on "
            "every call. The webapp does not depend on it: candidate letters "
            "are gated by evaluate_email at send time and invites by their own "
            "gate. Command-line sends have no automated net, so run "
            "scripts/evals/run_eval.py by hand."
        ),
    },
    {
        "key": "calendar_oauth",
        "severity": "medium",
        "title": "Google Calendar OAuth is dead",
        "detail": (
            "The client returns `deleted_client` and no live token holds a "
            "calendar scope. Interview times come from booking emails in "
            "comm_evidence and from invite.ics attachments instead, which is "
            "why an interview reminder requires the date typed from verified "
            "evidence rather than read from a calendar."
        ),
    },
    {
        "key": "migrations_on_boot",
        "severity": "medium",
        "title": "Migrations do not run on deploy",
        "detail": (
            "Deliberate: running alembic on startup couples boot to database "
            "locks and caused healthcheck hangs. A new table therefore has to "
            "be applied by hand. `ensure_app_tables()` recreates the app-owned "
            "tables as a safety net, so check the table list above after any "
            "deploy that adds one."
        ),
    },
]


def summarise(table_report: dict, integrations: list[dict]) -> dict:
    """One line for the top of the page, and the status behind it."""
    unconfigured = [i["label"] for i in integrations if not i["configured"]]
    missing = table_report.get("missing") or []

    if table_report.get("status") == UNKNOWN:
        status, line = DEGRADED, "The database could not be read."
    elif missing:
        status = DEGRADED
        line = (f"{len(missing)} app table{'s' if len(missing) > 1 else ''} "
                f"missing: {', '.join(missing)}.")
    elif unconfigured:
        status = DEGRADED
        line = f"Not configured: {', '.join(unconfigured)}."
    else:
        status = OK
        line = "Everything the app needs is configured and present."

    return {
        "status": status,
        "headline": line,
        # The gap count is always shown, including when everything else is
        # green, so "ok" never reads as "nothing to know about".
        "known_gaps": len(KNOWN_GAPS),
        "checked_at": dt.datetime.now(dt.timezone.utc),
    }
