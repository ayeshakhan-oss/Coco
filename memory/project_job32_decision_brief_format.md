---
name: Job 32 Decision Brief — Final Email Format
description: CRITICAL — exact format for all hiring decision briefs. Dark navy header, 4 stat boxes, Where We Are narrative, Debrief Schedule, Leading Candidates with signal+probe blocks, Discussion, Also in Pipeline. Inline HTML, no PDF. cv_link() on all names.
type: feedback
---

Decision briefs use a specific format — never simplified pipeline tables, never plain PDF.

**Why:** User corrected this explicitly in April 2026 after receiving table-only briefs for Job 35 and Job 36. Said: "why are you spiraling? this is how we used to do it but you are doing totally opposite." The correct format is judgment-led — narrative, probes, signals per candidate — not just a status table.

**How to apply:**
- HTML email body (inline), no PDF attachment
- Dark navy header (#1a2a3a) with "Final Candidates & Decision View" title + position subtitle
- 4 stat boxes at top (pastel backgrounds): e.g. Values invites · Calls completed · Cleared/Offers · Debriefs this week
- "Where We Are" — free prose paragraph, current pipeline state
- "Debrief Schedule" — table with candidate name (hyperlinked), date, status, notes; colour-coded rows
- "Leading Candidates" — one block per candidate: name (cv_link), verdict badge, debrief date/status, italic tagline, signal paragraph, "At debrief, probe:" in dark red (#7b341e)
- "Discussion Candidates" — same block format for candidates needing decisions or with open flags
- "Also in Pipeline" — two-column table: name (cv_link) | status text
- Optional free-text "Note" section at bottom for context not fitting elsewhere
- All candidate names in every section use cv_link() — upload all CVs to Google Drive first
- **Audit every section before sending:** Leading, Discussion, Pipeline, Debrief Schedule — all names must have Drive links. See feedback_decision_brief_hyperlinks.md.
- **Verdict labels (confirmed 2026-04-08):** post-debrief pre-decision = "PANEL DECISION" (never "OFFER STAGE", never "OFFER OUT"). Values pass = "VALUES PASS". Debrief today = "DEBRIEF TODAY". Debrief confirmed = "DEBRIEF CONFIRMED". Case study submitted = "CASE STUDY IN". Case study sent = "CASE STUDY SENT". Overdue = "OVERDUE". Not interviewed = "NOT INTERVIEWED".
- **5 stat boxes (confirmed 2026-04-08):** Total applied · Panel decisions pending (or Values cleared count) · Values cleared · Debriefs this week · Values failed — OUT. Adjust labels to fit the pipeline stage.
- **Combined multi-position brief:** wrap each position in its own navy-header block ("Position 1", "Position 2"), with shared intro paragraph. Reference: scripts/jobs/combined/send_combined_impact_reply_pilot.py
- Reference scripts: send_job32_decision_brief_pilot.py · send_job35_decision_brief_v2.py · send_job36_decision_brief_v3.py · send_combined_impact_reply_pilot.py
