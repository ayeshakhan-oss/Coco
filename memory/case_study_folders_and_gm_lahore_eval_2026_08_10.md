---
name: Case-Study Drive Folders (KHI + SMG) & GM-Lahore Case Study Evaluation (2026-08-10)
description: Built Drive submission folders for GM-Karachi + Senior Manager Growth mirroring Noah's GM-Lahore structure; reconciled Muneeb/Waqas submissions; full case-study evaluation of the 4 GM-Lahore submitters (scores, verdicts, flags) — pilot report sent to Ayesha; Markaz score-fill pending approval.
type: project
---

# 2026-08-10 — Case-Study Folders + GM-Lahore Evaluation

## 1. Drive submission folders (mirror of Noah's structure)
Convention per candidate folder: `CV - [Name] [Role].pdf` + `Case Study - [Name] - [original filename]` per file + `Case Study - [Name] - Submission Links.txt` for link submissions.
- **Growth Manager - Lahore (Noah's, pre-existing):** https://drive.google.com/drive/folders/1ohbfTtzfUBWry8sJmoC_oc7oxz0NnUyt
- **Growth Manager - Karachi (built today):** https://drive.google.com/drive/folders/1xHkwebowKnb2GnQsFFe5HqbKeAYxbeGD — subfolders: Muneeb Arif (Submission Links.txt → his Drive folder, submitted via Markaz Aug 9 20:16 PKT; CV added today from Ayesha's file, also stored into Markaz candidate 3129), Waqas Hassan (3 emailed submission files archived: Taleemabad Case Study.docx, Assignment 1.pptx, Assignment 3.xlsx; Markaz app 3870 marked submitted @ Aug 7 14:46; ⚠️ CV still missing anywhere), Zirghaam Ahmad (CV), Zubair Hussain (CV).
- **Senior Manager Growth (built today):** https://drive.google.com/drive/folders/1mkrVspKtD1QLFK277dmPPirCP_lHglJA — subfolders: Jam Zeshan Nawaz (CV), Muhammad Arshan Bilal (CV).
- Build path: Drive API via `.claude/config/token_sheets_broad.json`; both top folders link-shareable (viewer).

## 2. GM-Lahore case study evaluation (4 submissions, brief: "The Story, the Room, and the Deal" + A4 extension/renewal)
All submissions read in full (PDFs, all spreadsheet tabs, both link-folders resolved). Scores /10 per assignment (A1-A4), judged against the brief + A4 evaluator guide — no cross-candidate comparisons in the write-ups.

| Candidate | App | A1/A2/A3/A4 | Verdict | Key flags |
|---|---|---|---|---|
| Muhammad Waqas | 3651 | 6.5/9/8/8.5 | STRONG, 1 gap | **Reflective MISSING** (only incomplete in batch); heaviest disclosed AI collab — test live ownership |
| Abdul Wahab | 3614 | 9/8/8.5/8 | STRONG | Reflective = voice note mp4 — needs human listen; "lead with lowest number" vs pitch-high-buffer |
| Ahmad Wajahat | 3635 | 7.5/7/7.5/6.5 | SOLID | A4 re-routes approval chain + skips host institute in day-1 roadmap; 7-8 hrs spent (honest, 3x time-box); reflective missing "what differently" |
| Salman Tariq | 3656 | 8.5/9/9/9.5 | STRONG PLUS | Only one hitting all 5 A4 evaluator-guide criteria (incl. 285/263/245 negotiation ladder); identified NIETE as analogue; verify his research figures (0.28 SD, 522 obs, 261 schools); consultancy-grade polish — test live |

Highlights: Wahab best A1 vs the skeptical-Secretary ask; M. Waqas best convening (A2) w/ real current names; Ahmad only one citing published impact numbers w/ footnotes + Adhoc-Relief-allowance costing literacy; Salman benchmark A4.

**Report:** locked report format (navy header, 4 stat boxes, candidate blocks) piloted to Ayesha — script `scripts/send_gm_lahore_case_study_eval_pilot.py`. Live recipients TBD.
**Pending Ayesha:** live send + recipients; fill `case_study_score`/`case_study_notes` on Markaz for the four; M. Waqas's missing reflective; listen to Wahab's voice note; verify Ahmad/Salman's quoted impact figures.

## 3. SMG profile folders + submission archiving (later same day)
- **All shortlisted/invited SMG candidates now have Drive subfolders with CVs from Markaz** — 16 total (14 built in this pass + Zeshan/Arshan earlier; Jawwad test entry excluded). **Ayesha decided (2026-08-10): KEEP ALL 16** — folders stay for the full shortlist; case-study files drop in per candidate as submissions arrive.
- **Arshan Bilal (app 3884)** submitted via Markaz Aug 7: files live behind the Markaz staff-login API (`/api/case-study-file/3884/word|excel` — automation gets 401; any logged-in staff can download). His folder holds Submission Note (verbatim summary) + Submission Links; real copies pending a staff download.
- **Junaid Ali (app 3992)** submitted via Markaz Aug 9 — same treatment (note + links; staff download pending).
- **Arooj Khalid (app 3868)** submitted BY EMAIL Aug 10 19:17 (links: Google Doc + Drive folder). **Fully archived** — main PDF, Reflection & AI Note, Assignments 1a/1b/2a/2b/3 (exported from her Google-native files incl. subfolders) + Submission Links.txt; Markaz marked submitted with corrected note.
- **⚠️ Lesson (2026-08-10):** first pass archived a 19KB attachment named "noname" that was actually the Taleemabad logo (image/png without .png filename). Rule: filter email attachments by MIME type, not filename; and when a submission email has no real attachments, read the BODY for links before archiving anything.

## Related
[[values_scorecard_zubair_hussain_gm_karachi_2026_08_07]] · **Correction (verified in Markaz comm history, 2026-08-10):** case-study invites WERE sent — Zubair Aug 7, Zirghaam Aug 7 (note: Zirghaam received the *Senior Manager Growth* template, not the GM one), Syeda Masooma Aug 10, and all SMG invites Aug 6–7 (Arooj, Zeshan, Junaid, M. Bilal 4051, Yusra 4061). Outstanding submissions as of end of 2026-08-10: Hafiz Osama (GM-LHR, sent Aug 4); Zubair, Zirghaam, Syeda Masooma (GM-KHI); Muhammad Zeshan, Muhammad Bilal, Yusra Amjad (SMG). Submitted: GM-LHR ×4, Muneeb + Waqas Hassan (KHI), Arshan Bilal Aug 7 + Junaid Ali Aug 9 + **Arooj Aug 10 19:17 by email — hours after her nudge went LIVE** (SMG; see §3 + [[case_study_nudge_type_2026_08_10]]).
