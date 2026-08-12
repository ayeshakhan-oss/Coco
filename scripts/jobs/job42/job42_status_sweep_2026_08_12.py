# -*- coding: utf-8 -*-
"""Job 42 (SMG) status sweep — Ayesha's instruction 2026-08-12:
- Mark shortlisted: Bilal Sadiq 4051, Yusra Amjad 4061, Junaid Ali 3992 (case studies sent),
  Arooj Khali 3868 (values pass + case study submitted, was stuck 'applied'),
  batch-3 shortlist-grade still 'new': Ahmad Taj 3971, Ali Wajdan Khan 3977, Hania Khan 4035.
- Mark rejected: 77 explicitly-listed screened no-hires + maybes-below-bar + no-CV stubs.
- HOLD (untouched): Kamran 3930 (Ayesha standing instruction), Jawwad test entry 3867.
Rule 13: explicit ID whitelist, per-row expected-status guard, row-count asserts. NO emails.
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv(r"c:\Agent Coco\.env")
URL = os.environ["DATABASE_URL"]
HOST = URL.split("@")[1].split("/")[0]

SHORTLIST = {  # app_id: expected current status
    4051: "case_study_sent",   # Muhammad Bilal (Bilal Sadiq)
    4061: "case_study_sent",   # Yusra Amjad
    3992: "case_study_sent",   # Junaid Ali
    3868: "applied",           # Arooj Khali
    3971: "new",               # Muhammad Ahmad Taj
    3977: "new",               # Ali Wajdan Khan
    4035: "new",               # Hania Khan
}

REJECT = [  # all currently 'new', screened in batch-3 (or no-CV stubs) — explicit list
    3964, 3965, 3966, 3967, 3968, 3969, 3970, 3972, 3973, 3974, 3975, 3976,
    3978, 3979, 3980, 3981, 3982, 3983, 3984, 3985, 3986, 3987, 3988, 3989,
    3990, 3991, 3993, 3994, 3995, 3996, 3997, 3998, 3999, 4000, 4001, 4002,
    4003, 4004, 4005, 4006, 4007, 4009, 4010, 4011, 4012, 4013, 4014, 4015,
    4016, 4017, 4018, 4019, 4020, 4021, 4022, 4023, 4027, 4028, 4029, 4030,
    4031, 4032, 4034, 4036, 4038, 4039, 4041, 4042, 4043, 4044, 4045, 4046,
    4048, 4049, 4050, 4052, 4053,
]
HOLD = [3930, 3867]

assert len(REJECT) == 77, f"reject list {len(REJECT)} != 77"
assert not (set(REJECT) & set(SHORTLIST)) and not (set(REJECT) & set(HOLD)), "overlap!"


def q(sql, params=None):
    r = requests.post(f"https://{HOST}/sql",
                      headers={"Neon-Connection-String": URL, "Content-Type": "application/json"},
                      json={"query": sql, "params": params or []}, timeout=120)
    r.raise_for_status()
    return r.json()["rows"]


# Step 0: re-pull current statuses and verify expectations before any write
rows = q("SELECT id, status, job_id FROM applications WHERE id = ANY($1::int[])",
         [list(SHORTLIST) + REJECT + HOLD])
by_id = {r["id"]: r for r in rows}
assert len(rows) == len(SHORTLIST) + len(REJECT) + len(HOLD), "missing app rows"
problems = []
for app_id, expected in SHORTLIST.items():
    r = by_id[app_id]
    if r["job_id"] != 42 or r["status"] != expected:
        problems.append((app_id, "shortlist", expected, r["status"], r["job_id"]))
for app_id in REJECT:
    r = by_id[app_id]
    if r["job_id"] != 42 or r["status"] != "new":
        problems.append((app_id, "reject", "new", r["status"], r["job_id"]))
if problems:
    for p in problems:
        print("GUARD FAIL:", p)
    raise SystemExit("Aborting - statuses changed since assessment. Re-verify.")
print(f"Pre-check OK: {len(SHORTLIST)} to shortlist, {len(REJECT)} to reject, {len(HOLD)} held.")

# Shortlist updates (one by one, guarded)
for app_id, expected in SHORTLIST.items():
    r = q("UPDATE applications SET status='shortlisted', updated_at=NOW() "
          "WHERE id=$1 AND job_id=42 AND status=$2 RETURNING id",
          [app_id, expected])
    assert len(r) == 1, f"shortlist update failed for {app_id}"
    print(f"  shortlisted: {app_id}")

# Reject updates (explicit ID whitelist, single statement, row-count assert)
r = q("UPDATE applications SET status='rejected', updated_at=NOW() "
      "WHERE id = ANY($1::int[]) AND job_id=42 AND status='new' RETURNING id",
      [REJECT])
assert len(r) == 77, f"expected 77 rejected, got {len(r)} - INVESTIGATE"
print(f"  rejected: {len(r)} applications")

# Post-verify
final = q("SELECT status, COUNT(*) AS n FROM applications WHERE job_id=42 GROUP BY status ORDER BY n DESC")
print("\nJob 42 final status counts:", final)
held = q("SELECT id, status FROM applications WHERE id = ANY($1::int[])", [HOLD])
print("Held (untouched):", held)
