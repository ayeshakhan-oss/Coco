---
name: P.S. Section Styling — Locked Guidelines (2026-06-08)
description: Premium personal styling for postscript sections in all candidate feedback/communication emails. Creates handwritten-note feel. Required for warm bench, GWC, values feedback, all candidate emails.
type: reference
metadata:
  appliesTo: All candidate communication emails (warm bench, GWC rejection, values feedback, screening rejection, offer, etc.)
  status: MANDATORY FOR ALL EMAILS
---

# P.S. Section Styling — Locked (2026-06-08)

**Status:** 🔒 MANDATORY — Apply to ALL candidate communication emails going forward.

**Goal:** P.S. section should feel like a personal handwritten note added after the formal email—intimate, memorable, emotionally resonant, premium.

---

## Visual Design

### Whitespace & Spacing
- **Top margin:** 30px (generous separation from main body)
- **Top border:** None (no line separator)
- **Padding:** 0 (no extra box)
- **Bottom padding:** Inherited from parent (50px from main email padding)

### Typography

**"P.S." Label:**
- Font: Georgia serif
- Size: 15px (or 90-95% of body 16px)
- Weight: Bold
- Color: #555 (dark gray, not pure black)
- Margin below: 12px

**P.S. Body Text:**
- Font: Georgia serif
- Size: 15px (90-95% of body 16px)
- Weight: Regular
- Style: **ITALIC** (critical—this is the personal touch)
- Color: #555 (dark gray #555, not #333)
- Text alignment: Justified
- Line height: 1.8 (increased from 1.75 for thoughtful, breathable feel)
- Margin: 0

### No Styling Elements
- ❌ No background color
- ❌ No borders
- ❌ No callout boxes
- ❌ No colored backgrounds
- ❌ No emojis
- ❌ No heavy visual elements
- ✅ Pure text, pure Georgia serif, pure italics

---

## HTML/CSS Implementation

**Exact code for P.S. section:**

```html
<div style="margin-top:30px; padding-top:30px; border-top:none;">
  <p style="font-family:Georgia,serif; font-size:15px; color:#555; font-weight:bold; margin:0 0 12px 0;">P.S.</p>
  <p style="font-family:Georgia,serif; font-size:15px; color:#555; text-align:justify; line-height:1.8; margin:0; font-style:italic;">
    {ps_content}
  </p>
</div>
```

**Key points:**
- `margin-top:30px` — generous whitespace above
- `border-top:none` — explicitly no divider line
- `font-size:15px` — 15px is 93.75% of 16px body (within 90-95% range)
- `color:#555` — dark gray, softer than pure black (#333)
- `font-style:italic` — CRITICAL—makes it feel personal
- `line-height:1.8` — slightly increased from 1.75 for breathing room
- `text-align:justify` — consistent with body text
- **No extra styling, no borders, no colors**

---

## When to Use

**Apply to:**
- ✅ Warm bench emails (GWC rejections using warm bench structure)
- ✅ Values feedback emails
- ✅ GWC rejection emails
- ✅ Screening rejection emails
- ✅ Any candidate feedback/rejection email
- ✅ Offer emails

**P.S. Content Rules:**
- Reference ONE powerful interview moment
- Tie back to character/who they are
- Emotional, brief (2-3 sentences max), memorable
- Personal tone (contrasts with formal 3 sections above)
- Candidate should want to screenshot it
- Never generic encouragement—always specific to their story

**Example P.S.:**
```
P.S. The panel asked you a hard question about how you support a teacher who's stuck. 
And instead of the clinical answer, you went somewhere real. You talked about actually 
sitting with that teacher, understanding their frustration, and then helping them see 
possibility again. That kind of human attunement, that willingness to be present with 
difficulty rather than solve it, that's a strength that will serve you well wherever 
you work next.
```

---

## Template Integration

**For warm_bench_email.html:**

```html
<!-- P.S. Section with Premium Personal Styling -->
<tr>
  <td style="padding:0 70px 50px 70px;">
    <div style="margin-top:30px; padding-top:30px; border-top:none;">
      <p style="font-family:Georgia,serif; font-size:15px; color:#555; font-weight:bold; margin:0 0 12px 0;">P.S.</p>
      <p style="font-family:Georgia,serif; font-size:15px; color:#555; text-align:justify; line-height:1.8; margin:0; font-style:italic;">
        {ps_content}
      </p>
    </div>
  </td>
</tr>
```

**For custom HTML emails:**
- Copy exact div + p styling above
- Replace `{ps_content}` with actual P.S. text
- Keep padding consistent with email body (70px)

---

## Script Implementation

When building email body content in Python:

```python
PS_CONTENT = """
The panel asked you a hard question... [your P.S. text]
"""

BODY_CONTENT = f"""
<p style="font-family:Georgia,serif; ...">Dear [Name],</p>

[Main body sections: Stayed, Honest, Leave]

<div style="margin-top:30px; padding-top:30px; border-top:none;">
  <p style="font-family:Georgia,serif; font-size:15px; color:#555; font-weight:bold; margin:0 0 12px 0;">P.S.</p>
  <p style="font-family:Georgia,serif; font-size:15px; color:#555; text-align:justify; line-height:1.8; margin:0; font-style:italic;">
    {PS_CONTENT}
  </p>
</div>

[Signature: Warm regards, etc.]
"""
```

---

## Email Client Compatibility

**Tested on:**
- Gmail (desktop + mobile)
- Outlook (desktop + mobile)
- Apple Mail
- Mobile email clients

**Ensures:**
- ✅ Italics render correctly across all clients
- ✅ Font size 15px readable on mobile (no size jumps)
- ✅ Color #555 displays consistently (not too light on dark backgrounds)
- ✅ Line height 1.8 provides breathing room without excessive space
- ✅ Justified text aligns cleanly without breaking on mobile
- ✅ No CSS that unsupported email clients will strip

---

## Design Philosophy

**This styling creates:**
1. **Visual separation** — P.S. feels distinct from formal body (30px margin, italics, softer color)
2. **Personal intimacy** — Italics + smaller font + dark gray = handwritten feel
3. **Premium aesthetic** — No borders, no colors, no clutter—pure text elegance
4. **Emotional resonance** — Readers pause at P.S., re-read it, remember it
5. **Mobile-friendly** — Readable on all devices, no layout breaks

**Non-goal:** Heavy visual styling, borders, callouts, emojis, background colors. Those undermine the "personal note" feeling.

---

## Checklist (Before Sending)

- [ ] P.S. content references ONE specific interview moment
- [ ] P.S. ties moment back to character/who they are
- [ ] P.S. is 2-3 sentences max (brief, memorable)
- [ ] P.S. styling: 15px, #555 color, italic body, bold "P.S." label
- [ ] P.S. margin-top: 30px (generous whitespace above)
- [ ] P.S. line-height: 1.8 (breathable)
- [ ] No borders, no colors, no boxes around P.S.
- [ ] Paragraph margin: 0 (no extra spacing below)
- [ ] Font: Georgia serif (consistent with body)
- [ ] Text alignment: Justified (consistent with body)
- [ ] Tested on mobile + desktop email clients

---

## Reference

**Updated:** 2026-06-08  
**Applied to:** All candidate communication emails  
**Template:** `templates/warm_bench_email.html` (now includes P.S. placeholder)  
**Example:** Hira Abbasi email (2026-06-08)

---

**This is now MANDATORY for all candidate feedback emails. No exceptions.**
