---
name: Automated Weekly Hiring Pipeline Monitor (2026-04-10)
description: Proactive automated system that runs Monday 10:30am + Friday 3pm. Checks all open positions across Markaz+Gmail+Calendar. Flags candidates stuck at pipeline stages. Sends report to both Ayesha and Jawwad. Identifies next actions needed.
type: project
---

## Context
**User request (2026-04-10):** "My process has slowed down a lot... I need constant reminders. Build some kind of mechanism, Coco, through which I keep receiving constant reminders so that my process speeds up."

Ayesha needed a proactive system that would automatically surface bottlenecks in the hiring pipeline — candidates stuck waiting for the next action without being noticed.

## Solution Built
Three-file implementation:
1. **skills/hiring-pipeline-weekly-report.md** — Comprehensive SOP documentation
2. **scripts/reports/weekly_pipeline_monitor.py** — Main monitoring engine (~500 lines)
3. **scripts/reports/setup_pipeline_monitor_schedule.py** — Windows Task Scheduler setup

## How It Works

### Schedule
- **Monday 10:30am** — Full pipeline scan
- **Friday 3:00pm** — Full pipeline scan

### Data Sources (Cross-Checked)
- **Markaz DB**: candidate status, values results, case study flags, debrief outcomes
- **Gmail API**: verify invite/send emails actually went (DB can lag)
- **Calendar API**: verify interview slots actually booked

### Pipeline Stages Tracked
1. Shortlisted → Values invited → Values booked → Values completed → Scorecard filled
2. Values pass → Case study sent → Case study submitted → Debrief invited → Debrief booked → Debrief completed → Panel decision

### Escalation Logic
- **3-14 days stuck at a stage** → ⚠️ Flag badge
- **14+ days stuck at a stage** → 🔴 Urgent badge (moved to top)
- Draft messages generated for FLAG + URGENT candidates only

### Output
Inline HTML email to both Ayesha + Jawwad with:
- Header stat boxes (total positions, urgent count, flagged count)
- Per-position sections
- Candidate rows with stage, days stuck, next action
- Draft messages section (ready for approval and send)

### Color Theme
- Header: **Taleemabad green** (#2e7a4f)
- Primary: **Blue** (#1565c0) — user specified "keep theme bluish... elegant and nice"
- Urgent: **Red** (#c62828)
- Warning: **Amber** (#f57c00)

## Implementation Details

### Key Functions in weekly_pipeline_monitor.py
- `get_open_jobs()` → fetches all active positions from Markaz
- `get_candidates_for_job()` → fetches all shortlisted+ candidates per position
- `check_values_invite_sent()`, `check_case_study_sent()`, `check_debrief_invite_sent()` → Gmail queries
- `check_values_booked()`, `check_debrief_booked()` → Calendar queries
- `classify_candidate()` → determines stage + days_stuck + next_action
- `build_report_html()` → assembles full inline HTML report
- `send_report()` → sends via safe_sendmail() bouncer

### Email Security
- All sends via `safe_sendmail()` with audit logging to `email_audit.log`
- All DB reads logged via `log_db_query()` to `read_audit.log`
- All Gmail reads logged via `log_gmail_read()` to `read_audit.log`
- Error handling: if script crashes, sends error email to Ayesha only

### Task Scheduler
Run once: `python scripts/reports/setup_pipeline_monitor_schedule.py`
This registers:
- `CocoPipelineMonitor_Monday` → 10:30am every Monday
- `CocoPipelineMonitor_Friday` → 3:00pm every Friday

## Non-Negotiable Rules
1. Always cross-check all three sources (DB, Gmail, Calendar)
2. Escalation thresholds fixed: 3 days flag, 14 days urgent
3. All open positions must appear in report
4. All shortlisted+ candidates must appear
5. Days stuck calculated accurately from most recent status change
6. Draft messages only for FLAG + URGENT candidates
7. All candidate names hyperlinked to Drive CVs (where available)
8. Draft message tone must be warm, professional, "we" voice, no em-dashes
9. Both Ayesha and Jawwad get identical FULL report
10. Token refresh on startup (Gmail + Calendar)
11. Graceful error handling with fallback notification

## Recipients
- **TO**: ayesha.khan@taleemabad.com, jawwad.ali@taleemabad.com
- **CC**: hiring@taleemabad.com
- All on safe_sendmail allowlist (@taleemabad.com domain)

## Next Steps
1. **Manual test**: `python scripts/reports/weekly_pipeline_monitor.py`
   - Verify report arrives at both recipients
   - Check email_audit.log and read_audit.log for entries
   - Verify all open positions have sections
   - Verify all shortlisted+ candidates appear
   - Verify escalation badges are correct
2. **Register tasks**: `python scripts/reports/setup_pipeline_monitor_schedule.py`
3. **Verify in Task Scheduler**: `schtasks /query /tn CocoPipelineMonitor*`
4. **Monitor first runs**: check for any errors or missing data

## Files
- **Skill SOP**: c:/Agent Coco/skills/hiring-pipeline-weekly-report.md
- **Main script**: c:/Agent Coco/scripts/reports/weekly_pipeline_monitor.py
- **Setup script**: c:/Agent Coco/scripts/reports/setup_pipeline_monitor_schedule.py
- **Logs**: c:/Agent Coco/logs/email_audit.log + read_audit.log

## Commitment (Coco, 2026-04-10)
I will maintain the automated weekly hiring pipeline monitor. It will run reliably on Monday and Friday, check all open positions across Markaz + Gmail + Calendar, accurately classify each candidate's stage, calculate days stuck, flag at 3 and 14 days, generate draft messages, and send comprehensive reports to both Ayesha and Jawwad. The system will be super solid, with cross-source verification, graceful error handling, and full audit logging. It will help Ayesha's process speed up by constantly surfacing what needs attention.
