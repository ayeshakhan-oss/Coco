---
name: Ayesha Noreen — OPL Project-Based Audio Monitoring contract (LIVE 2026-08-24)
description: First OPL fixed-fee project contract off the NIETE master. Records the "Per month" master trap, the hardcoded project line, the acceptance-label bolding, the Design 3 optional-prose slots, and the send-hook render gap.
type: project
---

# Ayesha Noreen — Audio Monitoring Officer (Assessments) — LIVE 2026-08-24

**Package:** Contract (OPL Project-Based) + Permanent Employee NDA, both PDF.
**Sent:** 2026-08-24 from ayesha.khan@ · To `ayeshanoreen0773@gmail.com` · Cc hiring@,
ayesha.khan@, abubakr@, sabeena.abbasi@, muzzammil.patel@, accounts.query@.
**Build:** `scripts/contracts/build_opl_audio_monitoring_ayesha_noreen.py`
**Email:** `scripts/contracts/send_audio_monitoring_joining_design3.py`

## Confirmed terms (Ayesha Khan, 2026-08-24)

Entity **OPL** · Ms. Ayesha Noreen · CNIC [CNIC redacted - in the gitignored build script] · Audio Monitoring Officer ·
**24 Aug 2026 (Mon) → 3 Sep 2026 (Thu), 11 days inclusive** · **PKR 36,667**
(90/9/1 split: 33,000 / 3,300 / 367) · direct report **Abubakr** · signed by the HOD
**Sabeena Abbasi** (Impact & Policy), not the COO · lunch + business-travel clauses
stripped · JD supplied verbatim.

**Compensation derivation (deliberately absent from both documents, per Ayesha):**
cohort rate PKR 50,000 / 15 days pro-rated to 11 days = 36,666.67, rounded to the rupee.

## 🔴 Master traps found on this build

1. **"Per month" is hardcoded next to the compensation fill spot.** The cell reads
   `Total Earnings PKR XYZ Per month inclusive of Tax` and "Per month" is NOT a yellow
   field, so a normal fill leaves it in place. On a **fixed-fee project contract that is
   factually wrong** and Ayesha caught it in pilot. Replaced with
   `for the complete assignment inclusive of Tax` (her own welcome-email phrasing).
   The builder asserts the string exists so a changed master fails loudly.
   **Check this on every fixed-fee contract built off this master.**
2. **The project line is hardcoded to "National Institute of Excellence in Teacher
   Education"** (Skill 07 quirk #7). Overwritten to `Assessments` rather than left
   silently.
3. **Acceptance-block labels are not bold in the master.** Ayesha asked for
   `Signature:`, `Contract Acceptance Date:` and `Direct Report to:` bolded.
   `Direct Report to: <name>` is a **single run**, so it must be split and only the
   label half bolded. Set bold on the RUN, never the style, or Drive's PDF conversion
   flattens it.

## 🔴 Send-hook gap (fixed)

`scripts/hooks/pre_contract_send_hook.py` could render a script's real email HTML only
via `render(key)` + `COACHES` or `build_html` + `COACHES`. A **single-candidate** send
script with a zero-arg `render()` fell through to static source scanning, which cannot
connect a value held in a dict to bold styling applied in a separate function. Result:
**FALSE "compensation is not bold" / "joining date is not bold" HARD BLOCKS on a correct
email.** Added a `_takes_arg()` check plus a zero-arg `render()` branch.

## Design 3 — new optional prose slots

Rule 15 says Design 3 is variable-driven, but several prose blocks were hardcoded.
Added four optional variables so other programmes can vary wording **without touching
the locked layout**, following the existing `RETURNING_SENTENCE` pattern:
`WELCOME_EXTRA` · `ATTACHMENT_NOTE` · `CLOSING_EXTRA` · `CLOSING_WELCOME`.
`send_niete_email_design3.py` now passes its original wording explicitly, so **NIETE
joining emails render identically** (verified).

**Template-wide change (affects NIETE too):** "HR team" → "People & Culture team" and
"HR portal account" → "People & Culture portal account", per Ayesha. ⚠️ Flagged to her
that the portal may be a system name.

**De-duplication:** the closing's "Welcome to the team! We're excited to have you
onboard." sat directly beneath Ayesha's requested "We are really excited to have you on
board." That half was dropped **for this send only**.

## Deliberately NOT carried over from the CPD-coach batch

The hyperlinked "Leaves" clause and the authenticity clause in Termination were
**batch-specific instructions for Hina and Noor (2026-08-13), never made standing**.
Omitted here and flagged to Ayesha. The email also drops the probation and
commute-support items: an 11-day remote assignment carrying a three-month probation note
would read as an error. The contract's own probation clause is untouched.

## Still unconfirmed at send time

Signatory title was rendered as **"Head of Department, Impact and Policy"** — Ayesha said
"write the name of HOD" but never gave the exact title string. Flagged in every pilot;
she went live without correcting it.

## Process notes

- `contract_docx_eval.py --type project` passed clean. **The `--type` flag is mandatory**
  (it defaults to `fellow` and throws 11 false blocks).
- **Never resolve a bare identifier**: her email arrived as `ayeshanoreen0773gmail.com`
  with the `@` missing. Confirmed with Ayesha rather than reconstructed.
- 🔴 **Rule 1 still holds: no Word or LibreOffice on this machine, so no page was ever
  actually seen.** Every round here was a visual defect Ayesha caught by eye
  ("Per month", the bold labels) after structural checks reported clean.
