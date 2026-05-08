---
name: Values Scorecard — Markaz JSON Schema
description: The exact JSON structure required for values_scorecard to render in Markaz UI — wrong schema = invisible on front-end
type: feedback
---

Always use the Markaz-compatible JSON schema when writing values scorecards to the DB. A different schema will write to the DB successfully but will be completely invisible in the Markaz UI.

**Why:** Arsalan's scorecard (Job 32, 2026-04-07) was written with a custom nested schema. The DB write succeeded and the data was there, but Ayesha could not see it on Markaz. Had to rewrite and re-run.

**How to apply:** Every time you write a values_scorecard, use this exact schema:

```json
{
  "date": "Apr 2, 2026",
  "host": "Ayesha Khan",
  "candidateName": "Syed Arsalan Ashraf",
  "noteTaker": "",
  "values": [
    {
      "name": "Don't Walk Away from Hard Things",
      "rating": "+",
      "deepDive": "...",
      "curveBall": "...",
      "microCase": ""
    }
  ],
  "finalComments": "...",
  "proceedToRightSeat": "No"
}
```

Reference script: `scripts/jobs/job36/write_job36_values_scorecards.py` — this is the canonical reference for the correct format.

## Valid Markaz statuses for values outcomes
- Values failed → `rejected`
- Values passed → `shortlisted`
- **Never use `values_failed`** — not a recognised Markaz status, scorecard will not render.
