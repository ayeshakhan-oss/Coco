# Scripts & Utilities Context

**When to load this file:** You're writing Python scripts for database queries, email operations, report generation, or API integration.

---

## What You're Building Here

Scripts in this folder handle:
- **Database operations** — PostgreSQL (Neon) queries: Talent Acquisition + HR/Markaz schemas
- **Email operations** — Safe sendmail bouncer, Gmail API reads, audit logging
- **Report generation** — ReportLab PDFs (landscape A4), HTML email templates
- **API integration** — Teams presence channel reading (Microsoft Graph), LinkedIn/Google searches

---

## Critical Technical Rules

### Database Access
- **Always use MCP** — `mcp__neon-postgres__query()` for reads
- **Read-only discipline** — Never write or modify; log all queries via audit_log.py
- **Schema context:**
  - **Talent Acquisition:** candidates, job_positions, evaluations, scorecards, sourcing_records
  - **HR/Markaz:** leave_requests, employees, payroll, attendance, org_structure
- **Connection:** Neon PostgreSQL via .env `DATABASE_URL` (never commit)
- **Audit logging:** MANDATORY — Every query logged with user, timestamp, query text, rows returned

### Email Operations
- **Safe bouncer:** Use `safe_sendmail()` from audit_log.py (never call smtplib directly)
- **Read audit:** Use `log_gmail_read()` before accessing Gmail API
- **Approval gate:** Always pilot to Ayesha before sending to candidates
- **Credentials:** Gmail API token in `token_gmail.json` (stored securely, never commit)
- **Threading:** In-Reply-To + References headers required for proper Gmail threading (see [memory/feedback_gmail_thread_reply.md](../memory/feedback_gmail_thread_reply.md))

### Report Generation
- **Format:** ReportLab for PDFs (landscape A4)
- **Text alignment:** Use `TA_JUSTIFY` on all body paragraph styles (non-negotiable)
- **HTML emails:** Table-based layout (Gmail-safe), colors via hex codes
- **Templates:** Reference locked formats in [templates/](../templates/) and memory/

### API Integration
- **Teams API:** Microsoft Graph API reader in `utils/teams_reader.py`
  - Reads presence channel for attendance updates
  - Query result must be verified against ground truth (no suspiciously small result sets)
  - See [memory/discipline_failure_teams_api_incomplete.md](../memory/discipline_failure_teams_api_incomplete.md)
- **LinkedIn:** Use Google site:linkedin.com searches (no direct API)
- **Google Sheets:** OAuth2 credentials in `token_sheets.json` (readonly scope)

---

## Folder Structure

```
scripts/
├── CLAUDE.md (this file)
├── setup/
│   ├── setup_sheets_token.py — OAuth token generation for Google Sheets
│   └── setup_pipeline_monitor_schedule.py — Cron job setup
├── utils/
│   ├── audit_log.py — Logging bouncer: safe_sendmail(), log_gmail_read(), log_db_query()
│   ├── teams_reader.py — Teams presence API reader
│   ├── read_employee_sheet.py — Google Sheets employee count reader
│   └── [other utilities]
├── jobs/
│   ├── job32/ — Fundraising & Partnerships Manager
│   ├── job35/ — Product Designer
│   ├── job36/ — Backend Engineer
│   └── job26/ — Soul Architect (completed)
├── reports/
│   ├── attendance_*.py — Daily attendance report scripts
│   ├── send_*.py — Report delivery scripts
│   └── [other report generators]
└── sourcing/
    ├── soul_architect_sourcing_*.py — Talent sourcing scripts
    └── AUTOMATION_GUIDE.md — Sourcing workflow documentation
```

---

## Common Script Patterns

### Database Query Pattern
```python
from mcp__neon_postgres import query

result = query(
    "SELECT * FROM candidates WHERE job_id = ? AND status = ?",
    (job_id, 'screening')
)
log_db_query('SELECT candidates', len(result))
```

### Email Send Pattern
```python
from audit_log import safe_sendmail

success = safe_sendmail(
    to='ayesha.khan@taleemabad.com',
    subject='Screening Report',
    body=html_body,
    pilot=True  # Always pilot first
)
log_email_send(to_addr, len(recipients))
```

### Report Generation Pattern
```python
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.enum.text import TA_JUSTIFY

style = ParagraphStyle(
    name='Body',
    alignment=TA_JUSTIFY,  # MANDATORY
    fontName='Helvetica',
    fontSize=11
)
```

---

## Key Dependencies

| Module | Purpose | Notes |
|--------|---------|-------|
| `google.oauth2.credentials` | Google API auth | Token refresh handled by auth modules |
| `googleapiclient.discovery` | Google Sheets + Gmail API | Readonly + audit logging |
| `reportlab.platypus` | PDF generation | Always use TA_JUSTIFY |
| `requests` | HTTP calls for LinkedIn/Google | Verify ground truth before reporting |
| `python-dotenv` | Environment variables | .env file (never commit) |

---

## Testing Before Running

1. **Syntax check:** `python -m py_compile scripts/your_script.py`
2. **Import test:** Run script imports without executing main logic
3. **Pilot mode:** Always send reports to Ayesha first (set `pilot=True`)
4. **Verify output:** Spot-check PDF, HTML, and database results before sending live

---

## Common Mistakes (By Script Type)

### Database Queries
- ✗ Using direct psycopg2 instead of MCP
- ✗ Forgetting audit logging
- ✗ Trusting API results without verification (Teams API can return incomplete data)
- ✓ Solution: Always use MCP + log_db_query(). Verify results with ground truth.

### Email Scripts
- ✗ Calling smtplib directly instead of safe_sendmail()
- ✗ Skipping pilot to Ayesha
- ✗ Missing In-Reply-To headers for threading
- ✓ Solution: Use safe_sendmail(), always pilot, add threading headers.

### PDF Reports
- ✗ Using TA_LEFT instead of TA_JUSTIFY
- ✗ Fabricating data to fill stat boxes
- ✗ Forgetting to hyperlink candidate CVs
- ✓ Solution: Use TA_JUSTIFY always. Verify data from database. Check hyperlinks before sending.

### Sourcing Scripts
- ✗ Using only Google search (missing org pages + LinkedIn layers)
- ✗ Adding candidates to Markaz without verification
- ✗ Not verifying LinkedIn links are active
- ✓ Solution: Execute all 7 steps in sequence. Verify before Markaz insert.

---

## Reference Memory Files

- [memory/project_teams_integration.md](../memory/project_teams_integration.md) — Teams API setup + known issues
- [memory/discipline_failure_teams_api_incomplete.md](../memory/discipline_failure_teams_api_incomplete.md) — When API results are suspiciously small, verify with ground truth
- [memory/project_security_hardening.md](../memory/project_security_hardening.md) — Token monitoring, scope auditing
- [memory/feedback_gmail_thread_reply.md](../memory/feedback_gmail_thread_reply.md) — Threading header requirements

---

## Current Active Scripts

| Job | Status | Scripts |
|-----|--------|---------|
| Job 32 (Fundraising) | In Progress | send_job32_decision_brief_pilot.py |
| Job 35 (Product Designer) | Complete | decision brief sent live |
| Job 36 (Backend Engineer) | Complete | decision brief sent live |
| Job 26 (Soul Architect) | Complete | soul_architect_screening_pilot_2026-04-20_FINAL.html |
| Hackathon GWC | In Review | 6 warm-tone rejection emails (awaiting approval) |

---

## Credential Files

| File | Purpose | Scope | Updated |
|------|---------|-------|---------|
| `.env` | Database URL + API keys | Never commit | As needed |
| `token_gmail.json` | Gmail API refresh token | readonly | Refreshed per session |
| `token_sheets.json` | Google Sheets API token | readonly | Setup script refreshes |
| `data/credentials.json` | OAuth client credentials | OAuth flow setup | 2026-05-08 (new) |

---

**Scope:** Progressive disclosure L2 — Load this file when working in scripts/ folder  
**Updated:** 2026-05-08  
**Owner:** Coco
