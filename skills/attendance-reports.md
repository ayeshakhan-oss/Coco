---
name: Attendance Reports SOP
description: Daily attendance showing where OPL+OWT employees are. 7 sections, 8 stat boxes. PAYROLL_TOTAL=84 static. Check Markaz + Teams + sign-in + user feedback.
type: feedback
---

## Objective

Daily attendance report showing where Taleemabad's active OPL+OWT employees are on a given day (onsite, leave, WFH, out of office, etc.). Used for operational planning, capacity visibility, and hiring team coordination.

**Scope:** OPL+OWT employees only (84 active as of 2026-04-09, static payroll count)

**Frequency:** Daily (typically Mon–Thu for I-10 onsite office)

**Recipients:** Ayesha Khan + Jawwad Ali + Aymen Abid

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

## Step-by-Step Process

1. **Query Database** — Connect to Neon PostgreSQL. Pull all active OPL+OWT employees (should return 84). Note this count as PAYROLL_TOTAL (static).

2. **Read Teams Presence Channel** — Call scripts/utils/teams_reader.py. Extract all leave announcements, WFH updates, arrival times from Presence channel. Save as teams_presence_data.json (or similar).

3. **Query Markaz for Leave Records** — Query jobs.applications table or leave table. Filter by reporting_date. Extract: employee name, leave type, date range. Save as markaz_leave_data.json.

4. **Categorize Each Employee** — For each of the 84 employees:
   - Check Markaz leave records → if hit, goes to ON LEAVE
   - Check Teams Presence → if "WFH" announced, goes to WFH (UNLOGGED) OR ARRIVING LATER
   - Check permanent WFH list → if yes, goes to WFH — CONFIRMED (regardless of other data)
   - Check OOO records → if yes, goes to OUT OF OFFICE
   - User says they were onsite → goes to ONSITE
   - If no record found anywhere → goes to FLAGGED

5. **Cross-Check Against User Feedback** — Ask user: "Does this look right for today?"
   - Accept user corrections:
     - "X should be onsite" → move X to ONSITE
     - "Y is WFH but not confirmed WFH" → move Y to WFH (UNLOGGED)
     - "Z is not in the list but should be flagged" → add to FLAGGED with status note
   - Update categorization based on user input

6. **Build Stat Boxes** — Count each section. Calculate: ONSITE + ON LEAVE + WFH (UNLOGGED) + WFH CONFIRMED + OOO + ARRIVING LATER + FLAGGED. Must equal 84. If not, ask user to clarify discrepancies before proceeding.

7. **Generate PDF** — Use ReportLab (Python). Layout:
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

8. **Verify PDF Format** — Check stat boxes are colored and readable, all names spelled correctly (user-corrected spelling), counts add up to 84, no duplicate names across sections, all flagged people have status notes.

9. **Send Report** — Recipient list: ayesha.khan@taleemabad.com + jawwad.ali@taleemabad.com + aymen.abid@taleemabad.com
   - Email body: brief summary (e.g., "56 onsite, 8 on leave, 2 WFH unlogged, 9 permanent WFH, 2 OOO, 1 arriving, 6 flagged")
   - Attachment: PDF (filename: attendance_DDMMMYYYY.pdf, e.g., attendance_9apr2026.pdf)
   - Safe_sendmail() bouncer (never smtplib directly)
   - Audit log: context='attendance_report_DDMMMYYYY'

10. **Document Corrections** — Save any user corrections to session notes. If flagged section changes, document why.

---

## Non-Negotiable Rules

1. **PAYROLL_TOTAL = 84 (static)** — Number of active OPL+OWT employees. Does NOT change day-to-day.

2. **TOTAL in stat box = PAYROLL_TOTAL** — Not the sum of attendance categories. Categories show WHERE the 84 are; TOTAL always shows 84.

3. **Categorization is mutually exclusive** — Each employee appears in ONE section only. No duplicate names across sections.

4. **WFH — CONFIRMED is permanent** — These 8 employees always in this section. Not "missing" — legitimately WFH by design. Excluded from "unlogged WFH".

5. **FLAGGED section requires status notes** — Never just list a name. Always add reason: "RWP Team", "On severance", "Last month with org", "No record found".

6. **User corrections are final truth** — If user says "X was onsite", move X to ONSITE regardless of data. User feedback overrides all sources.

7. **Verify sum = 84 before sending** — Do the math: ONSITE + ON LEAVE + WFH (UNLOGGED) + WFH CONFIRMED + OOO + ARRIVING LATER + FLAGGED. Must equal 84. If not, ask user to clarify before sending.

8. **PDF format must match pattern exactly** — Colored stat boxes, 2-column onsite grid, name|status tables. User will reject if format drifts.

9. **Teams Presence + Markaz + sign-in = three-source rule** — Don't rely on one source. Cross-check all three.

10. **Send only Mon–Thu** — Attendance reports for I-10 office days. Don't send Fri/Sat/Sun unless explicitly asked.

11. **Audit log always** — safe_sendmail() bouncer with context logged. Every send is tracked in logs/email_audit.log.

12. **Ask for approval before sending** — Confirm with user first (or get standing approval once per week).

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

## Commitment (Coco, 2026-04-10)

I will check all three sources (Markaz, Teams, sign-in). I will categorize each employee in one section only. I will verify sum = 84 before sending. I will include status notes in flagged section. I will accept user corrections. I will match PDF format exactly. I will ask for approval before sending.
