---
name: Gmail Thread Reply — Threading Headers
description: Rule established 2026-04-08. When replying in an existing Gmail thread, include In-Reply-To and References headers for proper threading.
type: feedback
---

# GMAIL THREAD REPLY — THREADING HEADERS
**Established:** 2026-04-08  
**Status:** MANDATORY — All reply emails  
**Applies to:** Decision briefs, decision updates, or any email replying in existing thread

---

## THE RULE

When replying to an existing Gmail thread:

1. **Subject line:** Must start with `Re: [original subject]`
2. **In-Reply-To header:** Must include original message ID
3. **References header:** Must include original message ID

### Why:
Without these headers, Gmail treats your email as a new thread instead of a reply. Hiring manager gets fragmented conversation instead of coherent thread.

---

## IMPLEMENTATION IN PYTHON

### Using Gmail API (smtplib):
```python
import smtplib
from email.mime.text import MIMEText

# Get the original message ID
original_message_id = "<message-id@gmail.com>"

msg = MIMEText(body_html, 'html')
msg['Subject'] = "Re: [original subject]"
msg['To'] = recipient_email
msg['In-Reply-To'] = original_message_id
msg['References'] = original_message_id

# Send via SMTP
server = smtplib.SMTP('smtp.gmail.com', 587)
server.sendmail(from_addr, to_addr, msg.as_string())
```

### Using Google Gmail API:
```python
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import Request
from google.oauth2 import service_account
import base64
from email.mime.text import MIMEText

# Create message with threading headers
msg = MIMEText(body_html, 'html')
msg['Subject'] = "Re: Original Subject"
msg['To'] = recipient_email
msg['In-Reply-To'] = '<original.message.id@mail.google.com>'
msg['References'] = '<original.message.id@mail.google.com>'

# Send via Gmail API
service.users().messages().send(
    userId='me',
    body={'raw': base64.urlsafe_b64encode(msg.as_bytes()).decode()}
).execute()
```

---

## GETTING THE ORIGINAL MESSAGE ID

When you're replying to an existing thread:

```python
# Get original message from Gmail API
original_msg = service.users().messages().get(
    userId='me',
    id=message_id,
    format='full'
).execute()

original_message_id = original_msg['payload']['headers'][
    [h for h in original_msg['payload']['headers'] if h['name'] == 'Message-ID'][0]
]['value']
```

---

## REFERENCE SCRIPTS

- **Job 35/36 Combined Reply:** `scripts/jobs/combined/send_combined_impact_reply_pilot.py`
  - Shows how to extract message ID from existing thread
  - Shows how to add In-Reply-To and References headers
  - Demonstrates correct subject line format

---

## AUDIT CHECKLIST

Before sending a reply email:

- [ ] Subject starts with `Re: `?
- [ ] In-Reply-To header set correctly?
- [ ] References header set correctly?
- [ ] Original message ID obtained correctly?
- [ ] Email will thread under original instead of as new thread?

---

**Owner:** Coco  
**Status:** LOCKED IN — Applied to all future reply emails  
**Reference:** scripts/jobs/combined/send_combined_impact_reply_pilot.py
