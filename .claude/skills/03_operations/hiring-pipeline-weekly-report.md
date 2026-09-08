---
name: Automated Weekly Hiring Pipeline Report
description: Proactive weekly monitoring across all open positions, flagging candidates stuck at pipeline stages. Runs Monday 10:30am + Friday 3pm. Sends to both Ayesha and Jawwad.
type: feedback
---

## Objective

Create an automated weekly hiring pipeline report that runs on a fixed schedule (Monday 10:30am, Friday 3pm) and proactively alerts Ayesha and Jawwad when candidates are stuck at any stage of the hiring pipeline. The system identifies bottlenecks, flags overdue candidates, and drafts follow-up messages ready for approval.

**Audience:** Ayesha Khan + Jawwad Ali (co-P&C leads)

**Frequency:** Automated — runs twice weekly, Monday 10:30am and Friday 3:00pm

**Quality expectation:** Accurate, cross-source verified, nothing missed, draft messages ready to send

---

## Problem This Solves

**Challenge:** The hiring process was slowing down because there was no mechanism to proactively surface when a candidate needed the next action. Candidates could be invited to values interviews but the booking would be missed. Case studies could be sent but forgotten about. Follow-ups would be delayed.

**Solution:** Automated twice-weekly scans of the entire pipeline, with clear escalation logic:
- **3 days stuck** at a stage → ⚠️ warning flag
- **14 days stuck** at a stage → 🔴 urgent flag
- **Draft messages** auto-generated for all flagged candidates, ready for Ayesha to approve and send

---

## Data Sources (Non-Negotiable: Check All Three)

This skill requires the system to consult three separate sources for complete accuracy:

1. **Markaz Database** — candidate status, values interview results, case study received flags, debrief outcomes
2. **Gmail API** — to verify when invites/sends actually went out (DB status can lag reality)
3. **Google Calendar API** — to verify when interview slots were actually booked (candidates may not respond immediately)

**Rule:** Never rely on DB alone. Cross-check all three sources.

---

## Pipeline Stages Tracked

The system classifies each shortlisted-or-beyond candidate into one of these stages:

| Stage | Detected By | Next Action Required |
|-------|---|---|
| **shortlisted_no_invite** | DB status=shortlisted, no "invitation for values" email sent | Send values interview invite |
| **invited_not_booked** | Email sent, no calendar slot booked | Follow up: ask candidate to book |
| **booked_upcoming** | Calendar slot exists, future date | None (monitor until it happens) |
| **values_completed_no_scorecard** | Past calendar slot, no scorecard in DB | Fill scorecard on Markaz |
| **values_failed** | values_interview_result='fail' | Send warm rejection |
| **values_pass_no_case_study** | values_interview_result='pass', no case study email sent | Send case study assignment |
| **case_study_pending** | Email sent, no submission in DB, <3 days | None (await submission) |
| **case_study_overdue** | Email sent, no submission in DB, 3-14 days | Send reminder email |
| **case_study_critical** | Email sent, no submission in DB, >14 days | Escalate to hiring manager |
| **case_study_received_no_debrief_invite** | Case study marked received, no debrief email sent | Send debrief invite |
| **debrief_invited_not_booked** | Email sent, no calendar slot booked | Follow up: ask candidate to book |
| **debrief_upcoming** | Calendar slot exists, future date | None (monitor) |
| **debrief_completed_panel_pending** | DB shows gwc_scorecard filled, no offer status yet | Panel decision required |

---

## Escalation Thresholds (Non-Negotiable)

- **DAYS_FLAG = 3**: Any candidate stuck >3 days at a stage gets ⚠️ warning badge
- **DAYS_URGENT = 14**: Any candidate stuck >14 days gets 🔴 urgent badge (moved to top of position section)
- **Draft messages generated for**: All FLAG (3-14 days) and URGENT (>14 days) candidates only

Days stuck = today − last status change date. For example:
- Shortlisted on 2026-04-05, today is 2026-04-09 → 4 days stuck, qualifies for flag
- Values pass on 2026-03-20, today is 2026-04-10 → 21 days stuck, qualifies for urgent

---

## 5-Step SOP (Automated Execution)

### Step 1: Query Markaz DB for All Open Positions

**Action:** Connect to Neon PostgreSQL via psycopg2. Query:

```sql
SELECT j.id, j.job_id, j.title, j.department,
       j.hiring_manager, u.email as hiring_manager_email, u.first_name as hm_first_name
FROM jobs j
LEFT JOIN users u ON j.hiring_manager = u.id
WHERE j.job_status = 'Active'
ORDER BY j.created_at DESC
```

**Document:** List of all open positions with hiring manager emails.

---

### Step 2: Get Shortlisted-and-Beyond Candidates Per Position

**Action:** For each open position, query:

```sql
SELECT a.id, c.first_name, c.last_name, c.email,
       a.status, a.stage, a.applied_at,
       a.values_interview_result, a.values_interview_date, a.values_scorecard,
       a.gwc_scorecard, a.gwc_interview_date,
       a.notes
FROM applications a
JOIN candidates c ON a.candidate_id = c.id
WHERE a.job_id = $1
  AND (a.status != 'applied' OR a.values_interview_result IS NOT NULL)
ORDER BY a.applied_at DESC
```

**Document:** All candidates with any pipeline progress (past applied stage).

---

### Step 3: Cross-Check Gmail for Invite/Send Emails

**Action:** For each candidate, run targeted Gmail queries:

- **Values invite**: `from:ayesha.khan@taleemabad.com to:{candidate_email} subject:(Invitation for Values OR Zero In)`
- **Case study send**: `from:ayesha.khan@taleemabad.com to:{candidate_email} subject:(case study OR KCD assignment)`
- **Debrief invite**: `from:ayesha.khan@taleemabad.com to:{candidate_email} subject:(debrief OR GWC)`

For each query, capture:
- Email found (bool)
- Send date (timestamp from email headers)
- Subject line

**Document:** Dict per candidate: `{values_invite_sent: bool, values_date, case_study_sent: bool, case_study_date, debrief_invite_sent: bool, debrief_date}`

---

### Step 4: Cross-Check Calendar for Booked Slots

**Action:** Query Google Calendar for events with these criteria:

- **Values slots**: Summary contains "Zero In" or "Values Interview", attendee = candidate email, look back 60 days, forward 60 days
- **Debrief slots**: Summary contains "Case Study Debrief" or "GWC", attendee = candidate email, look back 60 days, forward 60 days

For each slot, capture:
- Slot found (bool)
- Start datetime (ISO format)
- Is past (bool) — True if startTime < now
- Attendee response status (accepted/declined/tentative/needsAction)

**Document:** Dict per candidate: `{values_booked: bool, values_start_dt, values_past: bool, debrief_booked: bool, debrief_start_dt, debrief_past: bool}`

---

### Step 5: Classify Each Candidate + Generate Draft Messages

**Action:** For each candidate, combine DB, Gmail, Calendar data and classify into one of the stages above.

**For each FLAG (3-14 days) or URGENT (>14 days) candidate**, generate a draft message:

**Draft message template — Values follow-up** (if stuck at "invited_not_booked" > 3 days):
```
Subject: [Reminder] Booking your values interview for [Position] — [Candidate Name]

Dear [Candidate Name],

We sent you an invitation to our values interview for the [Position] role on [date_of_original_email]. 

We'd love to get your interview scheduled — could you pick a slot from the calendar link we provided? 
Slots are available Mon–Fri, 11am–12pm or 1pm–2pm.

Please let us know if you have any questions.

Warm regards,
Ayesha Khan & Team
```

**Draft message template — Case study reminder** (if stuck at "case_study_pending" > 3 days):
```
Subject: [Gentle Reminder] Your case study for [Position] — [Candidate Name]

Hi [Candidate Name],

We sent you a case study assignment for [Position] on [date_of_original_email]. 

We're looking forward to reviewing your work. Do you have questions about the assignment, or do you need more time? 
Please let us know your timeline.

Warm regards,
Ayesha Khan & Team
```

**Draft message template — Debrief follow-up** (if stuck at "debrief_invited_not_booked" > 3 days):
```
Subject: [Reminder] Let's schedule your case study debrief — [Candidate Name]

Hi [Candidate Name],

We sent you an invite to discuss your case study for [Position] on [date_of_original_email]. 

We'd like to get your debrief scheduled — could you pick a slot from the calendar link?
Slots are available Mon–Fri, 2pm–4pm.

Looking forward to chatting with you.

Warm regards,
Ayesha Khan & Team
```

**All draft messages:**
- Use the v8 email tone (warm, professional, "we" voice, no em-dashes, storytelling-based)
- Are placed in a **Draft Messages** section at the bottom of the report
- Include a disclaimer: *"These are draft messages ready for approval. Copy, personalize, and send at your discretion."*

---

## Email Report Structure (Non-Negotiable)

### Header
- Subject: `Hiring Pipeline Update — [Mon/Fri] [Date] (Positions: [count])`
- Dark Taleemabad green header (`#2e7a4f`) with white text
- Stat boxes: Total positions, total shortlisted, urgent candidates, flagged candidates
- Run timestamp

### Per-Position Section
For each open position (in order of urgency):

1. **Position title** + hiring manager first name
2. **URGENT candidates first** (🔴 badge, 14+ days stuck), then **FLAGGED** (⚠️ badge, 3-14 days), then **NO ACTION NEEDED**
3. **Per candidate row:**
   - Name (hyperlinked to Drive CV if available)
   - Current stage (e.g., "Case Study Pending — 5 days")
   - Escalation badge (🔴 or ⚠️)
   - Next action (text, e.g., "Send reminder email")

### Draft Messages Section
- Heading: "DRAFT MESSAGES — Ready for Approval"
- One message block per URGENT/FLAGGED candidate
- Each block: candidate name, message subject, full draft body, copy button prompt

### Footer
- "Compiled by Coco — AI Pipeline Monitor (runs Mon 10:30am, Fri 3pm)"
- Timestamp of run

---

## Email Format Rules (Non-Negotiable)

- **Format:** Inline HTML, no PDF attachment
- **Recipient fields:**
  - TO: ayesha.khan@taleemabad.com, jawwad.ali@taleemabad.com
  - CC: hiring@taleemabad.com
- **Design:** v8+ Taleemabad green/blue color scheme, stat boxes with colored badges, aligned tables, justified text
- **Safe sending:** All sends routed through `scripts/utils/safe_send.py`'s `safe_sendmail()` function
- **Audit logging:** Every DB query logged via `audit_log.log_db_query()`, every Gmail read via `audit_log.log_gmail_read()`
- **Error handling:** If script encounters error, send error notice to Ayesha only (not Jawwad) with full traceback

---

## Implementation Details

### Script Location
`scripts/reports/weekly_pipeline_monitor.py` (~500 lines)

### Task Scheduler Setup
After script is created, run:
```bash
python scripts/reports/setup_pipeline_monitor_schedule.py
```

This registers two Windows Task Scheduler tasks:
- **CocoPipelineMonitor_Monday** → runs `weekly_pipeline_monitor.py` every Monday at 10:30am
- **CocoPipelineMonitor_Friday** → runs `weekly_pipeline_monitor.py` every Friday at 3:00pm

### Dependencies
- `psycopg2` — DB connection
- `google-auth`, `google-auth-oauthlib`, `google-api-python-client` — Gmail + Calendar APIs
- `python-dotenv` — load EMAIL_USER, EMAIL_PASSWORD
- Token files: `token_gmail.json` (Gmail API), `token.json` (Calendar API)

### Log Files
- `logs/email_audit.log` — send attempts (all safe_sendmail calls)
- `logs/read_audit.log` — DB query + Gmail read audit trail

---

## Non-Negotiable Rules

1. **Always cross-check all three sources** — DB, Gmail, Calendar. DB status can lag; Gmail and Calendar are the truth.

2. **Escalation thresholds are fixed**: 3 days = flag, 14 days = urgent. No exceptions.

3. **Draft messages generated for FLAG + URGENT only** — candidates with "no action needed" don't get draft messages.

4. **All candidate names must be hyperlinked** — link to Drive CV where available.

5. **Every open position must appear in the report** — even if all candidates are green (no action).

6. **All shortlisted-and-beyond candidates must appear** — no candidate omitted from any section.

7. **Days stuck calculation is accurate** — use the most recent date from {applied_at, values_interview_date, calendar slot start, case_study_sent_date}.

8. **Draft messages match v8 tone** — warm, professional, "we" voice, no em-dashes, short and clear.

9. **Safe_sendmail bouncer is mandatory** — never call smtplib directly. Context log: `hiring_pipeline_monitor`.

10. **Both Ayesha and Jawwad get the FULL report** — no filtering per person. Both see all candidates, all positions, all draft messages.

11. **Token refresh on startup** — check if `token_gmail.json` and `token.json` are expired, refresh if needed (use `creds.refresh(Request())`).

12. **Graceful error handling** — if script fails mid-run, catch exception, log it, send error email to Ayesha with traceback, exit cleanly.

---

## Pre-Run Checklist

**Setup (one-time):**
- [ ] `token_gmail.json` exists and has Gmail API scopes
- [ ] `token.json` exists and has Calendar API scopes
- [ ] `scripts/utils/safe_send.py` and `audit_log.py` exist
- [ ] `scripts/reports/weekly_pipeline_monitor.py` is in place
- [ ] `setup_pipeline_monitor_schedule.py` has been run (tasks registered)

**Per run (automatic, but verify after first manual test):**
- [ ] All open positions queried from DB
- [ ] All shortlisted+ candidates retrieved
- [ ] Gmail queries complete for invites/sends
- [ ] Calendar queries complete for bookings
- [ ] Classification logic correct (stage assignment, days-stuck calculations)
- [ ] Draft messages generated for URGENT/FLAGGED only
- [ ] HTML built with all stat boxes, all candidates, all sections
- [ ] Email sent to both Ayesha and Jawwad
- [ ] Audit logs written (`email_audit.log`, `read_audit.log`)

---

## Common Mistakes

1. **Relying on DB status alone** — candidate marked shortlisted but email never sent. Gmail is the source of truth.

2. **Missing escalation badges** — report shows days stuck but no flag. Every 3+ day candidate should have a badge.

3. **Incomplete candidate list** — one position missing a candidate. Cross-check DB count vs. report count.

4. **Draft messages for all candidates** — should be only URGENT + FLAGGED. Green candidates shouldn't get drafts.

5. **Wrong date calculations** — counting from wrong field (applied_at vs. values_interview_date). Use most recent status change.

6. **Hardcoded position IDs** — report should dynamically pull all active positions, not a fixed list.

7. **No error handling** — script crashes mid-run, no email sent, no log. Always wrap main() in try/except.

8. **Tokens not refreshed** — Gmail query fails because token expired. Refresh on startup.

9. **CV links missing** — candidate names not hyperlinked. Reduces usefulness to hiring manager.

10. **Draft message tone wrong** — sounds AI-generated or too formal. Should be warm and human.

---

## Reference

**Execution:** `python scripts/reports/weekly_pipeline_monitor.py`

**Setup:** `python scripts/reports/setup_pipeline_monitor_schedule.py`

**Audit logs:** `logs/email_audit.log`, `logs/read_audit.log`

**Email sending:** `scripts/utils/safe_send.py` → `safe_sendmail()`

**Audit logging:** `scripts/utils/audit_log.py` → `log_db_query()`, `log_gmail_read()`

**Similar skill:** [skills/hiring-decision-brief.md](hiring-decision-brief.md) — also checks Markaz + Gmail + Calendar, but for a single position in depth; this skill is shallower but continuous across all positions.

---

## Commitment (Coco, 2026-04-10)

I will build and maintain an automated weekly hiring pipeline monitor that runs Monday 10:30am and Friday 3pm, checks all open positions across Markaz + Gmail + Calendar, classifies each candidate's current stage, calculates days stuck, flags at 3 and 14 days, drafts follow-up messages ready for approval, and sends a comprehensive report to both Ayesha and Jawwad. I will cross-check all three sources. I will include all open positions and all shortlisted+ candidates. I will generate escalation badges accurately. I will use safe_sendmail with audit logging. I will handle errors gracefully. The system will be super solid.
