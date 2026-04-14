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
- `updated_at` — last status update

**Common queries:**

1. **Pipeline status for a specific job:**
   ```sql
   SELECT a.id, c.name, a.status, a.created_at
   FROM applications a
   JOIN candidates c ON a.candidate_id = c.id
   WHERE a.job_id = [job_id]
   ORDER BY a.status, a.created_at DESC;
   ```

2. **All applications for a specific candidate:**
   ```sql
   SELECT a.id, j.title as position, a.status, a.created_at
   FROM applications a
   JOIN jobs j ON a.job_id = j.id
   WHERE a.candidate_id = [candidate_id];
   ```

---

### Query Type 3: JOB DETAILS & BUDGET

**Purpose:** Pull job description, budget, requirements for screening

**Table:** `jobs`

**Key columns:**
- `id` — job ID
- `title` — job title
- `description` / `jd_text` — full job description
- `min_budget` / `max_budget` — salary range
- `location` — office location
- `status` — job status ('open', 'filled', 'closed', etc.)

**Common query:**

```sql
SELECT id, title, description, min_budget, max_budget, location
FROM jobs
WHERE id = [job_id];
```

---

### Query Type 4: LEAVE & TIME OFF

**Purpose:** Check employee leave/time off records for attendance reporting

**Table:** `leave_requests` OR `time_off`

**Key columns:**
- `employee_id` — link to employees table
- `leave_type` — 'annual', 'sick', 'maternity', etc.
- `start_date` / `end_date` — dates of leave
- `status` — 'approved', 'pending', 'rejected'

**Common query:**

```sql
SELECT employee_id, leave_type, start_date, end_date, status
FROM leave_requests
WHERE start_date = [specific_date]
  AND status = 'approved';
```

---

### Query Type 5: EMPLOYEE ROSTER

**Purpose:** Pull list of all active employees, WFH status, office assignment

**Table:** `employees` OR `payroll`

**Key columns:**
- `id` — employee ID
- `name` — full name
- `email` — employee email
- `office_location` — assigned office
- `employment_type` — 'OPL', 'OWT', 'Intern', etc.
- `wfh_status` — permanent WFH or not
- `status` — 'active', 'inactive', 'terminated'

**Common query:**

```sql
SELECT id, name, email, office_location, employment_type, wfh_status
FROM employees
WHERE status = 'active'
  AND employment_type IN ('OPL', 'OWT')
ORDER BY name;
```

---

### Query Type 6: INTERVIEW & SCORING DATA

**Purpose:** Pull values interview scorecards, case study results, GWC assessments

**Table:** `values_scorecards` OR `application_scores`

**Key columns:**
- `application_id` — link to applications table
- `interviewer` — who conducted interview
- `values` — JSON array of value scores (+, +/-, -)
- `pass_fail` — PASS or OUT
- `gwc_assessment` — GWC data (gets_it, wants_it, capacity)
- `submitted_at` — when scorecard was submitted

**Common query:**

```sql
SELECT a.id, c.name, v.pass_fail, v.gwc_assessment, v.submitted_at
FROM applications a
JOIN candidates c ON a.candidate_id = c.id
JOIN values_scorecards v ON a.id = v.application_id
WHERE a.job_id = [job_id]
ORDER BY v.submitted_at DESC;
```

---

## Audit Logging (MANDATORY)

**Rule:** Every query must be logged to scripts/utils/audit_log.py.

**Method:**
```python
from scripts.utils.audit_log import log_db_query

log_db_query(
    query_type="CV screening",
    table="candidates",
    num_results=42,
    context=f"Job 36 CV screening for position: Senior Engineer"
)
```

**What to log:**
- Query type (CV data, pipeline status, leave records, etc.)
- Table(s) queried
- Number of results returned
- Context (what this query is for, which position, candidate name if specific)

**Why:** Audit trail for data access compliance and debugging.

---

## Non-Negotiable Rules

1. **Read schema first** — Before writing a query, check docs/schema.md for table structure.

2. **MCP only** — Always use MCP for database access. Never direct JDBC/connection strings.

3. **Credentials in .mcp.json only** — Never hardcode credentials. File is in .gitignore.

4. **Read-only access** — Never attempt INSERT, UPDATE, DELETE. Read-only queries only.

5. **Audit every query** — Every database access must be logged.

6. **Cross-check sources** — For important data (candidate names, leave records), verify with multiple sources.

7. **Verify results** — Spot-check query results for accuracy before using in reports.

8. **Handle NULL/missing data** — Don't assume all fields are populated. Handle NULL gracefully.

---

## Common Mistakes

1. **Querying without schema** — Writing SQL without checking table structure first. Always read schema.md.

2. **Hardcoding credentials** — Putting connection strings or passwords in code. Use .mcp.json only.

3. **Forgetting to log** — Running queries without audit logging. Log every access.

4. **Assuming data exists** — Assuming all candidates have all fields populated. Handle missing data.

5. **Wrong table name** — Using "time_off" when table is "leave_requests". Verify table names in schema.

6. **Complex joins without testing** — Writing complex queries without testing on small datasets first.

7. **Not verifying results** — Trusting query results without spot-checking a few rows.

8. **SQL injection risk** — Concatenating user input directly into queries. Use parameterized queries.

---

## Pre-Query Checklist

- [ ] Schema documentation read (docs/schema.md)
- [ ] Table names verified
- [ ] Column names verified
- [ ] Query logic is correct
- [ ] Query tested on small dataset first
- [ ] Results spot-checked for accuracy
- [ ] Audit logging code included
- [ ] No credentials in code
- [ ] MCP used for connection
- [ ] Read-only query (no INSERT/UPDATE/DELETE)

---

## Commitment (Coco, 2026-04-10)

I will read schema.md before writing queries. I will use MCP for all database access. I will never hardcode credentials. I will audit log every query. I will verify results before using in reports. I will handle missing data gracefully. I will keep queries read-only. I will cross-check important data with multiple sources.
