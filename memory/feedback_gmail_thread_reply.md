---
name: Gmail Thread Reply — Threading Headers
description: To reply inside an existing Gmail thread (not create a new email), must set In-Reply-To + References headers and reply to the last message's Message-ID.
type: feedback
---

Replying to an existing Gmail thread requires specific email headers — SMTP alone creates a new thread.

**Why:** Sabeena's "Impact hiring Update" thread needed a reply in-thread (not a new separate email). SMTP by default creates a new conversation. The correct approach uses Gmail threading headers.

**How to apply:**
1. Find thread via Gmail API: `svc.users().messages().list(userId='me', q='subject:"..."')` 
2. Get the last message's `Message-ID` header — reply `In-Reply-To` this
3. Set `References` to the full chain of Message-IDs (space-separated, oldest first)
4. Subject must be `Re: [original subject]` (exact match including "Re: ")
5. Send via SMTP as normal — Gmail matches the thread via headers automatically
6. Recipients: reply-all = TO includes original sender + all TO recipients, CC = all CC recipients, minus self (EMAIL_USER)

**Code pattern:**
```python
msg["Subject"]    = "Re: Impact hiring Update"
msg["In-Reply-To"] = "<last_message_id@mail.gmail.com>"
msg["References"]  = "<original_id@...> <last_message_id@...>"
```

**Reference script:** scripts/jobs/combined/send_combined_impact_reply_pilot.py
**Thread found:** 19d6bb06e8872637 — "Impact hiring Update" (Sabeena Abbasi, 8 Apr 2026)
