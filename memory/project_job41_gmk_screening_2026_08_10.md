---
name: Job 41 — GM-Karachi New-Batch Screening (2026-08-10)
description: 84 'new' apps screened (69 CVs read fully, 15 LinkedIn stubs no CV). 8 shortlist / 7 maybe / 54 no-hire. Honest verdict — strong partnership profiles exist but ask 350–800k vs 210–270k band; only in-band true fits Zubair Ali + Khizran. Pilot sent to Ayesha; NO Markaz statuses changed yet.
type: project
---

# Job 41 (Growth Manager – Karachi) — New-Batch Screening, 2026-08-10

**Scope:** All 84 applications in status `new` as of 10 Aug (separate from the 9 earlier shortlisted). 15 were LinkedIn-import stubs with no CV (13 unique people — bisma batool x3 stubs: apps 4056/4057/4085; Sumaima Alvi's stub 4088 superseded by her real app 4089). **69 CVs read manually and in full** against the JD's four pillars (storytelling for govt/institutional audiences, high-level convenings, partnerships→deal closure, pipeline discipline), band PKR 210–270k, Karachi + ~50% travel as modifiers.

**Result:** 8 shortlisted · 7 maybe · 54 no-hire. Stat check: 8+7+54=69; 69+15=84.

## Honest pool verdict
Two-thirds of the pool is generic sales/digital-marketing/SEO — no-hires. The strong cluster is real (resource mobilization / policy partnerships) but asks 350–800k vs the 270k ceiling. Only two in-band true fits; Amsal Malik is the standout junior bet at 225k. Options for Ayesha: stretch band for a top-4, hire in-band with a caveat, or source proactively like SMG.

## Shortlist (8)
1. **Kanooz Ahmed Siddiqui** (app 3811) 78% — Mgr Fundraising NOWPDP, $700k+/yr institutional revenue, UN Zero Project, AKU-IED research. Karachi. ⚠️ asks 500k.
2. **Rida Fatima** (4083) 76% — GIZ Technical Advisor (EU Talent Partnerships, BMZ/EU/GoP dialogue), ex-CERP ($2M raised, 40 proposals 55% win, presented to SBP Governor), **worked with Taleemabad on FCDO TIP Balochistan**. ⚠️ Lahore-based (maybe route to GM-Lahore Job 39), asks 450k, avail 1 Oct.
3. **Amnah Ejaz Khan** (4121) 75% — Kialo Sr Mgr Growth & Partnerships (IB, Singapore MoE, 40+ institutions, B2G). ⚠️ asks 800k (current 900k), Islamabad, avail 1 Nov.
4. **Lamis Maniar** (4063) 72% — Habib Univ President's Office fundraising, Legal Aid Society ($150k UNDF), Impetus/Sindh Health. ⚠️ asks 550k; CV says London vs application address Karachi — verify location.
5. **Faheem Vohra** (4132) 70% — GM Outreach & Growth Hikmah Institute + Learning Minds (closed bank training partnerships, convenings). Karachi. ⚠️ asks 450k; CV mirrors JD phrasing — probe with concrete examples.
6. **Rahima Tahir** (4075) 66% — Mgr Linkages & Outreach Ziauddin Univ (ACU grants, SVRI $116k Co-PI, international partnerships). Karachi. ⚠️ asks 350k (current 250k — negotiable gap).
7. **Syed Zubair Ali** (4113) 65% — IN BAND 250k. 11y executive convenings (Qorus, The Leaders Roundtables C-suite platform, USD 85k sponsorships), HTA BD. Karachi. ⚠️ zero education/B2G sector exposure.
8. **Khizran Zehra Baloch** (4065) 63% — IN BAND 200–230k. BD Mgr Intellexal (PKR 95M+ MRR portfolio) + KDSP resource mobilization. Karachi. ⚠️ ~3 yrs, lightest CV on the list.

## Maybe (7)
Amsal Malik (3832, 58%, junior star 225k) · Nabiha Nadeem (4128, 55%, Fulbright/Teach For Pakistan) · Ali Aftab Ghias (4092, 54%, Impetus data-storytelling, asks 350k) · Anum Khalil (4072, 52%, NGO Program Director) · Zaheer Ahmed (4097, 50%, SBCC 15y, Sukkur, 350k) · Syeda Noorulain Fatima (4087, 48%, PPAF) · Shomaila Shamim (4073, 45%, SEDF gender desk).

## Flags recorded in report
Moiz Ahmed (4070) lists Axact + ABTACH (same pattern as Job 42); Faheem Vohra + Ahsan Samejo (4076) CVs conspicuously reuse JD phrasing; 15 stubs unscreenable.

## Artifacts
- Report (locked Job-42 format): `output/job41/job41_gmk_screening_pilot.html` — **PILOT sent to Ayesha only 2026-08-10** (`scripts/jobs/job41/send_job41_screening_pilot.py`). Awaiting approval.
- CV texts + per-candidate verdicts: `output/cv_texts_job41_new_batch/` (incl. `_screening_notes.md`); extractor `scripts/jobs/job41/extract_cv_text_job41_new_batch.py` (Neon HTTPS SQL API).
- Drive CV folder (15 shortlist+maybe CVs, anyone-with-link): https://drive.google.com/drive/folders/1xbiqpkci-F8c8h6JrOxzapxdOV_VbsTV — links in `output/job41/cv_drive_links.json`; uploader `scripts/jobs/job41/upload_job41_screening_cvs.py`.

## Ayesha's verdict + Markaz update (2026-08-12) ✅ DONE
- **Shortlisted (2, both in-band):** Khizran Zehra Baloch (4065) + Syed Zubair Ali (4113).
- **Rejected (67):** all other screened new-batch apps — the 6 over-band shortlist recs (incl. Kanooz, Rida Fatima, Amnah, Lamis, Faheem, Rahima), 7 maybes (Amsal Malik explicitly: too young/fresh for this position), 54 no-hires. **NO rejection emails sent** — status updates only.
- **Held (15):** LinkedIn no-CV stubs remain `new` (excluded per pilot-report plan; Ayesha may clear separately).
- Executed via `scripts/jobs/job41/job41_status_update_2026_08_12.py` (Neon HTTPS SQL, Rule-13 whitelist derived from frozen `_summary.json`, per-row status guards, unscreened-arrival guard, row-count asserts 2/67 ✓). Final counts: 129 rejected / 15 new (stubs) / 10 shortlisted / 1 case_study_sent / 1 consider_other_roles.
- Rida Fatima (4083) rejected on Job 41 as instructed — the GM-Lahore (Job 39) routing option was NOT exercised; flag to Ayesha if Job 39 needs her.

## Values invites — batch 3 LIVE (2026-08-12)
- Khizran (4065) + Syed Zubair Ali (4113) sent live values invites after pilot approval — `scripts/send_values_invite_gm_karachi_batch3_pilot.py` (exact batch-2 template/links; CC waqas.tanveer, ayesha.khan, hiring@, ali.sipra).
- Invite-coverage audit of all 10 shortlisted (Markaz comm history + read-only IMAP on Ayesha's mailbox): no missed invites in batches 1–2.

## Pending
- Rejection emails for the 67, if Ayesha wants them (Job-42 precedent: none sent).
- Decision on the 15 stubs (reject vs leave).
- **Marzia Hasnain (3819):** values invite 3 Aug + call booked 4 Aug, but NO scorecard/result in Markaz (Waqas + Zeshan declined the calendar invite) — confirm with Ayesha whether the interview happened.
- **Huzaifa Wakil (3825):** values FAIL 7 Aug but still status `shortlisted`, no feedback email — awaiting Ayesha's instruction.

## Related
[[values_scorecard_huda_shaikh_gm_karachi_2026_08_10]] (same-day PASS, pre-batch shortlist) · [[project_job42_smg_screening_2026_08_05]] (format + method reference).
