---
name: Job 36 — Decision Brief Report (approved 2026-04-03)
description: Final Candidates & Decision View report for Job 36 — approved format, script, and design confirmed by user
type: project
---

The "Final Candidates & Decision View" report for Job 36 (Field Coordinator, Research & Impact Studies) was approved by the user on 2026-04-03. Last pilot version was confirmed as best.

**Why:** Multiple rebuild rounds based on user feedback — final version was decision-framed, judgment-led, no scores, no TBC noise.

**Approved design:**
- Title: "Final Candidates & Decision View — [Position]"
- Candidate names: blue + underlined, hyperlinked to CV on Google Drive (opens in new tab)
- CVs uploaded to Google Drive via API, public view link injected into PDF via PyMuPDF
- Debrief schedule pulled from Google Calendar — actual dates only, no "Today/Tomorrow/This week"
- Scores removed entirely — debrief scorecard not complete, no fabricated numbers
- Sections: Where We Are (snapshot) → Debrief Schedule → Leading Candidates → Still Under Discussion → Suggested Candidates
- Suggested Candidates: based on case study + resume only, clearly labelled, no rankings imposed
- Table headers: white background, black border, blue text
- Body text: TA_JUSTIFY throughout
- Single merged PDF sent as one attachment (no individual CV attachments)

**Reference script:** `scripts/jobs/job36/send_job36_decision_brief_pilot.py`

**How to apply:** Use this exact structure and script as the template for all future position decision briefs. Replicate for Job 32, Job 35, and any future positions reaching final stage.
