---
name: case-studies-smg-gm-from-hog-2026-07-31
description: SMG + Growth Manager case studies derived from the HOG "Growth Flywheel Stress Test" — calibration logic, Google Doc links, HOG-matching layout spec, and the DOCX→Google Doc generator pattern.
type: project
---

# Case Studies — SMG + Growth Manager, derived from HOG (2026-07-31)

Ayesha shared the **Head of Growth "Growth Flywheel Stress Test"** case study + the SMG and Growth Manager (Lahore) JDs, and asked Coco to derive one case study per role. Both delivered as Google Docs matching the HOG document's layout.

## The two case studies

| Role | Case study | Google Doc |
|---|---|---|
| Senior Manager Growth (SMG) | **The Execution Sprint** (2.5–3h) | https://docs.google.com/document/d/1Ygsscl6nIjuCr2kbdosQuhwWMNjamox4cDohcZgw014/edit |
| Growth Manager (Lahore) | **The Story, the Room, and the Deal** (2–2.5h) | https://docs.google.com/document/d/1FKIKc7T1rCqr5jbi3SEdJLDxzBGyNVWHSJE-t8UF1Bk/edit |

**Repo sources:** [docs/case_studies/smg_case_study_execution_sprint.md](../docs/case_studies/smg_case_study_execution_sprint.md) · [docs/case_studies/gm_case_study_story_room_deal.md](../docs/case_studies/gm_case_study_story_room_deal.md) · generator: [scripts/case_studies/make_growth_case_study_docs.py](../scripts/case_studies/make_growth_case_study_docs.py)

## Calibration logic (reusable when deriving case studies from a senior role's case)

- **Scale time down with seniority:** HOG 3–4h → SMG 2.5–3h → GM 2–2.5h.
- **Test the JD's verbs, not the senior role's.** SMG JD says *execute* loops designed by leadership → the loop is GIVEN in the case; candidate builds the 60-day run plan (K-factor 0.2 from the JD). HOG designs the loop; SMG spins it.
- **SMG assignments:** (1) channel/cohort analysis on the SAME Alpha Platform dataset but scoped to 4 of 8 CSVs + pick-two-areas + 3 experiments with kill criteria (Product–Channel/Channel–Model fit at execution level); (2) growth-loop execution plan; (3) stalled B2G deal scenario (DEO silent, budget cycle closing) — candidate writes the actual stakeholder email + honest internal update.
- **GM assignments mirror its JD's three muscles:** storytelling (policy-facing one-pager + 5-slide narrative arc for a sceptical Secretary), convening design (thought-leadership study launch, NOT marketing event — JD's own words), partnership pipeline (5 real partners + tracker + one deal end-to-end).
- **Ground-rules block added to both:** honest time-boxing, AI-tool use allowed WITH disclosure (mirrors SMG JD's AI Adoption responsibility), no fabricated data / label assumptions.
- **Reflective 200-word ask** mirrors each JD ("flagged a failing strategy early" for SMG; "a room you led" for GM).

## ⚠️ Open item

SMG Assignment 1's "Data Access: Here / Dataset Description: Here" lines are **NOT hyperlinked** — Ayesha must attach the same Alpha Platform dataset links from the HOG doc (Coco only had the PDF text, never fabricate these links).

## Layout spec (HOG-matching Google Doc pattern — reuse for future case studies)

Generator builds DOCX with python-docx, then uploads via Drive API with `mimeType=application/vnd.google-apps.document` (auto-converts) using the broad Drive token at `.claude/config/token_sheets_broad.json` (see [[google-api-tokens-location-scopes-2026-07-06]]).

- Per-page header: centered `assets/logo_taleemabad.png` at 1.15".
- Centered bold black title ("Role @ Taleemabad", 17pt) + centered bold **blue #3C78D8** "Case Study: …" subtitle (15pt).
- Bold meta block: Role / Time Recommended / Submission Format.
- Section headings 15pt bold black; assignment headings 12.5pt bold blue; "Your Analysis Must Address:" bold underlined.
- Body 11pt **Quicksand**, justified; bold inline labels on bullets; italic equal-opportunity footer ("We hire for grit, learning velocity, and outcomes.").

Docs uploaded to the connected account's My Drive, NOT publicly shared.

Related: [[case-study-project-extension-renewal-2026-07-31]] (same-day curated Growth/Govt-Partnerships case-study question).
