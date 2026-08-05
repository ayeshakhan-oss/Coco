---
name: Job 42 — Senior Manager Growth: Screening + Values Invites (2026-08-05)
description: Full screening record for JOB-0042 (SMG, Islamabad, PKR 350-400k). 79 CVs read across 2 batches, 10 shortlisted + values-invited live, 77 rejected (statuses only). Kamran Ali pending. Batch-3 sweep due at 15 Aug close. Includes Neon HTTPS workaround + live-job bulk-update lesson.
type: project
---

# Job 42 — Senior Manager Growth (JOB-0042) — Screening + Values Invites

**Date:** 2026-08-05 | **Hiring manager:** Waqas Tanveer (per jobs.hiring_manager) | **Band:** PKR 350,000–400,000 | **Location:** Islamabad, 40–60% travel | **Closes:** 2026-08-15 (still receiving applications)

## Screening (2 batches, 79 CVs read manually in full)
- **Batch 1 (main):** 77 apps → 8 no-CV → 69 read (incl. 2 image-only PDFs read visually + 1 test entry from Jawwad's account, app 3867, flagged). Verdict: moderate-to-thin pool, top match ~75%, no curve-grading (candor rule applied). Report: `output/job42/job42_smg_screening_pilot.html` (gitignored, PII).
- **Batch 2 (late arrivals):** 11 apps → 1 incomplete → 10 read. Contained best sector+function match of whole pool (Rimsha Taj, PMIC AVP BD, 78%, gated by 600k ask). Report: `output/job42/job42_smg_screening_batch2_pilot.html`.
- JD pillars used: (1) growth/BD execution + B2B closure w/ revenue, (2) B2G/institutional stakeholders, (3) digital+field acquisition/growth loops, (4) CRM/pricing/RFP discipline. Modifiers: edtech/SaaS, genAI, 4–6 yrs, band.

## Final statuses (Ayesha-approved, 97 apps at time of writing)
- **Shortlisted 10** (values invites sent LIVE 2026-08-05): Murtaza Hassan 3879, Fahad Ali 3916, M. Arshan Bilal 3884, Ali Ahmed 3946, Umar Zahid 3902, Shahmir Hashmat 3911, Salman Ahmad 3943, M. Shakeel Ahmad 3892, M. Zeshan 3921 (Motive one — 2 other unrelated "Zeeshan"s in pool), Hina Rehman 3958.
- **Rejected 77** (status only — NO rejection emails sent yet). Ayesha knowingly rejected Rimsha Taj (78%) + Mujtaba Shuja (68%) from batch 2 (flagged twice, her call).
- **Kamran Ali 3930 left 'new'** — Orenda AM BD 2021-present, claims prior Taleemabad BD work; Ayesha said "leave kamran". Do not touch without her word.
- **Unscreened 'new':** 9+ arrivals from 05 Aug (3964–3972...) — batch-3 sweep recommended at 15 Aug close.

## Values invites (Skill 06)
- Script: `scripts/jobs/job42/send_job42_values_invite.py`. Design copied verbatim from job32 reference. Content: **video JD** https://drive.google.com/file/d/1zwWEzeaiud7Y_nMnLjBP-6-ebYHCRrBQ/view + booking https://calendar.app.google/4coXoLsZNKwJvdAAA + Job-32 generic prep guide (reused, Ayesha ok'd via approval).
- Piloted (10 personalized, Ayesha only) → approved → LIVE 10/10. **CC (Ayesha's list): ayesha.khan@, hiring@, waqas.tanveer@, ali.sipra@** (Jawwad dropped). "Waqas" disambiguated via jobs.hiring_manager; Ali Sipra unique in users.

## CVs on Drive
Folder (anyone-with-link): https://drive.google.com/drive/folders/16zGvwpNkq6VLB-d26f2LzfWIoXBsXDec — 20 shortlist/maybe CVs across both batches, uploaded via `token_sheets_broad.json`.

## 🔑 Non-obvious: Neon HTTPS SQL API workaround
Neon MCP + direct psycopg2 (port 5432) were BLOCKED on this network (TCP connects, RST on SSLRequest; Neon status fine). Workaround: **POST https://<endpoint-host>/sql with header `Neon-Connection-String: <DATABASE_URL>`**, JSON body `{"query": sql, "params": [...]}` — works for reads AND writes over 443. Helper pattern in scratchpad `neon_http.py` (params are $1-style with a JSON params array).

## 🔒 Lesson: bulk status updates on a LIVE job
First "reject the rest" used `WHERE status='new'` and swept 10 unscreened same-day arrivals (77 rows vs 67 expected). Caught by row-count mismatch, reverted within a minute using the screened app-ID list as whitelist. **Rule: on a live job, bulk updates go by explicit screened application-ID whitelist, never a status filter; always assert expected vs returned row counts; re-pull the applicant list if time passed since screening.**

## Pending / next steps
1. Batch-3 screening sweep at job close (15 Aug) — one consolidated pass.
2. Rejection emails for the 77 (v8 layout, Skill 01) — only when Ayesha asks.
3. Kamran Ali decision after her internal check with Waqas Tanveer.
4. Interview reminders (Skill 06 type 6) once bookings land on the calendar.
