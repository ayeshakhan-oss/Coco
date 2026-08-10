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

## Related
[[values_scorecard_zubair_hussain_gm_karachi_2026_08_07]] · Karachi pending case studies: Zubair (not yet sent), Zirghaam (send after mid-Aug return). SMG case studies not yet sent (Alpha dataset links still pending from Ayesha).
