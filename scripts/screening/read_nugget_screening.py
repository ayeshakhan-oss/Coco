"""Read Nugget's technical-screening results out of the shared Markaz database.

Technical roles are screened by Nugget (Aymen Abid's agent), which writes to the
`public.nugget_screening_*` tables. Coco reads those results so they can feed
screening reports and decision briefs.

🔒 READ ONLY. These are not Coco's tables. This module refuses to issue anything
   but a SELECT. Rubric changes, re-runs and tier changes go to Aymen.

See .claude/skills/02_candidate-evaluation/technical-screening.md for the method.

Usage:
    python scripts/screening/read_nugget_screening.py --list
    python scripts/screening/read_nugget_screening.py --job 38
    python scripts/screening/read_nugget_screening.py --job 38 --tier P1
    python scripts/screening/read_nugget_screening.py --job 38 --tier P1 --detail
"""
from __future__ import annotations

import argparse
import os
import sys

import requests
from dotenv import load_dotenv

sys.path.insert(0, r"c:\Agent Coco")
from scripts.utils.audit_log import log_db_query  # noqa: E402
from webapp.services.nugget_reads import UNSCORED_TIERS, assert_read_only  # noqa: E402

load_dotenv(r"c:\Agent Coco\.env")
_URL = os.environ["DATABASE_URL"]
_HOST = _URL.split("@")[1].split("/")[0]

# The `nugget_deg` schema holds the same table names but is EMPTY. Always public.
SCHEMA = "public"


def q(sql: str, params=None, *, table: str = "nugget_screening", context: str = "read"):
    """Run one read-only query against Neon over HTTPS (port 5432 is blocked)."""
    assert_read_only(sql)
    r = requests.post(
        f"https://{_HOST}/sql",
        headers={"Neon-Connection-String": _URL, "Content-Type": "application/json"},
        json={"query": sql, "params": params or []},
        timeout=120,
    )
    r.raise_for_status()
    rows = r.json()["rows"]
    log_db_query(table=table, filters=context, rows_returned=len(rows), context="nugget_screening")
    return rows


def list_rubrics():
    rows = q(
        f"""
        SELECT r.job_id, j.title AS job_title, r.version, r.status, r.seniority,
               r.min_years, r.max_score, r.created_by, r.activated_at
        FROM {SCHEMA}.nugget_screening_rubrics r
        LEFT JOIN {SCHEMA}.jobs j ON j.id = r.job_id
        ORDER BY r.activated_at DESC NULLS LAST
        """,
        table="nugget_screening_rubrics",
        context="list rubrics",
    )
    print(f"\n=== RUBRICS ({len(rows)}) ===")
    for x in rows:
        print(
            f"  Job {x['job_id']:>4}  v{x['version']}  {x['status']:<8} "
            f"{(x['job_title'] or '?'):<28} {x['seniority'] or '?':<8} "
            f"min {x['min_years']}y   by {x['created_by']}"
        )

    runs = q(
        f"""
        SELECT job_id, mode, status, model, total_items, ok_count, unusable_count,
               failed_count, actual_cost_usd, created_at, finished_at
        FROM {SCHEMA}.nugget_screening_runs ORDER BY created_at DESC
        """,
        table="nugget_screening_runs",
        context="list runs",
    )
    print(f"\n=== RUNS ({len(runs)}) ===")
    for x in runs:
        flag = "  <-- FAILED" if x["status"] == "failed" else ""
        print(
            f"  Job {x['job_id']:>4}  {x['status']:<10} {x['model']:<20} "
            f"items {x['total_items']:>4}  ok {x['ok_count']:>4}  "
            f"unusable {x['unusable_count']:>3}  failed {x['failed_count']:>4}  "
            f"${x['actual_cost_usd']}{flag}"
        )


def job_summary(job_id: int):
    rows = q(
        f"""
        SELECT tier, status, COUNT(*) AS n,
               ROUND(AVG(score_pct), 1) AS avg_pct,
               MIN(score_pct) AS min_pct, MAX(score_pct) AS max_pct
        FROM {SCHEMA}.nugget_screening_evals
        WHERE job_id = $1 AND is_current
        GROUP BY tier, status
        ORDER BY tier
        """,
        [job_id],
        table="nugget_screening_evals",
        context=f"summary job {job_id}",
    )
    if not rows:
        print(f"No current screening evaluations for job {job_id}.")
        return
    print(f"\n=== JOB {job_id} SCREENING (current evals only) ===")
    total = 0
    for x in rows:
        total += int(x["n"])
        if x["tier"] in UNSCORED_TIERS:
            # avg/min/max are 0.00 artefacts here (the CV never cleared the
            # readability floor), not a measurement. Never print them as a score.
            rng = "  not scored (document unreadable / below readability floor)"
        elif x["avg_pct"] is None:
            rng = ""
        else:
            rng = f"  avg {x['avg_pct']}%  range {x['min_pct']}-{x['max_pct']}"
        print(f"  {x['tier']:<14} {x['status']:<10} n={x['n']:>4}{rng}")
    print(f"  {'TOTAL':<14} {'':<10} n={total:>4}")
    print(
        "\n  NOTE: UNUSABLE and MANUAL_REVIEW both mean the CV could not be read\n"
        "  (unusable at all, or below the rubric's readability floor). Neither is\n"
        "  a rejection or a real score, and those candidates still need a human\n"
        "  to look at them."
    )


def tier_list(job_id: int, tier: str, detail: bool = False):
    rows = q(
        f"""
        SELECT candidate_name, candidate_email, application_id, score_pct, tier,
               tier_reason, confidence, resume_health, verdict, strengths, gaps
        FROM {SCHEMA}.nugget_screening_evals
        WHERE job_id = $1 AND is_current AND tier = $2
        ORDER BY score_pct DESC
        """,
        [job_id, tier],
        table="nugget_screening_evals",
        context=f"job {job_id} tier {tier}",
    )
    print(f"\n=== JOB {job_id} · TIER {tier} ({len(rows)}) ===")
    for x in rows:
        score = (
            "not scored (document unreadable / below readability floor)"
            if tier in UNSCORED_TIERS
            else f"score {x['score_pct']}%"
        )
        print(
            f"\n  {x['candidate_name']}  ({x['candidate_email']})"
            f"\n    app {x['application_id']}  {score}  "
            f"confidence {x['confidence']}  resume health {x['resume_health']}"
            f"\n    {x['tier_reason']}"
        )
        if detail:
            print(f"    VERDICT: {x['verdict']}")
            for s in (x["strengths"] or [])[:5]:
                print(f"      + {s}")
            for g in (x["gaps"] or [])[:5]:
                print(f"      - {g}")
    print("\n  Source: Nugget screening engine (Aymen Abid). Attribute it as such.")


def main():
    p = argparse.ArgumentParser(description="Read Nugget's technical screening results.")
    p.add_argument("--list", action="store_true", help="list rubrics and runs")
    p.add_argument("--job", type=int, help="job id to summarise")
    p.add_argument("--tier", help="tier to list, e.g. P1")
    p.add_argument("--detail", action="store_true", help="include verdict, strengths and gaps")
    a = p.parse_args()

    if a.list:
        list_rubrics()
    elif a.job and a.tier:
        tier_list(a.job, a.tier.upper(), a.detail)
    elif a.job:
        job_summary(a.job)
    else:
        p.print_help()


if __name__ == "__main__":
    main()
