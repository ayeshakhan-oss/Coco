#!/usr/bin/env python3
"""
Growth Roles Pipeline Report — SMG (Job 42) + GM Karachi (Job 41) + GM Lahore (Job 39).
2026-08-12. Locked report family: navy header + 4 stat boxes + key observation + tables.
Data verified against Markaz (statuses, values fields, communication_history, case_study fields),
logs/email_audit.log, and read-only IMAP sweep of ayesha.khan@ (bookings/replies, 2026-08-12).
PILOT_MODE=True -> Ayesha only, [PILOT - ] prefix, no CC.
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

SUBJECT = "Growth Roles Pipeline Report - SMG | GM Karachi | GM Lahore | August 12, 2026"
if PILOT_MODE:
    SUBJECT = "[PILOT - ] " + SUBJECT

# ── palette ───────────────────────────────────────────────────────────────────
GREEN = "#1b5e20"
RED = "#b3261e"
AMBER = "#b26a00"
BLUE = "#3157b7"
GREY = "#8a94a3"

def ok(t):    return f'<span style="color:{GREEN};font-weight:bold;">{t}</span>'
def bad(t):   return f'<span style="color:{RED};font-weight:bold;">{t}</span>'
def warn(t):  return f'<span style="color:{AMBER};font-weight:bold;">{t}</span>'
def dim(t):   return f'<span style="color:{GREY};">{t}</span>'

def job_table(rows):
    """rows: list of (name_app, invite, call, case_study, debrief)."""
    tr = []
    for i, (name, invite, call, cs, db) in enumerate(rows):
        bg = "#ffffff" if i % 2 == 0 else "#f4f6fa"
        tr.append(f"""
      <tr bgcolor="{bg}">
        <td style="padding:9px 10px;font-family:Georgia,serif;font-size:13px;color:#1a2a3a;line-height:1.5;">{name}</td>
        <td style="padding:9px 10px;font-family:Georgia,serif;font-size:13px;line-height:1.5;">{invite}</td>
        <td style="padding:9px 10px;font-family:Georgia,serif;font-size:13px;line-height:1.5;">{call}</td>
        <td style="padding:9px 10px;font-family:Georgia,serif;font-size:13px;line-height:1.5;">{cs}</td>
        <td style="padding:9px 10px;font-family:Georgia,serif;font-size:13px;line-height:1.5;">{db}</td>
      </tr>""")
    return f"""
    <table width="100%" cellpadding="0" cellspacing="0" style="border:1px solid #d9dee7;border-radius:6px;margin:0 0 8px 0;">
      <tr bgcolor="#eaf1fb">
        <td style="padding:9px 10px;font-family:Arial,sans-serif;font-size:10px;letter-spacing:1px;color:#3157b7;"><strong>CANDIDATE</strong></td>
        <td style="padding:9px 10px;font-family:Arial,sans-serif;font-size:10px;letter-spacing:1px;color:#3157b7;"><strong>VALUES INVITE</strong></td>
        <td style="padding:9px 10px;font-family:Arial,sans-serif;font-size:10px;letter-spacing:1px;color:#3157b7;"><strong>VALUES CALL</strong></td>
        <td style="padding:9px 10px;font-family:Arial,sans-serif;font-size:10px;letter-spacing:1px;color:#3157b7;"><strong>CASE STUDY</strong></td>
        <td style="padding:9px 10px;font-family:Arial,sans-serif;font-size:10px;letter-spacing:1px;color:#3157b7;"><strong>DEBRIEF</strong></td>
      </tr>{''.join(tr)}
    </table>"""

def section(title, subtitle, table_html, note_html=""):
    return f"""
  <tr><td style="padding:22px 36px 4px 36px;">
    <p style="margin:0 0 2px 0;font-family:Georgia,serif;font-size:17px;color:#1a2a3a;font-weight:bold;">{title}</p>
    <p style="margin:0 0 12px 0;font-family:Georgia,serif;font-size:12px;color:#8a94a3;">{subtitle}</p>
    {table_html}{note_html}
  </td></tr>"""

def note(text):
    return f"""<p style="margin:6px 0 0 0;font-family:Georgia,serif;font-size:13px;line-height:1.7;color:#555;text-align:justify;">{text}</p>"""

# ── Job 42 rows ───────────────────────────────────────────────────────────────
J42 = [
    ("<strong>Arooj Khalid</strong> " + dim("3868"), "Sent", ok("PASS &middot; 3 Aug"), "Sent 6 Aug &rarr; " + ok("Submitted 10 Aug"), bad("Not sent")),
    ("<strong>M. Arshan Bilal</strong> " + dim("3884"), "Sent 5 Aug", ok("PASS &middot; 7 Aug"), "Sent 7 Aug &rarr; " + ok("Submitted 7 Aug"), bad("Not sent")),
    ("<strong>Umar Zahid</strong> " + dim("3902"), "Sent 5 Aug", ok("PASS &middot; 11 Aug"), bad("Not sent yet"), dim("&mdash;")),
    ("<strong>Rimsha Taj</strong> " + dim("3956"), "Sent 5 Aug", ok("PASS &middot; 12 Aug"), bad("Not sent yet"), dim("&mdash;")),
    ("<strong>Muhammad Zeshan</strong> " + dim("3921"), "Sent 5 Aug", ok("PASS &middot; 7 Aug"), "Sent 7 Aug &rarr; " + warn("awaited"), dim("&mdash;")),
    ("<strong>Fahad Ali</strong> " + dim("3916"), "Sent 5 Aug", bad("FAIL &middot; 10 Aug") + "<br>" + dim("still marked shortlisted"), dim("&mdash;"), dim("&mdash;")),
    ("<strong>Salman Ahmad</strong> " + dim("3943"), "Sent 5 Aug", bad("FAIL &middot; 10 Aug") + "<br>" + dim("rejected; feedback email pending"), dim("&mdash;"), dim("&mdash;")),
    ("<strong>Hina Rehman</strong> " + dim("3958"), "Sent 5 Aug", warn("Held today 11am &middot; result pending"), dim("&mdash;"), dim("&mdash;")),
    ("<strong>Shahmir Hashmat</strong> " + dim("3911"), "Sent 5 Aug", "Booked Thu 13 Aug 1pm", dim("&mdash;"), dim("&mdash;")),
    ("<strong>Vaneeza Baig</strong> " + dim("4033"), "Sent 7 Aug", "Booked Wed 19 Aug 12pm", dim("&mdash;"), dim("&mdash;")),
    ("<strong>Ali Ahmed</strong> " + dim("3946"), "Sent 5 Aug", bad("Canceled 11 Aug &middot; not rebooked"), dim("&mdash;"), dim("&mdash;")),
    ("<strong>Murtaza Hassan</strong> " + dim("3879"), "Sent 5 Aug", warn("Never booked (7 days)"), dim("&mdash;"), dim("&mdash;")),
    ("<strong>M. Shakeel Ahmad</strong> " + dim("3892"), "Sent 5 Aug", warn("Never booked (7 days)"), dim("&mdash;"), dim("&mdash;")),
    ("<strong>Junaid Ali</strong> " + dim("3992"), warn("None on record"), warn("Blank scorecard 7 Aug &middot; no result"), "Sent 7 Aug &rarr; " + ok("Submitted 9 Aug"), bad("Not sent")),
    ("<strong>Muhammad Bilal</strong> " + dim("4051"), warn("None on record"), warn("Blank scorecard 7 Aug &middot; no result"), "Sent 7 Aug &rarr; " + warn("awaited"), dim("&mdash;")),
    ("<strong>Yusra Amjad</strong> " + dim("4061"), warn("None on record"), warn("Blank scorecard 7 Aug &middot; no result"), "Sent 7 Aug &rarr; " + ok("Submitted 10 Aug"), bad("Not sent")),
    ("<strong>M. Ahmad Taj</strong> " + dim("3971"), bad("Never sent"), dim("&mdash;"), dim("&mdash;"), dim("&mdash;")),
    ("<strong>Ali Wajdan Khan</strong> " + dim("3977"), bad("Never sent"), dim("&mdash;"), dim("&mdash;"), dim("&mdash;")),
    ("<strong>Hania Khan</strong> " + dim("4035"), bad("Never sent"), dim("&mdash;"), dim("&mdash;"), dim("&mdash;")),
    ("<strong>Kanooz Ahmed Siddiqui</strong> " + dim("4111"), bad("Never sent"), dim("&mdash;"), dim("&mdash;"), dim("&mdash;")),
    ("<strong>Khushal Khan</strong> " + dim("4134"), bad("Never sent"), dim("&mdash;"), dim("&mdash;"), dim("&mdash;")),
    ("<strong>Lamis Maniar</strong> " + dim("4062"), bad("Never sent"), dim("&mdash;"), dim("&mdash;"), dim("&mdash;")),
    ("<strong>Sara Obaid Ul Islam</strong> " + dim("4138"), bad("Never sent"), dim("&mdash;"), dim("&mdash;"), dim("&mdash;")),
    ("<strong>Shafaq Syed</strong> " + dim("4137"), bad("Never sent"), dim("&mdash;"), dim("&mdash;"), dim("&mdash;")),
]
J42_OFFM = [
    ("<strong>Syed Basit</strong> " + dim("not in Markaz"), "Sent 7 Aug", "Booked Thu 13 Aug 9am", dim("&mdash;"), dim("&mdash;")),
    ("<strong>Furqan Afzal</strong> " + dim("not in Markaz"), "Sent 7 Aug", "Booked Fri 14 Aug 11am", dim("&mdash;"), dim("&mdash;")),
    ("<strong>Irfan Siddiqui</strong> " + dim("not in Markaz"), "Sent 7 Aug", "Booked Fri 14 Aug 12pm", dim("&mdash;"), dim("&mdash;")),
    ("<strong>Yusra Wahid</strong> " + dim("not in Markaz"), "Sent 7 Aug", warn("Not booked"), dim("&mdash;"), dim("&mdash;")),
    ("<strong>Imran Mehmood Choudhry</strong> " + dim("not in Markaz"), "Sent 7 Aug", warn("Not booked"), dim("&mdash;"), dim("&mdash;")),
]

# ── Job 41 rows ───────────────────────────────────────────────────────────────
J41 = [
    ("<strong>Waqas Hassan</strong> " + dim("3870"), "Sent", ok("PASS &middot; 24 Jul"), "Sent 4 Aug, nudged 6 Aug &rarr; " + ok("Submitted 7 Aug"), "Sent 7 Aug &middot; " + warn("not booked yet")),
    ("<strong>Muneeb Arif</strong> " + dim("3869"), "Sent 26 Jul", ok("PASS &middot; 30 Jul"), "Sent 4 Aug, nudged 6 Aug &rarr; " + ok("Submitted 9 Aug"), bad("Not sent")),
    ("<strong>Zirghaam Ahmad</strong> " + dim("3830"), "Sent", ok("PASS &middot; 27 Jul"), "Sent 7 Aug &rarr; " + warn("asked extension till after 12 Aug"), dim("&mdash;")),
    ("<strong>Zubair Hussain</strong> " + dim("3792"), "Sent 4 Aug", ok("PASS &middot; 7 Aug"), "Sent 7 Aug &rarr; " + warn("asked one-night extension 10 Aug"), dim("&mdash;")),
    ("<strong>Syeda Masooma Asif</strong> " + dim("3865"), "Sent 4 Aug", ok("PASS &middot; 10 Aug"), "Sent 10 Aug &rarr; " + warn("awaited"), dim("&mdash;")),
    ("<strong>Huda Shaikh</strong> " + dim("3803"), "Sent 4 Aug", ok("PASS &middot; 10 Aug"), "Sent 10 Aug &rarr; " + warn("awaited"), dim("&mdash;")),
    ("<strong>M. Huzaifa Wakil</strong> " + dim("3825"), "Sent 4 Aug", bad("FAIL &middot; 7 Aug") + "<br>" + dim("still marked shortlisted"), dim("&mdash;"), dim("&mdash;")),
    ("<strong>Marzia Hasnain</strong> " + dim("3819"), "Sent 4 Aug", warn("Booked Thu 13 Aug 3pm &middot; hosts declined the block"), dim("&mdash;"), dim("&mdash;")),
    ("<strong>Khizran Zehra Baloch</strong> " + dim("4065"), "Sent 12 Aug", "Rebooked Tue 18 Aug 3pm", dim("&mdash;"), dim("&mdash;")),
    ("<strong>Syed Zubair Ali</strong> " + dim("4113"), "Sent 12 Aug", "Booked Mon 17 Aug 3pm", dim("&mdash;"), dim("&mdash;")),
    ("<strong>Yashfeen Zahid</strong> " + dim("3799"), "Sent 4 Aug", bad("FAIL &middot; 11 Aug") + "<br>" + dim("rejected; feedback email pending"), dim("&mdash;"), dim("&mdash;")),
]

# ── Job 39 rows ───────────────────────────────────────────────────────────────
J39 = [
    ("<strong>Abdul Wahab</strong> " + dim("3614"), "Sent 8 Jul", ok("PASS &middot; 27 Jul"), "Sent 4 Aug &rarr; " + ok("Submitted 5 Aug"), "Booked Thu 13 Aug 2pm"),
    ("<strong>Muhammad Waqas</strong> " + dim("3651"), "Sent 8 Jul", ok("PASS &middot; 27 Jul"), "Sent 4 Aug &rarr; " + ok("Submitted 5 Aug"), ok("Held 11 Aug")),
    ("<strong>Ahmad Wajahat</strong> " + dim("3635"), "Sent 8 Jul", ok("PASS &middot; 29 Jul"), "Sent 4 Aug &rarr; " + ok("Submitted 5 Aug"), "Booked today 3pm"),
    ("<strong>Salman Tariq</strong> " + dim("3656"), "Sent 8 Jul", ok("PASS &middot; 24 Jul"), "Sent 4 Aug &rarr; " + ok("Submitted 6 Aug"), ok("Held 10 Aug")),
    ("<strong>Hafiz Osama</strong> " + dim("3601"), "Sent 8 Jul", ok("PASS &middot; 29 Jul"), "Sent 4 Aug &rarr; " + bad("8 days outstanding, no nudge"), dim("&mdash;")),
    ("<strong>Maheen Arif</strong> " + dim("3608"), "Sent 8 Jul", bad("FAIL &middot; 28 Jul") + "<br>" + dim("still marked shortlisted"), dim("&mdash;"), dim("&mdash;")),
    ("<strong>Anushey Tahir</strong> " + dim("3660"), "Sent 8 Jul", bad("Canceled her 28 Jul call &middot; never rebooked"), dim("&mdash;"), dim("&mdash;")),
    ("<strong>Mahnoor Farooq Khan</strong> " + dim("3613"), "Sent 8 Jul", warn("Call booked ~24 Jul &middot; no result recorded"), dim("&mdash;"), dim("&mdash;")),
    ("<strong>Usman Ali</strong> " + dim("3629"), "Sent 8 Jul", warn("Never booked (5 weeks)"), dim("&mdash;"), dim("&mdash;")),
    ("<strong>Zeeshan Ahmed</strong> " + dim("3641"), "Sent 8 Jul", warn("Never booked (5 weeks)"), dim("&mdash;"), dim("&mdash;")),
    ("<strong>Ahmad Khan</strong> " + dim("3697"), bad("Never sent"), dim("&mdash;"), dim("&mdash;"), dim("&mdash;")),
    ("<strong>Ali Murad</strong> " + dim("3704"), bad("Never sent"), dim("&mdash;"), dim("&mdash;"), dim("&mdash;")),
    ("<strong>M. Hamid Yaqoob</strong> " + dim("3695"), bad("Never sent"), dim("&mdash;"), dim("&mdash;"), dim("&mdash;")),
    ("<strong>M. Qasim Mujahid</strong> " + dim("3696"), bad("Never sent"), dim("&mdash;"), dim("&mdash;"), dim("&mdash;")),
]

HTML = f"""
<html><body style="margin:0;padding:0;background:#f5f5f5;">
<table width="100%" cellpadding="0" cellspacing="0" bgcolor="#f5f5f5"><tr><td align="center" style="padding:30px 0;">
<table width="760" cellpadding="0" cellspacing="0" bgcolor="#ffffff" style="max-width:760px;">

  <tr><td bgcolor="#1a2a3a" style="padding:28px 36px;">
    <p style="margin:0;font-family:Arial,sans-serif;font-size:11px;letter-spacing:2px;color:#9fb3cc;text-transform:uppercase;">People &amp; Culture &middot; Pipeline Status Report</p>
    <p style="margin:8px 0 0 0;font-family:Georgia,serif;font-size:24px;color:#ffffff;font-weight:bold;">Growth Roles &mdash; Full Pipeline</p>
    <p style="margin:4px 0 0 0;font-family:Georgia,serif;font-size:13px;color:#9fb3cc;">Senior Manager Growth &middot; Growth Manager Karachi &middot; Growth Manager Lahore &middot; August 12, 2026</p>
  </td></tr>

  <tr><td style="padding:26px 36px 6px 36px;">
    <table width="100%" cellpadding="0" cellspacing="0"><tr>
      <td width="25%" align="center" style="background:#eaf7ee;padding:14px 4px;border-radius:6px;">
        <p style="margin:0;font-family:Georgia,serif;font-size:26px;color:#1b5e20;font-weight:bold;">16</p>
        <p style="margin:2px 0 0 0;font-family:Arial,sans-serif;font-size:10px;letter-spacing:1px;color:#55606e;">VALUES CLEARED</p></td>
      <td width="8"></td>
      <td width="25%" align="center" style="background:#fdecea;padding:14px 4px;border-radius:6px;">
        <p style="margin:0;font-family:Georgia,serif;font-size:26px;color:#b3261e;font-weight:bold;">5</p>
        <p style="margin:2px 0 0 0;font-family:Arial,sans-serif;font-size:10px;letter-spacing:1px;color:#55606e;">VALUES NOT CLEARED</p></td>
      <td width="8"></td>
      <td width="25%" align="center" style="background:#eaf1fb;padding:14px 4px;border-radius:6px;">
        <p style="margin:0;font-family:Georgia,serif;font-size:26px;color:#3157b7;font-weight:bold;">10<span style="font-size:15px;color:#8a94a3;">/17</span></p>
        <p style="margin:2px 0 0 0;font-family:Arial,sans-serif;font-size:10px;letter-spacing:1px;color:#55606e;">CASE STUDIES SUBMITTED</p></td>
      <td width="8"></td>
      <td width="25%" align="center" style="background:#fdf3e7;padding:14px 4px;border-radius:6px;">
        <p style="margin:0;font-family:Georgia,serif;font-size:26px;color:#b26a00;font-weight:bold;">17</p>
        <p style="margin:2px 0 0 0;font-family:Arial,sans-serif;font-size:10px;letter-spacing:1px;color:#55606e;">ACTION FLAGS</p></td>
    </tr></table>
  </td></tr>

  <tr><td style="padding:20px 36px 0 36px;">
    <p style="margin:0 0 6px 0;font-family:Georgia,serif;font-size:15px;color:#3157b7;font-weight:bold;">Key observation</p>
    <p style="margin:0 0 4px 0;font-family:Georgia,serif;font-size:14px;line-height:1.75;color:#222;text-align:justify;">
      The three Growth pipelines are healthy in the middle and leaking at both ends. In the middle: 16 candidates have
      cleared values, 17 case studies are out, 10 are back, and every GM-Lahore submitter is booked or done on debriefs.
      At the front: 12 shortlisted candidates (8 SMG, 4 GM-Lahore) have never been sent a values invite. At the back:
      all four SMG submissions plus Muneeb Arif on GM-Karachi are waiting on debrief invites that do not exist yet, and
      two fresh SMG values-passers (Umar Zahid, Rimsha Taj) have no case study. Every date below is verified against
      Markaz, the send log, and the booking confirmations in the mailbox &mdash; nothing is assumed.</p>
  </td></tr>

  {section("Senior Manager Growth &mdash; Job 42", "24 candidates in Markaz (23 shortlisted + Salman Ahmad, resolved) &middot; band PKR 350&ndash;400k &middot; closes 15 Aug", job_table(J42),
    note("Rows 14&ndash;16 (Junaid, Muhammad Bilal, Yusra): no invite or booking exists anywhere, yet blank scorecards dated 7 Aug carry your name as host and case studies went out the same day &mdash; please confirm their values calls happened off-calendar so the results can be recorded. Jawwad's test entry (3867) excluded."))}

  {section("Senior Manager Growth &mdash; direct invitees (not in Markaz)", "Invited 7 Aug at your instruction &middot; outcomes cannot be tracked in Markaz until records exist", job_table(J42_OFFM), "")}

  {section("Growth Manager Karachi &mdash; Job 41", "10 shortlisted + Yashfeen Zahid (resolved) &middot; band PKR 210&ndash;270k", job_table(J41),
    note("Marzia's interview is tomorrow 3pm but Waqas and Zeshan declined the calendar block &mdash; a host needs to attend. Zirghaam was sent the SMG case-study template by mistake on 7 Aug. Zubair Hussain also holds a stray second Zero-In booking for 13 Aug 1pm (his call already happened 7 Aug) &mdash; worth canceling. His reminder nudge was piloted 10 Aug and never approved live. Aqleem Ullah Khan (3797) sits separately at consider_other_roles."))}

  {section("Growth Manager Lahore &mdash; Job 39", "14 in pipeline &middot; case-study evaluation report for the 4 submitters piloted to you 10 Aug", job_table(J39),
    note("Rows 11&ndash;14 applied on 7 Jul and appear to have been shortlisted after the 8 Jul invite wave, so they were never picked up."))}

  <tr><td style="padding:22px 36px 4px 36px;">
    <p style="margin:0 0 6px 0;font-family:Georgia,serif;font-size:15px;color:#3157b7;font-weight:bold;">Updates found in the mailbox &amp; calendar (read-only check, 12 Aug)</p>
    <table width="100%" cellpadding="0" cellspacing="0" style="border:1px solid #d9dee7;border-radius:6px;"><tr><td style="padding:14px 20px;">
      <p style="margin:0 0 8px 0;font-family:Georgia,serif;font-size:13px;line-height:1.7;color:#222;"><strong>1. Zubair Hussain</strong> (GM-KHI) emailed 10 Aug asking for one more night on the case study &mdash; Saturday working day plus hostel electricity shortfall in Khairpur. Not submitted yet; his reply is unanswered.</p>
      <p style="margin:0 0 8px 0;font-family:Georgia,serif;font-size:13px;line-height:1.7;color:#222;"><strong>2. Zirghaam Ahmad</strong> (GM-KHI) replied 8 Aug asking to take the case study up after 12 Aug &mdash; traveling in the Northern Areas with patchy internet.</p>
      <p style="margin:0 0 8px 0;font-family:Georgia,serif;font-size:13px;line-height:1.7;color:#222;"><strong>3. Ali Ahmed</strong> (SMG) canceled his values call at call time on 11 Aug and has not rebooked.</p>
      <p style="margin:0 0 8px 0;font-family:Georgia,serif;font-size:13px;line-height:1.7;color:#222;"><strong>4. Khizran</strong> (GM-KHI) asked this morning whether the 14 Aug 3pm slot stands given the public holiday; the calendar now shows her at Tue 18 Aug 3pm.</p>
      <p style="margin:0 0 8px 0;font-family:Georgia,serif;font-size:13px;line-height:1.7;color:#222;"><strong>5. Vaneeza Baig</strong> (SMG) accepted warmly on 10 Aug and is booked for Wed 19 Aug 12pm.</p>
      <p style="margin:0 0 8px 0;font-family:Georgia,serif;font-size:13px;line-height:1.7;color:#222;"><strong>6. Marzia Hasnain</strong> (GM-KHI) is not a missed interview &mdash; the 4 Aug booking was for Thu 13 Aug 3pm, tomorrow.</p>
      <p style="margin:0;font-family:Georgia,serif;font-size:13px;line-height:1.7;color:#222;"><strong>7. Anushey Tahir</strong> (GM-LHR) canceled her 28 Jul call the night before and never rebooked &mdash; that is why she has no result.</p>
    </td></tr></table>
  </td></tr>

  <tr><td style="padding:22px 36px 4px 36px;">
    <p style="margin:0 0 6px 0;font-family:Georgia,serif;font-size:15px;color:#3157b7;font-weight:bold;">Action flags (17)</p>
    <table width="100%" cellpadding="0" cellspacing="0" style="border:1px solid #d9dee7;border-radius:6px;"><tr><td style="padding:14px 20px;">
      <p style="margin:0 0 8px 0;font-family:Georgia,serif;font-size:13px;line-height:1.7;color:#222;">
        <strong style="color:{RED};">Values invite never sent (12):</strong> SMG &mdash; Ahmad Taj, Ali Wajdan Khan, Hania Khan, Kanooz Siddiqui, Khushal Khan, Lamis Maniar, Sara Obaid, Shafaq Syed. GM-Lahore &mdash; Ahmad Khan, Ali Murad, Hamid Yaqoob, Qasim Mujahid.</p>
      <p style="margin:0 0 8px 0;font-family:Georgia,serif;font-size:13px;line-height:1.7;color:#222;">
        <strong style="color:{RED};">Case study submitted, debrief invite not sent (5):</strong> Arshan Bilal, Junaid Ali, Arooj Khalid, Yusra Amjad (SMG &mdash; no SMG debrief invites exist yet) and Muneeb Arif (GM-KHI).</p>
      <p style="margin:0;font-family:Georgia,serif;font-size:13px;line-height:1.7;color:#222;">
        <strong style="color:{AMBER};">Also waiting on a decision:</strong> case studies for Umar Zahid + Rimsha Taj (values cleared, nothing sent); the three fail-but-still-shortlisted statuses (Fahad Ali, Huzaifa Wakil, Maheen Arif); pending feedback emails for Salman Ahmad + Yashfeen Zahid; a nudge for Hafiz Osama; replies to the two extension requests; re-engaging or releasing Ali Ahmed, Murtaza Hassan, Shakeel Ahmad, Usman Ali, Zeeshan Ahmed, Anushey Tahir and Mahnoor Farooq.</p>
    </td></tr></table>
  </td></tr>

  <tr><td style="padding:20px 36px 8px 36px;">
    <p style="margin:0;font-family:Georgia,serif;font-size:12px;line-height:1.7;color:#8a94a3;">
      Case-study submission folders: <a href="https://drive.google.com/drive/folders/1mkrVspKtD1QLFK277dmPPirCP_lHglJA" style="color:#3157b7;">Senior Manager Growth</a> &middot;
      <a href="https://drive.google.com/drive/folders/1xHkwebowKnb2GnQsFFe5HqbKeAYxbeGD" style="color:#3157b7;">Growth Manager Karachi</a> &middot;
      <a href="https://drive.google.com/drive/folders/1ohbfTtzfUBWry8sJmoC_oc7oxz0NnUyt" style="color:#3157b7;">Growth Manager Lahore</a></p>
  </td></tr>

  <tr><td style="padding:10px 36px 28px 36px;border-top:1px solid #e4e8ef;">
    <p style="margin:12px 0 0 0;font-family:Georgia,serif;font-size:12px;color:#8a94a3;">Taleemabad Talent Acquisition &nbsp;|&nbsp; hiring@taleemabad.com &nbsp;|&nbsp; August 12, 2026</p>
  </td></tr>

</table>
</td></tr></table>
</body></html>
"""


def main():
    recipients = [PILOT_TO] if PILOT_MODE else LIVE_TO + LIVE_CC
    msg = MIMEMultipart("alternative")
    msg["Subject"] = SUBJECT
    msg["From"] = SENDER
    msg["To"] = PILOT_TO if PILOT_MODE else ", ".join(LIVE_TO)
    if not PILOT_MODE and LIVE_CC:
        msg["Cc"] = ", ".join(LIVE_CC)
    msg.attach(MIMEText(HTML, "html"))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(SENDER, PASSWORD)
    safe_sendmail(
        smtp_server=server,
        sender=SENDER,
        recipients=recipients,
        message=msg.as_string(),
        context=f"growth_pipeline_report_2026_08_12_{'PILOT' if PILOT_MODE else 'LIVE'}",
    )
    server.quit()
    print(f"[{'PILOT' if PILOT_MODE else 'LIVE'}] Growth pipeline report sent -> {recipients}")


if __name__ == "__main__":
    main()
