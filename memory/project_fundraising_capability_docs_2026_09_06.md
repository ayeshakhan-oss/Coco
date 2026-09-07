---
name: Fundraising Capability Doc Set (P&C, 2026-09-06)
description: Working guide + facilitator guide + 10-slide deck for the Fundraising theme. No personal names, no invented Taleemabad figures, internal working-doc tone.
type: project
---

# Fundraising Capability Doc Set — P&C (2026-09-06)

Built for Ayesha's **P&C Buddy work on the Fundraising theme**. Companion to
[pnc_buddy_tracker_project_2026_08_19](pnc_buddy_tracker_project_2026_08_19.md) and
[pnc_buddy_meeting_tracker_sheet_2026_09_06](pnc_buddy_meeting_tracker_sheet_2026_09_06.md).

Origin: Ayesha pasted a long ChatGPT research output (fundraising best practice, sector JDs,
and the funders she cares about) and asked for a Google Doc. It then went through a full tone
rewrite and split into three artefacts.

## The five files

All owned by `ayesha.khan@`, folder **"People and Culture Buddy"** `1R0ZZCZ81v-cgHr22PbRp_KFJiCJ91_Kj`.
Sources are in `docs/pnc_buddy/`. **Edit the source and re-render to the SAME file IDs. Never
create a second copy.**

| Artefact | Source | ID |
|---|---|---|
| Fundraising Capability \| P&C + Fundraising Working Guide (master, ~5,300 words) | `FUNDRAISING_CAPABILITY_WORKING_GUIDE.md` | `1ERHy6vp_T0ERorKKEvvdrJUPtwx0BCYJHsyIqcp7IJ8` |
| Fundraising Capability Workshop \| Facilitator Guide (7 pages) | `FUNDRAISING_WORKSHOP_FACILITATOR_GUIDE.md` | `1IkXbBZeLPq9KXBOaL6kmJcU3ULhHWTYmEJmDNhkwV8I` |
| Fundraising Capability Workshop \| Deck Outline | `FUNDRAISING_WORKSHOP_DECK_OUTLINE.md` | `1af_qcCZxIRN4YOS6J-DrRSV1Y6EVl4PCCO-UcTGA5gk` |
| **Fundraising Capability Workshop** (Google Slides, 10 slides) | `scripts/pnc/build_fundraising_workshop_deck.py` | `10jpoN7IsA0Az-zNeRx1kkJq2blyceIQKP69RlcGGSeo` |
| Fundraising Capability Workshop.pptx (downloadable) | same script | `1nFJJvs4Fdv6dE0xvXdg5jsaEK8Q1JAjm` |

`FUNDRAISING_CAPABILITY_WORKSHOP_GUIDE.md` is the **superseded v1.0 source**, committed only as
a record. Do not render it.

## 🔴 NO PERSONAL NAMES. EVER.

Ayesha said it twice. The second time was in caps, after I reintroduced the names because her
own brief referenced them in required content ("for X to use while running the workshop",
"we want Y and Z to understand..."). **A brief that mentions people by name is not permission to
put those names in the document.** Use role labels: **Senior Manager Fundraising** for the lead,
**Track A** (donor intelligence and relationships) and **Track B** (opportunity and proposal
development) for the two team members. Placeholders read
`[To be added/validated with Fundraising / Finance / Programmes]`, never a person's name.
Verify with a name scan on the **rendered** Doc and on the deck's text and speaker notes, not
just the markdown source.

## 🔴 Tone: an internal working document, not a consulting report

Ayesha rejected v1.0's register outright. What she wants is something P&C could plausibly have
drafted after a working session, now going to the fundraising lead for correction.

- Voice: "we", "our team", "for our context", "what we want the team to be able to do".
- Hedge anything proposed: "we could", "one way we can approach this", "the Senior Manager
  Fundraising may already have a way of doing this".
- **Leave real questions open.** The master ends on a list of open questions rather than a
  packaged answer for everything.
- **BANNED constructions:** "the key is", "at its core", "X is not Y, it is Z", "the most common
  mistake", "this is where the magic happens", motivational one-liners, dramatic single-line
  statements, a tidy conclusion after every section, symmetrical three-part phrasing, and the
  same headings repeated under every item (v1.0 had "What it means / What good looks like / How
  we build it" twelve times).
- Her own rewrites, worth keeping as calibration:
  - ✗ "The most common mistake in a young fundraising team is to treat fundraising as proposal
    writing." → ✓ "One thing we want to avoid is thinking of fundraising as mainly proposal
    writing. Proposal development is one part of the overall process."
  - ✗ "Reward the best judgement, not the most pages of notes." → ✓ "When reviewing donor
    research, we should focus more on the quality of the recommendation than the amount of
    information collected."
  - ✗ "A pipeline that is not current is worse than no pipeline because it creates false
    confidence." → ✓ "The pipeline will only be useful if we keep it current, particularly the
    next action, owner, expected value and status of each opportunity."
- Do not over-explain obvious concepts, do not add jargon for sophistication, go easy on bold.
- **Never invent a Taleemabad figure, result, donor example or impact claim.** A placeholder
  always beats a generic example. The master carries 15 on purpose; the budget exercise table is
  deliberately blank.
- Keep external research, our proposal, and what still needs validating clearly separate. Never
  present a funder's published criteria as our existing practice.

## Content notes

- Structure: 11-stage journey (Research → ... → Renew), 11 questions, 12 capabilities, a Donor
  Fit Score, two proposed development tracks, a financial-literacy module, a funder table, the
  2.5-hour workshop plan, a role-play question bank, a capability matrix and a 30-60 day plan.
- 🔑 **Vitol was fetched from vitol-foundation.com/our-approach**, not inferred: they accept
  **no unsolicited applications** and invite organisations through a programme manager. That
  makes Vitol a cultivation problem, not a proposal problem, and it is used deliberately as a
  teaching trap in the qualification exercise. Mulago, GiveWell and DIV criteria came from
  Ayesha's own research paste.

## The deck

python-pptx **1.0.2** (installed), 16:9, brand navy `#2F4FA2` + blue `#3C78D8`, logo
`assets/logo_taleemabad.png`, Calibri. Rebuild with the script and re-upload; never hand-edit
the Slides deck or the two drift.

- The outline's **facilitator notes and discussion questions become the speaker notes** on each
  slide. Slides carry 3 to 5 short lines at most.
- Slides 1 and 8 are navy statement slides. Slide 8 is one line: "No pitching for the first
  five minutes."
- 🔴 **Slide 9 lesson:** the first version listed the twelve capability names only, and Ayesha
  caught it. **A list of capability names is not the capabilities section** — each box needs the
  name **plus** the one-line *what we would expect to see in practice*, and the slide carries her
  own heading, "The capabilities we want to build". Still **no split of responsibilities**
  between the team members, so nothing looks decided.
- Grid boxes with two tiers of text must be **top-anchored** (`MSO_ANCHOR.TOP` + top margin).
  Middle anchoring with a mix of one- and two-line descriptors leaves the headings at ragged
  heights across a row.
- Upload path: build the .pptx, then Drive `files().create` twice, once with
  `mimeType='application/vnd.google-apps.presentation'` (converts to Slides) and once without
  (keeps the .pptx downloadable). Drive scope suffices. ⚠️ **The Slides API is NOT enabled on
  this GCP project** (403) — do not try to read or edit presentations through it.

## 🔑 How to actually SEE a generated deck or PDF on this machine

`pdftoppm`/poppler is **not installed**, so the Read tool cannot render a PDF directly. The
working path:

1. Export the Drive file as PDF (`drive.files().export(..., mimeType="application/pdf")`).
2. Render pages to PNG with **PyMuPDF**: `fitz.open(pdf)[i].get_pixmap(dpi=110).save(png)`.
3. Read the PNGs.

This is a **genuine visual check** and it lifts the Rule 14 limitation for anything Drive can
export (Docs, Sheets, Slides, and any .docx/.pptx uploaded for conversion). Used here to confirm
all 10 slides before reporting.

## Rendering markdown to a Doc

Upload the `.md` with `mimetype='text/markdown'` + `mimeType='application/vnd.google-apps.document'`
using `.claude/config/token_sheets_broad.json` (Ayesha's **own** OAuth token, so she owns the
file — the claude.ai connectors are authed as jawwad.ali@). Drive converts real headings and
real tables. Verify with an export back to `text/plain`, plus table and heading counts via the
Docs API.
