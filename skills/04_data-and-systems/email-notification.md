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
