---
name: Email Template Format - EXACT (Confirmed)
description: Taleemabad email template format - MANDATORY for all rejection/feedback emails
type: reference
---

# Email Template Format - EXACT REQUIREMENTS

**THIS IS THE STANDARD FORMAT FOR ALL REJECTION AND FEEDBACK EMAILS. USE EVERY TIME.**

## Structure (Top to Bottom):

1. **Logo** (centered, ~0.8 inch height)
   - Taleemabad logo image at top

2. **Header Text** (centered, small, blue #1565c0, letter-spaced)
   - "PEOPLE & CULTURE • [TYPE]"
   - Examples: "PEOPLE & CULTURE • REJECTION DECISION", "PEOPLE & CULTURE • APPLICATION UPDATE"

3. **Yellow/Gold Position Box** (centered, bright yellow #FDD835 background)
   - Position name or role (e.g., "Hackathon 2026", "Field Coordinator, Research & Impact Studies")
   - Padding: 8px top/bottom, 12px left/right
   - Bold, centered text

4. **Horizontal Dividing Line** (dark #333333, 2px)
   - Full width separator below yellow box

5. **Body Content** (justified Georgia serif, 11px, 16px leading)
   - Greeting: "Hi [FirstName]," in regular text
   - Paragraphs in justified Georgia serif
   - Headings in bold, blue #1565c0
   - No "I" voice—always "We"

## CSS/Styling Details:

- **Font:** Georgia serif throughout body
- **Justification:** TA_JUSTIFY for all body paragraphs
- **Line height:** 16px leading
- **Color scheme:** Blue #1565c0 for headers/headings, Gold #FDD835 for position box
- **Background:** White body on light background

## Reference Scripts:

- Generation: `generate_gwc_exact_format.py`
- Similar: `send_job32_values_invite.py`, other rejection emails

## Critical Remember:

**DO NOT USE PLAIN TEXT. DO NOT USE V8 BLUE HEADER BAND. ALWAYS USE THIS EXACT TEMPLATE WITH LOGO, YELLOW BOX, AND HORIZONTAL LINE.**

This format has been used for 30+ days. Never forget it again.
