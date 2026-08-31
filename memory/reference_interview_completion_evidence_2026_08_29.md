---
name: Interview completion evidence — which tool proves which call happened (2026-08-29)
description: Values (Zero In) calls are recorded by Fathom; case-study debriefs by Read AI + Rumi. Neither writes back to Markaz, so "did this call happen" is answered only from the mailbox — and absence of a report is never proof a call did not happen.
type: reference
---

# Proving an interview actually happened (verified 2026-08-29)

Markaz records **none** of this. `gwc_interview_date` and `interview_steps` stay empty after real
interviews (see [[markaz_submissions_arrive_by_email_2026_08_17]]), so the only evidence is in
Ayesha's mailbox, via read-only IMAP.

## The two stages use different note-takers

| Stage | Calendar subject | Completion evidence | Sender |
|---|---|---|---|
| **Values / Zero In** | `Zero In Call for <role> (<name>)` · `Invitation for the Values Interview for <role>` | `Recap of your meeting with <candidate email>` | Fathom `no-reply@fathom.video` |
| **Case-study debrief** | `Case Study Debrief <role> (<name>)` | `🗓 <meeting title> on <date> \| Read Meeting Report` **and** `📋 Meeting Summary: <meeting title>` | `<host> via Read AI` · `Rumi <rumi@hellorumi.ai>` |

🔴 **Do not look for a Fathom recap to prove a debrief happened.** Fathom covers the values calls;
debriefs are captured by Read AI and Rumi. Searching Fathom alone returns zero debriefs and makes a
working pipeline look dead. Debrief reports carry the **meeting title**, so they are findable by the
word `debrief`; Fathom recaps carry only the **candidate's email address**, so match those on the
email in the SUBJECT, not in To/Cc/From.

🔴 **Absence of a report is NOT proof the call did not happen.** A report exists only if a note-taker
joined. Abdul Wahab's 13 Aug debrief was captured by **his own** Read AI, not ours — so for calls
where no participant ran a note-taker, there is simply no record either way. Always report this as
"no completion evidence in the mailbox", never as "the call did not happen".

## Reading the calendar without calendar access

`.claude/config/token.json` still fails `deleted_client` (re-verified 2026-08-29) and the only
live token (`token_sheets_broad.json`) has **drive + sheets, no calendar**. So do not report
"cannot check the calendar" — **reconstruct it from the `invite.ics` attachments** on the
invitation emails. Each VEVENT carries:

`UID` · `SEQUENCE` · `STATUS` (CONFIRMED / CANCELLED) · `METHOD` (REQUEST / CANCEL) ·
`DTSTART`/`DTEND` · `ATTENDEE;PARTSTAT=` (ACCEPTED / DECLINED / NEEDS-ACTION)

**Group by `UID` and keep the highest `SEQUENCE`** — that is the event's final state; earlier
revisions are superseded reschedules. Unfold RFC-5545 line continuations (`\r\n` + space) before
regexing, or long SUMMARY/ATTENDEE lines parse wrong.

🔴 **`PARTSTAT=NEEDS-ACTION` does not mean a no-show.** These slots are booked through Google
appointment schedules, so the candidate picked the time themselves and never needs to RSVP again.
Abdul Wahab sat at NEEDS-ACTION and his debrief demonstrably happened. Treat an explicit
`ACCEPTED` as positive evidence and `NEEDS-ACTION` as no information.

## Booking-side vocabulary

`Appointment booked:` (from `ayesha.khan@niete.edu.pk`, the appointment-schedule alias) ·
`Appointment canceled:` (from the **candidate**, when they cancel) · `Updated invitation:`
(a reschedule — the *last* one wins, so always read the whole chain before quoting a slot) ·
`Declined:` (candidate declined the calendar invite).

A candidate can be invited, booked, rescheduled twice and still not have attended. Count
**people at each stage**, not events — Marzia showed 5 "debrief invite" events because replies in
the thread inherit the subject.

## Practical retrieval

Scan `[Gmail]/All Mail` `SINCE` the job's start with `UID FETCH ... BODY.PEEK[HEADER.FIELDS ...]`,
filter subjects on: `debrief · appointment booked · canceled · updated invitation · invitation: ·
recap of your meeting · meeting report · meeting summary · zero in · values interview ·
lets proceed with the case study · new case study submission`. **Use UIDs and checkpoint to disk** —
a full-mailbox header scan takes ~20 minutes and the connection drops; a resumable script that
reconnects on `IMAP4.abort`/`SSLError` is the difference between finishing and starting over.

Related: [[reference_ayesha_mailbox_imap_2026_08_10]] ·
[[comm_evidence_dual_source_rule_2026_06_20]] · [[feedback_db_status_vs_pipeline]]
