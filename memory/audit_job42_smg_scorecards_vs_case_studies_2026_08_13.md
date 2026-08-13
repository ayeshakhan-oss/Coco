---
name: Audit — Job 42 SMG values scorecards vs case studies (2026-08-13)
description: Triple-source audit (Markaz + email_audit.log + Ayesha's IMAP booking mail) of Job-42 Senior Manager Growth. 6 values-passers, ALL 6 have case studies sent. 7 interviewed/advanced candidates have NO usable values scorecard (3 confirmed interviews unscored, 4 blank Markaz UI shells). Fahad Ali values-OUT but still 'shortlisted'. Furqan + Irfan interview 14 Aug with no Markaz record.
type: project
---

# Audit — Job 42 SMG: scorecards vs case studies (2026-08-13)

**Sources used (all three):** Markaz `applications` (values_scorecard, case_study_status, communication_history), local `logs/email_audit.log` (values invites we sent), read-only IMAP into ayesha.khan@ ("Appointment booked: Zero In Call For Senior Growth Manager (...)" mails). Per [[comm_evidence_dual_source_rule_2026_06_20]].

## Values PASS with a real scorecard = 6 — case study sent to ALL 6 ✅
| Candidate | App | Score | CS sent | CS submitted |
|---|---|---|---|---|
| Arooj Khalid | 3868 | 6+ | 6 Aug | ✅ |
| Muhammad Arshan Bilal | 3884 | 4+ | 7 Aug | ✅ |
| Muhammad Zeshan (Jam Zeshan Nawaz) | 3921 | 4+ | 7 Aug | ❌ **6 days — nudge candidate** |
| Umar Zahid | 3902 | 5+ | 13 Aug | ❌ (just sent) |
| Rimsha Taj | 3956 | 6+ | 13 Aug | ❌ (just sent) |
| Syed Basit Hussain | 4142 | 5+ | 13 Aug | ❌ (just sent) |

Values FAIL = 2: Salman Ahmad (3943, OUT, status rejected ✅) · Fahad Ali (3916, OUT — 5+ but one **−** on Don't Hold On Too Tight; host Jawwad Ali, scored by Noah) → **status still `shortlisted`, never rejected — INCONSISTENCY to fix.**

## 🔴 MISSED SCORECARDS — no usable values scorecard
**A. Booked calls with no scorecard — RESOLVED 2026-08-13 by mailbox check (Ayesha asked "check my email for any record of hina and ali ahmed"):**
1. **Shahmir Hashmat** (3911) — booked + held Thu 13 Aug 12pm; **case study already sent same day** (so effectively passed) — **genuinely unscored**.
2. **Ali Ahmed** (3946) — ❌ **NOT a missed scorecard.** He **cancelled himself**: "Appointment canceled: Zero In Call For Senior Growth Manager (Ali Ahmed) @ Tue Aug 11, 2026 12pm-1pm" sent FROM aliahmed209@gmail.com on Tue 11 Aug 06:17 UTC (11:17am PKT, 43 min before the slot). Never rebooked. No interview happened → nothing to score. **Needs rebooking or closing out.**
3. **Hina Rehman** (3958) — ❌ **NOT a missed scorecard. NO-SHOW, confirmed by Ayesha 2026-08-13 ("hina didn't join the call").** Her booking (Wed 12 Aug 11am-12pm) was never cancelled and she never emailed back — she simply did not join. The email trail matched this: no candidate-named Fathom recap for hinarehman1794@gmail.com, unlike every candidate who was actually interviewed ("Recap of your meeting with zedef@hotmail.com / hudashaikh8080@ / yashfeen_zahid02@ / syed.basit89@ / merzia.hasnain99@"). Jawwad's 11:10am PKT invite re-send (adding notetaker rumi@hellorumi.ai) was the panel waiting for a candidate who never arrived. **Decision needed from Ayesha: re-invite or close out; status still `shortlisted`.**

**→ NET RESULT: only ONE confirmed unscored interview (Shahmir Hashmat) + the 4 blank shells. Ali Ahmed (cancelled) and Hina Rehman (no-show) were never interviewed — nothing was missed for either.**

**⚠️ METHOD LESSON:** a calendar booking alone does NOT prove an interview happened — always check for cancellations. Gmail IMAP `SUBJECT "cancel"` returns **0 hits** for subjects containing "canceled" (no stem matching): search **`"canceled"` AND `"cancelled"` exactly**.

**B. Blank Markaz UI scorecard shells** (dated "Aug 7, 2026", host "Ayesha Raza Khan", noteTaker empty, all 6 values present but rating/deepDive/curveBall/microCase ALL empty, finalComments empty, yet `proceedToRightSeat: "Yes"`; `values_interview_result` NULL). No booking mail found for them 25 Jun–13 Aug, so their calls were not booked through Ayesha's scheduler:
4. **Jawwad Ali Syed Rizvi** (3867) — CS sent 6 Aug + 7 Aug; status `case_study_sent`.
5. **Junaid Ali** (3992) — CS sent 7 Aug, **submitted**.
6. **Muhammad Bilal** (4051) — CS sent 7 Aug.
7. **Yusra Amjad** (4061) — CS sent 7 Aug, **submitted**.

→ 5 of these 7 (Shahmir, Rizvi, Junaid, M. Bilal, Yusra Amjad) already hold case studies without a completed values scorecard. Coco can score any of them from transcripts if Ayesha supplies the Fathom links.

## Upcoming SMG interviews (booked, from IMAP)
14 Aug: Furqan Afzal 11am, Irfan Siddiqui 12pm · 17 Aug: Ahmad Taj 11am, Shafaq Syed 12pm · 18 Aug: Kanooz Siddiqui 11am, Lamis Maniar 12pm · 19 Aug: Hania Khan 11am, Veniza (Vaneeza) Baig 12pm · 20 Aug: Ali Wajdan Khan 12pm.

**🔴 URGENT:** **Furqan Afzal** and **Irfan Siddiqui** interview **tomorrow 14 Aug** and still have **no Markaz records** (2 of the 4 remaining Markaz-missing invitees) — no application to attach a scorecard to.

## Invited but never booked (no booking mail on record)
Murtaza Hassan + Muhammad Shakeel Ahmad (invited 5 Aug, 8 days) · Yusra Wahid + Imran Mehmood Choudhry (invited 7 Aug; also Markaz-missing) · Khushal Khan + Sara Obaid Ul Islam (invited 12 Aug, still recent).
**Booked but no interview (both still `shortlisted` — decision needed: re-invite or close out):** Ali Ahmed (self-cancelled 43 min before his 11 Aug slot, never rebooked) · Hina Rehman (**no-show** for her 12 Aug slot, confirmed by Ayesha; never cancelled, never wrote in).

## Related
[[markaz_live_job_bulk_update_whitelist_2026_08_05]] · [[reference_ayesha_mailbox_imap_2026_08_10]] · repo memory/project_job42_smg_screening_2026_08_05.md · [[values_scorecard_syed_basit_smg_2026_08_13]] · case-study nudge type: repo memory/case_study_nudge_type_2026_08_10.md
