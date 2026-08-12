# Contract Drafting (Skill 07)

Prepare employment contracts, NDAs, addendums, and joining-email packages from Ayesha's approved templates. Identify the correct document type, select the correct entity template, populate it accurately, validate every field, and prepare the complete outgoing package.

**Created:** 2026-08-12, from Ayesha's 23-section specification (locked same day).
**Prime directive:** The approved template is the source of truth. NEVER create, rewrite, or "improve" legal wording, clauses, or formats. Accuracy over speed. When anything material is unclear — STOP AND ASK.

---

## Architecture — Sub-Skills

**This SKILL.md is the orchestration layer** (like Skill 02). Each entity and document family has its own sub-skill — the file to read side-by-side once entity + situation are known:

| Sub-skill | Covers | Mirrors folder |
|---|---|---|
| [opl-contracts.md](opl-contracts.md) | OPL (Orenda Private Limited) contracts | `Contracts\OPL\` |
| [owt-contracts.md](owt-contracts.md) | OWT (Orenda Welfare Trust) contracts — ⚠️ no-highlight fill-spot exception | `Contracts\OWT\` |
| [inc-contracts.md](inc-contracts.md) | Taleemabad Inc. contracts | `Contracts\INC\` |
| [niete-contracts.md](niete-contracts.md) | NIETE project-based contracts | `Contracts\NIETE\` |
| [fellow-contracts.md](fellow-contracts.md) | Fellows/interns — contract + Fellow NDA | `Contracts\Fellow\` |
| [addendum-promotion.md](addendum-promotion.md) | Same-team promotion → Addendum | `Contracts\Addendum\` |
| [team-move-new-contract.md](team-move-new-contract.md) | Internal team move → new contract | `Contracts\Promotion\` |
| [ndas.md](ndas.md) | Permanent Employee NDA vs Fellow NDA | NDA masters |
| [joining-emails.md](joining-emails.md) | The 5 email situations — ⏳ templates pending | — |

Routing: **confirm entity + situation first (Steps 1–3 below), then open the matching sub-skill(s)** — entity file + ndas.md + joining-emails.md for a new hire; addendum-promotion.md or team-move-new-contract.md for internal changes.

---

## When to Use This Skill

Trigger on any contract-related request:
- "Prepare a contract" / "make the contract for this candidate"
- "We need to send this person a contract" / "send their employment documents"
- "Prepare the offer documents"
- "[Name] is joining as a Fellow"
- "We promoted [Name]" / "[Name] is moving to another team"
- "Prepare an addendum"
- Any NDA request

---

## Template Library

**Location:** `c:\Agent Coco\Contracts\` (local folder, Ayesha-approved masters).
**Full map with per-template fill fields:** [TEMPLATE_MAP.md](TEMPLATE_MAP.md) — read it side-by-side with this file before every drafting task.

**Fill-field rule:** Fill ONLY the yellow-highlighted spaces in each template. Exception (Ayesha-approved 2026-08-12): the two OWT templates carry no yellow highlighting — there, the official fill fields are the `XYZ` placeholders and the blank-after-colon header spots (Date:, CNIC:, Name:). After populating a copy, REMOVE the yellow highlighting from filled fields — a finished contract must contain zero highlights and zero placeholders.

---

## The Mental Workflow (locked order)

**Entity → Situation → Contract Type → Correct Template → Employee Details → NDA Type → Dates → Validation → Correct Email Template → Attachments**

### Step 1 — Entity (NEVER assume)
Four entities: **OPL** (Orenda Private Limited) · **OWT** (Orenda Welfare Trust) · **Inc.** (Taleemabad Inc.) · **NIETE**.
If not already specified, the FIRST question is: *"Which entity should this be issued from: OPL, OWT, Inc., or NIETE?"*

### Step 2 — Situation (new hire vs existing employee)
- **New hire** → Step 3.
- **Existing employee, role changing** → determine which case. If unclear, ask: *"Is this a promotion/change within the same team, or is the employee moving to a different team?"*
  - **Same team + promotion/change → ADDENDUM** (we treat the Addendum as the promotion document — Ayesha 2026-08-12). Never auto-generate a full new contract.
  - **Different team / internal move → NEW CONTRACT** (masters for all entities are staged in `Contracts\Promotion\` for exactly this case). Never use an Addendum unless Ayesha explicitly instructs.

### Step 3 — Contract Type (NEVER assume)
If not already specified, ask: *"What type of contract is required: Permanent Full-Time, Part-Time, Project-Based, or Fellow/Internship?"*
- **Fellow rule:** interns are called **Fellows**. Fellow/internship = the Fellow Project-Based contract + the **Fellow NDA** (NEVER the Permanent Employee NDA).
- **OWT note (Ayesha 2026-08-12):** OWT has only a Full-Time template as its standard offering. The OWT Part-Time/Project-Based file exists in `Promotion\` — use it only when Ayesha directs.
- If no approved template exists for the requested entity/type combination, SAY SO. Never convert a Full-Time template into Part-Time (or any other cross-conversion) unless Ayesha explicitly instructs.

### Step 4 — Employee Details (collect ONLY what's missing — Smart Questioning)
Never re-ask anything Ayesha already provided. Required for every contract:
- Full legal name (+ salutation **Mr./Ms. — always ask, never infer from the name**)
- CNIC number (Inc.: CNIC/Passport/Company registration)
- Designation / position (+ team/department where the template has that field)
- Joining date / contract start date
- Entity · Employment type
- Salary/compensation figures required by the template
- **Project-Based / Fellow additionally:** contract END date (and duration), and "Direct Report to" where the template has it
- **Addendum additionally:** previous contract date, HOD name + designation, and whether **compensation is changed or unchanged** — Ayesha states this each time; fill Addendum A and its "compensation remains unchanged" line accordingly, exactly as she instructs

Do not invent or estimate ANY missing field. Ask.

### Step 5 — JD (mandatory for every position)
**Always ask Ayesha for the JD for the position.** The JD goes **under Annexure-A inside the same contract document** (not as a separate attachment). In the Addendum, the JD goes in the "Job Description" section of Addendum A.

### Step 6 — NDA
- Permanent employees → **Permanent Employee NDA** (`Promotion\Template - NDA Full Time Permanent Employee.docx`). The single Orenda NDA covers OPL, OWT, NIETE — and Inc. hires (Ayesha 2026-08-12).
- Fellows → **Fellow NDA** (`Fellow\Template - NDA Fellow Employee.docx`). Never swap the two.
- NDA fills: full legal name + joining date + current date (exactly the yellow fields). NEVER insert CNIC, designation, or anything else into an NDA that the template doesn't ask for; preserve every existing field.
- Addendum-only cases: no new NDA unless Ayesha says otherwise.

### Step 7 — Package (Contract + NDA together)
A joining package is not ready unless BOTH the completed contract AND the completed NDA are prepared. Never one without the other (Addendum situations excepted).

### Step 8 — Validation (mandatory gates, run BEFORE showing Ayesha)

**Contract checklist:**
- [ ] Correct full name (spelling verified against what Ayesha provided) · correct salutation
- [ ] Correct CNIC · designation · entity · contract type
- [ ] Correct joining/start date · end date where applicable (**double-check start AND end on Project-Based/Fellow**)
- [ ] Correct template used (verify against TEMPLATE_MAP.md)
- [ ] JD present under Annexure-A
- [ ] No leftover details from a previous employee (scan the whole document)
- [ ] No unresolved placeholders (XYZ, DATE MONTH YEAR, EMPLOYEE NAME, blank-after-colon) and no remaining yellow highlighting
- [ ] No accidental changes to standard legal clauses — only the fill fields differ from the master (verify by diff against the master's text)
- [ ] Formatting identical to the approved template

**NDA checklist:**
- [ ] Correct full legal name · correct NDA type (Permanent vs Fellow) · correct dates
- [ ] No details belonging to another person · no unresolved placeholders
- [ ] Standard NDA wording untouched

### Step 9 — Email
Approved email templates are **PENDING — Ayesha will share them as a set** (Full-Time joining, Part-Time joining, Fellow/Project-Based joining, Addendum/promotion, internal team-move). Until they arrive: flag "email template missing" on every package and draft nothing freelance. Once shared, populate the matching approved template only — never invent a new email style.

### Step 10 — Review & Send
Show Ayesha the completed package (contract + NDA + email draft) for review. **Nothing goes to the employee/candidate without her explicit approval** (house pilot/approval gate). All sends via `safe_sendmail()`.

---

## File Handling (Section 21 — locked)

1. NEVER overwrite a master template. Work on a **copy**.
2. Output populated documents to `output/contracts/<Full Name>/` — e.g. `Contract - Ali Khan - OPL Full-Time.docx`, `NDA - Ali Khan - Fellow.docx`. Clear, identifiable filenames.
3. Replace only the intended fill fields. Preserve clauses, formatting, signatures, headers, footers, entity details, structure.
4. Populated contracts and NDAs contain CNIC and salary — **PII: they stay out of git** (`output/` is untracked; keep it that way).
5. Prefer python-docx run-level replacement on the yellow-highlighted runs so the rest of the document is physically untouched; clear the highlight on filled runs.

---

## Never Guess (hard list)

Entity · employment type · CNIC · name spelling · salutation · designation · start date · end date · whether someone is a Fellow or permanent · same-team promotion vs team move · which template · compensation changed vs unchanged · any legal language. If unclear, missing, or contradictory → stop and ask Ayesha.

---

## Known Template Quirks (flagged & ruled 2026-08-12)

1. **Addendum "compensation remains unchanged" line** — Ayesha states changed/unchanged per case; edit that line and Addendum A per her instruction only.
2. **Addendum "required to work from the office"** — hardcoded; if the employee is remote/hybrid, flag to Ayesha before finalizing.
3. **Addendum is branded plain "Orenda"** — one master serves all entities for now.
4. **NIETE Project-Based contract is on OPL letterhead** — intentional; it also serves as OPL's project-based template. No changes required.
5. **OWT templates unhighlighted** — treat `XYZ`/blank-after-colon as fill fields (approved).
6. **Inc. contract** — effective date format "Date Month, Year"; acceptance line takes CNIC/Passport/Company registration; salary is a PKR figure "disbursed in dollars at time of conversion"; signed Haroon Yasin, CEO. Fill only the yellow fields; the "technical services and operation management" WHEREAS wording stays untouched.
7. **Duplicate Inc. masters in Promotion\** (two near-identical files, filenames differ by a space) — use `Template - Contract Taleemabad Inc.  .docx` (64,664 bytes, matches the INC\ master); ignore the 64,663-byte near-duplicate until Ayesha cleans it up.

---

## Example Workflows (from Ayesha's spec)

**New full-time hire** ("prepare the contract for Sara"): confirm entity → confirm type → collect missing details + JD → populate entity FT contract → populate Permanent NDA → validate both → joining email (once templates shared) → package with BOTH docs → show Ayesha.

**Fellow** ("Ahmed is joining as a Fellow"): confirm entity → Fellow Project-Based contract → collect name/CNIC/role/START+END dates + JD → **Fellow NDA** → Fellow joining email → package → show Ayesha.

**Promotion** ("We promoted Sana to Senior Manager"): do NOT draft a contract yet → confirm same-team → Addendum (previous contract date, dates, designation, JD, compensation per Ayesha's changed/unchanged instruction) → promotion email → show Ayesha.

**Team move** ("Bilal is moving from Team A to Team B"): NEW contract from the entity's master (staged in Promotion\) → internal-move email → show Ayesha.

---

## Self-QA Before Showing Ayesha

- [ ] Entity + contract type were confirmed (or already given), not assumed
- [ ] All required fields collected; nothing invented
- [ ] Correct templates per TEMPLATE_MAP.md; JD in Annexure-A
- [ ] Both validation checklists pass
- [ ] Contract + NDA both present in the package
- [ ] Correct email template used (or "email template missing" flagged)
- [ ] Files named clearly, saved under output/contracts/, masters untouched
- [ ] Package presented to Ayesha for approval — no send without it
