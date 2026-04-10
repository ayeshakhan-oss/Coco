---
name: Database Queries SOP
description: Access PostgreSQL (Neon) for candidates, jobs, budget, leave, employees. 6 query types. Audit logging mandatory. Read-only via MCP.
type: feedback
---

## Objective

Access Taleemabad's candidate, job, budget, and employee data from Neon PostgreSQL for CV screening, attendance reporting, case study evaluation, and hiring decisions.

**Database Type:** PostgreSQL (Neon serverless, read-only via MCP)

**Host:** ep-gentle-glitter-adkkn981.c-2.us-east-1.aws.neon.tech

**Access Method:** MCP (Model Context Protocol, config in .mcp.json — do NOT commit)

---

## Connection Setup (Prerequisites)

### 1. Verify MCP Configuration
- File: `.mcp.json` (project root, NOT version-controlled)
- Contains: PostgreSQL connection string, credentials, host, database name
- **CRITICAL:** Never commit .mcp.json to git. File is in .gitignore.
- **CRITICAL:** Never expose credentials in code. Read from .mcp.json only.

### 2. Verify Schema Documentation
- File: `docs/schema.md`
- Contains: All table names, columns, data types, relationships
- Read this FIRST before writing queries
- If schema is missing or outdated, ask user to regenerate from DB

### 3. Test Connection (One-time setup)
- Run: `python scripts/utils/test_db_connection.py` (if exists) or manually connect via MCP
- Expected: "Connection successful" + list of tables
- If fails: Check credentials in .mcp.json, verify host is reachable, contact user

---

## Common Queries by Purpose (6 Query Types)

### Query Type 1: CANDIDATE CV DATA

**Purpose:** Pull resume text, name, email, application ID for a specific candidate or cohort

**Table:** `candidates`

**Key columns:**
- `id` — candidate ID
- `name` — candidate full name
- `email` — candidate email
- `resume_data` — Base64-encoded PDF resume
- `experience_years` — years of experience
- `current_company` — current employer
- `current_role` — current job title

**Common query patterns:**

1. **Single candidate by name:**
   ```sql
   SELECT id, name, email, resume_data, experience_years, current_role
   FROM candidates
   WHERE name ILIKE '%candidate_name%';
   ```

2. **All candidates for a specific job application:**
   ```sql
   SELECT c.id, c.name, c.email, c.resume_data, c.experience_years, c.current_role
   FROM candidates c
   JOIN applications a ON c.id = a.candidate_id
   WHERE a.job_id = [job_id];
   ```

3. **Candidates with specific experience level:**
   ```sql
   SELECT id, name, email, experience_years, current_role
   FROM candidates
   WHERE experience_years >= [min_years]
   ORDER BY experience_years DESC;
   ```

**Decode Resume:**
- resume_data is Base64-encoded PDF
- Decode in Python: `base64.b64decode(resume_data)` → binary PDF → save to file
- Example: `with open('candidate_cv.pdf', 'wb') as f: f.write(base64.b64decode(resume_data))`

---

### Query Type 2: APPLICATION STATUS & PIPELINE

**Purpose:** Pull application status, screening result, interview history for a candidate

**Table:** `applications`

**Key columns:**
- `id` — application ID
- `candidate_id` — link to candidates table
- `job_id` — link to jobs table
- `status` — pipeline status ('applied', 'shortlisted', 'offer', 'rejected', etc.)
- `created_at` — application date
- `updated_at` — last status change date

**Common query patterns:**

1. **All applications for a candidate:**
   ```sql
   SELECT a.id, a.job_id, a.status, a.created_at, a.updated_at
   FROM applications a
   WHERE a.candidate_id = [candidate_id]
   ORDER BY a.created_at DESC;
   ```

2. **All candidates at a specific pipeline stage:**
   ```sql
   SELECT a.candidate_id, c.name, a.status, a.updated_at
   FROM applications a
   JOIN candidates c ON a.candidate_id = c.id
   WHERE a.job_id = [job_id] AND a.status = 'shortlisted';
   ```

3. **Applications by date range:**
   ```sql
   SELECT a.id, c.name, a.status, a.created_at
   FROM applications a
   JOIN candidates c ON a.candidate_id = c.id
   WHERE a.created_at BETWEEN '[start_date]' AND '[end_date]';
   ```

**Important caveat:** status='offer' means the application is in the offer stage, NOT that an offer was sent. Always verify with Ayesha before asserting a candidate has an offer.

---

### Query Type 3: JOB DESCRIPTIONS & BUDGET

**Purpose:** Pull JD text, budget range, requirements for a job posting

**Table:** `jobs`

**Key columns:**
- `id` — job ID
- `title` — job title
- `description` — full JD text
- `jd_text` — structured JD (may be different field)
- `min_budget` — minimum salary budget
- `max_budget` — maximum salary budget
- `min_experience` — minimum required experience (years)
- `created_at` — job posted date
- `status` — job status ('open', 'closed', 'on hold', etc.)

**Common query patterns:**

1. **Full JD for a specific job:**
   ```sql
   SELECT id, title, description, min_budget, max_budget, min_experience
   FROM jobs
   WHERE id = [job_id];
   ```

2. **All open jobs:**
   ```sql
   SELECT id, title, min_budget, max_budget, min_experience, status
   FROM jobs
   WHERE status = 'open'
   ORDER BY created_at DESC;
   ```

3. **Budget range for screening:**
   ```sql
   SELECT min_budget, max_budget
   FROM jobs
   WHERE id = [job_id];
   ```

---

### Query Type 4: VALUES SCORECARD DATA

**Purpose:** Pull values interview scorecards, ratings, and verdicts for a candidate

**Table:** `values_scorecards` (or similar)

**Key columns:**
- `id` — scorecard ID
- `candidate_id` — link to candidates
- `job_id` — link to jobs
- `rating` — overall verdict (PASS/OUT/CONDITIONAL)
- `values_json` — JSON object with 6 values and ratings
- `gwc_assessment` — GWC (Gets it/Wants it/Capacity) verdict
- `created_at` — scorecard date

**Common query patterns:**

1. **Scorecard for a specific candidate + job:**
   ```sql
   SELECT id, candidate_id, values_json, rating, gwc_assessment, created_at
   FROM values_scorecards
   WHERE candidate_id = [candidate_id] AND job_id = [job_id];
   ```

2. **All PASS candidates for a job:**
   ```sql
   SELECT vs.candidate_id, c.name, vs.values_json, vs.gwc_assessment, vs.created_at
   FROM values_scorecards vs
   JOIN candidates c ON vs.candidate_id = c.id
   WHERE vs.job_id = [job_id] AND vs.rating = 'PASS';
   ```

3. **Values OUT candidates (for warm bench tracking):**
   ```sql
   SELECT c.name, vs.values_json, vs.created_at
   FROM values_scorecards vs
   JOIN candidates c ON vs.candidate_id = c.id
   WHERE vs.job_id = [job_id] AND vs.rating = 'OUT';
   ```

---

### Query Type 5: LEAVE & ATTENDANCE RECORDS

**Purpose:** Pull employee leave records for attendance reporting

**Table:** `leave_records` or `time_off` (depends on schema)

**Key columns:**
- `id` — leave record ID
- `employee_id` — employee (from employees table)
- `leave_type` — 'annual', 'sick', 'maternity', 'unpaid', etc.
- `start_date` — first day of leave
- `end_date` — last day of leave
- `status` — 'approved', 'pending', 'rejected', etc.

**Common query patterns:**

1. **Leave records for a specific date:**
   ```sql
   SELECT employee_id, leave_type, start_date, end_date
   FROM leave_records
   WHERE start_date <= '[report_date]' AND end_date >= '[report_date]'
   AND status = 'approved';
   ```

2. **All leave in a date range:**
   ```sql
   SELECT employee_id, leave_type, start_date, end_date
   FROM leave_records
   WHERE start_date BETWEEN '[start_date]' AND '[end_date]'
   AND status = 'approved';
   ```

---

### Query Type 6: EMPLOYEE ROSTER & PAYROLL

**Purpose:** Pull active employee list (OPL+OWT payroll) for attendance baseline

**Table:** `employees` or `payroll`

**Key columns:**
- `id` — employee ID
- `name` — full name
- `email` — email address
- `department` — org unit (OPL, OWT, NIETE, etc.)
- `status` — 'active', 'on leave', 'on severance', 'terminated', etc.
- `employment_date` — hire date
- `wfh_status` — 'permanent_wfh', 'flexible', 'onsite_only', etc.

**Common query patterns:**

1. **All active OPL+OWT employees:**
   ```sql
   SELECT id, name, email, department, wfh_status
   FROM employees
   WHERE department IN ('OPL', 'OWT')
   AND status = 'active';
   ```

2. **Count active employees:**
   ```sql
   SELECT COUNT(*) as total_active
   FROM employees
   WHERE department IN ('OPL', 'OWT')
   AND status = 'active';
   ```
   Expected: 84 (as of 2026-04-09)

3. **Permanent WFH employees:**
   ```sql
   SELECT id, name, email
   FROM employees
   WHERE wfh_status = 'permanent_wfh'
   AND status = 'active';
   ```

---

## Result Handling (After Query)

### 1. Parse Results
- Query returns rows (list of dicts in most Python DB libraries)
- Iterate: `for row in results: print(row['column_name'])`

### 2. Handle Null/Missing Data
- If a column is NULL, check query logic. Don't assume.
- If required data is missing, flag to user
- Never fill in gaps with assumptions

### 3. Decode Base64 Data (Resumes)
- resume_data is Base64-encoded
- Decode: `base64.b64decode(resume_data)`
- Save to file: `with open('output.pdf', 'wb') as f: f.write(decoded_bytes)`

### 4. Parse JSON Data (Values Scorecard, etc.)
- Some columns store JSON (e.g., values_json)
- Parse: `json.loads(values_json_string)` → dict
- Access: `values_dict['Don't Walk Away']` → rating

### 5. Format Results for Output
- If generating report, format results into tables/sections
- If sending email, format into HTML or markdown
- Always cite the DB query in comments (for audit trail)

---

## Audit & Logging (Non-Negotiable)

### 1. Log Every Query
- Import: `from scripts.utils.audit_log import log_db_query`
- After query executes: `log_db_query(query_text, row_count, purpose)`
- Example:
  ```python
  results = db.query("SELECT * FROM candidates WHERE id = 123")
  log_db_query(
      query_text="SELECT * FROM candidates WHERE id = 123",
      row_count=len(results),
      purpose="CV screening for Job 35"
  )
  ```

### 2. Log Output Location
- All logs go to: `logs/read_audit.log`
- Format: timestamp | query type | row count | purpose | user
- Example: `2026-04-10 14:32:15 | db_query | SELECT candidates | 1 row | CV screening Job 35 | Coco`

### 3. Purpose Field (Required)
- Always specify WHY you're querying
- Examples: "CV screening Job 35", "Attendance report 9 Apr 2026", "Values scorecard lookup"
- Never leave purpose blank

### 4. Row Count (Required)
- Log how many rows were returned
- Large result sets (>100 rows) warrant investigation
- If expecting 1 row but got 0 or 10+, flag it

---

## Non-Negotiable Rules

1. **Read-only access only** — never INSERT, UPDATE, DELETE. All changes go through Ayesha/Markaz UI.

2. **Never commit credentials** — .mcp.json is in .gitignore. If credentials are exposed, rotate immediately.

3. **Always verify schema first** — before writing a query, check docs/schema.md. If field name is wrong, query fails silently or returns NULL.

4. **Log every query** — no exceptions. audit_log.py is mandatory. Unlogged queries bypass security monitoring.

5. **Handle NULL data gracefully** — don't assume data exists. Check for NULL before using.

6. **Never assume data consistency** — just because the schema says a column is there doesn't mean it's populated. Query first, then use.

7. **Decode Base64 carefully** — resize CV PDFs if they're >10MB (may crash email). Test file size before attaching.

8. **Never expose candidate data in logs or emails** — logs should show row counts, not names. Never commit output files with candidate data to git.

9. **Batch queries when possible** — instead of querying one candidate at a time, pull a cohort and iterate. Reduces DB load.

10. **Verify results before using** — if a query returns 0 rows when you expected 10, investigate before assuming candidates don't exist.

---

## Common Mistakes

1. **Field name wrong** — queried `candidate_resume` instead of `resume_data`. Query returns NULL. Check schema.

2. **Case sensitivity** — queried `Candidates` instead of `candidates`. PostgreSQL is case-sensitive for unquoted identifiers. Use lowercase.

3. **Missing WHERE clause** — queried `SELECT * FROM candidates` without a filter. Returns all 1000+ candidates. Use WHERE to narrow.

4. **Forgot to log query** — queried DB for attendance data but didn't call log_db_query(). Unauditable. Always log.

5. **Assumed data exists** — queried resume_data for a candidate, got NULL. Assumed PDF was missing. Actually, resume wasn't uploaded. Check first.

6. **Used wrong table** — queried `applications` for leave records instead of `leave_records` table. Wrong results. Read schema carefully.

7. **Decoded Base64 wrong** — forgot to call base64.b64decode(). Tried to save the Base64 string as a PDF. File is corrupted. Always decode.

8. **Joined tables incorrectly** — queried candidates + applications but didn't specify join condition. Got cross-product. Use proper JOIN ON.

9. **Status value typo** — queried WHERE status = 'shortlisted' but DB uses 'shortlist' (no 'd'). No results. Check exact value.

10. **Didn't test on sample first** — wrote complex query for 1000 candidates without testing on 5. Query runs out of memory. Test with LIMIT first.

---

## Step-by-Step Workflow

1. **Understand the question** — what data do you need and why? (e.g., "I need all CV texts for Job 35 candidates")

2. **Check schema** — open docs/schema.md. Find relevant tables and columns.

3. **Write query** — use a common pattern from this guide or adapt one.

4. **Test on sample** — add LIMIT 5 to the query. Run it. Check results make sense.

5. **Remove LIMIT** — run full query (without LIMIT 5).

6. **Check row count** — how many rows? Expected? Unexpected?

7. **Parse results** — iterate through rows, extract needed columns, decode Base64 if needed.

8. **Log the query** — call log_db_query() with query_text, row_count, purpose.

9. **Use results** — feed into next step (screening, report generation, email, etc.).

10. **Verify output** — does the final output (report/email) reflect the query results correctly?

---

## Reference

**Database connection module:** scripts/utils/database_connection.py (or similar) — handles MCP setup, connection pooling, error handling

**Audit log module:** scripts/utils/audit_log.py — log_db_query() and log_gmail_read() functions

**Example CV screening query:** scripts/jobs/job35/screening_job35.py (or any screening script) — shows SELECT candidates + applications + resume_data pattern

**Example attendance query:** scripts/reports/attendance_9apr2026_exact.py — shows SELECT employees + leave_records + cross-check pattern

**Database schema:** docs/schema.md — comprehensive table reference (regenerate if outdated)

---

## When to Escalate to User

- Schema in docs/schema.md doesn't match actual DB columns → ask user to regenerate docs/schema.md
- Query returns 0 rows when you expect results → ask user to verify data exists in DB
- MCP connection fails → ask user to check .mcp.json credentials and host
- Query is slow (>5 seconds) on small dataset → ask user if DB needs optimization
- Permission denied error on a table → ask user to check read-only access in MCP config

---

## Commitment (Coco, 2026-04-10)

I will check schema first. I will log every query. I will handle NULL data gracefully. I will never expose credentials. I will batch queries when possible. I will verify results before using. I will decode Base64 carefully. I will test on sample before running full query.
