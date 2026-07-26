---
name: 06_candidate-invites
description: "Send interview invites and candidate communication emails for all stages: Values Interview Invite, Case Study Debrief Invite, Exploratory Call Invite, Warm Bench Opportunity Invite, Keep-in-Touch Note, Interview Reminder. Always use this skill when you need to invite a candidate to any interview stage, send them an opportunity, communicate next steps, send a post-conversation warm-hold/keep-in-touch note while a decision is pending, or remind a candidate about an already-booked interview (day-before reminder with verified date/time from the calendar or Gmail). The skill enforces locked design—design is 100% locked, ONLY content changes. Uses scripts/send_[type]_pilot.py."
compatibility:
  tools:
    - safe_sendmail (scripts/utils/safe_send.py)
    - Email MIME (Python standard library)
---

# 06 — Candidate Interview Invites

**Status:** 🔒 PRODUCTION READY — Design locked, no deviations allowed.

**Applies to:**
- ✅ Values Interview Invite
- ✅ Case Study Debrief Invite
- ✅ Exploratory Call Invite
- ✅ Warm Bench Opportunity Invite
- ✅ Keep-in-Touch Note (post-conversation warm hold — NO booking button)
- ✅ Interview Reminder (day-before nudge for an ALREADY-BOOKED interview — verified calendar data only)

---

## Quick Start

**Type:** Interview/Opportunity Invite  
**Design:** Locked (see [memory/locked_email_template_interview_invites_FINAL_2026_05_13.md](../../memory/locked_email_template_interview_invites_FINAL_2026_05_13.md))  
**Flow:** Gather info → Customize script → Generate pilot → Ayesha approves → Send live

---

## The Six Invite Types

### 1. Values Interview Invite

**When:** Candidate passes initial screening, moves to values round.

**Required Info:**
- Candidate name (CANDIDATE_NAME)
- Position title (POSITION)
- JD link (JD_LINK)
- Prep guide link (PREP_GUIDE_LINK)
- Calendar booking link (BOOKING_LINK)

**Script:** `scripts/send_values_interview_pilot.py`

**Key Content:**
- Greeting: "Hi [CANDIDATE_NAME],"
- Hook: "Thank you for your interest in the [POSITION] role at Taleemabad."
- Purpose: "45-minute values conversation" to learn about alignment
- Callout: "This session will be recorded."
- CTA: Calendar booking button
- Button text: "📅 Book your Interview"

**Example:**
```
Candidate: Sarah Mitchell
Position: CPD Coach
JD: [Google Doc URL]
Prep Guide: [Google Doc URL]
Booking: [Google Calendar URL]
```

---

### 2. Case Study Debrief Invite

**When:** Candidate submits case study, moves to debrief interview.

**Required Info:**
- Candidate name
- Position title
- Case study submission link (or context)
- Debrief interview link
- Calendar booking link

**Script:** `scripts/send_case_study_debrief_pilot.py`

**Key Content:**
- Greeting: "Hi [NAME],"
- Hook: "Thank you for completing the case study."
- Purpose: "30-minute debrief" to discuss approach + thinking
- CTA: Calendar booking button
- Button text: "📅 Schedule Your Debrief"

---

### 3. Exploratory Call Invite

**When:** Candidate is interesting but doesn't match open role; exploratory call to learn more.

**Required Info:**
- Candidate name
- Context (why you're reaching out)
- Role/area of interest
- Calendar booking link

**Script:** `scripts/send_exploratory_call_pilot.py`

**Key Content:**
- Greeting: Personal tone, reference where you found them
- Hook: "We think you'd be interesting to talk to about..."
- Purpose: "20-minute exploratory conversation"
- CTA: Calendar booking
- Button text: "📅 Let's Chat"

---

### 4. Warm Bench Opportunity Invite

**When:** Candidate cleared values + strong GWC but wasn't selected; new role opens up that fits them.

**Required Info:**
- Candidate name
- Previous role they interviewed for
- New role/position (POSITION)
- Why they'd be good fit (brief context)
- Calendar booking link

**Script:** `scripts/send_warm_bench_invite_pilot.py`

**Key Content:**
- Greeting: Reference previous interview
- Hook: "A new opportunity has opened that aligns with your strengths."
- Purpose: "Discuss this new role and how it might be a fit"
- CTA: Calendar booking
- Button text: "📅 Let's Discuss"

---

### 5. Keep-in-Touch Note

**When:** We have already had a conversation with the candidate (e.g. an exploratory call), the role/decision is being revisited, and we need time. This note tells them honestly that they are still in our thinking — so silence is not mistaken for a "no" — WITHOUT promising a timeline or an outcome. The recurring "we talked, now we need time, we'll circle back" situation.

**Required Info:**
- Recipient list (first name + email) — send only to people we actually spoke with
- Role/area the conversation was about

**Script:** `scripts/send_keep_in_touch_pilot.py` (holds a `CANDIDATES` list; pilots one sample to Ayesha, then sends each person an individual live email)

**Key Content:**
- Greeting: "Hi [First Name],"
- Hook: Thank them for the conversation we already had + name the role
- Purpose: Honest update — we are revisiting the role, you are still in our thinking
- CTA: **NONE** — no calendar booking button, no booking/document link
- Subject (default): "Still very much in our thinking — [Name]"

**🔒 TWO HARD RULES for this type:**
1. **NO booking button / no links.** We are explicitly NOT asking them to schedule anything yet. Body flows straight from the closing paragraph to the signature.
2. **NO promise or commitment.** Forbidden: "we will reach out / be in touch / contact you", hard dates ("by early July"), or any outcome guarantee. Use honest, conditional language only ("when we have more clarity, we would genuinely welcome the chance to be back in touch"). The candidate must have nothing to "count on."

Full spec + tone rationale: [memory/keep_in_touch_note_type_2026_06_19.md](../../memory/keep_in_touch_note_type_2026_06_19.md)

---

### 6. Interview Reminder (Day-Before)

**When:** A candidate has an ALREADY-BOOKED interview tomorrow (any stage — zero-in, values, GWC, debrief). We remind them of the date and time so no-shows drop. Sent the day before, one individual email per candidate.

**Required Info (ALL must come from verified sources — the calendar event or its Gmail booking/invitation emails; NEVER assumed):**
- Candidate first name + email (from the booking email / Markaz — cross-check both)
- Position title
- Interview date ("Friday, July 24, 2026") and time range ("11:00 AM – 12:00 PM, Pakistan Standard Time")
- Google Meet link — OPTIONAL (see rules below)

**Script:** `scripts/send_interview_reminder_pilot.py` (holds an `INTERVIEWS` list; pilots every email to Ayesha first, then sends each candidate an individual live email)

**Key Content:**
- Header label: `TALENT ACQUISITION • INTERVIEW REMINDER`
- Title: "Your Interview is Tomorrow" / Subtitle: position title
- Greeting: "Hi [First Name],"
- Hook: friendly reminder naming the role + tomorrow's date and time (date/time also repeated as a bold blue callout line)
- Recording consent line (same as invite): "This session will be recorded..."
- Reschedule offer: "If anything has come up and the time no longer works, simply reply to this email..."
- CTA: purple button **"🎥 Join your Interview"** linking to the Google Meet link — ONLY if the real Meet link is verified. If no verified link, NO button; use the line "You can join using the Google Meet link in your calendar invitation." instead.
- Subject (default): "Reminder: Your Interview for [POSITION] is Tomorrow — [Day, Month DD]"

**🔒 HARD RULES for this type:**
1. **Verified calendar data only.** Date, time, timezone, and Meet link must come from the actual calendar event or its Gmail notification emails. If the calendar API token is unavailable, use the Gmail evidence trail (booking confirmations / "Invitation:" emails). NEVER reconstruct a time from memory or from Markaz stage data.
2. **Check for cancellations/reschedules first.** Before drafting, search Gmail for `subject:(cancelled OR canceled OR rescheduled)` + the date. A reminder for a cancelled slot is worse than no reminder.
3. **Never fabricate the Meet link.** No verified link → no button (fallback line above). A wrong link strands the candidate.
4. **No unverified names.** If the candidate booked with an email that has no display name and no Markaz record, get the name confirmed by Ayesha before drafting — never guess from the email address.
5. **Timing:** send the day before the interview (candidate already has the invite; this is a nudge, not a new invitation).

---

## Design Specification (LOCKED — NO DEVIATIONS)

**Read this first:** [memory/locked_email_template_interview_invites_FINAL_2026_05_13.md](../../memory/locked_email_template_interview_invites_FINAL_2026_05_13.md)

**Key specs:**
- **Colors:** #f5f5f5 (page bg), #e5e7e2 (wrapper), #ffffff (card), #3157b7 (headers), #3d63c8 (links), #5b3fc4 (button)
- **Typography:** Georgia serif only. 12px label, 24px title, 17px body, 1.85 line-height
- **Layout:** 775px white card in grey wrapper on light grey background
- **Logo:** 34px, centered, CID-embedded
- **Signature:** Left-aligned, 1px grey divider above
- **Button:** Purple (#5b3fc4), rounded corners (7px), 16px bold Georgia

**Self-Check (30 items):** [See locked template section "SELF-CHECK BEFORE SENDING"](../../memory/locked_email_template_interview_invites_FINAL_2026_05_13.md#self-check-before-sending)

---

## Workflow

### Step 1: Select Invite Type
Determine which of the 4 types applies to your candidate and situation.

### Step 2: Gather Required Information
For each invite type, collect:
- Candidate name and email
- Position/role info
- All required links (JD, booking, prep guide, etc.)
- Any custom context (exploratory call reason, warm bench context)

### Step 3: Customize the Script
1. Open the appropriate script: `scripts/send_[type]_pilot.py`
2. Set configuration variables:
   ```python
   CANDIDATE_NAME = "Full Name"
   POSITION = "Role Title"
   JD_LINK = "https://docs.google.com/..."
   PREP_GUIDE_LINK = "https://docs.google.com/..."
   BOOKING_LINK = "https://calendar.google.com/..."
   
   PILOT_MODE = True
   PILOT_TO = "ayesha.khan@taleemabad.com"
   ```
3. Customize email body content as needed (greeting, hook, purpose statement)
4. Keep HTML structure 100% identical—only change text

### Step 4: Generate Pilot Email
Run the script in pilot mode (sends to Ayesha only):
```bash
python scripts/send_values_interview_pilot.py
```

Output:
- Email sent to ayesha.khan@taleemabad.com
- Subject line matches template
- HTML renders with locked design
- Logo embeds correctly

### Step 5: Get Ayesha's Approval
- Ayesha reviews in her email
- Checks design matches locked spec
- Approves content and tone
- Gives thumbs-up to go live

### Step 6: Send Live
Once approved:
1. Change script settings:
   ```python
   PILOT_MODE = False
   TO = ["candidate.email@domain.com"]
   CC = ["ayesha.khan@taleemabad.com", "hiring@taleemabad.com"]
   ```
2. Run script again
3. Confirm send in console output
4. Log email in [memory/session_active.md](../../memory/session_active.md)

---

## Content Guidelines

### Tone (All Types)
- Professional yet warm
- Specific and personalized
- Clear about next steps
- No jargon or internal terms

### Greeting
- Use full first name: "Hi Sarah," not "Hi Sarah Mitchell,"
- Personal context if applicable: "Sarah," or "Dear Sarah,"

### Hook (First Paragraph)
- Reference why you're reaching out
- Acknowledge their application/submission/progress
- Set positive expectation

### Purpose Statement
- Clear: "45-minute values conversation"
- Specific: What will you discuss?
- Context: How does it fit in the process?

### Links
- Make them clickable (color: #3d63c8, underlined)
- Text should be descriptive: "interview prep guide" not "click here"
- Test all links before sending pilot

### CTA Button
- One clear action: "Book your Interview"
- Use calendar emoji or action verb
- Never multiple buttons

### Callouts (Important Info)
- Recording disclaimers: "This session will be recorded."
- Key requirements: "Please come prepared with..."
- Use bold (font-weight: 700) for emphasis

### Closing
- Reference next steps: "We look forward to speaking with you"
- Keep it brief
- Professional sign-off: "Warm regards," / "Best regards,"

---

## Technical Implementation

### Email Structure (Table-Based for Gmail)
```html
<table width="100%" bgcolor="#f5f5f5">
  <tr>
    <td align="center">
      <!-- Grey wrapper -->
      <table width="calc(100% - 90px)" bgcolor="#e5e7e2">
        <tr>
          <td align="center">
            <!-- White card (775px) -->
            <table width="775" bgcolor="#ffffff">
              <!-- Header section -->
              <!-- Divider -->
              <!-- Body content -->
              <!-- Signature -->
            </table>
          </td>
        </tr>
      </table>
    </td>
  </tr>
</table>
```

### Logo Embedding (CID Inline)
```python
img = MIMEImage(img_data, 'png')
img.add_header('Content-ID', '<taleemabad_logo>')
img.add_header('Content-Disposition', 'inline')
msg.attach(img)
```

In HTML:
```html
<img src="cid:taleemabad_logo" width="34" height="34">
```

### Font Rendering (Georgia Serif)
```html
<style>
  body, p, div {
    font-family: Georgia, Cambria, "Times New Roman", serif;
  }
</style>
```

---

## Common Mistakes (Never Do These)

- ❌ Change design elements (colors, fonts, spacing) — Design is locked
- ❌ Skip pilot to Ayesha — Always pilot first
- ❌ Use div-based layout — Table-based only (Gmail compatibility)
- ❌ Use modern fonts (Inter, Poppins) — Georgia serif only
- ❌ Include social media logos — Only Taleemabad logo
- ❌ Forget CID embedding — Images must be inline
- ❌ Add yellow highlighting — No highlighting anywhere
- ❌ Center signature — Left-aligned only
- ❌ Use multiple buttons — One CTA button per email
- ❌ Fabricate links — All links must be real and tested

---

## Reference Files

| File | Purpose |
|------|---------|
| [memory/locked_email_template_interview_invites_FINAL_2026_05_13.md](../../memory/locked_email_template_interview_invites_FINAL_2026_05_13.md) | Master design spec + 30-item self-check |
| [scripts/send_values_interview_pilot.py](../../scripts/send_values_interview_pilot.py) | Reference implementation (Values Interview) |
| [scripts/utils/safe_send.py](../../scripts/utils/safe_send.py) | Email bouncer (always use this, never smtplib) |
| [RULES.md](../../RULES.md) | Core discipline + all skill specs |

---

## Self-QA Before Sending Pilot

1. **Design Check:** Run against 30-item checklist from locked template
2. **Content Check:** Greeting, hook, purpose, CTA all clear and specific
3. **Link Check:** All URLs are real and clickable
4. **Logo Check:** 34px, centered, renders inline
5. **Tone Check:** Warm, specific, professional
6. **Format Check:** Table-based HTML, no div layout
7. **Color Check:** All colors match locked palette (no deviations)
8. **Font Check:** Georgia serif only, correct sizes (12px label, 24px title, 17px body)
9. **Spacing Check:** Padding and margins match spec (34px top header, 44px body top, etc.)
10. **Signature Check:** Left-aligned, grey divider, correct styling

---

**Last Updated:** 2026-05-13  
**Status:** 🔒 LOCKED FOR PRODUCTION  
**Design Verified:** Against reference screenshot + pilot testing  
**Enforcement:** Design deviations require explicit user approval (rare)
