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
1. **Opening** - Lead with specific interview moment, show company vulnerability
2. **"What Genuinely Impressed Us"** (Blue #1565C0 heading)
3. **"Here's the Part We Need to Be Honest About"** (Blue heading)
4. **"Here's Where We Want to Leave Things"** (Blue heading)
5. **P.S.** (before signature) - Memorable moment, reinforcement

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
"This isn't a yes for now. But we need to tell you something about what we saw 
in your interview that the panel kept discussing afterward, because it reveals 
something important about who you are."

[Specific interview story with timestamp + company vulnerability]
```

### Section 2: "What Genuinely Impressed Us"
- 1-2 additional moments from interview (different from opening)
- Each with specific timestamp
- Deep analysis: "Why does this matter? What does it reveal about their character?"
- Not just what they did, but why it's rare/valuable

### Section 3: "Here's the Part We Need to Be Honest About"
- Name the gap directly: "In our technical interview, we found..."
- Frame as role-specific: "For this role, at this moment, that gap matters"
- NOT a personal failing ("you lack X")
- Show we understand the potential

### Section 4: "Here's Where We Want to Leave Things"
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

## Signature HTML (CRITICAL - Prevents "..." menu)

```html
<p style="font-family:Georgia,serif; font-size:14px; color:#333; margin:30px 0 0 0; line-height:1.6;">
Warm regards,<br/>
<span style="font-weight:bold;">People and Culture Team</span><br/>
<span style="color:#1565C0; font-weight:bold;">Taleemabad</span>
</p>

<p style="font-family:Georgia,serif; font-size:14px; color:#333; margin:8px 0 0 0; line-height:1.6;">
<a href="mailto:hiring@taleemabad.com" style="color:#1565C0; text-decoration:none;">hiring@taleemabad.com</a> | <a href="http://www.taleemabad.com" style="color:#1565C0; text-decoration:none;">www.taleemabad.com</a>
</p>

<p style="font-family:Georgia,serif; font-size:13px; color:#888; margin:12px 0 0 0; line-height:1.6;">
Sent on behalf of Talent Acquisition Team by Coco
</p>
```

**Why this works**: Simple <p> tags with basic styling. NO border-top divs (they cause Gmail to render "..." menu). NO complex nesting.

---

## Color Scheme
- Blue headings: #1565C0
- Bold text (emphasis): #2ecc71 (green) or #1565C0 (blue)
- Links: #1565C0
- Footer text: #888 (grey)

---

## Self-QA Checklist (Before Sending)
- [ ] Word count 800+
- [ ] All 4 section headings present and blue
- [ ] Opening has specific timestamp + company vulnerability
- [ ] "What Genuinely Impressed Us" has 1-2 new moments
- [ ] "Here's the Part We Need to Be Honest About" names the gap
- [ ] "Here's Where We Want to Leave Things" does NOT prescribe
- [ ] P.S. is memorable and tied to subject
- [ ] Subject is poetic & story-based (NOT generic)
- [ ] No "GWC", "KCD", "I" voice
- [ ] No em dashes (only hyphens in compounds)
- [ ] Signature is simple HTML (no border-top divs)
- [ ] All timestamps specific
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

**Last Updated**: May 5, 2026
**Tested With**: Dur E Nayab, Daniyah Noor, Hassan Zafar, Mahnoor Hasan (JRA role)
**Author**: Coco (Talent Acquisition Agent)
