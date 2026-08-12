# -*- coding: utf-8 -*-
"""Job 41 (GM-Karachi) status update — Ayesha's instruction 2026-08-12:
- Shortlist: Khizran Zehra Baloch 4065, Syed Zubair Ali 4113 (the two in-band fits).
- Reject: all other SCREENED new-batch applicants (67 = 84 screened - 15 no-CV stubs - 2 shortlisted).
  Includes the 6 over-band shortlist recommendations, 7 maybes (Amsal Malik: Ayesha says too
  fresh for this position), and 54 no-hires.
- HOLD (untouched, still 'new'): 15 LinkedIn-import stubs with no CV — excluded from the sweep
  as flagged in the pilot report; Ayesha can clear them separately.
Rule 13: whitelist derived from the frozen 10-Aug screening summary (_summary.json), per-row
expected-status guard, row-count asserts. NO emails.
"""
import json
import os
import requests
from dotenv import load_dotenv

load_dotenv(r"c:\Agent Coco\.env")
URL = os.environ["DATABASE_URL"]
HOST = URL.split("@")[1].split("/")[0]

SUMMARY = r"c:\Agent Coco\output\cv_texts_job41_new_batch\_summary.json"
with open(SUMMARY, encoding="utf-8") as f:
    screened = json.load(f)

SCREENED_IDS = sorted(s["app_id"] for s in screened)
STUBS = sorted(s["app_id"] for s in screened if s.get("note") == "no_resume")
SHORTLIST = [4065, 4113]  # Khizran Zehra Baloch, Syed Zubair Ali
REJECT = sorted(set(SCREENED_IDS) - set(STUBS) - set(SHORTLIST))

assert len(SCREENED_IDS) == 84, f"screened {len(SCREENED_IDS)} != 84"
assert len(STUBS) == 15, f"stubs {len(STUBS)} != 15"
assert set(SHORTLIST) <= set(SCREENED_IDS) and not (set(SHORTLIST) & set(STUBS))
assert len(REJECT) == 67, f"reject list {len(REJECT)} != 67"
print("Stubs held (untouched):", STUBS)
print("Reject list (67):", REJECT)


def q(sql, params=None):
    r = requests.post(f"https://{HOST}/sql",
                      headers={"Neon-Connection-String": URL, "Content-Type": "application/json"},
                      json={"query": sql, "params": params or []}, timeout=120)
    r.raise_for_status()
    return r.json()["rows"]


# Step 0: re-pull current statuses and verify every target is still job 41 + 'new'
rows = q("SELECT id, status, job_id FROM applications WHERE id = ANY($1::int[])",
         [SHORTLIST + REJECT])
assert len(rows) == len(SHORTLIST) + len(REJECT), "missing app rows"
problems = [(r["id"], r["status"], r["job_id"]) for r in rows
            if r["job_id"] != 41 or r["status"] != "new"]
if problems:
    for p in problems:
        print("GUARD FAIL (id, status, job_id):", p)
    raise SystemExit("Aborting - statuses changed since assessment. Re-verify.")

# Guard: no application newer than the screening batch may exist in 'new'
extra = q("SELECT id FROM applications WHERE job_id=41 AND status='new' "
          "AND NOT (id = ANY($1::int[]))", [SCREENED_IDS])
assert not extra, f"unscreened 'new' apps present, aborting: {extra}"
print(f"Pre-check OK: {len(SHORTLIST)} to shortlist, {len(REJECT)} to reject, {len(STUBS)} stubs held.")

# Shortlist updates (one by one, guarded)
for app_id in SHORTLIST:
    r = q("UPDATE applications SET status='shortlisted', updated_at=NOW() "
          "WHERE id=$1 AND job_id=41 AND status='new' RETURNING id", [app_id])
    assert len(r) == 1, f"shortlist update failed for {app_id}"
    print(f"  shortlisted: {app_id}")

# Reject updates (explicit ID whitelist, single statement, row-count assert)
r = q("UPDATE applications SET status='rejected', updated_at=NOW() "
      "WHERE id = ANY($1::int[]) AND job_id=41 AND status='new' RETURNING id",
      [REJECT])
assert len(r) == 67, f"expected 67 rejected, got {len(r)} - INVESTIGATE"
print(f"  rejected: {len(r)} applications")

# Post-verify
final = q("SELECT status, COUNT(*) AS n FROM applications WHERE job_id=41 GROUP BY status ORDER BY n DESC")
print("\nJob 41 final status counts:", final)
held = q("SELECT id, status FROM applications WHERE id = ANY($1::int[]) ORDER BY id", [STUBS])
print("Stubs (should all still be 'new'):", held)
