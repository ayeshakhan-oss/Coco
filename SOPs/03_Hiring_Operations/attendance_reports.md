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

**Display format:** Name + leave type

Example:
```
Mahrah Ashraf         | Sick Leave
Momina Tariq          | Half-day (Exams)
```

---

### Section 3: WFH — CONFIRMED
**Definition:** Permanent work-from-home employees (authorized WFH status, not temporary).

**Data sources:** Markaz employee records (check WFH status field)

**Display format:** Name + status

**Current permanent WFH (as of 2026-04-09):** 8 employees
- Amina Tayyub
- Zuhaib Shaikh
- Ajlal Hasan
- Zeest Hassan Qureshi
- Ahwaz Akhtar
- Shayan Ahmad
- ABDUL AHAD
- Zulfiqar Ahmed Mughal

---

### Section 4: WFH — TEMPORARY (If Applicable)
**Definition:** Employees who reported WFH for this specific day (not permanent WFH status).

**Data sources:** Teams Presence channel announcements

**Display format:** Name + reason (if provided)

Example:
```
Zunaira Shahid       | Not feeling well
```

---

### Section 5: OUT OF OFFICE
**Definition:** Employees who are away (travel, conference, etc.) but not on formal leave.

**Data sources:** Teams Presence + Markaz

**Display format:** Name + reason + expected return

Example:
```
Haroon Yasin         | Fundraising trip, returning 2026-04-16
```

---

### Section 6: ARRIVING LATE / ARRIVING TODAY
**Definition:** Employees who confirmed arrival but at a time later than standard office hours, or arriving today after being absent.

**Data sources:** Teams Presence announcements

**Display format:** Name + arrival time

Example:
```
Muhammad Saim        | Arriving 2:30pm
Muhammad Umar Raza   | Arriving 3:00pm
```

---

### Section 7: FLAGGED — NO RECORD FOUND
**Definition:** Employees not accounted for in any of the above categories. Not on Ayesha's list, not in Teams, not in Markaz records.

**Data sources:** Cross-check against all 84 payroll total

**Action:** These people need follow-up to understand where they are and why they didn't inform anywhere.

**Display format:** Name + "No record found"

Example:
```
Unknown Employee     | No record found - follow up needed
```

---

## Stat Boxes (8 Required)

Create 8 colored stat boxes at the top of the report:

1. **Payroll Total** — 84 (static)
2. **Onsite** — count from Section 1
3. **On Leave** — count from Section 2
4. **WFH — Confirmed** — 8 (permanent)
5. **WFH — Temporary** — count from Section 4
6. **Out of Office** — count from Section 5
7. **Arriving Late** — count from Section 6
8. **Flagged — No Record** — count from Section 7

**Important:** Totals should roughly equal 84 when summed appropriately (some people may be in one category only).

---

## Non-Negotiable Rules

1. **Check ALL three sources** — Ayesha's list, Teams, Markaz. Never rely on one only.

2. **Use exact names from Ayesha** — If user provides names, use them exactly as spelled. No variations or corrections.

3. **Flag silent cases** — People with no record in any source must be flagged.

4. **Payroll total is static** — 84 OPL+OWT employees. Does not change day-to-day.

5. **Recipients exact** — Ayesha Khan, Jawwad Ali, Aymen Abid. No changes unless user specifies.

6. **7 sections required** — All sections must be present, even if empty.

7. **8 stat boxes required** — All boxes present with accurate counts.

---

## Pre-Send Checklist

- [ ] Payroll baseline confirmed (84 active OPL+OWT employees)
- [ ] Markaz queried for leave records (date-specific)
- [ ] Teams Presence channel read (all announcements reviewed)
- [ ] Ayesha's on-site list provided and read carefully (exact names used)
- [ ] All 84 employees cross-checked across sources
- [ ] 7 sections created (all required, even if empty)
- [ ] 8 stat boxes created with accurate counts
- [ ] Silent cases identified and flagged in Section 7
- [ ] No duplicate names
- [ ] No typos or name variations (use exact spelling)
- [ ] Format matches prior attendance reports
- [ ] Recipients: Ayesha, Jawwad, Aymen (verified)
- [ ] Ready to send

---

## Common Mistakes

1. **Checking only one source** — Relying on Teams only or Markaz only. Always check all three.

2. **Accepting name variations** — Using variations of names provided. Use exact spelling from Ayesha's list.

3. **Missing silent cases** — Not flagging people who have no record. Must identify these.

4. **Incomplete sections** — Missing one of the 7 required sections. All must be present.

5. **Wrong stat box totals** — Math errors in box creation. Verify all counts.

6. **Payroll total wrong** — Using different number than 84. Static count for OPL+OWT.

7. **Format mismatch** — Not matching prior attendance report format. Keep consistent.

8. **Wrong recipients** — Sending to wrong people or missing someone. Verify recipients.

---

## Commitment (Coco, 2026-04-10)

I will check all three sources (Ayesha's list, Teams, Markaz). I will use exact names as provided. I will flag silent cases with no record. I will create all 7 required sections. I will create all 8 stat boxes with accurate counts. I will keep payroll total at 84. I will match the format of prior reports. I will send to Ayesha, Jawwad, and Aymen. I will verify names, counts, and format before sending.
