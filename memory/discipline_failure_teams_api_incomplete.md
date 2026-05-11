---
name: Teams API Incompleteness — Discipline Failure (2026-04-15)
description: Failed to detect incomplete Teams API results; assumed no messages = no data; missed Haya Abid and Sabeen Fatima leave announcements
type: feedback
originSessionId: 3b8197e6-4562-4e77-a2b4-a739e8abac2a
---
## The Failure

**What happened:**
- Ran Teams Presence channel query via `get_channel_messages(..., since_hours=24)`
- API returned only 1 message (Shumaila Aslam)
- I reported "no messages from Sabeen or Haya" to user
- User showed screenshot with clear messages from both (12:31 AM Haya, 8:53 AM Sabeen)
- Both were on leave today (April 15) but I didn't catch it

**Impact:**
- Attendance report initially wrong: missing 2 employees on leave
- Required correction cycle
- Attendance counts had to be recalculated

## Root Cause — Discipline Breakdown

**Why:** I violated CLAUDE.md Section 4 — "NEVER assume":
> "Do not guess. Do not embellish. Do not fill gaps with plausible language."

**Specific error:**
- API returned 1 result
- I assumed that meant "no messages" instead of "query may be incomplete"
- Did NOT verify with user or retry with different parameters
- Did NOT recognize suspiciously small result set

## The Lesson

**Rule locked in:**
When an API or data source returns surprisingly few results (e.g., only 1 message in a channel where you expect multiple), **do not assume completeness**. Instead:
1. Recognize the small result as a red flag
2. Verify with ground truth (ask user, check UI, retry with different params)
3. Never report "no data" based on incomplete API results

**Why this matters:**
- Teams API may have pagination, caching, delays
- A query returning 1 result doesn't prove there's only 1 message
- This is not a capability issue (Teams reader works) — it's a judgment issue (I trusted incomplete data)

## How to Apply

**In future attendance reports or any Teams data work:**
- If the API query returns suspiciously few items (1-2 messages in a busy channel), flag it
- Ask the user: "Teams API returned only X messages — does that match what you see?"
- Never report absence of data as fact without verification

## Reference

Related to broader Execution Discipline failures documented in coco_core_problems_identified.md:
- Problem #4: "Overconfidence before verification"
- Problem #5: "Delegated internal QA to user"

This is the same pattern: verified data source incompleteness after the fact instead of being skeptical upfront.

---

**Incident Date:** 2026-04-15 (Attendance Report April 15)  
**Severity:** Medium (caught by user, required re-report)  
**Status:** Locked in — will not repeat
