---
name: email-notification
description: Send emails via safe_sendmail() bouncer. Pilot mode first. Threading headers for replies. Audit logging mandatory.
compatibility: Requires safe_sendmail bouncer, .env credentials, audit logging, RULES.md Email Rules
---

# Email Notification

Send emails via safe_sendmail bouncer. Pilot mode required. Threading headers for replies. Audit logging mandatory.

---

## When to Use This Skill

Trigger this skill when:
- User asks to "send email" or "notification"
- Email is part of hiring workflow (invites, feedback, decisions)
- Pilot mode required before live send
- Audit logging needed

---

## Related SOP

**Location:** `SOPs/04_Data_and_Systems/email_notification.md`

---

## Universal Rules

**Email Delivery (Non-Negotiable):**
- ALWAYS use `safe_sendmail()` bouncer
- NEVER use smtplib directly
- Set `pilot=True` for test mode
- Credentials from `.env` (never hardcoded)

**Pilot Mode (Mandatory):**
- Send to Ayesha/Jawad only (never direct to recipient)
- User reviews output
- User says "make it live"
- Set `pilot=False` for production

**Threading (For Replies):**
- Use In-Reply-To header (Message-ID of parent)
- Use References header (full thread chain)
- Subject line: "Re: [original subject]"

**Audit Logging (Mandatory):**
- Log all sends: `log_email_send(to, subject, purpose)`
- Timestamp, recipient, subject
- Log file: `logs/email_audit.log`

**Credentials:**
- Gmail credentials from `.env`
- Never hardcode in script
- Check `.env` exists before sending

---

## Detailed Procedure

**Setup (One-Time):**
1. Choose delivery method:
   - **Option A:** Gmail API (recommended) — requires credentials.json from Google Cloud Console
   - **Option B:** SMTP (simpler) — requires .env with EMAIL_HOST, EMAIL_PORT, EMAIL_USER, EMAIL_PASSWORD
   - **Option C:** SendGrid API (production) — requires SendGrid account + API key
2. Store credentials in `.env` or `.claude/config/` (NEVER commit to git)
3. Test connection: run script to verify delivery method works

**Recipients Mapping:**
- HR/Talent Lead: gets all position reports
- Hiring Manager: gets reports for their specific position only
- Additional stakeholders: as specified

**Email Sending Workflow:**
1. Prepare email content (HTML or text)
2. Set `pilot=True` (test mode)
3. Call `safe_sendmail(to=[Ayesha], subject=..., body=..., pilot=True)`
4. Wait for user approval: "looks good" or requested changes
5. Make any corrections to content/formatting
6. Set `pilot=False` (production mode)
7. Call `safe_sendmail(to=[actual recipients], subject=..., body=..., pilot=False)`
8. Log send: `log_email_send(to=[recipients], subject=..., purpose="...")`

**Threading Headers (For Email Replies):**
- Add In-Reply-To header: Message-ID of parent email
- Add References header: full thread chain of Message-IDs
- Set Subject: "Re: [original subject]"
- Example: `safe_sendmail(..., in_reply_to="<original_id>", references="<id1>, <id2>")`

**Audit Logging (Mandatory):**
```python
from scripts.utils.audit_log import log_email_send
log_email_send(
    to="ayesha.khan@taleemabad.com",
    subject="CV Screening Report: Senior Engineer",
    purpose="Pilot send for feedback"
)
```

**Common Mistakes to Avoid:**
- Sending directly to candidate without pilot/approval first
- Using smtplib instead of safe_sendmail()
- Hardcoding credentials in code
- Missing audit logging
- Not checking .env file exists before sending
- Wrong threading headers for replies
- Forgetting to switch pilot=False for live send

---

## Execution Discipline

1. Prepare email (HTML/text)
2. Set `pilot=True`
3. Call `safe_sendmail(to=..., subject=..., body=..., pilot=True)`
4. Send to Ayesha only
5. Wait for approval
6. Set `pilot=False`
7. Call `safe_sendmail(..., pilot=False)` to live recipients
8. Log send: `log_email_send(to, subject, purpose)`

---

## Success Criteria

✅ Used safe_sendmail bouncer  
✅ Pilot mode first (Ayesha review)  
✅ Threading headers set (if reply)  
✅ Audit logging in place  
✅ .env credentials used  

**Status:** ✅ PRODUCTION READY
