---
name: Locked Skill — Warm Bench Interview Invite
description: CPD Coach warm bench candidate interview invite template. Design specification LOCKED. Formal letter style. For candidates values+GWC cleared.
type: project
status: LOCKED
originSessionId: continuation-2026-04-27
---

# Warm Bench Interview Invite Skill — LOCKED

**Status:** PRODUCTION READY — DESIGN LOCKED

**Purpose:** Send interview invites to warm bench candidates (values + GWC cleared, newly opened positions). Tone: casual/quick conversation, not formal zero-in. Messaging emphasizes candidate's existing cultural fit and hiring manager's desire for quick chat to assess skills.

**Script Location:** `c:/Agent Coco/scripts/jobs/job17/send_job17_warmBench_pilot.py`

---

## Design Specification (LOCKED — DO NOT DEVIATE)

### 1. PAGE BACKGROUND
- Color: `#f3f4f6` (very light grey)
- Padding: 60px top/bottom

### 2. EMAIL CARD (MAIN CONTAINER)
- Background: `#ffffff`
- Max width: `620px`
- Center aligned
- Padding inside: `60px` top/bottom, `70px` left/right
- Border radius: `8px`
- Shadow: `box-shadow: 0 2px 12px rgba(0,0,0,0.04)`

### 3. LOGO
- Center aligned
- Width/Height: `48px`
- Space below: `24px`
- CID-embedded in email (not external link)

### 4. TOP LABEL
- Text: `PEOPLE & CULTURE • WARM BENCH OPPORTUNITY`
- Font: `Arial, sans-serif`
- Size: `12px`
- Letter spacing: `2px`
- Color: `#4b6cb7` (muted blue)
- Text transform: `UPPERCASE`
- Center aligned
- Margin bottom: `24px`

### 5. MAIN TITLE
- Example: `{POSITION}` (e.g., "CPD Coach")
- Font: `Georgia, serif`
- Size: `28px`
- Weight: `bold`
- Color: `#2f4fa2` (deep royal blue)
- Line height: `1.3`
- Center aligned
- Margin bottom: `10px`

### 6. SUBTITLE
- Example: `A New Role Aligned With Your Expertise`
- Font: `Georgia, serif`
- Size: `15px`
- Color: `#5a6ea8` (lighter blue)
- Center aligned
- Margin bottom: `32px`

### 7. DIVIDER LINE
- Height: `1px`
- Color: `#2f4fa2`
- Width: 100%
- Margin: `30px 0 50px 0` (before body, after subtitle)

### 8. GREETING
- Example: `Hi {candidate_name},`
- Font: `Georgia, serif`
- Size: `20px`
- Weight: `bold`
- Color: `#2f4fa2`
- Margin bottom: `18px`
- Line height: `1.3`

### 9. BODY TEXT
- Font: `Georgia, serif`
- Size: `16px`
- Color: `#000000` (pure black)
- Line height: `1.75`
- Margin bottom per paragraph: `18px`
- Text align: `LEFT`
- Max readable width (keep within padding)

### 10. LINKS
- Color: `#2f4fa2`
- Text decoration: `none`
- Font weight: `bold`

### 11. CALL-TO-ACTION BUTTON
- Background: `#2f4fa2`
- Text: `📅 Lock the Calendar`
- Font: `Georgia, serif`
- Size: `15px`
- Weight: `bold`
- Padding: `14px 32px`
- Border radius: `4px`
- Color: `#ffffff`
- Margin: `0 70px 50px 70px`

### 12. BUTTON SUBTITLE
- Font: `Georgia, serif`
- Size: `14px`
- Color: `#5a6ea8`
- Text: "Please lock a slot at your earliest convenience."
- Margin: `0 70px 60px 70px`

### 13. FOOTER TEXT
- Font: `Georgia, serif`
- Size: `14px`
- Color: `#5a6ea8`
- "Feel free to connect with us on our socials to get a sense of our culture:"
- Margin bottom: `20px`

### 14. SOCIAL ICONS
- Logo sizes: Taleemabad 32x48, Facebook 36x36, Instagram 36x36, LinkedIn 36x36
- Padding: 16px right (Taleemabad), 12px right (others)
- Border radius: `4px`

### 15. CLOSING
- "See you soon," — Georgia serif, 16px, bold, #000000, margin 0 0 6px 0
- "Team Taleemabad" — Georgia serif, 16px, #000000, margin 0 0 16px 0
- "Coco – AI Assistant Taleemabad" — Georgia serif, 13px, #5a6ea8, margin 0

### 16. FOOTER DIVIDER
- Height: `1px`
- Color: `#e8e8e8` (light grey)

---

## Spacing Rules (LOCKED)
- Large spacing between sections (40–60px)
- Do NOT compress text
- Design must feel: **airy**, **formal**, **like a printed letter**

---

## What to Avoid (LOCKED)
- ❌ Do NOT make it look like a marketing email
- ❌ Do NOT use bright blue (only #2f4fa2 and #4b6cb7)
- ❌ Do NOT reduce spacing
- ❌ Do NOT use modern UI fonts (Inter, Poppins, etc.)
- ❌ Do NOT make text grey (keep dark: #000000 for body, #2f4fa2 for accents)
- ❌ Do NOT change card width from 620px
- ❌ Do NOT change padding from 70px left/right, 60px top/bottom
- ❌ Do NOT change divider color or positioning
- ❌ Do NOT change background color from #f3f4f6

---

## Content Template

**Subject:** `A New Opportunity Aligned With Your Profile — {POSITION}`

**Body (in order):**
1. Greeting: "Hi {candidate_name},"
2. Intro: "You're one of our warm bench candidates..." (explain warm bench, opening, quick conversation)
3. Tone: "This is an informal chat..." (no prep needed, reconnect and explore fit)
4. Resources: "The JD for this position is here, and you can explore more about Taleemabad through the following links:"
   - Magic of Taleemabad (YouTube link)
   - Impact in a one-minute video (Drive link)
5. Consent: "This session will be recorded, and by joining, you consent to being a part of the recorded call."
6. Prep guide: "Please go through the interview prep guide to understand the process."
7. Closing: "Let us know if you need anything ahead of the conversation."
8. CTA: Button linking to Google Calendar booking

---

## Code Notes

- Script: `send_job17_warmBench_pilot.py`
- Uses: `safe_sendmail()` from scripts/utils/safe_send
- CID embedding: All 4 logos (Taleemabad, Facebook, Instagram, LinkedIn)
- PILOT_MODE: True by default (sends to Ayesha), set False for live send
- Database: Query candidates table for {candidate_name} and {email}

---

## Usage

1. **For pilot:** Run script with PILOT_MODE=True (default) → sends to ayesha.khan@taleemabad.com
2. **For live send:** 
   - Create list of candidates
   - Update CANDIDATES array with name/email pairs
   - Set PILOT_MODE=False
   - Run script
3. **Customization per position:** Only change POSITION, BOOKING_LINK, JD_LINK, TEAMS_LINK; everything else LOCKED

---

## Design Lock Reason

User explicitly specified: "This is a design specification, not a suggestion." Exact colors, fonts, spacing, and layout ratios must remain unchanged to maintain formal letter aesthetic and brand consistency.

**Locked Date:** 2026-04-27  
**Approved By:** Ayesha Khan  
**Status:** ✅ PRODUCTION READY
