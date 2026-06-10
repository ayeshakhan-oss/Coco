---
name: 🔒 LOCKED Email Template — INTERVIEW INVITES (Skill 06) (FINAL 2026-05-13)
description: Locked design for INTERVIEW INVITES & opportunity emails (Skill 06) — values invites, case study/GWC/exploratory call invites, round/final/offer meetings, warm bench OPPORTUNITY invites. Design locked. SCOPE NARROWED 2026-06-10 — feedback/rejection emails now use the v8 layout (see note below).
type: project
status: 🔒 LOCKED FOR PRODUCTION (INVITES ONLY) — NO DESIGN DEVIATIONS ALLOWED
originSessionId: session-2026-05-13
verifiedAgainst: Values Interview email + complete editorial refinement session
---

# 🔒 LOCKED EMAIL TEMPLATE — INTERVIEW INVITES (Skill 06)

**STATUS:** PRODUCTION READY — FINAL SPECIFICATION LOCKED 2026-05-13. **Scope narrowed 2026-06-10.**

> **⚠️ SCOPE CHANGE (2026-06-10):** This template is for **interview invites & opportunity
> emails only (Skill 06)**. It previously claimed to be universal for "ALL candidate
> communication," including rejections — that is **no longer true**. All **candidate
> communication feedback/rejection emails** (CV rejection, values feedback, warm bench
> FEEDBACK, GWC rejection — Skill 01) now use the **v8 layout**:
> [v8_candidate_comms_layout_LOCKED.md](v8_candidate_comms_layout_LOCKED.md) via
> `scripts/utils/v8_template.py`. Ayesha's decision, 2026-06-10. This resolves the
> long-standing design conflict between the two templates.

**APPLIES TO (invites / opportunity emails — Skill 06):**
- ✅ Values interview invites
- ✅ Case study submission invites
- ✅ Exploratory call invites
- ✅ GWC call invites
- ✅ Zero-in / Round interviews
- ✅ Final round interviews
- ✅ Offer acceptance meetings
- ✅ Warm bench OPPORTUNITY invites (interview invites only)

**DOES NOT APPLY TO (use v8 layout instead):**
- ❌ Rejection emails (any stage) → v8
- ❌ Values feedback emails → v8
- ❌ Warm bench FEEDBACK emails → v8
- ❌ CV-stage rejection feedback → v8

**RULE:** For invites, design is 100% locked. Only content changes per purpose. Layout, fonts, colors, spacing — NEVER deviate.

---

## DESIGN SPECIFICATION (LOCKED)

### THREE-LAYER STRUCTURE

```
OUTER: Gmail/Page background
  Color: #f5f5f5

MIDDLE: Grey wrapper section
  Color: #e5e7e2
  Width: calc(100% - 90px)
  Padding-top: 38px
  Padding-bottom: 38px
  Centered

INNER: White email card
  Width: 775px
  Max-width: 775px
  Background: #ffffff
  NO shadow, NO border-radius
  Occupies ~58-62% of viewport width
```

### HEADER SECTION

**Padding:** top 34px, bottom 30px, left/right 64px

**Logo:**
- Centered
- Width: 34px
- Height: auto
- Margin-bottom: 16px

**Top Label:**
- Text: `TALENT ACQUISITION • [STAGE_NAME]`
  - Examples: VALUES INTERVIEW, CASE STUDY SUBMISSION, GWC CALL, REJECTION, WARM BENCH OPPORTUNITY, EXPLORATORY CALL, etc.
- Font: Georgia, Cambria, "Times New Roman", serif
- Font-size: 12px
- Letter-spacing: 2.4px
- Font-weight: 500
- Text-transform: uppercase
- Color: #3157b7
- Line-height: 1.4
- Margin-bottom: 18px

**Main Heading:**
- Text: `[Customizable per stage]`
  - Examples: "Invitation for the Values Interview", "We'd Like to Hear More", "Next Steps in Our Process", "Thank You for Interviewing"
- Font: Georgia, Cambria, "Times New Roman", serif
- Font-size: 24px
- Line-height: 1.2
- Font-weight: 700
- Color: #3157b7
- Margin-bottom: 10px

**Subtitle:**
- Text: `[Position name or brief descriptor]`
- Font: Georgia, Cambria, "Times New Roman", serif
- Font-size: 13px
- Line-height: 1.5
- Color: #5d73b8

### DIVIDER

- Border-top: 2px solid #4b67d1
- Width: 100%
- Margin: 0

### BODY CONTENT

**Padding:** top 44px, left/right 64px, bottom 52px

**Body Text:**
- Font: Georgia, Cambria, "Times New Roman", serif
- Font-size: 17px
- Line-height: 1.85
- Color: #111111
- Font-weight: 400
- Margin-bottom: 26px (between paragraphs)

**Greeting:**
- Font-size: 17px
- Line-height: 1.8
- Margin-bottom: 30px

**Bold Text (when needed):**
- Font-weight: 700

**Links:**
- Color: #3d63c8
- Text-decoration: underline
- Font inherited from context

**Lists/Bullets:**
- Font: Georgia, Cambria, "Times New Roman", serif
- Font-size: 17px
- Line-height: 1.85
- Margin: 0 0 26px 0
- Padding-left: 50px

**Callout Text (important notices, recording disclaimers, etc.):**
- Font: Georgia, Cambria, "Times New Roman", serif
- Font-size: 17px
- Line-height: 1.85
- Font-weight: 700
- Color: #3d63c8
- Margin: 26px 0 26px 0

**CTA Button (when applicable):**
- Background: #5b3fc4
- Text-color: #ffffff
- Font: Georgia, Cambria, "Times New Roman", serif
- Font-size: 16px
- Font-weight: 700
- Text-decoration: none
- Border-radius: 7px
- Padding: 14px 34px
- Display: inline-block
- Text-align: center
- Margin: 40px 0 28px 0

**Button Subtitle (optional text below button):**
- Font-size: 16px
- Line-height: 1.6
- Color: #111111
- Text-align: center
- Margin: 18px 0 0 0

### SIGNATURE SECTION (LEFT-ALIGNED)

**Divider above signature:**
- Border-top: 1px solid #d9d9d9
- Margin-top: 22px
- Margin-bottom: 28px

**Warm regards,**
- Font-size: 16px
- Color: #5c5c5c
- Line-height: 1.7
- Margin-bottom: 10px
- Font-weight: 400

**People and Culture Team**
- Font-size: 18px
- Font-weight: 700
- Color: #111111
- Line-height: 1.6
- Margin-bottom: 6px

**Taleemabad**
- Font-size: 18px
- Font-weight: 700
- Color: #2f5fc7
- Line-height: 1.6
- Margin-bottom: 10px

**Email + Website**
- Font-size: 16px
- Line-height: 1.7
- Color: #2f5fc7
- Links: color #2f5fc7, text-decoration underline
- Separator pipe: color #7d7d7d, spacing 10px around

**Sent on behalf line**
- Font-size: 15px
- Line-height: 1.7
- Color: #9a9a9a
- Margin-top: 18px
- Font-weight: 400

**Signature padding:**
- Padding-top: 10px
- Padding-bottom: 18px

---

## COLOR PALETTE (LOCKED — NO EXCEPTIONS)

| Element | Color | Hex |
|---------|-------|-----|
| Page background | Light grey | `#f5f5f5` |
| Grey wrapper | Soft grey | `#e5e7e2` |
| Card background | White | `#ffffff` |
| Headers/titles/dividers | Royal blue | `#3157b7` |
| Subtitle | Muted blue | `#5d73b8` |
| Links | Blue | `#3d63c8` |
| CTA button | Purple | `#5b3fc4` |
| Button text | White | `#ffffff` |
| Body text | Pure black | `#111111` |
| Warm regards text | Grey | `#5c5c5c` |
| Signature blue | Dark blue | `#2f5fc7` |
| Signature grey | Light grey | `#9a9a9a` |
| Divider (sig) | Light grey | `#d9d9d9` |
| Divider (header) | Blue | `#4b67d1` |

**NO OTHER COLORS ALLOWED. NOT EVEN SLIGHTLY DIFFERENT SHADES.**

---

## TYPOGRAPHY (LOCKED — NO EXCEPTIONS)

| Element | Font | Size | Weight | Line-Height |
|---------|------|------|--------|-------------|
| Body/page | Georgia serif | — | — | — |
| Top label | Georgia serif | 12px | 500 | 1.4 |
| Title | Georgia serif | 24px | 700 | 1.2 |
| Subtitle | Georgia serif | 13px | 400 | 1.5 |
| Greeting | Georgia serif | 17px | 400 | 1.8 |
| Body text | Georgia serif | 17px | 400 | 1.85 |
| Links | Georgia serif | 17px | 400 | 1.85 |
| Callout | Georgia serif | 17px | 700 | 1.85 |
| Button | Georgia serif | 16px | 700 | — |
| Button subtitle | Georgia serif | 16px | 400 | 1.6 |
| Signature (warm) | Georgia serif | 16px | 400 | 1.7 |
| Signature (team) | Georgia serif | 18px | 700 | 1.6 |
| Signature (sent) | Georgia serif | 15px | 400 | 1.7 |

**NO INTER, POPPINS, SANS-SERIF BODY TEXT, OR MODERN FONTS.**

---

## WHEN TO USE THIS TEMPLATE

**ALWAYS use this template for:**
- ✅ Interview invites (all stages: values, warm bench, case study, GWC, zero-in, final, offer)
- ✅ Rejections (any stage)
- ✅ Exploratory call invites
- ✅ Follow-up/status emails to candidates
- ✅ Any formal candidate communication

**DO NOT use for:**
- ❌ Warm bench FEEDBACK emails (use warm_bench_final_locked_approach.md instead)
- ❌ Values feedback emails (use values_feedback_email_tone_locked template instead)
- ❌ Internal team emails

---

## SELF-CHECK BEFORE SENDING

- [ ] Background: `#f5f5f5`
- [ ] Grey wrapper: `#e5e7e2`, calc(100% - 90px) width, 38px padding top/bottom
- [ ] White card: 775px, `#ffffff`, centered
- [ ] Logo: 34px, centered, margin-bottom 16px
- [ ] Top label: Georgia 12px, `#3157b7`, uppercase, letter-spacing 2.4px
- [ ] Title: Georgia 24px bold, `#3157b7`, line-height 1.2
- [ ] Subtitle: Georgia 13px, `#5d73b8`
- [ ] Divider: 2px solid `#4b67d1`
- [ ] Body: Georgia 17px, `#111111`, line-height 1.85
- [ ] Links: `#3d63c8`, underlined
- [ ] Callout: Georgia 17px bold, `#3d63c8`
- [ ] Button: `#5b3fc4` background, white text, Georgia 16px bold
- [ ] Signature divider: 1px solid `#d9d9d9`, NOT centered
- [ ] Signature left-aligned (NOT centered)
- [ ] All spacing exactly as specified
- [ ] No yellow highlighting anywhere
- [ ] No shadows, no border-radius (except button)
- [ ] No modern fonts in body

---

## REFERENCE IMPLEMENTATION

**Script:** `scripts/send_values_interview_pilot.py`
- Table-based HTML for Gmail compatibility
- CID-embedded Taleemabad logo only
- Supports PILOT_MODE (Ayesha review) + LIVE mode (candidates)
- Configurable: CANDIDATE_NAME, POSITION, JD_LINK, PREP_GUIDE_LINK, BOOKING_LINK

**To adapt for other purposes:**
1. Copy the script
2. Rename (e.g., send_gwc_rejection.py)
3. Update config variables: CANDIDATE_NAME, POSITION, links
4. Update content sections: greeting, body paragraphs, callouts, button text
5. Keep HTML structure 100% identical
6. Send pilot to Ayesha before going live

---

## ENFORCEMENT

**This specification is LOCKED.** Any deviation requires explicit user approval and must be documented.

If you catch yourself about to send a candidate email that doesn't match:

1. **STOP**
2. **READ THIS FILE AGAIN**
3. **Rebuild using exact spec**
4. **Send to Ayesha for pilot approval FIRST**
5. **Only go live after approval**

---

**Locked Date:** 2026-05-13  
**Verified Against:** Complete editorial refinement session + reference screenshots  
**Approved By:** Ayesha Khan (implicit via email reference)  
**Scope:** ALL candidate-facing emails (invites, rejections, follow-ups, any formal communication)  
**Status:** 🔒 PRODUCTION READY — ZERO VARIATIONS ALLOWED

