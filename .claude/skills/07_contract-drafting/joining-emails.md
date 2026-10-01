# Sub-skill: Joining Emails

Sub-skill of [Skill 07 — Contract Drafting](SKILL.md). **Fellow templates LOCKED 2026-08-13** (given verbatim by Ayesha). Full-time / part-time / addendum / team-move templates still ⏳ pending.

---

## 🔒 THE PACKAGE RULE — paid vs volunteer

| Engagement | Documents attached |
|---|---|
| **Paid fellowship** | Contract **+** NDA |
| **Volunteer / unpaid fellowship** | **NDA ONLY — never a contract** |
| **Unpaid → paid transition** | **Contract only** (NDA was already signed at the unpaid stage) |

⚠️ This **overrides** the general "contract + NDA always ship together" rule for volunteer
Fellows. Sending a contract to a volunteer Fellow is a hard error.

**Always confirm paid vs volunteer before building anything.** Never infer it from a role title.

---

## 🔒 The two links — EVERY joining email carries BOTH (Ayesha 2026-10-01)

1. **Submit your signed documents** — the form where the joiner uploads the signed contract,
   signed NDA and their documents.
2. **Join the WhatsApp group** — the all-employee group.

No joining email goes out without both, whatever the engagement (permanent, project-based,
paid fellow, volunteer fellow, unpaid→paid transition). Plain-text templates hyperlink them on
**Click here** / **Click Here**; Design 3 renders them as the two buttons. Never a bare URL.

**🔒 The form follows the ENTITY, not the programme:**

| Entity | Form |
|---|---|
| **NIETE** and **NIETE fellowships** | `https://docs.google.com/forms/d/e/1FAIpQLSdVAYfCZZhusF_tNLn7mxzoK5BFXDa7xfj2FZifRlva-YDBHQ/viewform` |
| **OPL, OWT** and **OPL/OWT fellowships** (incl. permanent hires) | `https://docs.google.com/forms/d/e/1FAIpQLSf70SM4jlx4muDMLlN1ZMqHqVEQjJQgCBga-oRM-M1OZXCePw/viewform?usp=sharing&ouid=108638480093303713396&urp=gmail_link` |
| **Inc.** | ⏳ none given. Ask Ayesha; never borrow another entity's form |

| WhatsApp group (all entities, all employees) | `https://chat.whatsapp.com/HglkfuENmLqEbaq8N5jSVq` |
|---|---|

⚠️ This replaces the old "Fellow form vs NIETE form" split, and the 2026-09-12 note that a
permanent hire has no form: permanent OPL/OWT hires use the OPL/OWT form.
🛡️ Enforced: `contract_docx_eval.evaluate_joining_email` HARD BLOCKS a missing form, a missing
WhatsApp link, or the wrong entity's form (it used to check only emails that said "click here",
so Design 3 button emails were never checked). Web app: `joining_email.links_for(entity)` +
`check_body(..., entity=)`. Both Design 3 templates carry `{{ONBOARDING_FORM_URL}}` +
`{{WHATSAPP_GROUP_URL}}`, so a missing link fails at render time.

---

## Template 1 — Paid Fellowship (new joiner)

**Subject:** `Welcome to Taleemabad - [Designation] Fellow`

> Dear [First Name],
>
> I hope you read this in good health and high spirits.
>
> We are pleased to announce that you have been selected for the position of [Designation] (Fellowship) at Taleemabad, powered by Orenda, starting [Day], [Date] [Month] [Year]. Your monthly compensation for this [X]-month, fellowship-based role is PKR [amount], inclusive of taxes.
>
> Please find the Contract and Non-Disclosure Agreement (NDA) attached to this email.
>
> Additionally, please take note of the essential logistical requirements outlined below:
>
> Complete the form linked here with your information for record-keeping purposes and upload your educational documents, signed contracts, a signed NDA, and an experience letter: **Click here**
>
> Provide your bank name, account title, and IBAN number, matching the details on your cheque book. Upon the submission of all required documents, we will proceed to set up your teams and email ID.
>
> Join the Orenda | Taleemabad WhatsApp Group via the following link: **Click Here**
>
> Once you are officially registered in the company records, you will receive an HR portal account activation email.
>
> Welcome to the team once again!
>
> Should you have any queries or concerns, please feel free to reach out to the HR team.

**Attachments:** Contract + NDA.

---

## Template 2 — Volunteer / Unpaid Fellowship (new joiner)

**Subject:** same as Template 1 — `Welcome to Taleemabad - [Designation] Fellow`

> Dear [Full Name],
>
> I hope you read this in good health and high spirits.
>
> We are pleased to announce that you have been selected for the position of [Designation] (Fellowship) at Taleemabad, powered by Orenda, starting [Day], [Date] [Month] [Year]. This is a [X]-month, volunteer fellowship.
>
> Please find the Non-Disclosure Agreement (NDA) attached to this email.
>
> Additionally, please take note of the essential logistical requirements outlined below:
>
> Complete the form linked here with your information for record-keeping purposes and upload your educational documents, and a signed NDA: **Click here**
>
> Join the Orenda | Taleemabad WhatsApp Group via the following link: **Click Here**
>
> Welcome to the team once again!
>
> Should you have any queries or concerns, please feel free to reach out to the HR team.

**Attachments:** NDA **only**.
**Note the differences from Template 1:** no compensation sentence · no contract · no bank-details
paragraph · no HR-portal paragraph · form upload list omits signed contracts and experience letter.

---

## Template 3 — Unpaid → Paid Transition

**Subject:** none — **this is a reply in the existing thread** of the earlier joining email.
Use In-Reply-To + References headers so it threads correctly.

> Dear [Full Name],
>
> I hope you read this in good health and high spirits.
>
> We are pleased to confirm your transition to a paid fellowship as an [Designation] (Fellowship) at Taleemabad, powered by Orenda, effective [Day], [Date] [Month] [Year].
>
> This is a [X]-month fellowship, and you will receive a monthly compensation of PKR [amount] for the duration of the fellowship.
>
> Please find the Contract attached to this email.
>
> Additionally, please take note of the essential logistical requirements outlined below:
>
> Complete the form linked here with your information for record-keeping purposes and upload your educational documents, signed contracts, a signed NDA, and an experience letter: **Click here**
>
> Provide your bank name, account title, and IBAN number, matching the details on your cheque book. Upon the submission of all required documents, we will proceed to set up your teams and email ID.
>
> Join the Orenda | Taleemabad WhatsApp Group via the following link: **Click Here**
>
> Welcome to the team once again!
>
> Should you have any queries or concerns, please feel free to reach out to the HR team.

**Attachments:** Contract **only** — the NDA was signed at the unpaid stage.

---

## Template 4 — NIETE Coach (paid, full-time project-based)

**Subject:** `Congratulations [First Name] on Your Selection as a Coach for the NIETE Project!`

> Hi [First Name],
>
> I hope this message finds you in good health and high spirits.
>
> We are pleased to announce that you have been selected for the position of **CPD - Coach** for the NIETE project at **Taleemabad**, powered by **Orenda**. Your monthly compensation for this full-time, project-based role is **PKR [amount]**, inclusive of taxes. This role requires five days and 40 hours per week.
>
> *[Returning-member sentence — include ONLY if the person is a returning team member:* "We truly value the experience and insight you bring as a returning team member and are confident that you will continue to make meaningful contributions to our mission."*]*
>
> Please find the **Contract and Non-Disclosure Agreement (NDA)** attached to this email.
>
> Additionally, please take note of the essential logistical requirements outlined below:
>
> Complete the form linked here with your information for record-keeping purposes and upload your educational documents, signed contracts, a signed NDA, and an experience letter: **Click here** *(NIETE form)*
>
> Provide your bank name, account title, and IBAN number, matching the details on your cheque book. Upon the submission of all required documents, we will proceed to set up your teams and email ID.
>
> **A Few Important Things to Know:**  ← **must be bold**
>
> Please note that all documents, certificates, experience letters, and other credentials provided during the hiring process are expected to be authentic and verifiable. If any information or documentation is found to be false, misleading, or fabricated, Taleemabad reserves the right to take appropriate action, which may include termination of the contract.
>
> Also note that this role is subject to a three-month probationary period, during which your performance and overall suitability for the role will be assessed.
>
> Commute Support: Commute from home to schools and from schools to the office will be covered either through a Hub car or a commute allowance. Taleemabad reserves the right to determine which option will be provided. Please note that commute from the office to home will not be covered by Taleemabad.
>
> Join the Orenda | NIETE WhatsApp group via this link: **Click here**
>
> Once everything is in place, we will activate your HR portal account and proceed with team and email setup.
>
> Welcome to the team! We're excited to have you onboard.
>
> If you have any questions or concerns, please don't hesitate to reach out to the HR team.

**Attachments:** Contract **+** Permanent Employee NDA.
**Uses the NIETE form** (NIETE entity), not the OPL/OWT one. WhatsApp link is the shared one.
**"A Few Important Things to Know:" must be bold**, and the three items beneath it are a
**bulleted list** (`<ul><li>`), not plain paragraphs (Ayesha 2026-08-13).
⚠️ The returning-member sentence is **conditional** — always ask whether the person is returning.

---

## Rules for all templates

1. **Wording is locked.** Only names, designation, dates, duration and amount change. Do not
   re-word, "improve", or restyle these emails.
2. **"Click here" is always a hyperlink** on the two URLs above — never a bare URL in the body.
3. **🔒 Dates: NEVER name the weekday** (Ayesha 2026-08-13). Write `1st of August 2026`, not
   `Saturday, 1st of August 2026`. This supersedes the day names in the original template text.
4. **🔒 Bold everything that matters.** Always bold the **joining/effective date**, the
   **compensation figure**, and the **duration** — plus the designation, Taleemabad and Orenda,
   and the document name (Contract / NDA). If a detail is one the candidate will scan for or act
   on, it is bold. Harness blocks an unbolded date or compensation figure.
4. Role is always written **"[Designation] (Fellowship)"** and the employer as
   **"Taleemabad, powered by Orenda"**.
5. **Pilot to Ayesha first**, no CC. Nothing goes to the Fellow without her explicit approval.
   **🔒 The pilot must be byte-identical to what the candidate will receive** — same body, same
   formatting, same threading. **NEVER put a pilot banner, a "nothing has gone to X" note, flags
   or open questions inside the email.** Those go in chat. Harness blocks meta-commentary.
7. **🔒 Match the thread you are replying into.** When an email continues an existing thread,
   pull the original from Ayesha's Sent folder over IMAP and mirror its exact formatting —
   plain Gmail `<div dir="ltr">`, black text, `<br><br>` between paragraphs, bold on
   role / Taleemabad / Orenda / document name, "Click here" hyperlinked, and **her signature
   block copied verbatim**. Do not invent a house style for a reply.
8. **Thread the pilot too** — In-Reply-To + References on both pilot and live, so Ayesha reviews
   it in the real thread.
10. **🔒 Attachments are PDF, never Word.** Convert with `scripts/utils/docx_to_pdf_drive.py`
    (Drive is the only renderer on this machine; the temp Google Doc is deleted, the attachment
    is a real `.pdf`). Drive re-flows the layout — verify the text survived and have Ayesha
    eyeball the PDF. Harness blocks `.docx` attachments.
11. **🔒 Gmail "…" trimmed-content dots.** A threaded reply that repeats wording already in the
    thread gets its duplicate tail collapsed by Gmail. Wording is locked, so break the match with
    a zero-width space (`&#8203;`) inside the repeated closing lines.
9. **Check the original's CC list** before going live; a joining email thread usually carries
   Hiring, HR and the hiring manager. Confirm recipients with Ayesha — never add them silently.
6. Match attachments to the package rule at the top of this file — and verify what is actually
   attached before sending.

---

## Still pending from Ayesha ⏳

Part-Time joining · Addendum / promotion · Internal team-move.

(Permanent Full-Time exists since 2026-09-12: `templates/permanent_joining_design3.html`, rendered by `scripts/contracts/send_gm_opl_joining.py`. Start date, no end date, 3-month probation. See memory/opl_permanent_contract_and_joining_email_2026_09_12.md.)
