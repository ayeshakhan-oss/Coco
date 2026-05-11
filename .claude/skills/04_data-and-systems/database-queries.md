---
name: database-queries
description: Database queries via MCP (never direct psycopg2). Audit logging mandatory. Result verification required. Query templates for common operations.
compatibility: Requires MCP neon-postgres, audit logging, RULES.md Integration Rules
---

# Database Queries

Execute database queries via MCP only (never direct connection). Mandatory audit logging. Verify results against ground truth.

---

## When to Use This Skill

Trigger this skill when:
- User asks for "database query" or "data from Markaz"
- Need candidate data, staging data, leave requests
- Query must use MCP (never direct psycopg2)
- Audit logging required

---

## Related SOP

**Location:** `SOPs/04_Data_and_Systems/database_queries.md`

---

## Universal Rules

**Connection Method (Non-Negotiable):**
- ALWAYS use MCP (`mcp__neon-postgres__query()`)
- NEVER use direct psycopg2
- NEVER use custom connections

**Audit Logging (Mandatory):**
- Every query logged: `log_db_query(description, row_count)`
- Timestamp, user, query text, rows returned
- Log file: `logs/db_query_audit.log`

**Result Verification:**
- Small result sets (<5 rows) require manual verification
- Cross-reference with other sources
- Flag suspicious results

**Common Queries:**
- Candidate data from candidates table
- Leave requests from leave_requests table
- Application status from applications table
- Staging data from any relevant table

---

## Detailed Procedure

**Prerequisites (Complete in Order):**
1. Verify MCP configuration in `.mcp.json` (contains PostgreSQL connection string)
2. Read `docs/schema.md` for table names, columns, data types
3. Test connection: run `python scripts/utils/test_db_connection.py` (verify "Connection successful")
4. Set up audit logging: import `from scripts.utils.audit_log import log_db_query`

**6 Common Query Types:**

**Type 1 — Candidate CV Data:**
- Purpose: Pull resume text, name, email, application ID
- Table: `candidates`
- Key columns: id, name, email, resume_data (Base64-encoded), experience_years, current_role
- Decode: `base64.b64decode(resume_data)` → save as PDF
- Example: `SELECT id, name, email, resume_data FROM candidates WHERE name ILIKE '%name%'`

**Type 2 — Application Status & Pipeline:**
- Purpose: Pull application status, screening result, interview history
- Table: `applications` + JOIN `candidates`
- Key columns: id, candidate_id, job_id, status ('applied', 'shortlisted', 'offer', 'rejected')
- Example: `SELECT a.id, c.name, a.status FROM applications a JOIN candidates c ON a.candidate_id = c.id WHERE a.job_id = [job_id]`

**Type 3 — Job Details & Budget:**
- Purpose: Pull job description, budget, requirements
- Table: `jobs`
- Key columns: id, title, description, min_budget, max_budget, location, status
- Example: `SELECT id, title, description, min_budget, max_budget FROM jobs WHERE id = [job_id]`

**Type 4 — Leave & Time Off:**
- Purpose: Check employee leave/time off records for attendance
- Table: `leave_requests`
- Key columns: employee_id, leave_type ('annual', 'sick', 'maternity'), start_date, end_date, status ('approved', 'pending', 'rejected')

**Type 5 — Employee Roster:**
- Purpose: Pull list of active employees, WFH status, office assignment
- Table: `employees`
- Key columns: id, name, email, office_location, employment_type ('OPL', 'OWT'), wfh_status, status ('active', 'inactive')

**Type 6 — Interview & Scoring Data:**
- Purpose: Pull values interview scorecards, case study results, GWC assessments
- Table: `values_scorecards` + JOIN `applications`
- Key columns: application_id, interviewer, values (JSON array), pass_fail, gwc_assessment

**Audit Logging (Every Query):**
```python
from scripts.utils.audit_log import log_db_query
log_db_query(
    query_type="CV screening",
    table="candidates",
    num_results=42,
    context=f"Job 36 CV screening: Senior Engineer"
)
```

**Non-Negotiable Rules:**
1. Read schema FIRST before writing queries
2. Always use MCP (never direct psycopg2)
3. Never hardcode credentials (use .mcp.json only)
4. Always use read-only queries (no INSERT/UPDATE/DELETE)
5. Audit every query
6. Cross-check important data with multiple sources
7. Verify results before using in reports
8. Handle NULL/missing data gracefully

---

## Execution Discipline

1. Read the MCP documentation
2. Construct query (SELECT with proper WHERE)
3. Execute via MCP (`mcp__neon-postgres__query()`)
4. Log result: `log_db_query(description, row_count)`
5. Verify result (small set? cross-check)
6. Return data

---

## Success Criteria

✅ Used MCP (not direct DB)  
✅ Audit logging in place  
✅ Results verified (ground truth)  
✅ No hardcoded queries  

**Status:** ✅ PRODUCTION READY
