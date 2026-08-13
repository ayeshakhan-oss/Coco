# Contract Email — Design Variants

Sub-skill of [Skill 07](SKILL.md). A design bake-off ran 2026-08-13/14: same locked wording,
same attachments, different presentation.

## 🏆 WINNER — Design 3 is the STANDARD for ALL contract-related emails (Ayesha 2026-08-14)

Every joining / contract / onboarding email now uses **Design 3**. It is variable-driven, so it
serves any programme — not just NIETE. Designs 1 and 2 are kept below for reference only.

Went live 2026-08-14 to Hina Fatima Jafri and Noor Ul Ain Rana (NIETE CPD - Coach).

---

## ⚠️ Naming: "design" ≠ "template"

Two numbering schemes are live and they are NOT the same thing:

| Scheme | Meaning | Where |
|---|---|---|
| **Templates 1–4** | **Content** — which words go to whom (paid fellow, volunteer, transition, NIETE) | [joining-emails.md](joining-emails.md) |
| **Designs 1–3** | **Presentation** — how the NIETE email (Template 4) looks | this file |

All designs below carry the **same Template 4 wording**. Never mix the numbers up.

---

## Design 1 — Plain (DEFAULT)

**Script:** `scripts/contracts/send_niete_joining_emails.py`
Plain Gmail styling: black text, `<br><br>` paragraphs, bolded key details, bulleted
"Important Things", Ayesha's Gmail signature verbatim. Indistinguishable from a hand-typed
email. **This remains the approved default until Ayesha picks otherwise.**

```bash
python scripts/contracts/send_niete_joining_emails.py                 # pilot both
python scripts/contracts/send_niete_joining_emails.py --live --who hina --cc a@x,b@y
```

## Design 2 — Structured card

**Script:** `scripts/contracts/send_niete_email_design2.py`
Locked 2026-08-14 after five rounds of Ayesha's direction.

- **White header** so the logo carries it (66px, no box behind it), hairline bottom rule
- Eyebrow: **NIETE Project** in deep green `#2f6b52` · **Taleemabad** in blue `#2f4fa2`
- Headline serif navy, first name in deep green, 46px green accent rule
- Sub-line **sans-serif** blue: "We're glad to have you joining us as a **CPD - Coach**…"
- **"Your role at a glance"** table — **sans-serif**, muted labels left, bold values right,
  hairline rules, no card, no icons. Compensation is a **hero row**: 23px deep green.
  Muted tax note beneath, then a green left-bar callout with the first-day line.
- Numbered "Your next two steps", two buttons, three-across "Important Things" with
  line icons, signature with **phone + LinkedIn**, footer bar.

```bash
python scripts/contracts/send_niete_email_design2.py --who hina        # pilot
python scripts/contracts/send_niete_email_design2.py --live --who hina --cc a@x
```

## Design 3 — Two-column welcome letter

**Template:** `templates/niete_joining_design3.html` (variables only — no candidate data)
**Script:** `scripts/contracts/send_niete_email_design3.py`
Built 2026-08-14 from Ayesha's written spec.

- 880px card; navy hero with faint open-book line motif, logo top-right, name in green
- **65/35 two-column** built with the **fluid-hybrid** technique (inline-block + max-width
  + MSO ghost tables) so it stacks on mobile **without needing a media query** — this is
  what makes two columns safe in Gmail's app, where `<style>` can be stripped
- Left: details card (circular pale-blue icons), attachment callout, "Two things to do",
  two CTA buttons. Right: "Your journey starts here" (hill/flag illustration + 3 items),
  "A few important things to know" (3 items)
- Closing + signature with phone/LinkedIn, pale footer bar

**Variables:** `CANDIDATE_FIRST_NAME · ROLE · PROJECT_NAME · PARTNER_NAME · START_DATE ·
CONTRACT_END_DATE · COMPENSATION · COMMITMENT · ONBOARDING_FORM_URL · WHATSAPP_GROUP_URL ·
SENDER_NAME · SENDER_TITLE` plus generated blocks `DETAIL_ROWS · JOURNEY_ITEMS ·
IMPORTANT_ITEMS · SENDER_CONTACT` (optional blocks render empty, never blank text).
Rendering **fails loudly** on any unresolved variable rather than emailing `{{...}}`.

```bash
python scripts/contracts/send_niete_email_design3.py --who hina
python scripts/contracts/send_niete_email_design3.py --live --who hina --cc a@x
```

**Justified text (2026-08-14):** body copy in the wide main column is `text-align:justify`
(house style). It is tagged `class="just"` and **relaxes to left-aligned under 620px** —
justification in a narrow column opens rivers of white space. The narrow sidebar is never
justified for the same reason.

**Mobile hardening:** columns stack via fluid-hybrid (no media query needed); the media query
then adds reduced padding, smaller hero type, full-width tappable buttons (15px padding),
removes the sidebar's desktop gutter, and lets long values wrap (`.dval`) instead of forcing
the row wide. Only the Commitment value is allowed to wrap on desktop; dates and money stay
on one line.

**Omitted deliberately:** the plant/mug illustration — it needs real artwork, and the spec
said include only if clean. **Hero pattern caveat:** delivered as a CID background image;
clients that ignore background images fall back to flat navy, which is graceful.

---

## Constraints every design must respect

1. **Wording is Template 4** — only presentation changes.
2. **NIETE onboarding form**, not the Fellow form. Harness blocks a mismatch.
3. **Bold** the joining date, compensation, duration, designation, hours, probation.
4. Table layout + inline CSS only. **No flexbox, no grid, no web fonts, no SVG** (Gmail).
5. Icons are **CID-embedded PNGs** from `assets/email_icons/`; attach only those referenced.
6. **Single column.** Two-column layouts squash in Gmail's mobile app.
7. Attachments: Contract + Permanent Employee NDA, **PDF only**.
8. Pilot to Ayesha, no CC. Live CC is given per person.

## Assets

`assets/email_icons/*.png` — nine 40px line icons (briefcase, calendar, calendar-end,
wallet, clock, doc, shield-check, hourglass, bus), navy/slate stroke, drawn by
`scratchpad/mkicons2.py`. Regenerate rather than hand-editing.

⚠️ **No renderer on this machine** — designs cannot be visually verified. Every variant
needs Ayesha's eye on desktop *and* phone.
