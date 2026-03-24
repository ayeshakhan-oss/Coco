# Database Schema — Taleemabad HRIS (Neon PostgreSQL)

Last updated: 2026-02-26

## Core Tables for Talent Acquisition

---

### `candidates`
Stores candidate profiles. CVs are stored as Base64-encoded PDFs in `resume_data`.

| Column | Type | Notes |
|--------|------|-------|
| id | integer | Primary key |
| first_name | text | NOT NULL |
| last_name | text | NOT NULL |
| email | varchar | NOT NULL |
| phone | varchar | |
| resume_data | text | **Base64-encoded PDF** — must decode then parse |
| resume_file_name | text | Original filename |
| resume_mime_type | varchar | e.g. application/pdf |
| position | text | Position applied for |
| skills | ARRAY | Skills array (often NULL — extracted from resume) |
| experience | text | Experience description |
| education | text | Education description |
| location | text | |
| current_position | text | Current job title |
| current_company | text | Current employer |
| linkedin_url | text | |
| source | varchar | How they found the role |
| ai_skill_match_score | integer | Pre-existing AI score (often NULL) |
| ai_education_summary | text | Pre-existing AI education summary |
| ai_experience_highlights | text | Pre-existing AI highlights |
| ai_analyzed_at | timestamp | When AI last analyzed this candidate |
| assessment_score | integer | Score from any assessment taken |
| questions_answered | jsonb | Answers to screening questions |
| created_at | timestamp | |

**Current counts (2026-02-26):** 1,135 candidates, 997 with resume_data

---

### `jobs`
Stores open positions. Contains JD text and budget range.

| Column | Type | Notes |
|--------|------|-------|
| id | integer | Primary key |
| job_id | varchar | NOT NULL — human-readable ID |
| title | text | Job title NOT NULL |
| department | varchar | |
| description | text | Job description NOT NULL |
| jd_text | text | Full JD text — **use this for screening** (sometimes NULL — fall back to description) |
| required_skills | ARRAY | Required skills list |
| min_budget | numeric | **Salary budget minimum (PKR)** — often NULL, needs filling |
| max_budget | numeric | **Salary budget maximum (PKR)** — often NULL, needs filling |
| currency | varchar | Default: PKR |
| job_status | varchar | 'Active', 'Closed' — filter WHERE job_status = 'Active' |
| status | varchar | Secondary status field |
| hiring_manager | varchar | **User ID** — join to users.id to get email |
| poc_person | varchar | Point of contact |
| work_type | varchar | Remote/On-site/Hybrid |
| employment_type | varchar | Full-time/Part-time/Contract |
| priority | varchar | |
| published_at | timestamp | |
| created_at | timestamp | |

**IMPORTANT:** Most jobs have NULL min_budget/max_budget. These must be filled in before budget screening can work.

---

### `applications`
Links candidates to jobs. **AI screening results are written here.**

| Column | Type | Notes |
|--------|------|-------|
| id | integer | Primary key |
| candidate_id | integer | FK → candidates.id |
| job_id | integer | FK → jobs.id |
| status | varchar | Current application status |
| stage | varchar | Pipeline stage |
| applied_at | timestamp | |
| cover_letter | text | |
| notes | text | HR notes |
| **ai_jd_score** | numeric | **WRITE: JD match score (0–100)** |
| **ai_jd_analysis** | text | **WRITE: Detailed JD match analysis** |
| **ai_budget_fit** | boolean | **WRITE: true if within budget** |
| **ai_overall_score** | numeric | **WRITE: Composite score (0–100)** |
| **ai_recommendation** | varchar | **WRITE: 'shortlist', 'consider', 'discard'** |
| **ai_screening_summary** | text | **WRITE: Full screening summary** |
| **ai_screened_at** | timestamp | **WRITE: Timestamp of AI screening** |
| **values_scorecard** | jsonb | **WRITE: Full values scorecard JSON** — see memory/values_scorecard_db_write.md |
| **values_interview_result** | varchar | **WRITE: `'pass'` or `'fail'`** |
| **values_interview_date** | timestamp | **WRITE: Date of values interview** |
| **values_interviewer_name** | varchar | **WRITE: Host name** |
| values_interview_score | integer | Values interview score (optional) |
| values_interview_notes | text | Values interview notes (optional) |
| **gwc_scorecard** | jsonb | **WRITE: GWC scorecard JSON** |
| gwc_interview_result | varchar | GWC interview result |
| gwc_interview_score | integer | GWC interview score |
| gwc_interview_date | timestamp | GWC interview date |
| gwc_interviewer_name | varchar | GWC interviewer name |
| rejection_reason | text | |

**Current counts (2026-02-26):** 1,352 applications — 154 AI-screened, 1,198 pending

---

### `users`
Taleemabad employees. Used to look up hiring manager emails.

| Column | Type | Notes |
|--------|------|-------|
| id | varchar | Primary key (format: user-XXXX) |
| email | varchar | **Use this to send reports** |
| first_name | varchar | |
| last_name | varchar | |
| role | varchar | 'Employee', 'Line Manager', etc. |

---

## Key Queries

### Get all active jobs with budget and JD
```sql
SELECT j.id, j.title, j.department, j.jd_text, j.description,
       j.required_skills, j.min_budget, j.max_budget, j.currency,
       u.email as hiring_manager_email, u.first_name as hm_first_name
FROM jobs j
LEFT JOIN users u ON j.hiring_manager = u.id
WHERE j.job_status = 'Active'
ORDER BY j.created_at DESC;
```

### Get all unscreened applications for a job
```sql
SELECT a.id as application_id,
       c.first_name, c.last_name, c.email, c.phone,
       c.resume_data, c.skills, c.experience, c.education,
       c.current_position, c.current_company, c.location
FROM applications a
JOIN candidates c ON a.candidate_id = c.id
WHERE a.job_id = $1
  AND a.ai_screened_at IS NULL
ORDER BY a.applied_at DESC;
```

### Write AI screening results back to DB
```sql
UPDATE applications
SET ai_jd_score = $1,
    ai_jd_analysis = $2,
    ai_budget_fit = $3,
    ai_overall_score = $4,
    ai_recommendation = $5,
    ai_screening_summary = $6,
    ai_screened_at = NOW()
WHERE id = $7;
```

## CRITICAL NOTES
1. `resume_data` is **Base64-encoded PDF** — decode with Python before reading
2. `hiring_manager` in jobs is a **user ID** — always join to users table for email
3. Most jobs have **NULL budget** — flag these; budget screening is skipped until filled
4. If `jd_text` is NULL, fall back to `description` for JD content
5. Existing `ai_overall_score = 0.0` entries were from a previous broken implementation — re-screen them
