"""
Leave & WFH Report — 8 named staff (Ayesha, 2026-08-19).

Ayesha's brief: "get me a report of leaves for all these people ... the entire data from
Markaz, how many weeks they've taken and when did they take the leaves and also were they
approved or not ... a very thorough report."

Names supplied: Hamdan Ahmad, Muhammad Usman Javed, Nawal Khurram, Muhammad Muzzammil Patel,
Osama Ahmad, Rahima Omar, Taimoor Abdullah, Momina Raja.

Context: follows the Sabeena/Ayesha call of 19 Aug, where Sabeena asked for leave visibility,
an alternate approver, cover ownership, and an objective org-wide leave analysis (never done).

METHOD NOTES BAKED INTO THE REPORT:
  - Markaz stores WFH inside leave_requests as leave_type='work_from_home'. Reported as a
    SEPARATE column, never folded into leave days.
  - start_date/end_date are calendar dates. Working days computed Mon-Fri; public holidays are
    NOT in the database, so working-day figures are a slight OVER-count.
  - Nawal Khurram has TWO user records (active + archived). Both are pulled and shown
    separately, then combined, or her history undercounts.
  - Two different people are named Taimoor Abdullah. Both are shown, labelled.
  - Leave types are not equivalent: paternity, wedding grant and medical are entitlements,
    not discretionary absence. The report says so rather than ranking raw day counts.

Uses Neon HTTPS SQL API (port 5432 blocked). Read-only SELECTs.
No Word/PDF viewer on this machine -> structural verification only (CLAUDE.md Rule 14).
"""

import os
import smtplib
import sys
from datetime import date
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests
from dotenv import load_dotenv
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, KeepTogether, PageBreak,
                               PageTemplate, Paragraph, Spacer, Table, TableStyle)

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from scripts.utils.safe_send import safe_sendmail  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
load_dotenv(os.path.join(ROOT, ".env"))
URL = os.environ["DATABASE_URL"]
HOST = URL.split("@")[1].split("/")[0]

SENDER = "ayesha.khan@taleemabad.com"
RECIPIENTS = ["ayesha.khan@taleemabad.com"]
SUBJECT = "[PILOT - ] Leave & WFH Report - 8 named staff | as at 19 August 2026"
OUT_PDF = os.path.join(ROOT, "output", "reports", "Leave_Report_Named_Staff_2026-08-19.pdf")
TODAY = date(2026, 8, 19)

# user_id -> (display label, note)
TARGETS = {
    "user-1781766933165-6bennbn5a": ("Hamdan Ahmad", ""),
    "user-1751134210030-cast609wa": ("Muhammad Usman Javed", ""),
    "user-1784531629947-rhid5j0rj": ("Nawal Khurram", "active record"),
    "user-1752813207085-r82vkp1ys": ("Nawal Khurram", "archived record - same person"),
    "user-1767619173370-k06b07avk": ("Muhammad Muzzammil Patel", ""),
    "user-1751134200553-okyuusi6c": ("Osama Ahmad", ""),
    "user-1777985545895-r5avvx2xr": ("Rahima Omar", ""),
    "user-1783805300065-dxzh6ey44": ("Taimoor Abdullah", "Impact & Policy - active"),
    "user-1751134182423-9ceqh7vm3": ("Taimoor Abdullah", "NIETE ICT - archived, different person"),
    "user-1751134178503-lxckgoywv": ("Momina Raja", ""),
}
ORDER = ["Muhammad Usman Javed", "Muhammad Muzzammil Patel", "Rahima Omar", "Nawal Khurram",
         "Taimoor Abdullah", "Hamdan Ahmad", "Momina Raja", "Osama Ahmad"]


def q(sql, params=None):
    r = requests.post(f"https://{HOST}/sql",
                      headers={"Neon-Connection-String": URL, "Content-Type": "application/json"},
                      json={"query": sql, "params": params or []}, timeout=120)
    r.raise_for_status()
    return r.json()["rows"]


IDS = list(TARGETS)

PROFILES = q("""
SELECT u.id, u.first_name||' '||u.last_name AS name, u.email, u.status,
       ep.employee_id, ep.department, ep.payroll_entity, ep.job_title,
       ep.joining_date::date::text AS joined,
       lm.first_name||' '||lm.last_name AS line_manager
FROM users u
LEFT JOIN employee_profiles ep ON ep.user_id=u.id
LEFT JOIN users lm ON ep.line_manager_id=lm.id
WHERE u.id = ANY($1)""", [IDS])

REQS = q("""
SELECT lr.user_id, lr.id, lr.leave_type, lr.sub_category, lr.is_half_day,
       lr.start_date::text AS start_d, lr.end_date::text AS end_d,
       (lr.end_date - lr.start_date + 1) AS cal_days,
       (SELECT count(*) FROM generate_series(lr.start_date, lr.end_date, '1 day') d
         WHERE extract(isodow FROM d) < 6) AS work_days,
       lr.status, ap.first_name||' '||ap.last_name AS approver,
       lr.approved_at::date::text AS approved_on,
       lr.created_at::date::text AS requested_on,
       (lr.start_date - lr.created_at::date) AS notice_days,
       (lr.approved_at::date - lr.start_date) AS approval_vs_start,
       lr.backup_assignee_id IS NOT NULL AS has_cover,
       lr.approver_comments, lr.reason
FROM leave_requests lr
LEFT JOIN users ap ON ap.id=lr.approver_id
WHERE lr.user_id = ANY($1)
ORDER BY lr.start_date""", [IDS])

ORG = q("""
WITH exp AS (
  SELECT lr.user_id, lr.leave_type,
    (SELECT count(*) FROM generate_series(greatest(lr.start_date,'2026-01-01'::date),
        least(lr.end_date,$1::date), '1 day') d WHERE extract(isodow FROM d) < 6) AS wd
  FROM leave_requests lr
  WHERE lr.start_date <= $1::date AND lr.end_date >= '2026-01-01' AND lr.status='approved'),
per AS (SELECT ep.department, e.user_id,
          sum(e.wd) FILTER (WHERE e.leave_type<>'work_from_home') AS lv
        FROM exp e JOIN employee_profiles ep ON ep.user_id=e.user_id GROUP BY 1,2)
SELECT COALESCE(department,'(none)') AS department, count(*) AS n,
       round(avg(lv),1) AS avg_days, max(lv) AS max_days
FROM per GROUP BY 1 HAVING avg(lv) IS NOT NULL ORDER BY 3 DESC LIMIT 10""",
        [TODAY.isoformat()])

STATUSES = q("""
WITH exp AS (SELECT lr.status,
  (SELECT count(*) FROM generate_series(greatest(lr.start_date,'2026-01-01'::date),
     least(lr.end_date,$1::date),'1 day') d WHERE extract(isodow FROM d)<6) AS wd
  FROM leave_requests lr WHERE lr.start_date <= $1::date AND lr.end_date >= '2026-01-01')
SELECT status, count(*) AS reqs, sum(wd) AS wd FROM exp GROUP BY 1 ORDER BY 2 DESC""",
             [TODAY.isoformat()])

# ---------------------------------------------------------------- styles
NAVY = colors.HexColor("#34495e")
ORANGE = colors.HexColor("#f57c00")
DBLUE = colors.HexColor("#1565c0")
GREEN = colors.HexColor("#2e7a4f")
RED = colors.HexColor("#c62828")
PURPLE = colors.HexColor("#6a1b9a")
GREY = colors.HexColor("#6b7a90")
RULE = colors.HexColor("#d9dde3")

FONTS = r"C:\Windows\Fonts"
for nm, fn in [("Georgia", "georgia.ttf"), ("Georgia-Bold", "georgiab.ttf"),
               ("Georgia-Italic", "georgiai.ttf"), ("Georgia-BoldItalic", "georgiaz.ttf")]:
    pdfmetrics.registerFont(TTFont(nm, os.path.join(FONTS, fn)))
pdfmetrics.registerFontFamily("Georgia", normal="Georgia", bold="Georgia-Bold",
                              italic="Georgia-Italic", boldItalic="Georgia-BoldItalic")

BODY = ParagraphStyle("b", fontName="Georgia", fontSize=9.2, leading=14,
                      alignment=TA_JUSTIFY, textColor=colors.HexColor("#22303f"))
H1 = ParagraphStyle("h1", fontName="Georgia-Bold", fontSize=13.5, leading=17,
                    textColor=NAVY, spaceBefore=6, spaceAfter=5)
H2 = ParagraphStyle("h2", fontName="Georgia-Bold", fontSize=10.5, leading=14,
                    textColor=colors.white)
TC = ParagraphStyle("tc", fontName="Georgia", fontSize=7.8, leading=10.6)
TCS = ParagraphStyle("tcs", fontName="Georgia", fontSize=7.2, leading=9.8,
                     textColor=colors.HexColor("#3d4c5c"))
TH = ParagraphStyle("th", fontName="Georgia-Bold", fontSize=7.6, leading=10,
                    textColor=colors.white)
NOTE = ParagraphStyle("n", fontName="Georgia-Italic", fontSize=8.2, leading=12,
                      textColor=colors.HexColor("#5a4632"), alignment=TA_JUSTIFY)


def by_person():
    out = {}
    for uid, (label, note) in TARGETS.items():
        prof = next((p for p in PROFILES if p["id"] == uid), None)
        rs = [r for r in REQS if r["user_id"] == uid]
        out.setdefault(label, []).append((uid, note, prof, rs))
    return out


PEOPLE = by_person()


def tenure_days(joined):
    if not joined:
        return None
    y, m, d = map(int, joined.split("-"))
    return (TODAY - date(y, m, d)).days


def totals(rs):
    lv = sum(int(r["work_days"]) for r in rs
             if r["leave_type"] != "work_from_home" and r["status"] == "approved")
    wf = sum(int(r["work_days"]) for r in rs
             if r["leave_type"] == "work_from_home" and r["status"] == "approved")
    return lv, wf


def summary_table():
    head = [Paragraph(x, TH) for x in
            ["Person", "Dept / role", "Joined", "Leave<br/>requests", "Leave days<br/>(working)",
             "= weeks", "WFH<br/>reqs", "WFH days", "Approved /<br/>Pending / Rejected"]]
    rows = [head]
    for label in ORDER:
        for uid, note, prof, rs in PEOPLE[label]:
            if note.startswith("NIETE") and not rs:
                continue
            lv, wf = totals(rs)
            lvr = [r for r in rs if r["leave_type"] != "work_from_home"]
            wfr = [r for r in rs if r["leave_type"] == "work_from_home"]
            ap = sum(1 for r in rs if r["status"] == "approved")
            pe = sum(1 for r in rs if r["status"] == "pending")
            rj = sum(1 for r in rs if r["status"] == "rejected")
            nm = label + (f'<br/><font size="6.4" color="#6b7a90">{note}</font>' if note else "")
            dept = ((prof.get("department") or "-") + " / " +
                    (prof.get("job_title") or "not set")) if prof else "-"
            rows.append([Paragraph(nm, TC), Paragraph(dept, TCS),
                         Paragraph(prof.get("joined") or "not set", TCS) if prof else Paragraph("-", TCS),
                         Paragraph(str(len(lvr)), TC), Paragraph(f"<b>{lv}</b>", TC),
                         Paragraph(f"{lv/5:.1f}" if lv else "0", TC),
                         Paragraph(str(len(wfr)), TC), Paragraph(str(wf), TC),
                         Paragraph(f"{ap} / {pe} / {rj}", TC)])
    t = Table(rows, colWidths=[38*mm, 52*mm, 20*mm, 18*mm, 21*mm, 15*mm, 15*mm, 17*mm, 30*mm],
              repeatRows=1)
    st = [("BACKGROUND", (0, 0), (-1, 0), NAVY), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
          ("ALIGN", (3, 0), (-1, -1), "CENTER"),
          ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
          ("LEFTPADDING", (0, 0), (-1, -1), 5)]
    for i in range(1, len(rows)):
        if i % 2 == 0:
            st.append(("BACKGROUND", (0, i), (-1, i), colors.HexColor("#f5f7fa")))
    t.setStyle(TableStyle(st))
    return t


def request_table(rs):
    head = [Paragraph(x, TH) for x in
            ["#", "Dates", "Cal /<br/>work days", "Type", "Status", "Approver",
             "Approved on", "Requested<br/>on", "Notice<br/>(days)", "Cover<br/>named?", "Reason given"]]
    rows = [head]
    for r in rs:
        typ = r["leave_type"].replace("_", " ")
        if r["sub_category"]:
            typ += f'<br/><font size="6.2" color="#6b7a90">{r["sub_category"]}</font>'
        dates = (r["start_d"] if r["start_d"] == r["end_d"]
                 else f'{r["start_d"]}<br/>to {r["end_d"]}')
        late = (r["approval_vs_start"] is not None and int(r["approval_vs_start"]) > 0)
        appr = r["approved_on"] or "-"
        if late:
            appr = (f'<font color="#c62828">{appr}</font>'
                    f'<br/><font size="6.2" color="#c62828">+{r["approval_vs_start"]}d after start</font>')
        stat = r["status"]
        scol = {"approved": "#2e7a4f", "pending": "#f57c00",
                "rejected": "#c62828"}.get(stat, "#6b7a90")
        rows.append([Paragraph(str(r["id"]), TCS), Paragraph(dates, TCS),
                     Paragraph(f'{r["cal_days"]} / <b>{r["work_days"]}</b>', TCS),
                     Paragraph(typ, TCS),
                     Paragraph(f'<font color="{scol}"><b>{stat}</b></font>', TCS),
                     Paragraph(r["approver"] or "-", TCS), Paragraph(appr, TCS),
                     Paragraph(r["requested_on"], TCS),
                     Paragraph(str(r["notice_days"]), TCS),
                     Paragraph("yes" if r["has_cover"] else
                               '<font color="#c62828">no</font>', TCS),
                     Paragraph((r["reason"] or "-")[:200], TCS)])
    t = Table(rows, colWidths=[9*mm, 24*mm, 16*mm, 22*mm, 16*mm, 24*mm, 22*mm, 19*mm,
                               12*mm, 13*mm, 76*mm], repeatRows=1)
    st = [("BACKGROUND", (0, 0), (-1, 0), NAVY), ("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("ALIGN", (2, 1), (2, -1), "CENTER"), ("ALIGN", (8, 1), (9, -1), "CENTER"),
          ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
          ("LEFTPADDING", (0, 0), (-1, -1), 4)]
    for i in range(1, len(rows)):
        if i % 2 == 0:
            st.append(("BACKGROUND", (0, i), (-1, i), colors.HexColor("#f5f7fa")))
    t.setStyle(TableStyle(st))
    return t


def person_banner(label, note, prof, lv, wf, nreq):
    bits = []
    if prof:
        bits.append(prof.get("department") or "no dept")
        if prof.get("job_title"):
            bits.append(prof["job_title"])
        if prof.get("employee_id"):
            bits.append(f'emp {prof["employee_id"]}')
        if prof.get("joined"):
            td = tenure_days(prof["joined"])
            bits.append(f'joined {prof["joined"]} ({td//30} months)')
        if prof.get("line_manager"):
            bits.append(f'LM {prof["line_manager"]}')
        if prof.get("status") != "active":
            bits.append(prof["status"].upper())
    txt = (f'<b>{label}</b>'
           f'<font size="8"> &nbsp;·&nbsp; {nreq} request(s) &nbsp;·&nbsp; '
           f'<b>{lv}</b> leave working days ({lv/5:.1f} weeks) &nbsp;·&nbsp; '
           f'<b>{wf}</b> WFH days</font>')
    sub = " · ".join(bits) + (f" · {note}" if note else "")
    t = Table([[Paragraph(txt, H2)],
               [Paragraph(f'<font size="7.4" color="#dfe6ef">{sub}</font>', TC)]],
              colWidths=[253*mm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), NAVY),
                           ("LEFTPADDING", (0, 0), (-1, -1), 8),
                           ("TOPPADDING", (0, 0), (-1, 0), 5),
                           ("BOTTOMPADDING", (0, -1), (-1, -1), 5),
                           ("BOTTOMPADDING", (0, 0), (-1, 0), 1),
                           ("TOPPADDING", (0, -1), (-1, -1), 0)]))
    return t


def header_footer(canvas, doc):
    canvas.saveState()
    w, h = landscape(A4)
    canvas.setFillColor(NAVY)
    canvas.rect(0, h - 20*mm, w, 20*mm, stroke=0, fill=1)
    canvas.setFillColor(colors.HexColor("#aebccd"))
    canvas.setFont("Georgia", 7)
    canvas.drawString(15*mm, h - 8*mm, "PEOPLE & CULTURE  ·  LEAVE & WFH REPORT")
    canvas.setFillColor(colors.white)
    canvas.setFont("Georgia-Bold", 12)
    canvas.drawString(15*mm, h - 14*mm, "Leave & Work-From-Home Report — 8 named staff")
    canvas.setFillColor(colors.HexColor("#c3d0e6"))
    canvas.setFont("Georgia", 7.6)
    canvas.drawRightString(w - 15*mm, h - 14*mm, "Source: Markaz  ·  as at 19 August 2026")
    canvas.setStrokeColor(RULE)
    canvas.line(15*mm, 11*mm, w - 15*mm, 11*mm)
    canvas.setFillColor(GREY)
    canvas.setFont("Georgia", 7)
    canvas.drawString(15*mm, 7.5*mm, "Confidential — People & Culture")
    canvas.drawRightString(w - 15*mm, 7.5*mm, f"Page {canvas.getPageNumber()}")
    canvas.restoreState()


def build():
    os.makedirs(os.path.dirname(OUT_PDF), exist_ok=True)
    doc = BaseDocTemplate(OUT_PDF, pagesize=landscape(A4),
                          leftMargin=15*mm, rightMargin=15*mm,
                          topMargin=25*mm, bottomMargin=15*mm,
                          title="Leave & WFH Report - 8 named staff (19 Aug 2026)",
                          author="Taleemabad People & Culture")
    doc.addPageTemplates([PageTemplate(id="all",
        frames=[Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height)],
        onPage=header_footer)])

    total_lv = sum(totals(rs)[0] for l in ORDER for _, _, _, rs in PEOPLE[l])
    total_wf = sum(totals(rs)[1] for l in ORDER for _, _, _, rs in PEOPLE[l])
    nreq = sum(len(rs) for l in ORDER for _, _, _, rs in PEOPLE[l])
    zero = [l for l in ORDER if not any(rs for _, _, _, rs in PEOPLE[l])]

    story = [Paragraph("Scope and method", H1),
             Paragraph(
        "Every leave and work-from-home record held in Markaz for the eight people named, with "
        "no date cut-off — each person's full history is shown. For each request: the dates, "
        "calendar and working-day length, type, whether it was approved, by whom and when, how "
        "much notice was given, whether a cover person was named, and the reason given. "
        f"<b>{nreq} requests in total across the eight.</b>", BODY), Spacer(1, 7)]

    story += [Paragraph(
        "<b>Five things to read before the numbers.</b> "
        "<b>(1) Working days, not calendar days.</b> Markaz stores start and end dates, so a "
        "\u201c40-day\u201d request spanning weekends is fewer working days. Both are shown. Public "
        "holidays are not in the database, so working-day counts are a slight over-count. "
        "<b>(2) WFH is not leave.</b> Markaz files work-from-home inside the same table as "
        "<i>leave_type = work_from_home</i>. It is reported as a separate column and never added "
        "to leave days. "
        "<b>(3) Leave types are not equivalent.</b> Paternity, wedding grant and medical leave are "
        "entitlements, not discretionary absence. Raw day counts across different types should not "
        "be compared or ranked. "
        "<b>(4) Nawal Khurram has two user records</b> \u2014 one active, one archived. Both are shown "
        "and combined; reading either alone undercounts her. "
        "<b>(5) Two different people are named Taimoor Abdullah</b> \u2014 the Impact &amp; Policy "
        "colleague named in the call, and an archived NIETE ICT employee. Both are labelled.", NOTE),
        Spacer(1, 9)]

    story += [Paragraph("Summary", H1), summary_table(), Spacer(1, 6),
              Paragraph(f'<font size="8" color="#6b7a90">Totals across the eight: '
                        f'<b>{total_lv} leave working days</b> ({total_lv/5:.1f} weeks) and '
                        f'<b>{total_wf} WFH days</b>, from {nreq} requests. '
                        f'Weeks = working days ÷ 5.</font>', TC), Spacer(1, 10)]

    # ---- findings
    story.append(Paragraph("What the data shows", H1))
    findings = [
        (f"<b>{len(zero)} of the 8 have no leave or WFH record at all</b> \u2014 "
         f"{', '.join(zero)}. Two of them have long tenure: Osama Ahmad joined February 2022 and "
         "Momina Raja March 2024. A complete absence of records over two to four years is far "
         "more likely to mean leave is not being logged in Markaz than that no leave was taken. "
         "This is the visibility gap Sabeena described, visible in the data itself \u2014 and it "
         "means <b>this report cannot tell you what these four actually took.</b>"),
        ("<b>Nothing was refused.</b> Every one of the requests on record for these eight was "
         "approved \u2014 no rejections, and nothing left pending. Org-wide in 2026 the pattern is "
         f"the same: of {sum(int(s['reqs']) for s in STATUSES)} requests, "
         f"{next((s['reqs'] for s in STATUSES if s['status']=='rejected'), '0')} were rejected. "
         "Approval is close to automatic, which is what \u201ctrust-based\u201d has come to mean in "
         "practice."),
        ("<b>Approvals are frequently recorded after the leave has already begun \u2014 sometimes "
         "after it ended.</b> Marked in red in the tables. Muzzammil Patel's three April "
         "work-from-home days and his 27 April sick day were all approved on 21 May, up to five "
         "weeks later. Rahima Omar's 3 July and 8 July days were both approved on 21 July. Usman "
         "Javed's 23\u201324 October sick leave was approved on 26 October, after he was back. "
         "Nawal Khurram's current leave began on 17 August and was approved on 18 August. Where "
         "approval follows the absence, it is a record-keeping step, not a decision."),
        ("<b>Not one request names a cover person.</b> The <i>backup assignee</i> field is empty on "
         "every record for all eight. Sabeena's \u201cthere's no ownership\u201d is exactly right, and "
         "it is a field Markaz already has but nobody fills."),
        ("<b>No approver left a single comment</b> on any of these requests \u2014 no conditions, no "
         "context, no pushback recorded anywhere."),
        ("<b>Two team leads were away simultaneously for much of late July and August.</b> Usman "
         "Javed (Fundraising) has been on annual leave from 13 July to 21 August, and Muzzammil "
         "Patel (Impact &amp; Policy) on paternity leave from 20 July to 13 August \u2014 both report "
         "to Sabeena. Nawal Khurram's current leave (17\u201321 August) sits inside Usman's, and he "
         "was her previous line manager. This is the concurrency problem from the call, and it "
         "explains the alternate-approver gap: for five weeks, the people who would normally "
         "approve were themselves away."),
        ("<b>Rahima Omar's pattern is work-from-home, not leave</b> \u2014 8 WFH days against 6 days "
         "of annual leave, all single days, and six of the eight give a hybrid working arrangement "
         "as the reason (\u201cHybrid work agreement\u201d, \u201cHybrid work nature\u201d, \u201cHybrid work "
         "situation\u201d). Worth clarifying: if she has an agreed hybrid arrangement then filing each "
         "day as an exception is noise in the system; if she does not, the reason needs correcting. "
         "Either way it is an administrative question, not a conduct one."),
        ("<b>Hamdan Ahmad has no record of any kind</b> \u2014 no leave, no WFH \u2014 since joining on "
         "22 June 2026. Given the call flagged him as not coming on-site, note what this means "
         "precisely: <b>Markaz holds no evidence either way.</b> Days away from the office without "
         "a WFH request simply are not captured anywhere in this system, so absence of records is "
         "not evidence of attendance."),
    ]
    for i, f in enumerate(findings, 1):
        story.append(Paragraph(f, BODY, bulletText=f"{i}."))
        story.append(Spacer(1, 4))

    # ---- per person
    for label in ORDER:
        entries = [(u, n, p, r) for (u, n, p, r) in PEOPLE[label]]
        story.append(PageBreak())
        lv = sum(totals(r)[0] for _, _, _, r in entries)
        wf = sum(totals(r)[1] for _, _, _, r in entries)
        nr = sum(len(r) for _, _, _, r in entries)
        story.append(person_banner(label, entries[0][1], entries[0][2], lv, wf, nr))
        story.append(Spacer(1, 5))
        for uid, note, prof, rs in entries:
            if len(entries) > 1:
                story.append(Paragraph(
                    f'<font size="8.4" color="#34495e"><b>{note or uid}</b> '
                    f'\u2014 {prof["email"] if prof else uid}</font>', TC))
                story.append(Spacer(1, 3))
            if rs:
                story.append(request_table(rs))
            else:
                story.append(Paragraph(
                    '<font color="#c62828"><b>No leave or WFH records in Markaz.</b></font> '
                    'This is an absence of data, not evidence that no leave was taken.', BODY))
            story.append(Spacer(1, 6))

    # ---- org context
    story.append(PageBreak())
    story.append(Paragraph("Org-wide context — 2026 to date", H1))
    story.append(Paragraph(
        "Sabeena asked for an objective org-wide view and Ayesha confirmed it had never been run. "
        "This is the first cut: approved leave working days per person in 2026 to 19 August, by "
        "department, counting only staff who have at least one record. Departments where nobody "
        "logs leave are invisible here, which is itself the finding.", BODY))
    story.append(Spacer(1, 6))
    rows = [[Paragraph(x, TH) for x in
             ["Department", "Staff with records", "Avg leave days per person", "Highest individual"]]]
    for r in ORG:
        rows.append([Paragraph(r["department"], TC), Paragraph(str(r["n"]), TC),
                     Paragraph(str(r["avg_days"]), TC), Paragraph(str(r["max_days"]), TC)])
    t = Table(rows, colWidths=[80*mm, 40*mm, 55*mm, 40*mm], repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), NAVY),
                           ("ALIGN", (1, 0), (-1, -1), "CENTER"),
                           ("TOPPADDING", (0, 0), (-1, -1), 4),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                           ("ROWBACKGROUNDS", (0, 1), (-1, -1),
                            [colors.white, colors.HexColor("#f5f7fa")])]))
    story.append(t)
    story.append(Spacer(1, 8))
    srows = [[Paragraph(x, TH) for x in ["Status", "Requests", "Working days"]]]
    for s in STATUSES:
        srows.append([Paragraph(s["status"], TC), Paragraph(str(s["reqs"]), TC),
                      Paragraph(str(s["wd"]), TC)])
    st = Table(srows, colWidths=[60*mm, 45*mm, 45*mm], repeatRows=1)
    st.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), NAVY),
                            ("ALIGN", (1, 0), (-1, -1), "CENTER"),
                            ("TOPPADDING", (0, 0), (-1, -1), 4),
                            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                            ("ROWBACKGROUNDS", (0, 1), (-1, -1),
                             [colors.white, colors.HexColor("#f5f7fa")])]))
    story.append(Paragraph("All 2026 requests by status", H1))
    story.append(st)
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "<b>Limits of this report.</b> It reflects what is in Markaz and nothing else. It cannot "
        "see leave taken but never logged, days worked from home without a request, or attendance "
        "in the office \u2014 which is why four of the eight appear to have taken nothing at all. "
        "Public holidays are not in the database, so working-day figures run slightly high. And "
        "because approval is near-automatic and often retroactive, an \u201capproved\u201d status here "
        "should be read as \u201crecorded\u201d rather than as a decision someone made in advance.", NOTE))

    doc.build(story)
    return OUT_PDF


def main():
    pw = os.getenv("EMAIL_PASSWORD")
    if not pw:
        raise SystemExit("EMAIL_PASSWORD missing")
    path = build()
    import fitz
    d = fitz.open(path)
    txt = "".join(p.get_text() for p in d)
    for label in ORDER:
        assert label in txt, f"MISSING: {label}"
    print(f"PDF: {path}\n  pages={len(d)} size={os.path.getsize(path):,}B chars={len(txt):,}")
    print("  all 8 named people present; requests pulled live from Markaz")
    print("  NOTE: structural check only - no PDF viewer here (CLAUDE.md Rule 14)")

    body = (
        "Hi Ayesha,\n\n"
        "Leave and WFH report for the eight names, attached. Pulled live from Markaz, full "
        "history per person with no date cut-off - every request, its dates, working-day length, "
        "whether it was approved, by whom and when, notice given, whether a cover person was "
        "named, and the reason.\n\n"
        "Four things worth knowing before you read it:\n\n"
        "1. Four of the eight have NO records at all - Hamdan, Momina, Osama and Taimoor. Osama "
        "has been here since Feb 2022 and Momina since Mar 2024, so this almost certainly means "
        "leave is not being logged, not that none was taken. The report says so rather than "
        "showing them as zero.\n\n"
        "2. Nothing was ever refused. Every request on record was approved, and org-wide in 2026 "
        "only 8 of 1,153 requests were rejected.\n\n"
        "3. Approvals are often recorded after the leave started, sometimes after it ended - "
        "flagged in red. Muzzammil's April days were approved on 21 May.\n\n"
        "4. Not one request names a cover person. The field exists in Markaz and is empty on all "
        "of them - which is Sabeena's 'no ownership' point exactly.\n\n"
        "I have also included the first org-wide cut by department, which is the analysis Sabeena "
        "asked for and that had never been run.\n\n"
        "Please eyeball the layout before this goes anywhere - I have no PDF viewer here, so I "
        "can only verify the contents structurally, not how the pages look. It is landscape.\n\n"
        "One caution: leave types are not equivalent. Muzzammil's longest block is paternity "
        "leave and Usman's is wedding grant - both entitlements. I have not ranked anyone by raw "
        "days and would not recommend doing so.\n\n"
        "Coco")
    msg = MIMEMultipart()
    msg["Subject"] = SUBJECT
    msg["From"] = SENDER
    msg["To"] = ", ".join(RECIPIENTS)
    msg.attach(MIMEText(body, "plain"))
    with open(path, "rb") as fh:
        att = MIMEApplication(fh.read(), _subtype="pdf")
    att.add_header("Content-Disposition", "attachment", filename=os.path.basename(path))
    msg.attach(att)
    s = smtplib.SMTP("smtp.gmail.com", 587)
    s.starttls()
    s.login(SENDER, pw)
    safe_sendmail(s, SENDER, RECIPIENTS, msg.as_string(), context="leave_report_named_staff")
    s.quit()
    print(f"Sent to {RECIPIENTS}")


if __name__ == "__main__":
    main()
