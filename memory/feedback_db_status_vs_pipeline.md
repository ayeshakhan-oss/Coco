---
name: DB Status vs Actual Pipeline Reality
description: DB status fields in Markaz do NOT reflect communications sent. status='offer' is a pipeline stage, not a sent offer. status='rejected' may be a data entry error. Always flag, never assert.
type: feedback
---

DB `status` values are pipeline stage labels in Markaz — they do NOT confirm communications were sent.

**Why:** In Job 36 brief, status='offer' was treated as "offer extended" and written into the brief. User: "offer has not been extended to any candidate, how can you say it has been extended? coco, you're fabricating." Also, Moiz Khan and Maria Karim showed status='rejected' in DB but user confirmed both are active candidates.

**How to apply:**
- `status='offer'` → label as "PANEL DECISION" — a stage flag, not a sent offer
- `status='rejected'` → NEVER assert rejection. Flag it: "DB shows rejected — verify with hiring manager"
- `status='applied'` → may mask an active candidate (e.g. Rosheen Naeem cleared values + submitted case study but DB still showed 'applied')
- Never write "offer extended", "offer sent", "offer out" unless Ayesha explicitly confirms it
- Never write "rejected" unless Ayesha confirms the decision
- Verdict label for post-debrief, pre-decision candidates: **"PANEL DECISION"** (not OFFER STAGE, not REJECTED)
- Always flag DB anomalies explicitly — do not silently reconcile or assume
