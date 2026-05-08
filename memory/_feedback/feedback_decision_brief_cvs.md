---
name: Decision Brief — CV delivery method
description: CVs must be uploaded to Google Drive and hyperlinked in the PDF. Never attach CVs separately to the email.
type: feedback
---

In decision briefs, CVs go to Google Drive first, then hyperlinked onto candidate names in the PDF via PyMuPDF. The email gets one attachment only: the report PDF.

**Why:** Attaching individual CVs to the email is wrong. The correct method (confirmed April 2 2026, Field Coordinator brief) is: upload to Drive → get shareable link → inject as URI hyperlink over candidate name using `fitz.LINK_URI`. Names appear blue and underlined in the PDF; clicking opens the CV in Drive.

**How to apply:** Any future decision brief must follow this exact pattern. Reference: `send_job36_decision_brief_pilot.py` (Drive upload) and `send_job32_decision_brief_pilot.py` (same pattern applied to Job 32). Token: `token_drive.json`.
