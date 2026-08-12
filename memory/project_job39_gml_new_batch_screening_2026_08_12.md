---
name: Job 39 — GM-Lahore New-Batch Screening (2026-08-12)
description: All 36 'new' apps (8 Jul-9 Aug arrivals) screened strictly vs JD + PKR 210-270k band on Ayesha's instruction. ZERO shortlisted, all 36 rejected directly on Markaz (no pilot report requested, no emails). Closest misses all over band - Faryal Najeeb 475k, Shehreen Umair 350k, Hania Khan 300k (active on Job 42).
type: project
---

# Job 39 (Growth Manager – Lahore) — New-Batch Screening, 2026-08-12

**Instruction (Ayesha, verbatim intent):** check for new applicants only, be VERY strict against the JD and the salary bracket; worth interviewing → shortlist, else → reject directly on Markaz. No pilot report requested.

**Scope:** 36 apps in status `new` (applied 8 Jul–9 Aug, all post-dating the early-July screening that produced the original 13 shortlisted / 80 rejected). 32 CVs read fully; 2 recovered and read via retry (3712 OCR — PDF was image-based; 3791 docx via PyMuPDF); 3 LinkedIn no-CV stubs. JD pillars (same as GM-Karachi): storytelling for govt/institutional audiences, high-level convenings, partnerships→deal closure, pipeline discipline. Band **PKR 210–270k** (jobs.min_budget/max_budget), Lahore + ~50% travel.

## Verdict: 0 shortlisted / 36 rejected
Honest pool verdict: two-thirds generic sales / digital-marketing / PM / teaching profiles. The only real JD-fits ask far over band — the Karachi pattern repeating. **Nobody clears JD + band together.**

Closest misses (all over band, flagged to Ayesha):
- **Faryal Najeeb (4120)** — strongest JD match in the batch: 12y U.S. Consulate/PACC public engagement, 50+ institutional partnerships incl. Govt of Sindh MoUs, convenings w/ State Dept leadership, $3-4M grant portfolios; Karachi, open to Lahore relocation. Asks 475k (current 350k). Axact 2012-15 on CV (known flag pattern).
- **Shehreen Umair (3731)** — LUMS, 5y PET climate BD: closed advisory contracts, scaled REC programme to 1GW+, donor proposals ($200k grant, CAD 50k won), Amsterdam conference rep. Lahore. Asks 350k (current 300k).
- **Hania Khan (4037)** — Fulbright MDP, education/development partnerships, B2G. Asks 300k. **Already shortlisted on Job 42 SMG (app 4035)** — her live pipeline is there, untouched.

Cross-job duplicates rejected on 39 but active elsewhere: Zirghaam Ahmad 3831 (Job 41 shortlisted, case study sent) and Hania Khan 4037 (Job 42). Shahzeb Sohail 4115 also rejected on Job 41 (4114) same day. Stub 3733 "meena" likely = Tasmina Khan 3732 (LinkedIn slug "meenakhan"). CV-mismatch flag: 3872 "Jawwad Ali Syed Rizvi" uploaded someone else's CV (a "Raheela", teacher, different email) with junk answers ("YEs") — unassessable.

## Execution
- Extractor: `scripts/jobs/job39/extract_cv_text_job39_new_batch.py` → `output/cv_texts_job39_new_batch/` (+ `3712_retry.txt`, `3791_retry.txt`).
- Status update: `scripts/jobs/job39/job39_status_update_2026_08_12.py` — Rule-13 whitelist from frozen `_summary.json`, per-row job/status guards, unscreened-arrival guard, row-count assert 36/36 ✓. Stubs rejected per Job-42 precedent (NOTE: Job 41's 15 stubs still held `new`, Ayesha's call pending).
- Final counts: 116 rejected / 12 shortlisted / 2 case_study_sent / 0 new. (Shortlisted went 13→12 with case_study_sent 1→2 during the session — an external Markaz action by the team, not this sweep; my UPDATE returned exactly the 36 whitelisted IDs.)
- **NO rejection emails sent** — status-only, same as Jobs 41/42.

## Related
[[project_job41_gmk_screening_2026_08_10]] (band + honest-verdict pattern) · [[candor_weak_pool_verdict_2026_07_21]]
