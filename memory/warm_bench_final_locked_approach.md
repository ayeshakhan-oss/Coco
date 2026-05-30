---
name: Warm Bench Feedback Emails - Final Locked Approach
description: Complete specification for 800-1100 word rejection-keep-warm emails (Haroon-aligned). 4 sections, poetic subjects, simple signature HTML.
type: reference
---

# Warm Bench Feedback Emails - Final Locked Approach (May 2026)

## Overview
Personalized rejection-keep-warm emails for candidates who cleared values interview but weren't selected. Based on Haroon Yasin's training guide (Jan 29, 2026).

**Status**: ✅ PRODUCTION READY - Tested with 4 JRA candidates, all feedback incorporated.

---

## Non-Negotiable Requirements

### Word Count
- **800-1100 words minimum** (MANDATORY)
- Verified by adding multiple interview moments + deep analysis, NOT filler

### Structure (5 Parts)
1. **Logo + Header** - Taleemabad logo embedded (cid:logo_taleemabad), title, subtitle
2. **Opening** - Lead with specific interview moment, show company vulnerability
3. **"What Stayed With Us"** (Blue #1565C0 heading) — Updated May 15, 2026
4. **"Here's the Honest Part"** (Blue heading) — Updated May 15, 2026
5. **"Where We Want to Leave This"** (Blue heading) — Updated May 15, 2026
6. **P.S.** (before signature) - Memorable moment, reinforcement

---

## Logo Implementation (LOCKED 2026-05-30)

**Status:** Must embed logo directly in email (not URL-based)

**File:** `assets/logo_taleemabad.png`

**HTML Reference (EXACT):**
```html
<img src="cid:logo_taleemabad" width="40" height="40" alt="Taleemabad" style="display:block; margin:0 auto 15px auto; border-radius:20px;" />
```

**Why these styles:**
- `display:block; margin:0 auto` — Centers logo horizontally in the middle
- `width:40; height:40` — 40x40px size for visibility
- `border-radius:20px` — Rounded corners (half of width/height)
- `margin-bottom:15px` — Space between logo and title

**Python Code (REQUIRED):**
```python
from email.mime.image import MIMEImage
import os

logo_path = os.path.join(root_dir, "assets", "logo_taleemabad.png")
if os.path.exists(logo_path):
    with open(logo_path, "rb") as attachment:
        img_part = MIMEImage(attachment.read(), name=os.path.basename(logo_path))
        img_part.add_header("Content-ID", "<logo_taleemabad>")
        img_part.add_header("Content-Disposition", "inline", filename=os.path.basename(logo_path))
        msg.attach(img_part)
```

**Why this works:**
- External URLs fail in many email clients (Gmail, Outlook, corporate networks block remote images)
- Embedded images (cid:) render reliably across all email clients
- Content-ID approach is industry standard for email logos
- Inline disposition ensures logo displays in body, not as attachment

### Tone
- "We" voice always (never "I")
- Specific timestamps ("At 18 minutes...", "About 35 minutes in...")
- Show company vulnerability
- Memorable P.S. they'll screenshot

### Subject Line
- **POETIC & STORY-BASED** (not generic)
- Tied to specific interview story that left impact
- Examples: "When Gestures Speak Louder", "The Journal That Proved Your Resilience"

---

## Language Rules (CRITICAL)

✅ **DO**:
- "This isn't a yes for now" (not "for this round")
- "Technical interview" (not "GWC" - internal jargon)
- Hyphens ONLY in compound words (co-founder, etc)
- Specific timestamps throughout
- Company context in opening ("we were worried...", "the room felt...")

❌ **DON'T**:
- Em dashes (— becomes -)
- Prescriptive advice ("You should do X" in final section)
- "I" voice
- Generic timestamps
- "GWC", "KCD", "TBC" terminology

---

## Section Breakdown

### Section 1: Opening
```
"This is not a yes for now. But we need to tell you something about what we saw 
in your interview that the panel kept discussing afterward, because it reveals 
something important about who you are."

[Specific interview story with timestamp + company vulnerability]
```

### Section 2: "What Stayed With Us"
- 2-3 specific interview moments that impressed the panel
- Each with specific timestamp or context
- Deep analysis: "Why does this matter? What does it reveal about their character?"
- Not just what they did, but why it's rare/valuable
- Use: "the panel kept discussing this afterward"

### Section 3: "Here's the Honest Part"
- Acknowledge what the panel saw (warmly integrate scorecard observations)
- Include positive observations from interview + scorecard (NOT quoted directly)
- Explain the decision was narrow/situational
- Don't apologize; be matter-of-fact
- Frame as "timing didn't align" not "you weren't good enough"

### Section 4: "Where We Want to Leave This"
⚠️ **CRITICAL**: Do NOT suggest what they should do
- ❌ "You should go study X"
- ❌ "We recommend taking courses in Y"
- ✅ "We'd genuinely like to stay connected. If opportunity aligns with your experience and strengths, we'd welcome talking again."
- **Reason**: Prescriptive advice triggers defensiveness/offense

### Section 5: P.S.
- The ONE thing the room will remember
- Tied to subject line's story
- Positive reinforcement, not recap

---

## Signature HTML (EXACT FORMAT — LOCKED 2026-05-30)

```html
<div class="signature">
Warm regards,<br />
<div class="signature-name">People and Culture Team</div>
<div class="signature-company">Taleemabad</div>
<br />
<a href="mailto:hiring@taleemabad.com" style="color:#2f4fa2; text-decoration:none;">hiring@taleemabad.com</a> | <a href="http://www.taleemabad.com" style="color:#2f4fa2; text-decoration:none;">www.taleemabad.com</a>
<br /><br />
<div class="signature-coco">Sent on behalf of Talent Acquisition Team by Coco</div>
</div>
```

**CSS Classes (REQUIRED):**
```css
.signature {
  margin-top: 40px;
  padding-top: 15px;
  border-top: 1px solid #ccc;
  font-size: 14px;
  color: #666;
  font-family: Georgia, Cambria, "Times New Roman", serif;
}
.signature-name {
  font-weight: bold;
  color: #333;
  margin: 5px 0 0 0;
  font-size: 14px;
}
.signature-company {
  font-weight: bold;
  color: #2f4fa2;
  margin: 0;
  font-size: 14px;
}
.signature-coco {
  font-size: 13px;
  color: #888;
  margin: 10px 0 0 0;
}
```

**Why this works**: 
- Simple <div> structure with class-based styling
- NO border-top divs inside signature (they cause Gmail "..." menu)
- Email links clickable and branded (#2f4fa2 Taleemabad blue)
- Exact format for all warm bench emails (never deviate)

---

## Color Scheme
- Blue headings: #1565C0
- Bold text (emphasis): #2ecc71 (green) or #1565C0 (blue)
- Links: #1565C0
- Footer text: #888 (grey)

---

## Self-QA Checklist (Before Sending)
- [ ] Word count 800-1100
- [ ] All 4 section headings present and blue (exact wording: "What Stayed With Us" / "Here's the Honest Part" / "Where We Want to Leave This")
- [ ] Opening has "This is not a yes for now" (exact)
- [ ] No interviewer names mentioned
- [ ] No internal jargon (GWC, values, scorecard, case study, warm bench)
- [ ] "What Stayed With Us" has 2-3 specific moments
- [ ] "Here's the Honest Part" includes scorecard warmly integrated (not quoted)
- [ ] "Where We Want to Leave This" does NOT prescribe ("you should...")
- [ ] No comparative language ("another candidate", "tighter fit")
- [ ] No recruiting abstractions ("good candidate", "strong profile", "excellent fit")
- [ ] Praise examples ≈ Decision examples (Haroon Yasin balance)
- [ ] P.S. is memorable and ties back to powerful moment from interview
- [ ] Subject is poetic & story-based, tied to specific interview moment (NOT generic)
- [ ] "We" voice throughout (never "I")
- [ ] No em dashes (only hyphens in compounds)
- [ ] Signature is simple HTML (no border-top divs)
- [ ] P.S. before signature

---

## Implementation Files
- **`scripts/warm_bench_locked.py`**: Generic parameterized function
- **`scripts/warm_bench_jra_4candidates_haroon_final.py`**: Working example (JRA role, 4 candidates)

---

## Example Structure (Real Email)

**Subject**: "When Gestures Speak Louder" (poetic, story-based)

**Opening**: "This isn't a yes for now... [specific story about helping colleague, timestamp, company vulnerability]"

**Section 2 heading**: "What Genuinely Impressed Us" (blue)
Content: [Additional interview moment with deep analysis of why it matters]

**Section 3 heading**: "Here's the Part We Need to Be Honest About" (blue)
Content: [Names the gap, frames as role-specific, shows we see potential]

**Section 4 heading**: "Here's Where We Want to Leave Things" (blue)
Content: [Simple: stay connected if opportunity aligns - NO advice]

**P.S.**: [The memorable moment from interview that encapsulates who they are]

**Signature**: [Simple HTML, no borders]

---

## Lessons Learned
1. **800+ words is NOT negotiable** - Requires 2+ interview moments + deep analysis
2. **Don't prescribe** - "Study X" causes defensiveness. Just offer connection.
3. **Subject must be poetic** - Generic subjects miss the point of warm bench
4. **Simple HTML signature** - Complex styling (borders, divs) causes Gmail to render "..." menu
5. **Specific timestamps** - "At 18 minutes" is more powerful than vague reference
6. **Haroon's rules matter** - Company vulnerability, "we" voice, memorable P.S. land differently

---

**Last Updated**: 2026-05-30 (Updated headings + rules from May 15 Fatima Saeed reference)
**Original**: May 5, 2026
**Tested With**: Dur E Nayab, Daniyah Noor, Hassan Zafar, Mahnoor Hasan (JRA role); Huma Mumtaz (Fundraising & Partnerships Manager, 2026-05-30)
**Author**: Coco (Talent Acquisition Agent)

**2026-05-30 Updates:**
- Updated heading structure to match Fatima Saeed reference (May 15, 2026)
- Added 10 locked rules from warm_bench_locked_rules_2026_05_30.md
- Added quality review protocol (10-point checklist)
- Added recruiting abstractions prevention guidance
- Updated self-QA checklist with new rules (no names, no jargon, balance rule, etc.)
