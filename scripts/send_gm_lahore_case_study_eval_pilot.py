#!/usr/bin/env python3
"""
Case Study Evaluation Report — Growth Manager (Lahore), 4 submissions (2026-08-10).
Internal report email (locked report family: navy header + stat boxes + candidate blocks).
PILOT_MODE=True -> Ayesha only, [PILOT - ] prefix.
"""
import os
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

sys.path.insert(0, r"c:\Agent Coco")
from scripts.utils.safe_send import safe_sendmail

load_dotenv(r"c:\Agent Coco\.env")

SENDER = "ayesha.khan@taleemabad.com"
PASSWORD = os.getenv("EMAIL_PASSWORD")

PILOT_MODE = True
PILOT_TO = "ayesha.khan@taleemabad.com"
LIVE_TO = ["ayesha.khan@taleemabad.com"]
LIVE_CC = []

SUBJECT = "Case Study Evaluation Report - Growth Manager (Lahore) | 4 Submissions"
if PILOT_MODE:
    SUBJECT = "[PILOT - ] " + SUBJECT


def block(name, app_id, verdict, verdict_color, scores, strengths, gaps, flags, probes):
    flags_html = ""
    if flags:
        flags_html = f"""
        <p style="margin:10px 0 0 0;font-family:Georgia,serif;font-size:14px;line-height:1.7;color:#7b341e;">
          <strong>Flags:</strong> {flags}</p>"""
    return f"""
    <table width="100%" cellpadding="0" cellspacing="0" style="margin:0 0 26px 0;border:1px solid #d9dee7;border-radius:6px;">
      <tr><td style="padding:18px 22px;">
        <p style="margin:0 0 2px 0;font-family:Georgia,serif;font-size:17px;color:#1a2a3a;">
          <strong>{name}</strong> <span style="color:#8a94a3;font-size:13px;">App {app_id}</span>
          &nbsp;<span style="background:{verdict_color};color:#ffffff;font-size:11px;letter-spacing:1px;padding:3px 10px;border-radius:4px;font-family:Arial,sans-serif;">{verdict}</span></p>
        <p style="margin:8px 0 0 0;font-family:Georgia,serif;font-size:13px;color:#3157b7;"><strong>{scores}</strong></p>
        <p style="margin:10px 0 0 0;font-family:Georgia,serif;font-size:14px;line-height:1.7;color:#222;">
          <strong>Strongest:</strong> {strengths}</p>
        <p style="margin:10px 0 0 0;font-family:Georgia,serif;font-size:14px;line-height:1.7;color:#222;">
          <strong>Gaps:</strong> {gaps}</p>{flags_html}
        <p style="margin:10px 0 0 0;font-family:Georgia,serif;font-size:14px;line-height:1.7;color:#555;">
          <strong>Debrief probes:</strong> {probes}</p>
      </td></tr>
    </table>"""


HTML = f"""
<html><body style="margin:0;padding:0;background:#f5f5f5;">
<table width="100%" cellpadding="0" cellspacing="0" bgcolor="#f5f5f5"><tr><td align="center" style="padding:30px 0;">
<table width="720" cellpadding="0" cellspacing="0" bgcolor="#ffffff" style="max-width:720px;">

  <tr><td bgcolor="#1a2a3a" style="padding:28px 36px;">
    <p style="margin:0;font-family:Arial,sans-serif;font-size:11px;letter-spacing:2px;color:#9fb3cc;text-transform:uppercase;">People &amp; Culture &middot; Case Study Evaluation Report</p>
    <p style="margin:8px 0 0 0;font-family:Georgia,serif;font-size:24px;color:#ffffff;font-weight:bold;">Growth Manager &mdash; Lahore</p>
    <p style="margin:4px 0 0 0;font-family:Georgia,serif;font-size:13px;color:#9fb3cc;">"The Story, the Room, and the Deal" &middot; 4 submissions evaluated &middot; August 10, 2026</p>
  </td></tr>

  <tr><td style="padding:26px 36px 6px 36px;">
    <table width="100%" cellpadding="0" cellspacing="0"><tr>
      <td width="25%" align="center" style="background:#eaf1fb;padding:14px 4px;border-radius:6px;">
        <p style="margin:0;font-family:Georgia,serif;font-size:26px;color:#3157b7;font-weight:bold;">4</p>
        <p style="margin:2px 0 0 0;font-family:Arial,sans-serif;font-size:10px;letter-spacing:1px;color:#55606e;">SUBMITTED</p></td>
      <td width="8"></td>
      <td width="25%" align="center" style="background:#eaf7ee;padding:14px 4px;border-radius:6px;">
        <p style="margin:0;font-family:Georgia,serif;font-size:26px;color:#1b5e20;font-weight:bold;">4</p>
        <p style="margin:2px 0 0 0;font-family:Arial,sans-serif;font-size:10px;letter-spacing:1px;color:#55606e;">EVALUATED</p></td>
      <td width="8"></td>
      <td width="25%" align="center" style="background:#fdf3e7;padding:14px 4px;border-radius:6px;">
        <p style="margin:0;font-family:Georgia,serif;font-size:26px;color:#b26a00;font-weight:bold;">3</p>
        <p style="margin:2px 0 0 0;font-family:Arial,sans-serif;font-size:10px;letter-spacing:1px;color:#55606e;">FULLY COMPLETE</p></td>
      <td width="8"></td>
      <td width="25%" align="center" style="background:#fdecea;padding:14px 4px;border-radius:6px;">
        <p style="margin:0;font-family:Georgia,serif;font-size:26px;color:#b3261e;font-weight:bold;">1</p>
        <p style="margin:2px 0 0 0;font-family:Arial,sans-serif;font-size:10px;letter-spacing:1px;color:#55606e;">MISSING PART</p></td>
    </tr></table>
  </td></tr>

  <tr><td style="padding:20px 36px 4px 36px;">
    <p style="margin:0 0 6px 0;font-family:Georgia,serif;font-size:15px;color:#3157b7;font-weight:bold;">Key observation</p>
    <p style="margin:0 0 18px 0;font-family:Georgia,serif;font-size:14px;line-height:1.75;color:#222;text-align:justify;">
      A genuinely competitive batch: all four answered all four assignments, all four disclosed AI use per the ground rules,
      and every pipeline names real, current institutions. The differentiators are depth against the Assignment&nbsp;4 evaluator
      guide (ownership, costing realism, negotiation buffer), policymaker calibration in Assignment&nbsp;1, and how much of the
      thinking will survive a live, unscripted debrief. Scores are out of 10, per assignment (A1&ndash;A4), each judged against
      the brief &mdash; not against each other.</p>
  </td></tr>

  <tr><td style="padding:0 36px;">
    {block("Muhammad Waqas", 3651, "STRONG — 1 GAP", "#2e7d32",
      "A1: 6.5 &nbsp;|&nbsp; A2: 9 &nbsp;|&nbsp; A3: 8 &nbsp;|&nbsp; A4: 8.5",
      "The convening (A2) is excellent — success defined as the finding being cited by someone who isn't Taleemabad; 13 attendee types with current real names (Secretary Muddassir Riaz Malik, Minister Rana Sikandar Hayat); agenda engineered against speech-fatigue; segmented 24-hour follow-ups plus a 'What We Heard in the Room' recap. A4 is strategically sharp: extension treated as <em>time</em>, institute-first sequencing, the Ministry desk officer identified as the real file-mover, renewal homework from month one, escalating costing (8%/5%).",
      "The one-pager is his weakest piece: essayistic, slow to the point, and it references evidence without citing a single number. No negotiation-buffer logic in A4 (partly moot on his no-cost path).",
      "The reflective ('a room you led') is MISSING — the only incomplete submission in the batch. Ask him to send it before his debrief. Heaviest (candidly disclosed) AI collaboration of the four — test live ownership of the A2/A4 thinking at the debrief.",
      "Produce the missing reflective; defend the PITB deal path against a procurement objection unprepped; where would his convening fail in a real Punjab room?")}

    {block("Abdul Wahab", 3614, "STRONG", "#2e7d32",
      "A1: 9 &nbsp;|&nbsp; A2: 8 &nbsp;|&nbsp; A3: 8.5 &nbsp;|&nbsp; A4: 8",
      "The best-calibrated one-pager against the brief's skeptical Secretary: clean problem/approach/evidence/ask skeleton, one sourced hard statistic (77%, World Bank 2022), a 90-day joint review 'including no', and a modest 45-minute ask covering 'what didn't work at first'. A3 mitigations are street-smart: an internal champion who can explain the model without Taleemabad in the room; document everything because staff rotate; start no-cost to skip competitive bidding. A4 ownership language is the sharpest of the four ('their workload close to zero') with the staff-officer/PA access craft the role actually requires.",
      "'I lead with the lowest defensible number' runs opposite to the pitch-high-then-survive-three-cuts reality of government budget negotiation — he partially recovers with an explicit cut-protection order (salaries protected first).",
      "Reflective is a 2-minute voice note (mp4 in his Drive folder) — needs a human listen before the debrief; I evaluate text only.",
      "His lowest-number stance vs three tables of cuts; what happens when the no-cost pilot ends and money enters the room.")}

    {block("Ahmad Wajahat", 3635, "SOLID", "#b26a00",
      "A1: 7.5 &nbsp;|&nbsp; A2: 7 &nbsp;|&nbsp; A3: 7.5 &nbsp;|&nbsp; A4: 6.5",
      "The only candidate who pulled Taleemabad's actual published impact numbers with footnotes (1.5 years / 0.8 LAYS; +21pp Urdu, +16pp Maths, +4pp English; ICT and Balochistan rollouts) — verify before anyone repeats them. Real bureaucratic literacy: 10% increments justified via Adhoc Relief allowance, 'minutes drafted and issued' as success indicators, a 'Government Reflection' agenda slot that converts the launch into co-owned evidence, and the only full 3-year costing with actual totals (PKR 120.8M) plus per-table justifications for MoF, MoE and the Planning Commission.",
      "A4 strategy is the concern: he reproduces the prompt at length and his restated approval chain re-routes the extension through the Planning Commission while his day-one roadmap skips the host institute — the primary stakeholder. Ownership drifts abstract ('regular coordination') exactly where the role demands doing other offices' legwork. Pipeline owners are diffuse (CEO + HoP + GM). Officialese prose with recurring typos; follow-up engine is one bundle to everyone.",
      "Honest timekeeping disclosure: 7&ndash;8 hours against the 2&ndash;2.5-hour box — credit the honesty, note the calibration. Reflective is a real senior-room story (UNICEF/OPM, Sindh Directorate) but answers only half the question — no 'what would I do differently'.",
      "Re-walk the extension chain — who moves first and why; who drafts the PC-1; the missing half of his reflective.")}

    {block("Salman Tariq", 3656, "STRONG PLUS", "#1b5e20",
      "A1: 8.5 &nbsp;|&nbsp; A2: 9 &nbsp;|&nbsp; A3: 9 &nbsp;|&nbsp; A4: 9.5",
      "A4 is the benchmark answer against the internal evaluator guide — the only submission to hit all five criteria: drafts everything for the institute to issue, pre-briefs the Ministry before the file arrives, distinguishes the released-uncommitted-legally-usable balance from the book balance, cites the actual PSDP 2026-27 and the Manual for Development Projects, and lays out an explicit negotiation ladder — open 285M / defend 263M / red-line 245M — with the buffer itemised and a stated refusal to accept an undeliverable budget in the room. A2 features an independent red-team slot and a claims-and-limitations media pack; A3 uniquely maps the approval architecture (PECTAA, P&amp;D/PDWP) as part of the market — 'an unfunded MoU is not a closed deal.' His research even identified NIETE as the public-sector analogue.",
      "Uniformly consultancy-grade polish — the least personal voice on Assignment 1; density occasionally outruns readability.",
      "AI-assisted drafting disclosed on every document; and his research figures (0.28 SD effect, 522 AI observations, 6% student talk time, 261-school Punjab study) are hedged as 'Taleemabad reports' — VERIFY each against what Taleemabad has actually published before crediting them. The reflective is reassuringly real and senior (led a PITB session with the Chairmen of P&amp;D and PITB on Accelerate Punjab).",
      "Source every number on his evidence slide, live; rebuild the 285/263/245 ladder for a different programme on the spot.")}
  </td></tr>

  <tr><td style="padding:6px 36px 26px 36px;">
    <p style="margin:0 0 6px 0;font-family:Georgia,serif;font-size:15px;color:#3157b7;font-weight:bold;">Actions needed</p>
    <p style="margin:0;font-family:Georgia,serif;font-size:14px;line-height:1.8;color:#222;">
      1. Request Muhammad Waqas's missing reflective (200 words or voice note) before his debrief.<br>
      2. Someone listens to Abdul Wahab's voice-note reflective before his debrief.<br>
      3. Verify the published impact figures quoted by Ahmad Wajahat and Salman Tariq before they are repeated externally.<br>
      4. On approval, Coco fills case_study_score + case_study_notes on Markaz for all four.</p>
  </td></tr>

  <tr><td style="border-top:1px solid #e0e0e0;padding:16px 36px 22px 36px;">
    <p style="margin:0;font-family:Georgia,serif;font-size:12px;color:#8a94a3;">Taleemabad Talent Acquisition &nbsp;|&nbsp; hiring@taleemabad.com &nbsp;|&nbsp; August 10, 2026</p>
  </td></tr>

</table>
</td></tr></table>
</body></html>
"""


def main():
    msg = MIMEMultipart("alternative")
    msg["Subject"] = SUBJECT
    msg["From"] = SENDER
    recipients = [PILOT_TO] if PILOT_MODE else LIVE_TO + LIVE_CC
    msg["To"] = PILOT_TO if PILOT_MODE else ", ".join(LIVE_TO)
    if not PILOT_MODE and LIVE_CC:
        msg["Cc"] = ", ".join(LIVE_CC)
    msg.attach(MIMEText(HTML, "html"))
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(SENDER, PASSWORD)
    mode = "PILOT" if PILOT_MODE else "LIVE"
    safe_sendmail(server, SENDER, recipients, msg.as_string(),
                  context=f"{mode} GM-Lahore case study evaluation report")
    server.quit()
    print(f"{mode} sent: {SUBJECT} -> {recipients}")


if __name__ == "__main__":
    main()
