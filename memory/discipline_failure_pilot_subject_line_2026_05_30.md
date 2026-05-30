---
name: Discipline Failure — Pilot Subject Prefix in Live Email (2026-05-30)
description: Critical mistake. Sent live email with [PILOT – ] prefix in subject line. Candidate received email with "pilot" label. Never repeat.
type: feedback
---

# DISCIPLINE FAILURE — PILOT SUBJECT PREFIX (2026-05-30)

**What Happened:**
- Sent LIVE email to huma.mumtaz3@gmail.com
- Subject line: `[PILOT – Huma Mumtaz] When You Stop a Meeting to Protect Your Team`
- Should have been: `When You Stop a Meeting to Protect Your Team`
- The `[PILOT – Huma Mumtaz]` prefix is ONLY for pilot emails to Ayesha

**Why It's Wrong:**
- Candidate sees "[PILOT – ]" in their warm bench rejection email
- Appears unprofessional and sloppy
- Makes the email look like a test, not a real communication
- Violates warm bench email standard

**Root Cause:**
- Switched PILOT_MODE = False to enable live send
- Did NOT verify subject line construction in the script
- The SUBJECT variable was hardcoded with `[PILOT – Huma Mumtaz]` prefix
- Never checked that subject would be clean for live send

**Prevention (For Next Time):**

### Rule 1: Subject Line MUST Be Cleaned Before Live Send
When switching PILOT_MODE = False:
1. Check the SUBJECT variable in the script
2. Verify it does NOT contain "[PILOT – ]" prefix
3. If it does, remove it before sending live
4. Example:
   ```python
   SUBJECT = "[PILOT – Huma Mumtaz] When You Stop a Meeting to Protect Your Team"
   
   # Before live send:
   if not PILOT_MODE:
       SUBJECT = SUBJECT.replace("[PILOT – Huma Mumtaz] ", "")
   ```

### Rule 2: Explicit Subject Line Validation
Add a final check before sending:
```python
if not PILOT_MODE:
    assert "[PILOT" not in msg["Subject"], "ERROR: Live email has [PILOT] prefix in subject!"
```

### Rule 3: Use Separate Subject Variables
Instead of hardcoding subject with pilot prefix:
```python
SUBJECT_BASE = "When You Stop a Meeting to Protect Your Team"
SUBJECT = f"[PILOT – Huma Mumtaz] {SUBJECT_BASE}" if PILOT_MODE else SUBJECT_BASE
```

---

## Impact

**Status:** ✅ SENT (cannot be unsent)

**Candidate:** Huma Mumtaz

**Email Header Seen By Recipient:**
```
Subject: [PILOT – Huma Mumtaz] When You Stop a Meeting to Protect Your Team
```

**What Huma Thinks:** "This looks like a test email, not a real warm bench from Taleemabad"

---

## Lesson

**Never assume PILOT_MODE controls subject line construction.** Always verify subject explicitly before sending live.

This is embarrassing but locked in for future discipline.

---

**Locked in:** 2026-05-30
**Status:** 🔴 FAILURE (cannot undo, learn and prevent)
