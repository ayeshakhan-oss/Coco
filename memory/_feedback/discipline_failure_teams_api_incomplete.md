---
name: Teams API Incompleteness — Discipline Failure
description: Critical learning from Attendance Report (2026-04-15) incident. When API returns suspiciously few results, do NOT assume completeness. Always verify with ground truth.
type: project
---

# TEAMS API INCOMPLETENESS — DISCIPLINE FAILURE
**Date:** 2026-04-15  
**Incident:** Incomplete Teams API result assumed as "no data"  
**Impact:** Missed 2 employees on leave (Haya Abid, Sabeen Fatima)  
**Severity:** 🔴 Critical (attendance reporting is accurate only with complete data)

---

## WHAT HAPPENED

### The Situation
- Task: Generate Attendance Report for 2026-04-15
- Data source: Teams Presence channel (get_channel_messages with since_hours=24)
- User goal: Capture all leave/WFH announcements from past 24 hours

### The Failure
- API query returned: **1 message** (Shumaila Aslam's announcement)
- Coco's decision: "No leave announcements except this one"
- Reality: **2 more employees on leave** (Haya Abid, Sabeen Fatima)
- Evidence: User showed screenshot of Teams channel with 3 announcements
- Result: Final report missing 2 people. Inaccurate headcount.

### Root Cause
**Assumed API completeness instead of recognizing the red flag.**

- Query returned suspiciously small result set (1 message)
- Coco did NOT flag this as incomplete
- Coco did NOT request ground truth verification
- Coco reported the API result as authoritative

---

## THE LOCKED RULE

**When API/data source returns suspiciously few results, DO NOT assume completeness.**

### What "suspiciously few" means:
- **Attendance reports:** expect ≥3 leave announcements per day (we have 84 people, holidays/WFH common)
- **Email searches:** expect ≥5 matching results if asking for 30-day window
- **Database queries:** expect row counts that match business logic (not zero when you'd expect thousands)
- **API timeouts:** if you get partial results, acknowledge it, don't assume full set

### What to do when you see it:
1. **Flag immediately:** "This result looks incomplete. API returned only X when we'd expect Y."
2. **Verify with ground truth:** Ask user, check UI directly, retry with different params, use alternate data source
3. **Never report absence as fact.** Say: "Found 3, but result may be incomplete — verify with user" not "Only 3 exist"
4. **Confirm before including in final output.**

---

## EXAMPLE: HOW IT SHOULD HAVE GONE

**Coco's decision (correct):**
```
Teams API query returned: 1 message
Expected: 3-5 announcements for 84-person company
Red flag: Result is suspiciously small
Action: Ask user to verify
Message to user: "Teams returned 1 leave announcement (Shumaila Aslam). 
This seems incomplete for our company size. Can you check the channel 
directly to confirm if there are more announcements?"
User confirms: 3 total (includes Haya + Sabeen)
Final report: All 3 included
```

**What actually happened (incorrect):**
```
Teams API query returned: 1 message
Coco assumption: "This is the only announcement today"
Final report: Only Shumaila included
User screenshots: "Wait, what about Haya and Sabeen?"
Coco realizes: API was incomplete
```

---

## PREVENTION GOING FORWARD

### Add to Session Startup Checklist
- [ ] When using APIs/external data sources, watch for suspiciously small result sets
- [ ] Red flag: query expected to return 10+ items but got <5
- [ ] Default: verify with ground truth before reporting absence of data

### Add to Attendance Report SOP
- [ ] Teams Presence query: if <3 announcements returned, verify with user
- [ ] Markaz leave_requests query: if <5 pending leaves, verify with user
- [ ] Always cross-check Teams + Markaz data before finalizing

### Add to General Discipline
- **Never assume a result set is complete** just because the query succeeded
- **Absence of data in a query ≠ absence of real-world data**
- **Always verify suspiciously small results before using them**

---

## APPLICATIONS TO OTHER AREAS

This rule applies beyond just Teams:

| Data Source | Red Flag | Action |
|---|---|---|
| **Database queries** | Expected 50 rows, got 3 | Verify: check data source, retry query, ask user |
| **Gmail searches** | Expected 20 emails, got 2 | Verify: check manually, try different filters |
| **API calls** | Expected list of 100, got 5 | Verify: check API docs, retry, use alternate endpoint |
| **File searches** | Expected 10 files, found 1 | Verify: check directory structure, retry glob |
| **CSV imports** | Expected 500 rows, got 50 | Verify: check encoding, delimiter, completeness |

---

## INCIDENT CLOSURE

**What Coco will do differently:**
1. Flag suspiciously small result sets immediately (don't silently use them)
2. Always ask for ground truth verification before committing to "absence"
3. Document in report any incompleteness: "Teams API returned 1 announcement; user confirmed 3 total after manual check"

**Status:** RESOLVED — Rule locked in and applied to all future work

---

**Owner:** Coco  
**Date Identified:** 2026-04-15  
**Prevention:** Added to attendance SOP and session startup checklist
