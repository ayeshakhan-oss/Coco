---
name: Attendance Reports SOP (Updated 2026-04-10)
description: Track office presence for I-10 Head Office. OPL+OWT employees. 6-step workflow + 7 sections + 8 stat boxes. PAYROLL_TOTAL=84. Check payroll, Markaz, Teams, on-site list. Flag silent cases.
type: feedback
---

## Objective

Track office presence and reporting discipline, especially for the I-10 Head Office. Report where Taleemabad's active OPL+OWT employees are on a given day (onsite, leave, WFH, out of office, etc.). Used for operational planning, capacity visibility, and accountability.

**Purpose:** NOT micromanagement. Identify people who are absent or remote without informing anywhere (flag silent cases for follow-up).

**Context:**
- Three offices: I-10 (Head Office — focus), H-9, Rawalpindi
- Fridays are organization-wide work from home
- Main visibility focus: I-10 Head Office
- Scope: OPL + OWT employees only (84 active as of 2026-04-09, static payroll count)

**Frequency:** Daily (typically Mon–Thu for I-10 onsite office)

**Recipients:** Ayesha Khan + Jawwad Ali + Aymen Abid

---

## 6-Step Data Collection Workflow (Updated 2026-04-10)

### Step 1: Get Active Employee List from Payroll

Use the relevant month's payroll to identify active employees.

**Key rule:** Use the PREVIOUS month's payroll until current month is processed.
- Example: While working in April, use March payroll
- Example: When working in May, use April payroll

**Action:** Query Neon DB for active OPL+OWT employees in the relevant payroll month.

---

### Step 2: Pull Names and Active Counts from Markaz

Use Markaz to get:
- Names of all active employees
- Active employee count (should match payroll baseline)

**Action:** Query Markaz database for active employees as of the reporting date.

---

### Step 3: Check Teams Presence Channel

In Teams, check the relevant channel where people report:
- Work from home status
- Leave announcements
- Status updates
- Arrival/departure notifications

**What to look for:**
- "WFH today"
- "Out sick"
- "Annual leave"
- "Arriving at [time]"
- Any other presence-related updates

**Action:** Read Teams Presence channel using scripts/utils/teams_reader.py.

---

### Step 4: Cross-Check Markaz for Leave/WFH Records

If someone mentioned leave/WFH in Markaz (formal records), that counts.

**Rule:** Teams is acceptable if Markaz was not updated, but check both sources.

**Action:** Query Markaz leave records for the reporting date. Compare against Teams announcements.

---

### Step 5: Compare Against On-Site List Provided by Ayesha

Ayesha may provide a separate list/sheet of who was physically on-site in I-10.

**Rule:** Follow the same reporting pattern already used (careful name reading, accurate copying).

**Quality note (2026-04-10):** Coco previously did not read the provided list carefully enough. Names from folder/chat must be read and copied accurately.

**Action:** Accept Ayesha's on-site list as the ground truth for who was physically present. Use exact names and spelling provided.

---

### Step 6: Flag Silent Cases

Flag people who:
- Were NOT on the on-site list provided by Ayesha
- Did NOT mention leave/WFH in Teams
- Did NOT mention leave/WFH in Markaz

**These are the people who need to be highlighted.**

**Action:** Cross-check all 84 employees against all three sources (Ayesha's list, Teams, Markaz). Anyone not found in any source gets flagged in the FLAGGED section with status "No record found".

**Note:** This is NOT for micromanagement. It is to identify people who are absent or remote without informing anywhere.

---

## Data Sources (Non-Negotiable)

1. **PAYROLL_TOTAL (Static):** Query Neon DB for all active OPL+OWT employees. This number does NOT change day-to-day. As of 2026-04-09: **84 total active employees**

2. **Teams Presence Channel:** Read via Microsoft Graph API (scripts/utils/teams_reader.py). Presence channel shows:
   - Leave announcements ("Out sick", "Annual leave", "WFH today")
   - Arrival updates ("Arriving at 2pm")
   - Any presence-related status

3. **Markaz Database (Leave/Time Off):** Query for leave records with specific dates. Shows:
   - Annual leave
   - Sick leave
   - Maternity/paternity
   - Unpaid leave
   - Actual dates of absence

4. **Sign-in Records (If available):** Optional — building sign-in system (if integrated). Confirms physical onsite presence.

5. **Manual corrections from user:** Final source of truth. If user says "X was onsite", that overrides data sources. Always accept user corrections and update report.

---

## Attendance Categories (7 Sections)

### Section 1: ONSITE
**Definition:** Employees physically present at I-10 office on the reporting date.

**Data sources:** Teams Presence + sign-in records + user feedback

**Display format:** 2-column grid showing names and status

Example:
```
Abdul Rehman         | Present
Ahmed Javed          | Present
Ali Sipra            | Present
```

**Count:** Verify count matches. If user says "X was onsite", add them.

---

### Section 2: ON LEAVE
**Definition:** Employees with formal leave records (annual, sick, maternity, etc.) on the reporting date.

**Data sources:** Markaz leave records (query by date)

**Display format:** Table with name | leave type | date range

Example:
```
Ayesha Malik         | Annual Leave      | 2026-04-09 to 2026-04-11
Bilal Khan           | Sick Leave        | 2026-04-09
```

**Count:** Query DB, verify, display.

---

### Section 3: WFH (UNLOGGED)
**Definition:** Employees confirmed working from home but with NO formal leave record or Teams announcement. They're working, just not onsite.

**Data sources:** Teams Presence (if mentioned "WFH today") + user feedback

**Display format:** Simple list with names

Example:
```
Fatima Ahmed
Gul Perwasha Cheema
```

**Count:** Usually small (2–3 people).

---

### Section 4: WFH — CONFIRMED
**Definition:** Employees who are permanently work-from-home or have standing WFH arrangements. NOT temporary/daily WFH.

**Data sources:** Markaz configuration (or user-provided permanent WFH list)

**Current permanent WFH list (as of 2026-04-09):** 8 employees
- Amina Tayyub
- Zuhaib Shaikh
- Ajlal Hasan
- Zeest Hassan Qureshi
- Ahwaz Akhtar
- Shayan Ahmad
- ABDUL AHAD
- Zulfiqar Ahmed Mughal

**Display format:** Simple list (no status needed, they're always WFH by design)

**Count:** Should be constant month-to-month (currently 8).

**Key rule:** These are EXCLUDED from onsite count. They're not "missing" — they're legitimately working from home as their normal arrangement.

---

### Section 5: OUT OF OFFICE
**Definition:** Employees not working today — on vacation, off-site assignment, sabbatical, or unavailable.

**Data sources:** Markaz OOO records + Teams announcements + user feedback

**Display format:** Table with name | reason (if known) | date range

Example:
```
Haroon Yasin         | Personal Leave    | 2026-04-09
Jahan Zaib           | Off-site Visit    | 2026-04-08 to 2026-04-12
```

**Count:** Query and verify.

---

### Section 6: ARRIVING LATER
**Definition:** Employees who are coming onsite but not present at report time. They confirmed arrival time via Teams or user feedback.

**Data sources:** Teams Presence ("Arriving at 2pm") + user feedback

**Display format:** Table with name | confirmed arrival time

Example:
```
Muhammad Hassan      | 2:00 PM
Rosheen Naeem        | 10:30 AM
```

**Count:** Usually 0–2 people.

---

### Section 7: FLAGGED (People with Zero Record)
**Definition:** Employees in the payroll (OPL+OWT) with NO record anywhere:
- NOT on Markaz leave
- NOT in Teams Presence channel
- NOT in sign-in records
- NOT mentioned by user as onsite, WFH, or OOO

**Data sources:** Query all 84 OPL+OWT employees from DB. Cross-check against all other attendance categories. Whoever doesn't appear = FLAGGED.

**Display format:** Table with name | status note (if known)

Example:
```
Person A             | RWP Team (separate payroll)
Person B             | On severance (pending exit)
Person C             | Last month with org
Person D             | No record found
```

**Count:** Should be small (8–12 people). If large, something is wrong with data collection.

**Key rule:** FLAGGED section is NOT attendance data — it's an audit trail showing gaps. Flag these to user and investigate.

---

## Stat Boxes (Header Section)

**Format:** Colored boxes at top of report showing key counts.

**8 Stat Boxes (in order):**

1. **ONSITE** — number of people physically present today
2. **ON LEAVE** — number of people on formal leave
3. **WFH (UNLOGGED)** — number of people working from home without leave record
4. **WFH — CONFIRMED** — number of permanent WFH employees
5. **OUT OF OFFICE** — number of people unavailable
6. **ARRIVING LATER** — number of people coming onsite later
7. **FLAGGED** — number of people with zero record
8. **TOTAL** — must equal PAYROLL_TOTAL (84)

**Non-negotiable rule:** TOTAL = 84 (static payroll count), NOT the sum of categories. The 7 sections show WHERE the 84 are; together they should account for all 84.

**Verification formula:**
```
ONSITE + ON LEAVE + WFH (UNLOGGED) + WFH CONFIRMED + OOO + ARRIVING LATER + FLAGGED = TOTAL (should be 84)
```

If sum ≠ 84, you have a data gap. Do not send report. Investigate and ask user for corrections.

---

## Report Generation Workflow (Steps 7–10)

These steps follow the 6-step data collection workflow above.

### Step 7: Categorize Each Employee

For each of the 84 employees, place in appropriate section:
- Check Markaz leave records → if hit, goes to ON LEAVE
- Check Teams Presence → if "WFH" announced, goes to WFH (UNLOGGED) OR ARRIVING LATER
- Check permanent WFH list → if yes, goes to WFH — CONFIRMED (regardless of other data)
- Check Ayesha's on-site list → if yes, goes to ONSITE
- Check OOO records → if yes, goes to OUT OF OFFICE
- If no record found anywhere → goes to FLAGGED (with status "No record found")

---

### Step 8: Verify Completeness Against All Sources

**Cross-check:**
- All names on Ayesha's on-site list are in ONSITE section
- All names with Teams WFH announcement are in WFH (UNLOGGED)
- All names with Markaz leave record are in ON LEAVE
- All names with Markaz OOO are in OUT OF OFFICE
- All 84 payroll employees are accounted for somewhere

---

### Step 9: Build Stat Boxes

Count each section. Calculate:
```
ONSITE + ON LEAVE + WFH (UNLOGGED) + WFH CONFIRMED + OOO + ARRIVING LATER + FLAGGED = TOTAL (should be 84)
```

If sum ≠ 84, investigate discrepancies with user before proceeding. Do not send if math doesn't add up.

---

### Step 10: Generate PDF

Use ReportLab (Python). Layout:
- Header with report date + "I-10 Attendance Report"
- 8 colored stat boxes
- 2-column ONSITE grid (names in first column, status in second)
- ON LEAVE table
- WFH UNLOGGED list
- WFH CONFIRMED list
- OUT OF OFFICE table
- ARRIVING LATER table
- FLAGGED table with status notes
- Footer: "Compiled by Coco, Nugget & Noah" + date + time

---

### Step 11: Verify PDF Format

Check:
- Stat boxes are colored and readable
- All names spelled correctly (use Ayesha's provided spelling)
- Counts add up to 84
- No duplicate names across sections
- All flagged people have status notes

---

### Step 12: Send Report

**Recipients:** ayesha.khan@taleemabad.com + jawwad.ali@taleemabad.com + aymen.abid@taleemabad.com

**Email body:** brief summary (e.g., "56 onsite, 8 on leave, 2 WFH unlogged, 9 permanent WFH, 2 OOO, 1 arriving, 6 flagged")

**Attachment:** PDF (filename: attendance_DDMMMYYYY.pdf, e.g., attendance_9apr2026.pdf)

**Safe send:** Use safe_sendmail() bouncer (never smtplib directly)

**Audit log:** context='attendance_report_DDMMMYYYY'

---

### Step 13: Document Corrections

Save any user corrections to session notes. If flagged section changes, document why.

---

## Non-Negotiable Rules (Updated 2026-04-10)

1. **PAYROLL_TOTAL = 84 (static)** — Number of active OPL+OWT employees. Does NOT change day-to-day. Use payroll from previous month until current month is processed.

2. **Use previous month's payroll** — While in April, use March payroll. While in May, use April payroll. Wait for current month processing.

3. **TOTAL in stat box = PAYROLL_TOTAL** — Not the sum of attendance categories. Categories show WHERE the 84 are; TOTAL always shows 84.

4. **Categorization is mutually exclusive** — Each employee appears in ONE section only. No duplicate names across sections.

5. **Check all 3 sources (6-step workflow):** 
   - Step 1: Get active employee list from payroll
   - Step 2: Pull names from Markaz
   - Step 3: Check Teams Presence channel
   - Step 4: Cross-check Markaz leave/WFH records
   - Step 5: Compare against Ayesha's on-site list
   - Step 6: Flag silent cases (no record anywhere)

6. **Names must be accurate and complete** — Read provided list/names carefully. Copy exactly as Ayesha provides them. Quality correction (2026-04-10): Coco previously did not read lists carefully enough.

7. **WFH — CONFIRMED is permanent** — These 8 employees always in this section. Legitimately WFH by design. Excluded from "unlogged WFH".

8. **FLAGGED section requires status notes** — Never just list a name. Always add reason: "RWP Team", "On severance", "Last month with org", "No record found".

9. **Purpose is not micromanagement** — Flag silent cases to identify people absent/remote without informing anywhere. For accountability, not punishment.

10. **User corrections are final truth** — If Ayesha says "X was onsite", move X to ONSITE regardless of data. User feedback overrides all sources.

11. **Verify sum = 84 before sending** — Do the math: ONSITE + ON LEAVE + WFH (UNLOGGED) + WFH CONFIRMED + OOO + ARRIVING LATER + FLAGGED. Must equal 84. If not, investigate and ask user to clarify before sending.

12. **PDF format must match pattern exactly** — Colored stat boxes, 2-column onsite grid, name|status tables. User will reject if format drifts.

13. **Send only Mon–Thu** — Attendance reports for I-10 office days. Don't send Fri/Sat/Sun unless explicitly asked. (Fridays are org-wide WFH.)

14. **Audit log always** — safe_sendmail() bouncer with context logged. Every send is tracked in logs/email_audit.log.

15. **Ask for approval before sending** — Confirm with user first (or get standing approval once per week).

---

## Common Mistakes

1. **TOTAL ≠ 84** — Calculated TOTAL as sum of categories (e.g., 56+7+2+9+1+1+6=82). Wrong. TOTAL is always 84 (payroll static). If sections don't add to 84, you have unaccounted people.

2. **Duplicate names** — Same person in ONSITE and WFH (UNLOGGED). Categorization must be mutually exclusive.

3. **Wrong permanent WFH list** — Added temporary WFH people (1 day only) to WFH — CONFIRMED section. Only 8 standing WFH people belong here.

4. **Flagged section has no status notes** — Just a list of names. Unacceptable. Add reason for each.

5. **Ignoring Teams data** — User announced "I'm WFH today" on Teams. You put them in ONSITE anyway. Trust Teams Presence.

6. **PDF format drifts** — Stat boxes no longer colored, onsite grid becomes list format, tables missing. User will reject.

7. **Forgot to cross-check** — One source says "on leave", another doesn't mention them. Didn't investigate.

8. **Sending without approval** — Assumed daily report is auto-approved. Never.

9. **Sending Fri/Sat/Sun** — Attendance reports for Mon–Thu (I-10 office days).

10. **Missing audit log** — Sent email via smtplib directly without safe_sendmail() bouncer.

---

## Pre-Send Checklist

- [ ] Queried DB for all 84 OPL+OWT employees (static payroll total verified)
- [ ] Read Teams Presence channel (announcements extracted)
- [ ] Queried Markaz for leave records (by date)
- [ ] Categorized all 84 employees (one per section only)
- [ ] Cross-checked against user feedback (accepted all corrections)
- [ ] Stat boxes filled and math verified (sum = 84)
- [ ] 8 stat boxes created with correct counts
- [ ] Header with report date + "I-10 Attendance Report"
- [ ] 2-column ONSITE grid (names + status)
- [ ] ON LEAVE table (name | type | date range)
- [ ] WFH UNLOGGED list
- [ ] WFH CONFIRMED list (8 permanent employees)
- [ ] OUT OF OFFICE table
- [ ] ARRIVING LATER table
- [ ] FLAGGED table with status notes for each person
- [ ] Footer: "Compiled by Coco, Nugget & Noah" + date + time
- [ ] PDF format matches pattern exactly (colors, layout, tables)
- [ ] Recipients correct: Ayesha + Jawwad + Aymen
- [ ] Safe_sendmail() bouncer used, context logged
- [ ] Ready to ask Ayesha for approval before sending

---

## Reference

**Exact PDF format:** scripts/reports/attendance_9apr2026_exact.py — ReportLab PDF with 8 stat boxes, 2-column onsite grid, name|status tables, FLAGGED section
**Permanent WFH list:** memory/project_attendance_permanent_wfh.md — 8 employees, confirmed, excluded from daily counts
**Payroll Total logic:** memory/project_attendance_payroll_total.md — TOTAL always 84, breakdown shows WHERE they are
**Teams reader:** scripts/utils/teams_reader.py — reads Presence channel, attendance source

---

## Commitment (Coco, 2026-04-10, Updated)

I will:
1. **Follow 6-step data collection:** Payroll → Markaz → Teams → Markaz cross-check → Ayesha's on-site list → Flag silent cases
2. **Use previous month's payroll** until current month is processed
3. **Read Ayesha's provided list carefully** and copy names with exact spelling (quality correction)
4. **Check all 3 sources** (payroll, Markaz, Teams) — never rely on one alone
5. **Categorize each employee in one section only** — no duplicates
6. **Flag silent cases** — people not on Ayesha's list, not in Teams, not in Markaz
7. **Verify sum = 84 before sending** (ONSITE + LEAVE + WFH(unlogged) + WFH(confirmed) + OOO + ARRIVING + FLAGGED)
8. **Include status notes in flagged section** (RWP Team, On severance, Last month, No record, etc.)
9. **Accept user corrections** as final truth
10. **Match PDF format exactly** (colored stat boxes, 2-column grid, tables)
11. **Ask for approval before sending**
12. **Use safe_sendmail() bouncer** with audit log
13. **Send Mon–Thu only** (I-10 office days)
