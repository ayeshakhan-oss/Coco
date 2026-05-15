---
name: Locked Exploratory Call Invite Approach
description: Production-ready exploratory call invite template for candidates without immediate openings. Locked design, body text, links, and workflow.
metadata:
  type: project
  status: LOCKED — 2026-05-15
  originSessionId: continuation-2026-05-14
---

# LOCKED EXPLORATORY CALL INVITE APPROACH

**STATUS:** 🔒 PRODUCTION READY — Sent live 2026-05-15

**APPLIES TO:** Candidates who match culture/values but no immediate role fit. Exploratory 30-minute calls to understand fit for future opportunities.

**LOCKED COMPONENTS:** Design (HTML structure), body text (word-for-word), booking link, document link, CTA button styling.

---

## Email Design Specification

**Uses:** Universal locked email template (see [locked_email_template_interview_invites_FINAL_2026_05_13.md](locked_email_template_interview_invites_FINAL_2026_05_13.md))

### Design Locked Elements
- **Background:** #f5f5f5 (light grey wrapper)
- **Card:** #ffffff (white), 775px max-width, 64px padding, #e5e7e2 outer wrapper
- **Header label:** "TALENT ACQUISITION • EXPLORATORY CALL" (12px, uppercase, #3157b7)
- **Title:** "Let's Chat" (24px, #3157b7, Georgia serif)
- **Subtitle:** "An opportunity to connect" (13px, #5d73b8, Georgia serif)
- **Divider:** 2px solid #4b67d1
- **Body font:** Georgia, 17px, 1.85 line-height, #111111
- **Button:** "📅 Let's Chat", #5b3fc4 (purple), 14px padding vertical, 34px horizontal, border-radius 7px
- **Signature:** "People and Culture Team" / "Taleemabad" / "hiring@taleemabad.com | www.taleemabad.com"
- **Logo:** CID-embedded Taleemabad logo (34x34px)

---

## Body Text — LOCKED (Word-for-Word)

Opening:
```
Hi {candidate_name},

Thank you for expressing your interest when we reached out to connect. 
We really appreciate your openness to having a conversation with us.
```

Main body (EXACTLY this):
```
We'd love to invite you for a short exploratory conversation with the Taleemabad team. 
The call would be around 30 minutes and would primarily be an opportunity for us to understand 
your experience, skills, and aspirations better, while also giving you a chance to learn more 
about Taleemabad, the work we're building, and the kind of challenges we're solving.

We're approaching this as an open conversation, and while there may not be a specific role 
tied to it immediately, we genuinely hope that somewhere down the line there could be an 
opportunity for us to work together.

I'm also attaching Fundraising & Partnerships Overview for additional context 
ahead of the conversation.
```

CTA section:
```
[Button: "📅 Let's Chat" linking to BOOKING_LINK]

Pick a time that works for you.

Looking forward to connecting.
```

---

## Links — LOCKED

**Booking Link:** `https://calendar.app.google/r1Rj1b1UMiAqonDs5`
- Google Calendar scheduling link
- Same for all candidates

**Document Link:** `https://drive.google.com/file/d/1VV_gcRRBpt8LtYeILsRzAF320D4jP-Kv/view?usp=sharing`
- Text: "Fundraising & Partnerships Overview"
- Same for all candidates
- Inline link in paragraph (not standalone)

---

## Workflow — LOCKED

### Step 1: Prepare Candidate List
```
CANDIDATES = [
    {"name": "Full Name", "email": "email@domain.com"},
    ...
]
```

### Step 2: Pilot to Ayesha
- Run `scripts/send_exploratory_call_batch_pilot.py`
- Sends all customized invites to `ayesha.khan@taleemabad.com` for review
- Subject: `[PILOT] Exploratory Call Invite — {candidate_name}`
- Wait for Ayesha approval before proceeding

### Step 3: Go Live
- Run `scripts/send_exploratory_call_batch_live.py`
- Sends to actual candidate emails with CC:
  - ayesha.khan@taleemabad.com
  - hiring@taleemabad.com
  - sabeena.abbasi@taleemabad.com
- Subject: `Let's Chat - {candidate_name}`
- All sends logged to `logs/email_audit.log`

### Step 4: Verification
- Check email audit log for all recipients reached
- Confirm CC recipients received copies
- Monitor calendar for booking confirmations

---

## Production Scripts

**Pilot script:** `scripts/send_exploratory_call_batch_pilot.py`
- Configuration: CANDIDATES list, PILOT_TO, BOOKING_LINK, DOCUMENT_LINK
- Sends to Ayesha for review
- Logo embedded via CID

**Live script:** `scripts/send_exploratory_call_batch_live.py`
- Configuration: CANDIDATES list, CC recipients, BOOKING_LINK, DOCUMENT_LINK
- Requires `allow_candidate_addresses()` call to whitelist external emails
- Uses `safe_sendmail()` bouncer for security
- All sends logged

---

## Integration with 06_candidate-invites Skill

**Skill location:** `.claude/skills/06_candidate-invites/`

**Includes 4 invite types:**
1. Values Interview Invite (formal interview stage)
2. Case Study Debrief Invite (post-case study)
3. **Exploratory Call Invite** (no current role fit)
4. Warm Bench Opportunity Invite (values passed, keep warm)

**This locked approach covers type 3 only.** Other types follow separate locked approaches in skill documentation.

---

## Tested Candidates (2026-05-15 Live Send)

✅ **Kanooz Siddiqui** (kanoozay@gmail.com)
✅ **Mushahid Hussain** (mushahid.qau514@gmail.com)
✅ **Sadia Sohail** (Saadia.academicfora@gmail.com)
✅ **Rabia Abbas M.** (rabiaabbasmalik@outlook.com)

All sent with CC to hiring team. All logged.

---

## Self-QA Checklist (Before Sending Live)

- [ ] Candidate list verified (names + emails correct)
- [ ] Booking link copied from Google Calendar (active + correct)
- [ ] Document link verified (Drive link accessible)
- [ ] Pilot sent to Ayesha first (NOT direct to candidates)
- [ ] Ayesha approval received before live send
- [ ] CC recipients correct (Ayesha, Hiring, Sabeena)
- [ ] safe_sendmail() called with allow_candidate_addresses()
- [ ] Email audit log checked post-send

---

**Status:** ✅ LOCKED FOR PRODUCTION USE
**Last Updated:** 2026-05-15
**Tested:** ✅ All 4 candidates sent live
**Owner:** Coco
