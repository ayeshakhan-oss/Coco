---
name: Decision Brief — CV Hyperlink Completeness
description: Every candidate name in EVERY section of a decision brief must have a Drive CV link. Missing any = incomplete brief.
type: feedback
---

Every candidate name in a decision brief must be hyperlinked to their CV on Google Drive — no exceptions.

**Why:** First combined brief pilot was sent with missing hyperlinks for leading candidates (Rahima Omar, Dur E Nayab, Mahnoor Hasan, Hassan Zafar) and pipeline/failed candidates (Rabia Zafar, Zeeshan Ali, Muhammad Junaid) because they were not in the initial drive_links dict. User said "you haven't mentioned a few links/hyperlinks, you're prolonging my task."

**How to apply:**
- Before sending any brief, audit EVERY section: Leading, Discussion, Pipeline/Also in Pipeline, Debrief Schedule
- Build a complete list of ALL names that appear anywhere in the email
- Cross-check every name against drive_links — if missing, fetch CV from DB and upload to Drive
- Names with no CV in DB get bold formatting only (no link) — acceptable only if confirmed not in DB
- Upload gap candidates in one batch before sending — do not send with any empty links
- Reference: send_combined_impact_reply_pilot.py (all 30+ names hyperlinked across both position briefs)
