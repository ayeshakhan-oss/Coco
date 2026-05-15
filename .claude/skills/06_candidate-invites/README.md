# 06 Candidate Invites — Quick Reference

**Design:** 🔒 LOCKED (no deviations allowed)  
**Template:** [memory/locked_email_template_interview_invites_FINAL_2026_05_13.md](../../memory/locked_email_template_interview_invites_FINAL_2026_05_13.md)  
**Status:** ✅ PRODUCTION READY

---

## Quick Start (5 minutes)

### 1. Choose Your Invite Type

| Type | Use When | Script |
|------|----------|--------|
| **Values Interview Invite** | Candidate passes screening → moves to values round | `send_values_interview_pilot.py` |
| **Case Study Debrief Invite** | Candidate submits case study → moves to debrief | `send_case_study_debrief_pilot.py` |
| **Exploratory Call Invite** | Interesting candidate, no open role match | `send_exploratory_call_pilot.py` |
| **Warm Bench Opportunity Invite** | Past candidate cleared values+GWC, new role opens | `send_warm_bench_invite_pilot.py` |

### 2. Gather Candidate Info

Each invite type needs specific info. For **Values Interview**, you need:
- Candidate name
- Position title
- JD link
- Prep guide link
- Calendar booking link

(See SKILL.md for other types' requirements)

### 3. Customize the Script

```bash
cd scripts/
vim send_values_interview_pilot.py
```

Update configuration section:
```python
CANDIDATE_NAME = "Sarah Mitchell"
POSITION = "CPD Coach"
JD_LINK = "https://docs.google.com/..."
PREP_GUIDE_LINK = "https://docs.google.com/..."
BOOKING_LINK = "https://calendar.google.com/..."
```

**Important:** PILOT_MODE must be True (sends to Ayesha only, never candidate directly)

### 4. Run Pilot

```bash
python send_values_interview_pilot.py
```

Output:
```
Pilot sent to ayesha.khan@taleemabad.com
Subject: Invitation for the Values Interview for CPD Coach - Sarah Mitchell
Candidate: Sarah Mitchell
Position: CPD Coach
Type: VALUES INTERVIEW
```

### 5. Get Ayesha's Approval

Ayesha reviews the email in her inbox. She'll check:
- Design matches locked spec
- Content is clear and specific
- Links work correctly

Once approved, she tells you to go live.

### 6. Send Live

Change script settings:
```python
PILOT_MODE = False
TO = ["sarah.mitchell@example.com"]
CC = ["ayesha.khan@taleemabad.com", "hiring@taleemabad.com"]
```

Run script again:
```bash
python send_values_interview_pilot.py
```

Done! Email is sent to candidate.

---

## Design Spec Quick Check

Before sending pilot, verify:
- [ ] Colors match locked palette (no deviations)
- [ ] Typography: Georgia serif only
- [ ] Logo: 34px, centered
- [ ] Layout: 775px white card in grey wrapper
- [ ] Signature: Left-aligned (NOT centered)
- [ ] Button: Purple (#5b3fc4), rounded
- [ ] No yellow highlighting
- [ ] All links clickable (#3d63c8, underlined)

See [locked template checklist](../../memory/locked_email_template_interview_invites_FINAL_2026_05_13.md#self-check-before-sending) (30 items) for complete verification.

---

## Content Tips

### Greeting
- Use first name only: "Hi Sarah," ✅
- Not: "Hi Sarah Mitchell," ❌

### Hook (First Paragraph)
- Reference where they are in the process
- Why you're reaching out
- Set positive expectation

### Purpose Statement
- Be specific: "45-minute values conversation"
- Not vague: "interview" ❌

### Links
- Descriptive text: "interview prep guide" ✅
- Not: "click here" ❌

### CTA Button
- One button per email
- Use action word: "Book your Interview"
- Include emoji for visual appeal

### Closing
- Reference next steps
- Keep professional: "Warm regards," ✅
- Not: "Best wishes," ❌

---

## Reference Scripts

All scripts follow the same structure:
1. Configuration section (top)
2. HTML email template (middle)
3. send_pilot() function (bottom)

To create a new invite type:
1. Copy an existing script
2. Update configuration variables
3. Modify HTML content only
4. Change SUBJECT line
5. Update context in safe_sendmail() call
6. Test with pilot mode

---

## Troubleshooting

**Problem:** Logo doesn't show in email  
**Solution:** Check logo file exists: `c:/Agent Coco/assets/logo_taleemabad.png`

**Problem:** Email has styling issues (colors wrong, fonts weird)  
**Solution:** Read locked template again. Table-based HTML only. No div layout.

**Problem:** Links aren't clickable in email  
**Solution:** Check `<a>` tags have href attribute and style includes `color: #3d63c8; text-decoration: underline;`

**Problem:** Signature is centered instead of left-aligned  
**Solution:** Set `text-align: left;` on signature <td>. Not center.

---

## File Structure

```
skills/06_candidate-invites/
├── SKILL.md (main specification — read this first)
├── README.md (this file — quick reference)

scripts/
├── send_values_interview_pilot.py (reference implementation)
├── send_case_study_debrief_pilot.py
├── send_exploratory_call_pilot.py
├── send_warm_bench_invite_pilot.py

memory/
├── locked_email_template_interview_invites_FINAL_2026_05_13.md (design spec)
```

---

## Key Rules (Never Violate)

1. **Design is locked** — Colors, fonts, spacing cannot change
2. **Pilot first** — Always send to Ayesha before candidate
3. **PILOT_MODE must be True** initially — Prevents accidental live sends
4. **Content only** — Change text, never structure/HTML
5. **Test all links** — Before pilot, verify URLs work
6. **Use safe_sendmail()** — Never smtplib directly

---

**Created:** 2026-05-14  
**Status:** 🔒 PRODUCTION READY  
**Owner:** Coco
