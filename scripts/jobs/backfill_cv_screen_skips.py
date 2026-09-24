"""Backfill `coco.cv_screen_skips` for candidates already attempted and refused.

WHY THIS EXISTS. Refusing to screen an unreadable CV is correct (CLAUDE.md
Rule 32) but until 2026-09-25 the refusal was not written down, so a refused
candidate looked exactly like one nobody had opened yet. On CPD Coach that was
81 of 411 and Ayesha twice reported the screener as "stopping midway" when it
had in fact read the whole position.

The code now records a skip as it happens. This catches up the ones that were
already refused, so the page tells the truth on the first load rather than
after somebody runs the position again.

🔑 IT USES THE ROUTER'S OWN CODE PATH -- `_screen_and_store`, the same function
the batch endpoint calls. The reason text and the `kind` bucket therefore
cannot drift from what a live run would produce, which is exactly what copying
the message strings into this file would have guaranteed.

A CV that turns out to be READABLE is screened and stored properly, not forced
into a skip: that is the same function doing its normal job, and it is the
honest outcome if one of them was only ever a transient failure.

Usage:
    python scripts/jobs/backfill_cv_screen_skips.py --job 17 [--apply]

Dry run by default. Nothing is written without --apply.
"""

from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".env"))

from webapp.routers.cv_screening import (  # noqa: E402
    _job_and_jd,
    _record_skip,
    _screen_and_store,
    _skip_kind,
    _Skip,
)

UNSCREENED_SQL = text(
    """
    SELECT a.id
    FROM applications a
    WHERE a.job_id = :job_id
      AND NOT EXISTS (
          SELECT 1 FROM coco.cv_screens s
          WHERE s.application_id = a.id AND s.is_current
      )
      AND NOT EXISTS (
          SELECT 1 FROM coco.cv_screen_skips k WHERE k.application_id = a.id
      )
    ORDER BY a.id
    """
)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--job", type=int, required=True)
    ap.add_argument("--apply", action="store_true", help="write; otherwise dry run")
    args = ap.parse_args()

    # pool_pre_ping: this machine's direct 5432 connection to Neon drops on
    # idle, and a backfill is a long loop of small statements.
    engine = create_engine(os.environ["DATABASE_URL"], pool_pre_ping=True)
    db = sessionmaker(bind=engine)()

    job, jd, jd_sha = _job_and_jd(db, args.job)
    ids = [r[0] for r in db.execute(UNSCREENED_SQL, {"job_id": args.job}).all()]
    print(f"job {args.job} ({job['title']}): {len(ids)} attempted-but-unrecorded\n")

    counts: dict[str, int] = {}
    for app_id in ids:
        try:
            row = _screen_and_store(
                db, app_id, job_id=args.job, job=job, jd=jd, jd_sha=jd_sha,
                created_by="backfill-2026-09-25",
            )
            counts["SCREENED (was readable after all)"] = (
                counts.get("SCREENED (was readable after all)", 0) + 1
            )
            print(f"  app {app_id}: screened, {row.tier} {row.match}%")
            if args.apply:
                db.commit()
            else:
                db.rollback()
        except _Skip as exc:
            db.rollback()
            _record_skip(
                db, app_id, job_id=args.job, candidate_name=exc.candidate_name,
                reason=exc.reason, cv_file_name=exc.cv_file_name,
                created_by="backfill-2026-09-25",
            )
            kind = _skip_kind(exc.reason)
            counts[kind] = counts.get(kind, 0) + 1
            print(f"  app {app_id}: {kind} -- {exc.reason[:90]}")
            if args.apply:
                db.commit()
            else:
                db.rollback()
        except Exception as exc:  # noqa: BLE001
            # Left outstanding on purpose: an unexpected failure is a bug, not
            # a statement about the candidate's document.
            db.rollback()
            counts["UNEXPECTED (left outstanding)"] = (
                counts.get("UNEXPECTED (left outstanding)", 0) + 1
            )
            print(f"  app {app_id}: {type(exc).__name__}: {str(exc)[:110]}")

    print("\n--- summary ---")
    for k, n in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f"{n:4d}  {k}")
    print("\nDRY RUN, nothing written. Re-run with --apply." if not args.apply
          else "\nWritten.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
