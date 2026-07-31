---
name: Assessment Center Activity — Invite Type #7 (Skill 06)
description: Onsite full-day assessment center invite. Locked wording from Ayesha (2026-07-31). NO booking button/link — candidates reply to confirm; Google Calendar invitation (with venue) follows to confirmed candidates. Venue address + Maps link in email body.
type: project
status: 🔒 LOCKED — content wording + rules approved by Ayesha 2026-07-31
---

# Assessment Center Activity — Skill 06 Invite Type #7 (2026-07-31)

**What it is:** Invite to an onsite, full-day assessment center activity (e.g. 10:30 AM – 5:00 PM). Lives under **Skill 06 (candidate invites)** — locked interview-invite design (FINAL 2026-05-13), NOT candidate-communication (no "This is not a yes for now." opener, no 800-word rule).

**First use:** CPD Coach (JOB-0017), 2026-07-31 — 12 pilots to Ayesha, 11 sent live same day (Hajra Sajjad excluded at Ayesha's instruction). Activity date Thursday, August 6, 2026.

## Locked content (Ayesha's wording, 2026-07-31)

1. Header label `TALENT ACQUISITION • ASSESSMENT CENTER ACTIVITY`; title "Invitation to Our Assessment Center Activity"; subtitle = position.
2. Hook: "Congratulations on making it to the next stage of our recruitment process! We're excited to invite you to our Assessment Center Activity."
3. Logistics: onsite on **[ACTIVITY_DATE]**, starting promptly at **[START]** until **[END]**; arrive on time.
4. Venue line: "**Venue:** [ADDRESS] — [view on Google Maps](LINK)." Address + Maps link explicitly provided by Ayesha per batch; **NO Google plus codes** (e.g. "M27R+H5X") in the address.
5. Outside-Islamabad line: reply to this email so we can coordinate.
6. Confirmation ask: "To confirm your attendance, kindly reply to this email with your acknowledgement. We will send the Google Calendar invitation by **[CONFIRM_BY_DATE]** to the candidates who have confirmed."
7. Closing: look forward to meeting you + questions welcome.
8. Signature: standard block + **Ayesha Raza Khan** (hyperlinked to https://www.linkedin.com/in/ayesha-raza-khan-386668177/) with **03354288844** on the next line.
9. Subject: "Invitation to the Assessment Center Activity for [POSITION] - [CANDIDATE_NAME]".

## Hard rules

1. **NO booking button, NO booking link.** Reply-to-confirm flow only (Ayesha replaced an earlier "Reserve Your Slot" button draft — do not regress). Body flows straight to the signature.
2. **Onsite, not virtual** — no Meet link, no recording-consent line.
3. **Venue only as Ayesha provides it** — never source an address yourself; strip plus codes.
4. **Dates change per position/batch** — confirm activity date/time AND calendar-invite date with Ayesha every send.
5. Candidates verified against Markaz before sending; pilots to Ayesha only ([PILOT – ] prefix, no CC); live = individual email per candidate with the CC list Ayesha specifies for that batch.

**Scripts:** `scripts/send_assessment_center_pilot.py` (reference implementation, dummy candidate) · `scripts/send_assessment_center_cpd_coach_batch.py` (gitignored — candidate PII; CPD Coach batch with live CC list).

**Spec:** `.claude/skills/06_candidate-invites/SKILL.md` § type 7.
