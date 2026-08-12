# -*- coding: utf-8 -*-
"""Job 39 (GM-Lahore) new-batch status update — Ayesha's instruction 2026-08-12:
screen all 'new' applicants strictly against the JD (storytelling for govt/institutional
audiences, high-level convenings, partnerships->deal closure, pipeline discipline) and the
PKR 210-270k band; shortlist the worth-interviewing, reject the rest.

VERDICT: 36 'new' apps (33 assessed: 32 CVs read fully + 1 OCR-recovered + 1 docx-recovered;
3 LinkedIn no-CV stubs). ZERO meet JD + band together. All 36 rejected (stubs rejected per
Job-42 precedent). Closest misses (all over band): Faryal Najeeb 4120 (475k), Shehreen Umair
3731 (350k), Hania Khan 4037 (300k, active on Job 42). Cross-job dups rejected here but live
elsewhere: Zirghaam 3831 (Job 41), Hania 4037 (Job 42), Shahzeb 4115 (rejected Job 41).
Rule 13: whitelist from the frozen extraction summary, per-row guards, row-count asserts.
NO emails — status updates only.
"""
import json
import os
import requests
from dotenv import load_dotenv

load_dotenv(r"c:\Agent Coco\.env")
URL = os.environ["DATABASE_URL"]
HOST = URL.split("@")[1].split("/")[0]

SUMMARY = r"c:\Agent Coco\output\cv_texts_job39_new_batch\_summary.json"
with open(SUMMARY, encoding="utf-8") as f:
    screened = json.load(f)

REJECT = sorted(s["app_id"] for s in screened)
assert len(REJECT) == 36, f"screened {len(REJECT)} != 36"


def q(sql, params=None):
    r = requests.post(f"https://{HOST}/sql",
                      headers={"Neon-Connection-String": URL, "Content-Type": "application/json"},
                      json={"query": sql, "params": params or []}, timeout=120)
    r.raise_for_status()
    return r.json()["rows"]


# Guard 1: every target still job 39 + 'new'
rows = q("SELECT id, status, job_id FROM applications WHERE id = ANY($1::int[])", [REJECT])
assert len(rows) == 36, "missing app rows"
problems = [(r["id"], r["status"], r["job_id"]) for r in rows if r["job_id"] != 39 or r["status"] != "new"]
if problems:
    for p in problems:
        print("GUARD FAIL (id, status, job_id):", p)
    raise SystemExit("Aborting - statuses changed since assessment. Re-verify.")

# Guard 2: no unscreened arrival since extraction
extra = q("SELECT id FROM applications WHERE job_id=39 AND status='new' AND NOT (id = ANY($1::int[]))", [REJECT])
assert not extra, f"unscreened 'new' apps present, aborting: {extra}"
print(f"Pre-check OK: 0 to shortlist, {len(REJECT)} to reject.")

r = q("UPDATE applications SET status='rejected', updated_at=NOW() "
      "WHERE id = ANY($1::int[]) AND job_id=39 AND status='new' RETURNING id", [REJECT])
assert len(r) == 36, f"expected 36 rejected, got {len(r)} - INVESTIGATE"
print(f"  rejected: {len(r)} applications")

final = q("SELECT status, COUNT(*) AS n FROM applications WHERE job_id=39 GROUP BY status ORDER BY n DESC")
print("\nJob 39 final status counts:", final)
cross = q("SELECT id, job_id, status FROM applications WHERE id IN (4035, 3830) ORDER BY id")
print("Cross-job actives (must be untouched):", cross)
