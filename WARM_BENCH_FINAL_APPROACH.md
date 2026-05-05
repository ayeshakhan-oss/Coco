# Warm Bench Feedback Emails - Final Approach (May 2026)

## Overview
Personalized rejection-keep-warm emails for candidates who cleared values but didn't get selected. Based on Haroon Yasin's training guide (Jan 29, 2026).

## Requirements
- **Word Count**: 800-1100 words minimum (mandatory)
- **Structure**: 4 sections + P.S. + signature
- **Tone**: Haroon-aligned (specific timestamps, "we" voice, company vulnerability, memorable P.S.)
- **Subject**: Poetic & story-based (tied to specific interview moment)

## Section Structure

### 1. Opening
- "This isn't a yes for now. But we need to tell you something..."
- Lead with specific interview moment that stayed with panel
- Show company vulnerability ("we were worried...")

### 2. "What Genuinely Impressed Us" (Blue heading)
- 1-2 additional interview moments with specific timestamps
- Deep analysis of why trait matters
- Evidence of character/capability

### 3. "Here's the Part We Need to Be Honest About" (Blue heading)
- Name the specific gap/reason for rejection
- Frame as "for this role, at this moment" not personal failing
- Show we see the potential but role needs X

### 4. "Here's Where We Want to Leave Things" (Blue heading)
- DO NOT prescribe what they should do (avoid defensiveness)
- Simply: "We'd genuinely like to stay connected. If opportunity aligns with your experience/strengths, welcome talking again."

### 5. P.S. (Before signature)
- The thing that will stick with them
- Memorable moment tied to subject line
- Positive reinforcement

## Language Rules

- ✅ "This isn't a yes for now"
- ✅ Replace "GWC" with "technical interview"
- ✅ Use hyphens "-" ONLY in compound words (e.g., "co-founder"), never as clause connectors
- ✅ "We" voice always
- ✅ Specific timestamps: "At 18 minutes..." "About 35 minutes in..."

## Signature Format (CRITICAL - No "..." appears)

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

**Critical**: Use simple <p> tags, NO border-top divs (causes Gmail "..." menu to appear).

## Color Scheme
- Headings: #1565C0 (company blue)
- Bold emphasis text: #2ecc71 (green) or #1565C0 (blue)
- Links: #1565C0
- Footer: #888 (grey)

## Script Files
- `scripts/warm_bench_locked.py` - Generic function (parameterized)
- `scripts/warm_bench_jra_4candidates_haroon_final.py` - Example implementation for JRA role

## Self-QA Before Sending
- [ ] 800+ word count verified
- [ ] All 4 sections present with blue headings
- [ ] No "GWC" terminology
- [ ] No prescriptive advice in final section
- [ ] Subject is poetic & story-based
- [ ] Signature renders without "..."
- [ ] No em dashes (— becomes -)
- [ ] All timestamps specific
- [ ] P.S. before signature

## Status
✅ PRODUCTION READY - Haroon-aligned, tested with 4 JRA candidates (May 2026)
