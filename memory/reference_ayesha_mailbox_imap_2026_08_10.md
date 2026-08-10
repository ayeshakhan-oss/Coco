---
name: 🔑 Ayesha mailbox via IMAP app-password (calendar-evidence path) (2026-08-10)
description: Verified working method to read ayesha.khan@taleemabad.com's own mailbox (read-only IMAP with the stored SMTP app password) for calendar booking confirmations. Calendar OAuth token confirmed dead. Authorized by Ayesha 2026-08-10.
type: reference
---

# 🔑 Reading Ayesha's mailbox for calendar-booking evidence (verified 2026-08-10)

**Problem:** "Has candidate X booked a slot on my calendar?" — the Google Calendar API token (`.claude/config/token.json`, `calendar.readonly`) is **DEAD**: refresh fails with `deleted_client` (OAuth client deleted; re-verified 2026-08-10). The claude.ai Google Calendar connector needs interactive auth. The connected Gmail MCP is the **jawwad.ali** mailbox — appointment-schedule booking notifications do NOT land there.

**Working method (Ayesha explicitly asked for this access 2026-08-10):**
Booking confirmations ("Appointment booked: … (Candidate Name) @ date time") land in **ayesha.khan@taleemabad.com's own mailbox**, and the SMTP app password in `.env` (`EMAIL_PASSWORD`) also works for **read-only IMAP**:

```python
import imaplib, os
from dotenv import load_dotenv
load_dotenv(r"c:\Agent Coco\.env")
M = imaplib.IMAP4_SSL("imap.gmail.com")
M.login("ayesha.khan@taleemabad.com", os.environ["EMAIL_PASSWORD"])
M.select('"[Gmail]/All Mail"', readonly=True)
typ, data = M.search(None, '(SUBJECT "booked" SINCE "07-Aug-2026")')
# fetch BODY.PEEK[HEADER.FIELDS (FROM TO SUBJECT DATE)] per id
```

**Rules:**
- READ-ONLY (`readonly=True`, `BODY.PEEK`) — never mark read, move, or delete.
- Log every read to `logs/read_audit.log`.
- Booking subjects carry the slot: `Appointment booked: <schedule name> (<Candidate>) @ <Day Date, time> (GMT+5)`.
- Some bookings arrive from Ayesha's alias `ayesha.khan@niete.edu.pk` — search by SUBJECT, not FROM.
- Use for verified interview-reminder data (Skill 06 type 6) and booking-status checks; still cross-check Markaz per the dual-source rule.

Reference implementation this session: scratchpad `check_bookings_imap.py` (session-scoped; rebuild from snippet above).
