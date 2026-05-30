---
name: Warm Bench Email — FINAL LOCKED VERSION (2026-05-30)
description: Complete locked specification for all warm bench emails. SINGLE SOURCE OF TRUTH. Use this for all future warm bench drafts. Supersedes all prior versions.
type: reference
---

# WARM BENCH EMAILS — FINAL LOCKED SPECIFICATION (2026-05-30)

**STATUS:** 🔒 LOCKED & PRODUCTION READY

**REFERENCE:** Fatima Saeed warm bench email (May 15, 2026)

**APPLIES TO:** All rejection-keep-warm emails for candidates who cleared values + strong interview but weren't selected

---

## CRITICAL RULES (Non-Negotiable)

### ZERO. SUBJECT LINE — NO [PILOT – ] IN LIVE EMAILS (CRITICAL — 2026-05-30)

**RULE:** When sending LIVE email to candidate, subject MUST be clean.

❌ **FORBIDDEN:**
```
[PILOT – Huma Mumtaz] When You Stop a Meeting to Protect Your Team
```

✅ **CORRECT:**
```
When You Stop a Meeting to Protect Your Team
```

**Why:** 
- `[PILOT – ]` prefix is ONLY for emails to Ayesha/internal team
- Candidate should never see "[PILOT]" in their warm bench email
- Appears unprofessional, looks like a test, breaks confidentiality

**Implementation:**
```python
SUBJECT_BASE = "When You Stop a Meeting to Protect Your Team"
SUBJECT = f"[PILOT – Name] {SUBJECT_BASE}" if PILOT_MODE else SUBJECT_BASE

# Before live send, add assertion:
assert "[PILOT" not in SUBJECT, "ERROR: Subject still has [PILOT] prefix!"
```

---

### 1. OPENING LINE (MANDATORY — EXACT)
```
This is not a yes for now.

But we need to tell you something about what we saw in your interview 
that the panel kept discussing afterward...
```

### 2. HEADING STRUCTURE (EXACT)
- "What Stayed With Us"
- "Here's the Honest Part"
- "Where We Want to Leave This"
- NEVER use old headings ("What Genuinely Impressed Us", "Here's the Part We Need to Be Honest About")

### 3. NO EM DASHES (—) — ABSOLUTELY FORBIDDEN
- Replace ALL em dashes with:
  - Periods (.)
  - Commas (,)
  - Colons (:)
  - Hyphens (-) for compound words ONLY
- Example: "story—discovering" → "story. Discovering"
- Example: "style—how" → "style, how"

### 4. NEVER MENTION INTERVIEWER NAMES
- ❌ "During your values conversation with Jawwad Ali..."
- ✅ "You described a moment in your interview..."

### 5. NO INTERNAL JARGON
- ❌ FORBIDDEN: GWC, values interview, scorecard, case study, warm bench, KCD
- ✅ ALLOWED: "your interview", "when we asked", "the panel"

### 6. NO RECRUITING ABSTRACTIONS
- ❌ "good candidate", "strong profile", "excellent fit", "impressive background"
- ✅ "The way you identify gaps and follow through" (observed behavior)

### 7. NO COMPARATIVE LANGUAGE
- ❌ "Another candidate's background was a tighter fit"
- ✅ "We're moving into a specific phase where we need X capability"

### 8. WORD COUNT: 800-1100 MANDATORY
- Verified by character count
- No shortcuts, no filler

### 9. SIGNATURE FORMAT (EXACT)
```
Warm regards,
People and Culture Team
Taleemabad

hiring@taleemabad.com | www.taleemabad.com

Sent on behalf of Talent Acquisition Team by Coco
```

### 10. LOGO EMBEDDING (EXACT)
```html
<img src="cid:logo_taleemabad" width="48" height="48" alt="Taleemabad" style="display:block; margin:0 auto 20px auto; border-radius:0;" />
```
- File: assets/logo_taleemabad.png (embedded, not URL)
- Centered in middle of header
- 48x48px size
- No border-radius (preserves full logo)

### 11. SECTION STRUCTURE

**Section 1: What Stayed With Us**
- 2-3 specific interview moments
- Deep analysis of why it matters
- Affirm character, not just competence

**Section 2: Here's the Honest Part**
- Acknowledge what panel saw (warmly)
- Include positive scorecard observations (integrated, not quoted)
- Explain decision was narrow/situational
- Frame as "timing didn't align" not "you weren't good enough"

**Section 3: Where We Want to Leave This**
- Warm bench positioning
- Express genuine interest in future connection
- End with warmth, not finality

**P.S.: The Powerful Echo**
- Reference ONE powerful moment from interview
- Tie it back to who they are
- Emotional, brief, memorable

### 12. TONE CHECKLIST
- [ ] "We" voice (never "I")
- [ ] Warm + observational (not clinical)
- [ ] Specific interview moments (never generic)
- [ ] No prescriptive advice ("You should...")
- [ ] No life-coach language
- [ ] Vulnerable (show company perspective too)
- [ ] Poetic P.S.
- [ ] **NO EM DASHES**

### 13. HAROON YASIN BALANCE RULE
- Count specific praise examples
- Count specific decision examples
- These should be roughly equal
- **Test:** Would candidate think "If you valued all this, why wasn't I selected?"
- If yes: increase decision specificity

---

## QUALITY REVIEW CHECKLIST (Before Sending)

See memory/candidate_communication_quality_review_protocol_2026_05_30.md for full 10-point checklist:

1. Balance of Evidence — praise ≈ decision
2. Avoid Generic Labels — character observations only
3. Concrete Feedback — no vague language
4. Endorsement Level Test — passes the "why wasn't I hired?" test
5. Evidence Support — every claim cited
6. Emotional Arc — all 4 elements present
7. Character Over Assessment — no profile labels
8. Haroon Yasin Balance — equal specificity
9. Concrete Decision Rationale — as specific as praise
10. Final Test — candidate feels SEEN, not SCORED

---

## PYTHON SCRIPT REQUIREMENTS

**File:** scripts/warm_bench_huma_mumtaz_pilot.py (reference implementation)

**Key Code Sections:**

1. **Logo Attachment:**
```python
logo_path = os.path.join(root_dir, "assets", "logo_taleemabad.png")
if os.path.exists(logo_path):
    with open(logo_path, "rb") as attachment:
        img_part = MIMEImage(attachment.read(), name=os.path.basename(logo_path))
        img_part.add_header("Content-ID", "<logo_taleemabad>")
        img_part.add_header("Content-Disposition", "inline", filename=os.path.basename(logo_path))
        msg.attach(img_part)
```

2. **Email Send:**
```python
safe_sendmail(
    smtp_server=server,
    sender=SENDER,
    recipients=recipients,
    message=msg.as_string(),
    context="warm_bench_feedback_[candidate_name]"
)
```

3. **Pilot Mode:**
```python
PILOT_MODE = True
PILOT_TO = "ayesha.khan@taleemabad.com"
```
Change to `False` after approval for live send.

---

## WHAT CHANGED IN 2026-05-30 UPDATE

**Previous errors (now fixed):**
- ❌ Old headings: "What Genuinely Impressed Us"
- ❌ EM DASHES throughout email
- ❌ Logo from external URL (didn't display)
- ❌ No signature format locked in
- ❌ Generic language in places

**Current locked version:**
- ✅ New headings: "What Stayed With Us" / "Here's the Honest Part" / "Where We Want to Leave This"
- ✅ NO EM DASHES (all replaced with periods/commas/colons)
- ✅ Logo embedded (cid:) + centered + 48x48px
- ✅ Signature format exact and locked
- ✅ Character-focused language throughout
- ✅ All 13 rules locked into Skill 01
- ✅ Quality review protocol (10-point checklist)

---

## FILES UPDATED (2026-05-30)

1. **scripts/warm_bench_huma_mumtaz_pilot.py** — Reference implementation with all fixes
2. **.claude/skills/01_candidate-communication/SKILL.md** — 13 locked rules
3. **memory/warm_bench_final_locked_approach.md** — Technical specification
4. **memory/warm_bench_locked_rules_2026_05_30.md** — 10 rules (Fatima reference)
5. **memory/candidate_communication_quality_review_protocol_2026_05_30.md** — 10-point checklist
6. **memory/candidate_communication_avoid_recruiting_abstractions_2026_05_30.md** — Character focus guide

---

## FOR FUTURE SESSIONS

**When drafting the NEXT warm bench email:**

1. **Read THIS file first** (warm_bench_locked_final_2026_05_30.md)
2. Read RULES.md Skill 1 section
3. Read locked template (warm_bench_final_locked_approach.md)
4. Use scripts/warm_bench_huma_mumtaz_pilot.py as template
5. Run 10-point quality review before piloting

**DO NOT** use old notes or old skill versions — this is the SINGLE SOURCE OF TRUTH for 2026-05-30 forward.

---

**Locked:** 2026-05-30
**Final Pilot Sent:** Huma Mumtaz to ayesha.khan@taleemabad.com
**Status:** ✅ PRODUCTION READY

