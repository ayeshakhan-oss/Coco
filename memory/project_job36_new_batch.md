---
name: Job 36 — New Batch Rejection Emails (2026-04-02)
description: 19 new batch candidates screened; all rejected; 15 rejection emails generated and pilot sent
type: project
---

All 19 new batch candidates for Job 36 (Field Coordinator, Research & Impact Studies) screened and rejected. None shortlisted.

**Key gap across the board:** No operational field research coordination experience, no enumerator management, no survey firm oversight. Most are students, HR professionals, or have academic/health sector research only.

**4 excluded from emails:** LinkedIn temp accounts (app IDs: 2120, 2072, 2043, 2040) — no real email address.

**15 rejection emails generated:** Using Claude Haiku (claude-haiku-4-5-20251001), saved to `output/rejection_emails_job36_new_batch/`.

**Pilot PDF sent:** `send_job36_rejection_pilot_new_batch.py` — TO: ayesha.khan@taleemabad.com, CC: jawwad.ali@taleemabad.com. All 15 drafts compiled into one PDF.

**Status:** Awaiting Ayesha + Jawwad approval to go live.

**Why:** Full new batch from Markaz queued after initial Job 36 screening round. All candidates at CV stage, none reached values/KCD.

**How to apply:** When going live, use a separate `send_job36_rejection_live_new_batch.py` script that iterates each candidate and sends individually. Do not go live without explicit approval.

**Scripts:**
- `scripts/jobs/job36/extract_cv_text_job36_new_batch.py` — CV extraction
- `scripts/jobs/job36/generate_rejection_emails_job36_new_batch.py` — email generation
- `scripts/jobs/job36/send_job36_rejection_pilot_new_batch.py` — pilot PDF send
