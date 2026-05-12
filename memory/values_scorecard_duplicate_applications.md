---
name: Values Scorecard — Duplicate Application Records Issue
description: When submitting values scorecards, always verify which application record is being displayed in the Markaz UI. Multiple records can exist for the same candidate on the same job.
type: feedback
---

# VALUES SCORECARD SUBMISSION — DUPLICATE APPLICATION DETECTION

**Locked In:** 2026-05-12  
**Severity:** HIGH — Submission appears to fail silently  
**Prevention:** MANDATORY check before submitting

---

## The Problem

When submitting a values scorecard to Markaz, the form may appear empty even after successful database submission. This happens when:

**Two or more application records exist for the same candidate on the same job:**

Example (Laiba Ahmad, Job 20 - SPM):
```
Application 1389 → Stage: Right Seat | Last Updated: 2026-03-25 | Data: ✅ Scorecard filled
Application 2708 → Stage: Applied   | Last Updated: 2026-05-09 | Data: ❌ EMPTY
```

The **Markaz UI displays the most recently updated record** (2708). If you submit to the older record (1389), the form appears blank.

---

## The Solution (SOP Step 0: Pre-Submission Verification)

**BEFORE running any scorecard submission script:**

1. **Query the database** to find ALL application records for this candidate + job:
   ```sql
   SELECT id, status, stage, values_interview_date, updated_at 
   FROM applications 
   WHERE candidate_id = [CANDIDATE_ID] AND job_id = [JOB_ID] 
   ORDER BY updated_at DESC
   ```

2. **Identify the most recently updated record** — that's the one the UI is displaying

3. **Check which record is empty:**
   - If the most recent has `values_scorecard = NULL` → submit to that one
   - If an older record has the scorecard → you're looking at a stale record

4. **Submit to the correct record** — the one being displayed in Markaz UI

---

## How to Apply This

### Quick Verification Script Pattern

```python
# Before submitting scorecard:
conn.execute("SELECT id, updated_at, values_scorecard FROM applications WHERE candidate_id = X AND job_id = Y ORDER BY updated_at DESC")
rows = conn.fetchall()

# Use the FIRST row (most recently updated)
correct_app_id = rows[0]['id']  
correct_app_has_data = rows[0]['values_scorecard'] is not None

if correct_app_has_data:
    print(f"⚠️ App {correct_app_id} already has scorecard. Check if update needed.")
else:
    print(f"✅ App {correct_app_id} is correct target. Proceeding with submission.")
    # Submit to correct_app_id
```

### Lesson from 2026-05-12

**What Went Wrong:**
1. First script submitted to Application 1389 (older, from 2026-03-25)
2. User was viewing Markaz form for Application 2708 (recent, from 2026-05-09)
3. Form showed empty because data went to the wrong record

**What Fixed It:**
- Created new script targeting Application 2708 (the recently-updated one)
- Submitted same scorecard data to correct record
- Form now displayed all evidence fields

---

## Non-Negotiable Rules

1. **Always query for duplicates** — Never assume there's only one application record per candidate/job combo
2. **Use most recent updated_at** — That's what Markaz UI displays
3. **Verify the application ID** in your script before running
4. **Check values_scorecard column** — Ensure you're not overwriting existing data unintentionally
5. **Test on read-only query first** — Before running the submit script, verify which record you're targeting

---

## Reference

**When:** Values scorecard submission (any candidate, any job)  
**How to detect:** Form appears empty after "successful" submission  
**Fix:** Query for all app records, identify most recent, submit to correct one  
**Prevention:** Add Step 0 (duplicate check) before any scorecard submission script

---

**Locked in:** 2026-05-12 after Laiba Ahmad (Job 20, App 2708) scorecard submission.

