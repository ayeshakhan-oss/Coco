---
name: Teams Integration — Microsoft Graph API
description: Coco's Microsoft Graph API setup for reading Teams channels (especially Presence channel). Current use: attendance reporting.
type: project
---

# TEAMS INTEGRATION — MICROSOFT GRAPH API
**Established:** 2026-04-08  
**Status:** ACTIVE — Used for attendance reporting  
**Current use:** Reading Presence channel for leave/WFH announcements

---

## CURRENT CAPABILITY

Coco can read Teams channels via Microsoft Graph API, specifically:
- **Presence channel** — Team-wide announcements about leave, WFH, arriving late, etc.
- **All team channels** — Can read any channel the service account has access to
- **Message filtering** — Can query by time range (since_hours=X), search content

---

## CURRENT USE

### Attendance Reporting (2026-04-09+)
- Reads Presence channel for last 24 hours
- Extracts leave announcements, WFH updates, late arrival notifications
- Combines with Markaz leave_requests table
- Includes in attendance report output
- **Critical rule:** Verify result completeness (see discipline_failure_teams_api_incomplete.md)

---

## IMPLEMENTATION

### Reader Script
- **Location:** `scripts/utils/teams_reader.py`
- **Authentication:** Microsoft Graph API
- **Credentials:** In `.env` file (do NOT commit)
- **Credentials needed:**
  - TEAMS_TENANT_ID
  - TEAMS_CLIENT_ID
  - TEAMS_CLIENT_SECRET

### Usage Example
```python
from scripts.utils.teams_reader import get_presence_updates

# Get all messages from Presence channel in last 24 hours
announcements = get_presence_updates(since_hours=24)

# Returns list of messages with:
# - message content
# - author name
# - timestamp
# - channel name
```

---

## OPEN QUESTION (From Ayesha, 2026-04-10)

**Can Coco read individual Teams statuses (on leave, away, busy, in a call)?**

- This is a capability question that remains open
- Needs technical investigation/clarification with team on what's possible via Graph API
- If yes: could enhance attendance tracking and real-time status visibility
- If no: stick with Presence channel announcements

**Status:** Unresolved — investigate when next working on attendance automation

---

## KNOWN ISSUES

### 1. API Incompleteness (2026-04-15 Incident)
- API returns only messages in Presence channel history
- History may be limited by Graph API pagination/retention
- **Prevention:** Always verify result completeness with ground truth
- **Reference:** discipline_failure_teams_api_incomplete.md

### 2. Delay in Message Indexing
- Teams Graph API may have slight delay in returning newly posted messages
- If running query immediately after message posted, may miss it
- **Prevention:** Run attendance reports after main work day ends (not during morning)

---

## NEXT STEPS (Unresolved)

1. Investigate Graph API capability for individual presence status
2. Consider integrating real-time presence into automated monitoring (future)
3. Document response time/SLA of Graph API for our use case
4. Create fallback if API is unavailable (manual verification)

---

## OWNER

- **Implementation:** Coco (reads Teams via Graph API)
- **Data accuracy:** Coco + User (verify completeness)
- **Maintenance:** Coco (debug, troubleshoot, document)

**Status:** PRODUCTION READY (with verification discipline)
