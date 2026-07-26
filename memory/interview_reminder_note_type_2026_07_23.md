---
name: Interview Reminder — invite type #6 (2026-07-23)
description: "Day-before reminder for an ALREADY-BOOKED interview. Skill 06 invite family (NOT candidate-communication/v8). Verified calendar/Gmail data only; Meet-link button optional; never guess names or times."
type: project
status: LOCKED — invite family
---

# Interview Reminder (Day-Before) — Invite Type #6

**Added:** 2026-07-23 at Ayesha's request. First live use: 2026-07-23 (two Growth Manager - Lahore zero-in calls on Fri Jul 24 — Salman Tariq 11am–12pm, Mahnoor Farooq Khan 12pm–1pm PKT; CC ayesha.khan@, waqas.tanveer@, ali.sipra@taleemabad.com).

## Placement decision (Ayesha asked; recommendation accepted)
Lives under **Skill 06 (candidate-invites)**, NOT Skill 01 (candidate-communication):
- A reminder is **interview logistics** — the sequel to the invite, in the same locked invite design the candidate already saw.
- The candidate-comms rules would be actively wrong here: the mandatory "This is not a yes for now." opener, 800+ word minimum, and v8 layout are for **decision/feedback** emails. A day-before reminder must never open like a rejection.
- Same reasoning as Keep-in-Touch (type #5, 2026-06-19) and Role-Closure (2026-07-23).

## Spec (full version: `.claude/skills/06_candidate-invites/SKILL.md`, type 6)
- Locked interview-invite design (2026-05-13 spec). Label: `TALENT ACQUISITION • INTERVIEW REMINDER`. Title: "Your Interview is Tomorrow". Subtitle: position.
- Body: friendly reminder naming role + tomorrow's date/time; date/time repeated as bold blue callout; recording-consent line; "reply to this email and we will help you find another slot"; "See you tomorrow."
- Subject: `Reminder: Your Interview for [POSITION] is Tomorrow — [Day, Month DD]`
- CTA button **"🎥 Join your Interview"** ONLY with a verified Meet link. No verified link → NO button; use "You can join using the Google Meet link in your calendar invitation."
- Script: `scripts/send_interview_reminder_pilot.py` — gitignored (holds candidate PII); `INTERVIEWS` list + `PILOT_MODE` flag; pilots to Ayesha, then individual live emails.

## 🔒 HARD RULES
1. **Verified calendar data only.** Date/time/timezone/Meet link from the actual calendar event or its Gmail notification emails ("Appointment booked:", "Invitation:", "Accepted:"). NEVER reconstruct from memory or Markaz stage data.
2. **Check for cancellations/reschedules first** — Gmail `subject:(cancelled OR canceled OR rescheduled)` + the date. A reminder for a cancelled slot is worse than none.
3. **Never fabricate the Meet link.** No verified link → no button.
4. **No unverified names.** Booking email with no display name and no Markaz record → Ayesha confirms the name before drafting (e.g. the Jul-24 GM-Karachi call, waqashassan5@hotmail.com, was excluded for this).
5. **Send the day before.** It's a nudge, not a new invitation.

## Non-obvious findings from the build
- The **calendar-readonly token is DEAD** (its OAuth client was deleted). Until re-minted via a browser OAuth flow, get event data from the Gmail evidence trail in ayesha.khan's mailbox. The gmail/sheets tokens on the current client still work.
- Google appointment-scheduling **"Appointment booked" emails do NOT contain the Meet link** — it lives only in the calendar event. Hence the optional-button rule.
- Candidates can appear on the calendar with **no Markaz record and no display name**; that's why Rule 4 exists.
