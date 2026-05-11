---
name: data-and-systems
description: Manage backend systems for data access, security, and reporting infrastructure. Covers database queries, email notification systems, report generation, data analysis, and security protocols. All system work requires MCP (no direct DB access), audit logging, API verification, and OAuth token management.
compatibility: Requires MCP neon-postgres, audit_log.py, Teams API, Google APIs, safe_sendmail bouncer
---

# Data and Systems

Manage backend infrastructure for database queries, email systems, reporting, analytics, and security protocols.

---

## When to Use This Skill

Trigger this skill when:
- User asks for "database query" or "data from Markaz"
- User requests "email system setup" or "Gmail configuration"
- User wants "generate report" or "data analysis"
- User needs "security audit" or "token refresh"
- System configuration, API integration, or infrastructure work

---

## Related SOPs

All system SOPs fall under this skill:

1. **Database Queries** — `SOPs/04_Data_and_Systems/database_queries.md`
   - MCP only (never direct psycopg2)
   - Audit logging mandatory (log_db_query)
   - Query templates for common operations
   - Candidate data, staging, leave requests

2. **Email Notification** — `SOPs/04_Data_and_Systems/email_notification.md`
   - safe_sendmail() bouncer (never smtplib)
   - Pilot mode first (set pilot=True)
   - Threading headers for replies (In-Reply-To)
   - Audit logging (log_email_send)
   - .env credentials (never hardcoded)

3. **Report Generation** — `SOPs/04_Data_and_Systems/report_generation.md`
   - ReportLab for PDF generation
   - HTML email templates
   - Dynamic data insertion
   - Export to spreadsheet/JSON

4. **Data Analysis** — `SOPs/04_Data_and_Systems/data-analysis.md`
   - Query data with verification
   - Cross-reference multiple sources
   - Generate insights and trends
   - Document methodology

5. **Database Connection** — `SOPs/04_Data_and_Systems/database-connection.md`
   - Token refresh procedures
   - Connection pooling
   - Error handling and retry logic
   - Monitoring connection health

6. **Security** — `SOPs/04_Data_and_Systems/security.md`
   - OAuth token security
   - Credential management
   - Git secrets scanning
   - Audit trail maintenance

---

## Universal Rules (All Systems)

**Database Access:**
- ALWAYS use MCP (`mcp__neon-postgres__query()`)
- NEVER use direct psycopg2 or custom connections
- Audit logging mandatory: `log_db_query(description, row_count)`
- Verify results against ground truth (small result sets = red flag)

**Email Systems:**
- ALWAYS use `safe_sendmail()` bouncer
- NEVER use smtplib directly
- Pilot first: set `pilot=True`
- Credentials from `.env` (never hardcoded)
- Audit logging: `log_email_send()`
- Threading headers for replies: In-Reply-To + References

**API Integration:**
- Third-party results verified against database
- Small result sets (<5) trigger manual verification
- OAuth tokens refreshed before expiry
- Fallback plan if API unavailable

**Security:**
- Never commit credentials (.env, token files)
- .gitignore enforced (check before push)
- Tokens in `.claude/config/` (not root)
- Git secrets scanning enabled (GitHub push protection)
- Audit logs saved and searchable

**Audit Logging (MANDATORY):**
- Every DB query logged: timestamp, user, query text, rows returned
- Every email sent logged: recipient, timestamp, subject, purpose
- Query audit file: `logs/db_query_audit.log`
- Email audit file: `logs/email_audit.log`

**Self-QA Before Deploying:**
- [ ] Using MCP (not direct DB)
- [ ] Audit logging in place
- [ ] Results verified (ground truth)
- [ ] OAuth tokens current (not expired)
- [ ] .env properly excluded (.gitignore)
- [ ] No hardcoded credentials
- [ ] Error handling implemented
- [ ] Fallback plan documented

---

## Execution Discipline

**STEP 1: IDENTIFY SYSTEM TASK**
- Database query, email system, report generation, analysis, or security?

**STEP 2: READ SYSTEM SOP**
- RULES.md: Integration & Testing Rules (lines 446-526)
- MEMORY.md: Specific system SOP for task
- Audit file: Check prior queries/emails (audit_log.py)

**STEP 3: PREPARE CREDENTIALS**
- Check .env for email credentials
- Verify OAuth tokens current (not expired)
- Check token files in `.claude/config/`
- Refresh if needed: `setup_sheets_token.py`, `setup_gmail_labels.py`

**STEP 4: WRITE SYSTEM CODE**
- Database: MCP query with structured results
- Email: safe_sendmail with pilot mode
- Report: ReportLab or HTML template with data binding
- Analysis: Query → cross-reference → document methodology

**STEP 5: IMPLEMENT AUDIT LOGGING**
- DB queries: `log_db_query(description, row_count)`
- Email sends: `log_email_send(to, subject, purpose)`
- Save to logs/ folder
- Include timestamp and user

**STEP 6: VERIFY RESULTS**
- Small DB result sets? Manual verification required
- API call successful? Cross-check with database
- Email sent? Check audit log and recipient confirmation
- No assumptions (flag discrepancies)

**STEP 7: TEST (LOCAL)**
- Compile: `python -m py_compile script.py`
- Run: Test function calls with sample data
- Verify: Check audit logs, database records, emails

**STEP 8: DEPLOY WITH CAUTION**
- Pilot email first (set pilot=True)
- Log all queries (audit mandatory)
- Monitor for errors
- Document any API failures

---

## Common Mistakes (Do Not Repeat)

| Mistake | Why It's Wrong | Fix |
|---------|---|---|
| Direct psycopg2 connection | Bypasses auditing, not approved | Use MCP only |
| smtplib instead of safe_sendmail | No pilot protection, untracked | Use safe_sendmail bouncer |
| Small API result assumed complete | Misses data (Teams example: 1 result but 5 in Markaz) | Verify with ground truth manually |
| No audit logging | No accountability trail | Log every query and email send |
| Hardcoded credentials | Exposes secrets in code | Use .env file always |
| OAuth token expired | API calls fail silently | Check expiry, refresh before use |
| Skipping token refresh | App loses permission | Run setup script before each session |
| No error handling | Script crashes ungracefully | Add try/except with fallback |
| Forgetting .env in .gitignore | Credentials committed to git | Verify .gitignore before push |
| No fallback if API down | Report generation fails | Build fallback (cached data, error message) |

---

## Success Criteria

✅ Using MCP (not direct DB connection)  
✅ Audit logging in place (DB and email)  
✅ Results verified (ground truth checked)  
✅ OAuth tokens current (not expired)  
✅ .env excluded from git (.gitignore)  
✅ No hardcoded credentials in code  
✅ Error handling implemented  
✅ Fallback plan for API unavailability  
✅ Pilot tested (email systems)  
✅ All 8-item checklist items pass  

---

## Resources & Templates

**Reference Scripts:**
- Audit logging: `scripts/utils/audit_log.py`
- Teams reader: `scripts/utils/teams_reader.py`
- Report generator: `scripts/utils/report_generator.py`
- Attendance report: `scripts/reports/attendance_20apr2026.py`

**Configuration:**
- Credentials: `.env` (gitignored)
- Tokens: `.claude/config/token*.json` (gitignored)
- OAuth setup: `setup_gmail_labels.py`, `setup_sheets_token.py`

**Rules:**
- Core Discipline: `RULES.md` (Rules 1-7)
- Integration Rules: `RULES.md` (lines 446-526)
  - Database Rules (lines 449-469)
  - Email Rules (lines 472-500)
  - API Rules (lines 503-525)

---

## Commit to Discipline

I will manage systems and data with:
- ✅ MCP only (never direct DB)
- ✅ Audit logging on all queries and emails
- ✅ Results verified (ground truth)
- ✅ OAuth tokens current
- ✅ .env protected (.gitignore)
- ✅ No hardcoded credentials
- ✅ Error handling implemented
- ✅ Fallback plans in place

**Status:** ✅ PRODUCTION READY
