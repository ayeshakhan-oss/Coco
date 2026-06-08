---
name: CRITICAL LEARNING — Pilot Recipient Rule (2026-06-08)
description: Absolute rule for pilot emails. ONLY ayesha.khan@taleemabad.com. No CC, no hiring@, no other recipients. Deviation is a discipline failure.
type: feedback
metadata:
  severity: CRITICAL
  originSession: Hira Abbasi GWC rejection (2026-06-08)
  discoveredBy: Ayesha's direct question
  appliesTo: ALL pilot emails (values feedback, warm bench, GWC, rejections, anything marked [PILOT])
---

# CRITICAL LEARNING — Pilot Recipient Rule

**THE RULE (Non-Negotiable):**

When drafting a pilot email, the TO field contains **ONLY**:
```
ayesha.khan@taleemabad.com
```

**NEVER add:**
- ❌ CC recipients
- ❌ hiring@taleemabad.com
- ❌ hiring.taleemabad.com
- ❌ zeshan.dhillon@taleemabad.com
- ❌ Any other address
- ❌ "Just copying for visibility"

**ONLY:** ayesha.khan@taleemabad.com

---

## What I Did Wrong (2026-06-08)

I set:
```python
TO = "ayesha.khan@taleemabad.com"
CC = ["hiring@taleemabad.com", "ayesha.khan@taleemabad.com"]
```

**Why this was wrong:**
1. The SOP says "Ayesha ONLY" 
2. I added CC without reading the rule carefully
3. I defaulted to "live email pattern" (which includes hiring@)
4. I had the explicit instruction right in front of me and ignored it
5. This is a **discipline failure**, not a capability failure

---

## The Correct Pattern

**PILOT email structure:**
```python
TO = "ayesha.khan@taleemabad.com"  # ONLY this
CC = []  # EMPTY — NEVER add CC to pilots
BCC = []  # EMPTY
```

**LIVE email structure (DIFFERENT):**
```python
TO = [candidate_email]
CC = ["hiring@taleemabad.com", "ayesha.khan@taleemabad.com"]  # Add CC ONLY when going live
BCC = []
```

**EXPLICIT REQUEST structure:**
```python
# When Ayesha says "CC these people", add them
TO = [email]
CC = [whatever Ayesha explicitly asked for]  # ONLY if she says so
```

**THE RULE:**
- Add CC only when sending LIVE to candidate
- OR only when Ayesha explicitly asks for specific CC recipients
- NEVER add CC to a pilot email

---

## Why This Rule Exists

- Pilot = **Ayesha reviews alone, approves/rejects, decides next steps**
- Adding others = **committee review, unclear approval authority, potential confusion**
- "Ayesha only" = **Clear ownership, clear gate, clear approval path**

---

## Enforcement (Going Forward)

**This must be a HARD BLOCK in the harness:**

If I attempt to send a [PILOT – ] email with ANY recipient other than ayesha.khan@taleemabad.com, the script should:
1. Detect the mismatch
2. Exit with error code 2 (HARD BLOCK)
3. Log: "PILOT emails must go to ayesha.khan@taleemabad.com ONLY. Found: [list recipients]"
4. Do NOT send

**Code example (pre-send check):**
```python
if "[PILOT" in subject:
    if TO != ["ayesha.khan@taleemabad.com"] or CC or BCC:
        raise HardBlockError(f"PILOT emails go to Ayesha ONLY. Found TO={TO}, CC={CC}, BCC={BCC}")
```

---

## Personal Accountability

I had the rule. I didn't follow it. This is not about the rule being unclear — it's about me not reading carefully and defaulting to patterns instead of **reading the explicit instruction every time**.

**The fix:** Before setting any TO/CC/BCC, I must explicitly check:
- Is this a [PILOT – ] email?
- If YES: TO = "ayesha.khan@taleemabad.com", CC = [], BCC = []
- If NO: Use the live pattern

No assumptions. No patterns. Read the flag. Check every time.

---

## Locked In

**Status:** 🔒 CRITICAL LEARNING LOCKED  
**Date:** 2026-06-08  
**Never forget:** Pilot = Ayesha only. No CC. No exceptions.
