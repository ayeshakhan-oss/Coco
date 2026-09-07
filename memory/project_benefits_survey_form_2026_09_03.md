---
name: Benefits Pulse Check Google Form (P&C, 2026-09-03)
description: Staff benefits survey behind the T-Flex 2027 flexible-benefits draft; Forms API is now enabled and usable with the existing Drive token.
metadata:
  type: project
---

# Benefits Pulse Check — staff survey (built 2026-09-03)

## What it is

An anonymous 12-question staff survey supporting Ayesha's **Draft T-Flex 2027** flexible-benefits
paper (leadership working document, status: research in progress). Ayesha's brief was explicit:
**a vibe check only — nothing may give employees hope that a flexible pool is happening.**
The T-Flex name is deliberately **absent** from the form.

- **Form ID:** `1FJeLmuKHw-XVilArMFkodZobTMGep_fLcBER-_yFWmk`
- **Edit:** https://docs.google.com/forms/d/1FJeLmuKHw-XVilArMFkodZobTMGep_fLcBER-_yFWmk/edit
- **Live:** https://docs.google.com/forms/d/e/1FAIpQLSd-eStYElezDh5PuxaqtE0KstPrkaNPEkKP_T8pLuVGH22y2Q/viewform
- **Title:** Benefits Pulse Check · **Drive name:** Benefits Pulse Check - P&C 2026
- Owned by **ayesha.khan@** (built with `token_sheets_broad.json`, her own OAuth token), Drive root.
- Builder: `scripts/pnc/build_benefits_survey_form.py` (source of truth for all 12 items)
- Patcher: `scripts/pnc/patch_benefits_survey_form.py` — `python patch_benefits_survey_form.py info 1 7`
  pushes the form description (`info`) and/or 0-based item indices from the builder's `ITEMS`.

**Never re-run the builder to "fix" the live form** — it creates a second form on a new URL.
Edit `ITEMS`/`DESCRIPTION` in the builder, then patch the existing ID in place. Same rule as the
P&C tracker sheet and the fundraising deck: update in place, never create a second copy.

## 🔑 CAPABILITY UNLOCKED — the Google Forms API now works here

The probe returned **`SERVICE_DISABLED`, not a scope error**: the `drive` scope on
`token_sheets_broad.json` is **already accepted by the Forms API**, no new consent needed.
The only blocker was the API being off on **GCP project 954828175525**, which **Ayesha enabled on
2026-09-03**. Forms is therefore a live capability alongside Sheets/Docs/Drive.

**Diagnostic rule:** read the 403 body before declaring a capability unavailable.
`SERVICE_DISABLED` = one console click by Ayesha. `insufficient scope` = a real re-consent.
I nearly reported "we need a forms.body token" on a project that only needed the API switched on.
(Contrast: the **Slides API is still NOT enabled** on the same project — build .pptx with
python-pptx and let Drive convert.)

## What the Forms API cannot do (must be done in the UI)

- **Checkbox "select at most N" response validation is not exposed by the API.** Q2 and Q9 say
  "Please select up to 3" in the item description only; it is guidance, not a cap. Enforcing it =
  three-dot menu → Response validation → Select at most 3, per question.
- **Email-collection / response settings are not settable via the API.** Default is off (which is
  what an anonymous spend survey needs) but it must be eyeballed in Settings → Responses.
- **Clearing an item description:** `updateItem` with `updateMask: "title,description,questionItem"`
  and an item dict that simply omits `description` does NOT reliably clear it — set
  `item["description"] = ""` explicitly. `patch_benefits_survey_form.py` does this via `setdefault`.
- `forms.create` accepts only `info.title` / `info.documentTitle`; the description and every item
  must follow in a `batchUpdate`.

## Structure (12 questions, Ayesha's own wording, order unchanged)

1. Scale 1-5, how well current benefits meet needs
2. Checkbox, most valuable benefits (+Other) — includes **Physiotherapy, Dental, Cosmetics** added
   after OPD on 2026-09-03 at Ayesha's request
3. Checkbox, least used / not used at all (+Other)
4. Radio, OPD spend this year (7 bands, incl. Prefer not to say)
5. Checkbox, types of OPD expense (+Other)
6. Radio, mental wellbeing / personal development spend
7. Radio, professional learning spend
8. Scale 1-5, appeal of more choice in allocation
9. Checkbox, where additional support should go (+Other)
10. Radio, fixed vs hybrid vs flexible vs not sure
11. Paragraph, unmet needs (optional)
12. Paragraph, one thing to change (optional)

Q1-Q10 required, Q11-Q12 optional.

## 🔴 The worked example belongs in the FORM description, not the question description

I first put the hypothetical pool example on Q8's own description. Ayesha rejected it: it belongs in
the **form description at the top** so people understand the concept before they start. Current
top-of-form description runs four paragraphs in this order, and the order is deliberate — framing
lands before the number does:

1. P&C is reviewing how benefits are designed
2. **research exercise, not an announcement**; no change proposed, approved or budgeted; answers do
   not create an entitlement; a question being asked does not mean the benefit is being introduced
3. the hypothetical: *suppose a pool of PKR 200,000 per year per individual, drawn through a wallet
   or similar mechanism* — amount and mechanism **purely illustrative, nothing fixed, costed or approved**
4. aggregate review, ~5 minutes

**Reusable rule for any exploratory staff survey:** the no-promise framing goes in the form
description where it cannot be skipped, and every hypothetical figure is hedged in the same sentence
that introduces it.

## Reference numbers from the T-Flex draft (for reading results)

Current baseline **PKR 14.5M across 176 staff (107 permanent / 69 contractual), excluding OPD** —
roughly **PKR 82,000 a head**. IPD 400K, maternity 200K C-section / 150K normal, room limit 10K/day,
mental wellbeing cap 30K/yr, professional development cap 40K/yr.
⚠️ The **PKR 200,000** illustration is ~2.4x the current per-head average, so expect some anchoring
on it as a floor when results come back.

## Open flags raised to Ayesha, not yet decided

- **"Cosmetics"** in Q2 will be read inconsistently (cosmetic surgery vs skincare vs skipped).
  "Cosmetic procedures" is clearer if that is the intent.
- **No permanent/contractual field.** Ayesha specified exactly 12 questions and I built exactly
  those. Cost: Q3 ("least used or not at all") cannot distinguish *doesn't want it* from
  *not eligible for it* for the **69 contractual staff**, who receive no parents healthcare, no
  quarterly lunch and no BusCaro subsidy. One-minute fix if she wants it as a new Q1.
- I have **not visually checked** the rendered form (Rule 14) — API confirms structure, not
  appearance. Google Forms renders a long description as one dense grey block.
