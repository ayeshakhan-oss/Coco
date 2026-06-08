---
name: GWC Rejection Email Locked Approach (2026-06-08)
description: Complete locked approach for GWC rejection emails using warm bench structure, evidence-based methodology, and Haroon Yasin balance rule. Reference for all future GWC rejections.
type: feedback
metadata:
  originSession: Hira Abbasi GWC rejection (2026-06-08)
  appliesTo: All GWC rejection emails going forward
  status: PRODUCTION LOCKED
---

# GWC Rejection Email — Complete Locked Approach

**Status:** 🔒 LOCKED (2026-06-08) — Use this approach for ALL GWC rejections going forward. No back-and-forth needed.

---

## Architecture

**Use warm bench email structure for GWC rejections** — Same opening, same sections, same tone.

This is NOT a traditional GWC rejection. It's a warm rejection-keep-warm email using warm bench methodology.

**Template:** `templates/warm_bench_email.html` (locked)
**SOP:** `.claude/skills/01_candidate-communication/gwc-rejection-emails.md`
**Structure:** Opening → "What Stayed With Us" → "Here's the Honest Part" → "Where We Want to Leave This" → P.S.
**Length:** 800+ words MANDATORY

---

## Critical Rules (Non-Negotiable)

### 1. OPENING (EXACT)
```
This is not a yes for now.

But we need to tell you something about what we saw in your interview 
that the panel kept discussing afterward...
```

Never deviate. This is warm bench language, and it works for GWC rejections too.

---

### 2. THREE SECTIONS + P.S. (EXACT HEADINGS)

**"What Stayed With Us"**
- 2-3 concrete strengths from scorecard
- Specific interview moments
- Affirm character + capability

**"Here's the Honest Part"**
- Start with capability clarity: "This decision wasn't driven by concerns about your ability to do the work."
- State the decision driver (e.g., contract/situation mismatch, role requirements)
- Frame as "realities misaligned" NOT "you won't be committed"
- Include positive observations alongside gap
- Use Haroon Yasin balance rule

**"Where We Want to Leave This"**
- Affirm capabilities + potential
- Concrete fit patterns (help them recognize future opportunities)
- Warm bench positioning (genuine, not obligatory)

**"P.S."**
- Reference ONE powerful interview moment
- Tie back to character/who they are
- Emotional, brief, memorable

---

### 3. TONE — CRITICAL ADJUSTMENTS FOR GWC REJECTIONS

**DO NOT:**
- ❌ "Not partially focused" / "Not navigating uncertainty"
- ❌ "Fully present" / "Complete commitment" (use only once, if at all)
- ❌ Sound like you're judging their motivation
- ❌ Make assumptions about their willingness

**DO:**
- ✅ "Realities of the role and realities of her situation are misaligned"
- ✅ "The position comes with real uncertainty... You currently hold a permanent role that offers stability... Neither is better, they create tension"
- ✅ "We weren't fully convinced those conditions were in place right now"
- ✅ Frame as circumstances mismatch, not character judgment

**Example (Hira Abbasi):**
- ✅ "The contract uncertainty and the stability you currently have create a dynamic where your full commitment to this work would be genuinely difficult." (ONE use of full commitment, framed as circumstantial)
- ✅ "This isn't about you not being ready. It's about a specific mismatch in circumstances." (Clear clarity)

---

### 4. HAROON YASIN BALANCE RULE (2026-06-01)

**Count and balance:**
- Praise examples: 3-4 concrete moments with evidence
- Decision examples: 3-4 equally concrete reasons with evidence

**Test:** Can candidate answer "What exactly did I do or say that led to this decision?"
- If yes → Decision specificity is good
- If no → Rewrite decision section to be more concrete

**Example (Hira Abbasi):**
- **Praise:** "You could articulate immediately what coaching looks like" + "The way you adapted your approach" + "That kind of pedagogical thoughtfulness"
- **Decision:** "Contract uncertainty" + "Stability you currently have" + "Full commitment would be genuinely difficult" + "Mismatch in circumstances"

---

### 5. OBSERVABLE BEHAVIORS, NOT ABSTRACTIONS

**Never infer intent:**
- ❌ "You weren't committed"
- ❌ "Your motivation decreased"
- ❌ "You showed lack of interest"

**Stay observable:**
- ✅ "As we discussed X, something genuine happened"
- ✅ "The position comes with real uncertainty"
- ✅ "You currently hold a permanent role"
- ✅ "Neither reality is inherently better... they create tension"

---

### 6. TEMPLATE & ENCODING

**Use:** `templates/warm_bench_email.html`

**Format:**
- Logo: 48x48px, cid:logo_taleemabad
- Header: "PEOPLE &amp; CULTURE &bull; POSITION UPDATE" (use `&bull;` for bullet, `&amp;` for ampersand)
- Title: Candidate name, 32px, #1565C0
- Subtitle: Position, 14px, #7986CB
- Divider: 2px, #1565C0
- Body: Georgia serif, 16px, justified, 1.75 line-height, 70px padding
- Card width: 620px
- Background: #f3f4f6
- Colors: #1565C0 (dark blue headings), #5B8DBE (label), #7986CB (subtitle)

**CRITICAL:** Use HTML entities for special characters:
- `&amp;` for &
- `&bull;` for •
- `&nbsp;` for spaces (when needed)
- No raw UTF-8 characters in HTML

---

### 7. BODY CONTENT STRUCTURE (HTML)

All paragraphs styled with:
```html
style="font-family:Georgia,serif; font-size:16px; color:#333; text-align:justify; line-height:1.75; margin:0 0 20px 0;"
```

Section headings styled with:
```html
style="font-family:Georgia,serif; font-size:18px; color:#1565C0; font-weight:bold; margin:30px 0 15px 0; padding-top:20px;"
```

---

### 8. NO RECRUITING ABSTRACTIONS

**Never say:**
- ❌ "Good candidate"
- ❌ "Strong profile"
- ❌ "Impressive background"

**Say instead:**
- ✅ "Your pedagogical background is genuinely substantial"
- ✅ "That kind of thoughtfulness combined with capacity to execute is rare"
- ✅ "You've built them through real work with real people"

---

### 9. NO INTERNAL JARGON

**Never mention:**
- ❌ "GWC interview"
- ❌ "Values interview"
- ❌ "Scorecard"
- ❌ "Zero In Call"
- ❌ Interviewer names

**Use instead:**
- ✅ "Your interview"
- ✅ "When we asked about..."
- ✅ "The moment you described..."
- ✅ "Our conversation"

---

### 10. SUBJECT LINE (POETIC)

**Pattern:** [What/When] + [Specific action from interview]

**Examples:**
- ✅ "What We Saw When You Listened"
- ✅ "When Maturity Meets a Different Kind of Hunger"
- ✅ "The Gift of Knowing What You Need"

**NOT:**
- ❌ "Hira Abbasi - CPD Coach Update"
- ❌ "Interview Feedback"
- ❌ Generic role/candidate name

---

### 11. P.S. SECTION STYLING (LOCKED 2026-06-08)

**Reference:** [P.S. Section Styling Locked (2026-06-08)](ps_section_styling_locked_2026_06_08.md)

**Styling:**
- Font size: 15px (90-95% of 16px body)
- Color: #555 (dark gray, not pure black)
- Style: **ITALIC** (critical—makes it feel personal)
- Bold "P.S." label
- Top margin: 30px (generous whitespace separation)
- Line height: 1.8 (breathable, thoughtful)
- No borders, no colors, no callout boxes
- Text alignment: Justified (consistent with body)

**Goal:** P.S. feels like a handwritten note added after the formal email—intimate, memorable, personal.

**Content Requirements:**
- Reference ONE specific interview moment
- Tie back to character/who they are
- 2-3 sentences max (brief, memorable)
- Emotional, specific, not generic

---

### 12. SIGNATURE (EXACT)

```
Warm regards,
People and Culture Team
Taleemabad

hiring@taleemabad.com | www.taleemabad.com

Sent on behalf of Talent Acquisition Team by Coco
```

---

## Execution Checklist (Before Sending)

- [ ] GWC scorecard extracted (Get It, Want It, Capacity scores + comments)
- [ ] "This is not a yes for now" opening present
- [ ] Three sections + P.S. with exact headings
- [ ] Capability clarity statement: "This decision wasn't driven by concerns about your ability"
- [ ] Decision framed as "circumstances mismatch" not "commitment judgment"
- [ ] Haroon Yasin balance: praise examples ≈ decision examples (count them)
- [ ] No intent inference words (assumed, believed, thought, preferred, energized)
- [ ] No recruiting abstractions (good candidate, strong profile, impressive)
- [ ] No internal jargon (GWC, values, scorecard, interviewer names)
- [ ] Observable behaviors only (specific moments, concrete details)
- [ ] P.S. tied to powerful interview moment
- [ ] Word count 800+ (verified)
- [ ] Subject line poetic + tied to specific interview action
- [ ] HTML entities used (`&amp;`, `&bull;`, not raw UTF-8)
- [ ] Template: `templates/warm_bench_email.html` with {body_content} placeholder
- [ ] Logo embedded (cid:logo_taleemabad)
- [ ] Colors correct (#1565C0, #f3f4f6, #7986CB, #5B8DBE)
- [ ] Georgia serif, justified, 70px padding
- [ ] Warm bench opening + sections + P.S. (exact structure)
- [ ] Ready for Ayesha approval

---

## Common Mistakes (Do Not Repeat)

| Mistake | Fix |
|---------|-----|
| Custom HTML instead of template | Use `templates/warm_bench_email.html` |
| Repeated "fully present/completely focused" | Use once, if at all. Frame as "weren't fully convinced those conditions were in place" |
| "Your motivation decreased" / "lack of interest" | Frame as observable: "Uncertainty + stability mismatch creates tension" |
| "You won't be committed" judgment tone | Reframe as circumstances: "Realities are misaligned" |
| Raw UTF-8 bullet character (•) | Use `&bull;` HTML entity |
| Raw UTF-8 ampersand (&) | Use `&amp;` HTML entity |
| Missing capability clarity | Start "Here's the Honest Part" with "This decision wasn't driven by concerns about your ability" |
| Vague decision rationale | Ground in specific scorecard data + observable behaviors |
| No Haroon Yasin balance | Count praise moments, count decision moments, balance specificity |
| Intent inference words | Scan for assumed/believed/thought/preferred, replace with observations |
| Generic subject line | Make poetic + tied to specific interview moment |
| Missing P.S. | Always include—references powerful moment, short, emotional, memorable |

---

## Reference Files

- **Template:** `templates/warm_bench_email.html` (locked colors, fonts, layout)
- **SOP:** `.claude/skills/01_candidate-communication/gwc-rejection-emails.md`
- **Warm Bench Rules:** `memory/warm_bench_locked_rules_2026_05_30.md`
- **Haroon Yasin:** `memory/lesson_evidence_based_rejection_rationale_2026_06_01.md`
- **No Intent Inference:** `memory/lesson_no_intent_inference_rejection_emails_2026_06_01.md`
- **Reference Email:** Hira Abbasi email (2026-06-08) — Perfect example of locked approach
- **Previous Reference:** Muhammad Adnan email (2026-06-01) — Warm tone reference

---

## Script Template

Use this pattern for all GWC rejection scripts:

```python
from pathlib import Path

BODY_CONTENT = """
<p style="font-family:Georgia,serif; font-size:16px; color:#333; text-align:justify; line-height:1.75; margin:0 0 20px 0;">Dear [Name],</p>

<p style="font-family:Georgia,serif; font-size:16px; color:#333; text-align:justify; line-height:1.75; margin:0 0 20px 0;">This is not a yes for now.</p>

[3 sections + P.S. with inline styles]

<p style="font-family:Georgia,serif; font-size:16px; color:#333; text-align:justify; line-height:1.75; margin:30px 0 0 0;">Warm regards,<br>People and Culture Team<br>Taleemabad</p>
"""

TEMPLATE_PATH = Path(__file__).parent.parent / "templates" / "warm_bench_email.html"
with open(TEMPLATE_PATH, 'r') as f:
    template = f.read()

HTML_BODY = template.format(
    candidate_name=CANDIDATE_NAME,
    position=POSITION,
    body_content=BODY_CONTENT
)
```

---

## Status

✅ **LOCKED (2026-06-08)** — This approach is production-ready.

Next GWC rejection: Load this file, follow the checklist, send. No feedback sessions needed.

---

**Updated:** 2026-06-08  
**By:** Coco (Ayesha's feedback integrated)  
**Reference Case:** Hira Abbasi (CPD Coach, Job 17)
