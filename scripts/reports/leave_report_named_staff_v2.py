"""
Leave & WFH Report v2 — 8 named staff, BY LEAVE TYPE (Ayesha, 2026-08-19).

Ayesha: "Can you get me the types of leaves and make a proper report."

v2 vs v1:
  - Full LEAVE TYPE CATALOGUE from Markaz: all 4 leave families + WFH + one legacy type,
    21 type/sub-category combinations, with org-wide usage so the categories are complete
    (including types these eight never used).
  - Every type classified ENTITLEMENT vs DISCRETIONARY, and per-person totals split that way.
    Ranking people on raw days is unfair when the biggest blocks are paternity and wedding leave.
  - Person x type matrix.
  - Formatting moved onto the locked P&C report conventions
    (memory/attendance_report_complete_template.md): #34495e header bars, pastel stat boxes,
    alternating row fills, NO GRID LINES on any table.

DATA QUALITY — 4 records carry typo'd years (42026, 20226, 0026, 2016) which would otherwise
report as millions of days. They are EXCLUDED from all totals and listed for correction.
None belong to the eight named people.

Working days = Mon-Fri. Public holidays are not in Markaz, so figures run slightly high.
WFH lives in leave_requests as leave_type='work_from_home' and is never added to leave days.
No PDF viewer on this machine -> structural verification only (CLAUDE.md Rule 14).
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
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, PageBreak, PageTemplate,
                               Paragraph, Spacer, Table, TableStyle)

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from scripts.utils.safe_send import safe_sendmail  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
load_dotenv(os.path.join(ROOT, ".env"))
URL = os.environ["DATABASE_URL"]
HOST = URL.split("@")[1].split("/")[0]

SENDER = "ayesha.khan@taleemabad.com"
RECIPIENTS = ["ayesha.khan@taleemabad.com"]
SUBJECT = "[PILOT - ] Leave Report by Type - 8 named staff | as at 19 August 2026"
OUT_PDF = os.path.join(ROOT, "output", "reports", "Leave_Report_By_Type_2026-08-19.pdf")
TODAY = date(2026, 8, 19)

TARGETS = {
    "user-1751134210030-cast609wa": ("Muhammad Usman Javed", ""),
    "user-1767619173370-k06b07avk": ("Muhammad Muzzammil Patel", ""),
    "user-1777985545895-r5avvx2xr": ("Rahima Omar", ""),
    "user-1784531629947-rhid5j0rj": ("Nawal Khurram", "active record"),
    "user-1752813207085-r82vkp1ys": ("Nawal Khurram", "archived record, same person"),
    "user-1783805300065-dxzh6ey44": ("Taimoor Abdullah", "Impact & Policy, active"),
    "user-1751134182423-9ceqh7vm3": ("Taimoor Abdullah", "NIETE ICT, archived - different person"),
    "user-1781766933165-6bennbn5a": ("Hamdan Ahmad", ""),
    "user-1751134178503-lxckgoywv": ("Momina Raja", ""),
    "user-1751134200553-okyuusi6c": ("Osama Ahmad", ""),
}
ORDER = ["Muhammad Usman Javed", "Muhammad Muzzammil Patel", "Rahima Omar", "Nawal Khurram",
         "Taimoor Abdullah", "Hamdan Ahmad", "Momina Raja", "Osama Ahmad"]

# (leave_type, sub_category) -> (plain-English meaning, ENTITLEMENT | DISCRETIONARY | NOT LEAVE)
TYPE_MEANING = {
    ("annual", "me-time"): ("General annual leave - the default holiday category", "DISCRETIONARY"),
    ("annual", "big-day"): ("A significant personal occasion", "DISCRETIONARY"),
    ("annual", "birthday"): ("Own birthday", "DISCRETIONARY"),
    ("annual", "beloved-birthday"): ("Birthday of someone close", "DISCRETIONARY"),
    ("annual", "anniversary"): ("Personal anniversary", "DISCRETIONARY"),
    ("annual", "graduation"): ("Graduation ceremony", "DISCRETIONARY"),
    ("annual", "(unset)"): ("Annual leave logged before sub-categories existed", "DISCRETIONARY"),
    ("medical", "under-weather"): ("Ordinary sick leave", "ENTITLEMENT"),
    ("medical", "family-support"): ("Caring for an unwell family member", "ENTITLEMENT"),
    ("medical", "mental-health"): ("Mental-health day", "ENTITLEMENT"),
    ("medical", "maternity"): ("Maternity leave", "ENTITLEMENT"),
    ("medical", "paternity"): ("Paternity leave", "ENTITLEMENT"),
    ("medical", "(unset)"): ("Medical leave logged before sub-categories existed", "ENTITLEMENT"),
    ("grant", "wedding"): ("Own wedding - granted block", "ENTITLEMENT"),
    ("grant", "religious"): ("Religious observance, e.g. Hajj or Umrah", "ENTITLEMENT"),
    ("grant", "education"): ("Study, exams or coursework", "ENTITLEMENT"),
    ("grant", "sabbatical"): ("Extended sabbatical", "ENTITLEMENT"),
    ("grant", "dragon"): ("One-day grant, used 66 times org-wide at exactly 1 day each", "ENTITLEMENT"),
    ("grant", "(unset)"): ("Grant leave logged before sub-categories existed", "ENTITLEMENT"),
    ("work_from_home", "wfh"): ("Working from home - NOT absence", "NOT LEAVE"),
    ("Time-Off", "(unset)"): ("Legacy type, used Jul-Aug 2025 only, now superseded", "DISCRETIONARY"),
}

CLEAN = ("(lr.end_date - lr.start_date) BETWEEN 0 AND 365 "
         "AND lr.start_date >= '2024-01-01' AND lr.end_date <= '2027-06-30'")
WD = ("(SELECT count(*) FROM generate_series(lr.start_date, lr.end_date, '1 day') d "
      "WHERE extract(isodow FROM d) < 6)")


def q(sql, params=None):
    r = requests.post(f"https://{HOST}/sql",
                      headers={"Neon-Connection-String": URL, "Content-Type": "application/json"},
                      json={"query": sql, "params": params or []}, timeout=120)
    r.raise_for_status()
    return r.json()["rows"]


IDS = list(TARGETS)

PROFILES = q("""
SELECT u.id, u.first_name||' '||u.last_name AS name, u.email, u.status, ep.employee_id,
       ep.department, ep.job_title, ep.joining_date::date::text AS joined,
       lm.first_name||' '||lm.last_name AS line_manager
FROM users u LEFT JOIN employee_profiles ep ON ep.user_id=u.id
LEFT JOIN users lm ON ep.line_manager_id=lm.id WHERE u.id = ANY($1)""", [IDS])

REQS = q(f"""
SELECT lr.user_id, lr.id, lr.leave_type, COALESCE(lr.sub_category,'(unset)') AS sub_category,
       lr.is_half_day, lr.start_date::text AS start_d, lr.end_date::text AS end_d,
       (lr.end_date - lr.start_date + 1) AS cal_days, {WD} AS work_days, lr.status,
       ap.first_name||' '||ap.last_name AS approver, lr.approved_at::date::text AS approved_on,
       lr.created_at::date::text AS requested_on,
       (lr.start_date - lr.created_at::date) AS notice_days,
       (lr.approved_at::date - lr.start_date) AS approval_vs_start,
       lr.backup_assignee_id IS NOT NULL AS has_cover, lr.reason
FROM leave_requests lr LEFT JOIN users ap ON ap.id=lr.approver_id
WHERE lr.user_id = ANY($1) AND {CLEAN} ORDER BY lr.start_date""", [IDS])

CATALOGUE = q(f"""
SELECT lr.leave_type, COALESCE(lr.sub_category,'(unset)') AS sub_category,
       count(*) AS requests, count(DISTINCT lr.user_id) AS people, sum({WD}) AS working_days,
       round(avg({WD}),1) AS avg_len, count(*) FILTER (WHERE lr.is_half_day) AS half_days,
       min(lr.start_date)::text AS first_used, max(lr.start_date)::text AS last_used
FROM leave_requests lr WHERE {CLEAN}
GROUP BY 1,2 ORDER BY lr.leave_type, sum({WD}) DESC""")

BAD = q("""
SELECT lr.id, COALESCE(u.first_name||' '||u.last_name,'(unknown)') AS name, lr.leave_type,
       lr.start_date::text AS start_d, lr.end_date::text AS end_d, lr.status
FROM leave_requests lr LEFT JOIN users u ON u.id=lr.user_id
WHERE NOT ((lr.end_date - lr.start_date) BETWEEN 0 AND 365
       AND lr.start_date >= '2024-01-01' AND lr.end_date <= '2027-06-30')
ORDER BY lr.id""")

# ---------------------------------------------------------------- locked P&C palette
SLATE = colors.HexColor("#34495e")
ORANGE = colors.HexColor("#f57c00")
DBLUE = colors.HexColor("#1565c0")
DGREEN = colors.HexColor("#2e7a4f")
DRED = colors.HexColor("#c62828")
DPURPLE = colors.HexColor("#6a1b9a")
GREY = colors.HexColor("#6b7a90")
L_GREY = colors.HexColor("#f5f5f5")
L_GREEN = colors.HexColor("#e8f5e9")
L_ORANGE = colors.HexColor("#ffe0b2")
L_BLUE = colors.HexColor("#e3f2fd")
L_PURPLE = colors.HexColor("#f3e5f5")
L_RED = colors.HexColor("#ffebee")

FONTS = r"C:\Windows\Fonts"
for nm, fn in [("Georgia", "georgia.ttf"), ("Georgia-Bold", "georgiab.ttf"),
               ("Georgia-Italic", "georgiai.ttf"), ("Georgia-BoldItalic", "georgiaz.ttf")]:
    pdfmetrics.registerFont(TTFont(nm, os.path.join(FONTS, fn)))
pdfmetrics.registerFontFamily("Georgia", normal="Georgia", bold="Georgia-Bold",
                              italic="Georgia-Italic", boldItalic="Georgia-BoldItalic")

BODY = ParagraphStyle("b", fontName="Georgia", fontSize=9.2, leading=14, alignment=TA_JUSTIFY,
                      textColor=colors.HexColor("#22303f"))
NOTE = ParagraphStyle("n", fontName="Georgia-Italic", fontSize=8.2, leading=12,
                      alignment=TA_JUSTIFY, textColor=colors.HexColor("#5a4632"))
H1 = ParagraphStyle("h1", fontName="Georgia-Bold", fontSize=13, leading=17, textColor=SLATE,
                    spaceBefore=6, spaceAfter=5)
TC = ParagraphStyle("tc", fontName="Georgia", fontSize=7.8, leading=10.6)
TCS = ParagraphStyle("s", fontName="Georgia", fontSize=7.2, leading=9.8,
                     textColor=colors.HexColor("#3d4c5c"))
TH = ParagraphStyle("th", fontName="Georgia-Bold", fontSize=7.6, leading=10,
                    textColor=colors.white)
SECH = ParagraphStyle("sh", fontName="Georgia-Bold", fontSize=10, leading=13,
                      textColor=colors.white)


def nogrid(rows, widths, header_bg=SLATE, tint=L_GREY, repeat=1, align_from=1):
    """Locked P&C table: header bar, alternating fills, NO GRID LINES."""
    t = Table(rows, colWidths=widths, repeatRows=repeat)
    st = [("BACKGROUND", (0, 0), (-1, repeat - 1), header_bg),
          ("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("ALIGN", (align_from, 0), (-1, -1), "CENTER"),
          ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
          ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6)]
    for i in range(repeat, len(rows)):
        if (i - repeat) % 2 == 1:
            st.append(("BACKGROUND", (0, i), (-1, i), tint))
    t.setStyle(TableStyle(st))
    return t


def section_bar(text, bg, width=267 * mm):
    t = Table([[Paragraph(text, SECH)]], colWidths=[width])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), bg),
                           ("LEFTPADDING", (0, 0), (-1, -1), 8),
                           ("TOPPADDING", (0, 0), (-1, -1), 5),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
    return t


def wd(r):
    return int(r["work_days"])


def person_reqs(label):
    out = []
    for uid, (lab, note) in TARGETS.items():
        if lab == label:
            out.append((uid, note, next((p for p in PROFILES if p["id"] == uid), None),
                        [r for r in REQS if r["user_id"] == uid]))
    return out


def klass(r):
    return TYPE_MEANING.get((r["leave_type"], r["sub_category"]), ("", "DISCRETIONARY"))[1]


def split_days(rs):
    ent = sum(wd(r) for r in rs if r["status"] == "approved" and klass(r) == "ENTITLEMENT")
    dis = sum(wd(r) for r in rs if r["status"] == "approved" and klass(r) == "DISCRETIONARY")
    wfh = sum(wd(r) for r in rs if r["status"] == "approved" and klass(r) == "NOT LEAVE")
    return ent, dis, wfh


def stat_boxes():
    tot_e = tot_d = tot_w = 0
    nreq = 0
    for lab in ORDER:
        for _, _, _, rs in person_reqs(lab):
            e, d, w = split_days(rs)
            tot_e += e; tot_d += d; tot_w += w; nreq += len(rs)
    zero = sum(1 for lab in ORDER if not any(rs for _, _, _, rs in person_reqs(lab)))
    boxes = [(str(nreq), "Requests on record", L_GREY),
             (str(tot_d), "Discretionary leave days", L_ORANGE),
             (str(tot_e), "Entitlement leave days", L_GREEN),
             (str(tot_w), "WFH days", L_BLUE),
             (f"{(tot_d+tot_e)/5:.1f}", "Leave weeks total", L_PURPLE),
             (str(zero), "People with NO records", L_RED)]
    cells = []
    for n, l, bg in boxes:
        inner = Table([[Paragraph(f'<font size="17"><b>{n}</b></font>', TC)],
                       [Paragraph(f'<font size="6.6">{l.upper()}</font>', TC)]],
                      colWidths=[41 * mm])
        inner.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), bg),
                                   ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                                   ("TOPPADDING", (0, 0), (-1, 0), 7),
                                   ("BOTTOMPADDING", (0, 0), (-1, 0), 1),
                                   ("TOPPADDING", (0, -1), (-1, -1), 0),
                                   ("BOTTOMPADDING", (0, -1), (-1, -1), 7)]))
        cells.append(inner)
    outer = Table([cells], colWidths=[44.5 * mm] * 6)
    outer.setStyle(TableStyle([("ALIGN", (0, 0), (-1, -1), "CENTER"),
                               ("LEFTPADDING", (0, 0), (-1, -1), 0),
                               ("RIGHTPADDING", (0, 0), (-1, -1), 3)]))
    return outer


def catalogue_table():
    fam_col = {"annual": ORANGE, "medical": DGREEN, "grant": DPURPLE,
               "work_from_home": DBLUE, "Time-Off": GREY}
    rows = [[Paragraph(x, TH) for x in ["Leave type", "Sub-category", "What it is",
                                        "Class", "Reqs", "People", "Working<br/>days",
                                        "Avg<br/>length", "Half-day<br/>reqs", "Last used"]]]
    for c in CATALOGUE:
        key = (c["leave_type"], c["sub_category"])
        meaning, cls = TYPE_MEANING.get(key, ("(not documented)", "?"))
        col = fam_col.get(c["leave_type"], GREY)
        ccol = {"ENTITLEMENT": "#2e7a4f", "DISCRETIONARY": "#f57c00",
                "NOT LEAVE": "#1565c0"}.get(cls, "#6b7a90")
        rows.append([
            Paragraph(f'<font color="{col.hexval()}"><b>{c["leave_type"]}</b></font>', TCS),
            Paragraph(c["sub_category"], TCS), Paragraph(meaning, TCS),
            Paragraph(f'<font color="{ccol}"><b>{cls}</b></font>', TCS),
            Paragraph(str(c["requests"]), TCS), Paragraph(str(c["people"]), TCS),
            Paragraph(f'<b>{c["working_days"]}</b>', TCS), Paragraph(str(c["avg_len"]), TCS),
            Paragraph(str(c["half_days"]), TCS), Paragraph(c["last_used"], TCS)])
    return nogrid(rows, [24 * mm, 26 * mm, 74 * mm, 24 * mm, 14 * mm, 15 * mm,
                         17 * mm, 15 * mm, 17 * mm, 20 * mm], align_from=3)


def matrix_table():
    combos = []
    for lab in ORDER:
        for _, _, _, rs in person_reqs(lab):
            for r in rs:
                k = (r["leave_type"], r["sub_category"])
                if k not in combos:
                    combos.append(k)
    combos.sort(key=lambda k: (k[0] != "annual", k[0] != "medical", k[0], k[1]))
    head = [Paragraph("Person", TH)] + [
        Paragraph(f'{a}<br/><font size="6.2">{b}</font>', TH) for a, b in combos] + [
        Paragraph("Leave<br/>total", TH), Paragraph("WFH", TH)]
    rows = [head]
    for lab in ORDER:
        allrs = [r for _, _, _, rs in person_reqs(lab) for r in rs]
        cells = [Paragraph(lab, TC)]
        for k in combos:
            days = sum(wd(r) for r in allrs
                       if (r["leave_type"], r["sub_category"]) == k and r["status"] == "approved")
            cells.append(Paragraph(f"<b>{days}</b>" if days else
                                   '<font color="#b8c0cc">-</font>', TC))
        e, d, w = split_days(allrs)
        cells.append(Paragraph(f"<b>{e+d}</b>", TC))
        cells.append(Paragraph(str(w) if w else '<font color="#b8c0cc">-</font>', TC))
        rows.append(cells)
    widths = [46 * mm] + [(200 * mm - 46 * mm) / (len(combos) + 2)] * (len(combos) + 2)
    return nogrid(rows, widths)


def request_table(rs):
    rows = [[Paragraph(x, TH) for x in
             ["#", "Dates", "Cal /<br/>work", "Type", "Sub-category", "Class", "Status",
              "Approver", "Approved", "Notice", "Cover", "Reason given"]]]
    for r in rs:
        cls = klass(r)
        ccol = {"ENTITLEMENT": "#2e7a4f", "DISCRETIONARY": "#f57c00",
                "NOT LEAVE": "#1565c0"}[cls]
        dates = (r["start_d"] if r["start_d"] == r["end_d"]
                 else f'{r["start_d"]}<br/>to {r["end_d"]}')
        appr = r["approved_on"] or "-"
        if r["approval_vs_start"] is not None and int(r["approval_vs_start"]) > 0:
            appr = (f'<font color="#c62828">{appr}<br/>'
                    f'<font size="6">+{r["approval_vs_start"]}d late</font></font>')
        rows.append([
            Paragraph(str(r["id"]), TCS), Paragraph(dates, TCS),
            Paragraph(f'{r["cal_days"]} / <b>{r["work_days"]}</b>', TCS),
            Paragraph(r["leave_type"].replace("_", " "), TCS),
            Paragraph(r["sub_category"] + (" · half day" if r["is_half_day"] else ""), TCS),
            Paragraph(f'<font color="{ccol}"><b>{cls.split()[0]}</b></font>', TCS),
            Paragraph(r["status"], TCS), Paragraph(r["approver"] or "-", TCS),
            Paragraph(appr, TCS), Paragraph(str(r["notice_days"]), TCS),
            Paragraph("yes" if r["has_cover"] else '<font color="#c62828">no</font>', TCS),
            Paragraph((r["reason"] or "-")[:170], TCS)])
    return nogrid(rows, [8 * mm, 23 * mm, 14 * mm, 20 * mm, 26 * mm, 18 * mm, 16 * mm,
                         22 * mm, 20 * mm, 12 * mm, 11 * mm, 77 * mm], align_from=2)


def header_footer(canvas, doc):
    canvas.saveState()
    w, h = landscape(A4)
    canvas.setFillColor(SLATE)
    canvas.rect(0, h - 20 * mm, w, 20 * mm, stroke=0, fill=1)
    canvas.setFillColor(colors.HexColor("#aebccd"))
    canvas.setFont("Georgia", 7)
    canvas.drawString(15 * mm, h - 8 * mm, "PEOPLE & CULTURE  ·  LEAVE REPORT BY TYPE")
    canvas.setFillColor(colors.white)
    canvas.setFont("Georgia-Bold", 12)
    canvas.drawString(15 * mm, h - 14 * mm, "Leave & Work-From-Home by Type — 8 named staff")
    canvas.setFillColor(colors.HexColor("#c3d0e6"))
    canvas.setFont("Georgia", 7.6)
    canvas.drawRightString(w - 15 * mm, h - 14 * mm, "Source: Markaz  ·  as at 19 August 2026")
    canvas.setFillColor(GREY)
    canvas.setFont("Georgia", 7)
    canvas.drawString(15 * mm, 7.5 * mm, "Confidential — People & Culture")
    canvas.drawRightString(w - 15 * mm, 7.5 * mm, f"Page {canvas.getPageNumber()}")
    canvas.restoreState()


def build():
    os.makedirs(os.path.dirname(OUT_PDF), exist_ok=True)
    doc = BaseDocTemplate(OUT_PDF, pagesize=landscape(A4), leftMargin=15 * mm,
                          rightMargin=15 * mm, topMargin=25 * mm, bottomMargin=14 * mm,
                          title="Leave Report by Type - 8 named staff (19 Aug 2026)",
                          author="Taleemabad People & Culture")
    doc.addPageTemplates([PageTemplate(id="all", frames=[
        Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height)], onPage=header_footer)])

    story = [stat_boxes(), Spacer(1, 10)]
    story += [Paragraph(
        "Every leave and work-from-home record Markaz holds for the eight people named, broken "
        "down by leave type, with no date cut-off. <b>The single most important thing in this "
        "report is that leave types are not equivalent.</b> Paternity, maternity, sick leave, "
        "wedding, religious and study leave are <b>entitlements</b> \u2014 people are supposed to take "
        "them, and a large number against those categories is not a performance signal. Annual "
        "leave is <b>discretionary</b>. Work-from-home is <b>not absence at all</b>. Each is "
        "counted and coloured separately throughout, and no one is ranked on a combined total.", BODY),
        Spacer(1, 8)]

    story += [Paragraph("1 · Leave types in Markaz — the full catalogue", H1),
              Paragraph(
        "All 21 type and sub-category combinations that exist in the system, including those "
        "these eight have never used, with org-wide usage so you can see what each category is "
        "actually for. Four families (annual, medical, grant, work-from-home) plus one legacy "
        "type. The <i>(unset)</i> rows are requests filed before sub-categories were introduced "
        "\u2014 92 of them, all before October 2025.", BODY), Spacer(1, 5),
              catalogue_table(), Spacer(1, 10)]

    story += [PageBreak(),
              Paragraph("2 · Who took what — person by leave type", H1),
              Paragraph(
        "Working days per person per category. Dashes mean no record of that type. "
        "<b>Leave total excludes work-from-home.</b>", BODY), Spacer(1, 5),
              matrix_table(), Spacer(1, 9)]

    ent_note = []
    for lab in ORDER:
        allrs = [r for _, _, _, rs in person_reqs(lab) for r in rs]
        e, d, w = split_days(allrs)
        if e or d:
            ent_note.append(f"<b>{lab}</b>: {d} discretionary, {e} entitlement")
    story += [Paragraph("<b>Read that split before drawing conclusions.</b> " +
                        "; ".join(ent_note) + ".", NOTE), Spacer(1, 8)]

    story += [Paragraph("3 · What the type breakdown shows", H1)]
    findings = [
        ("<b>Usman Javed's 58 days are not one thing.</b> 31 days are discretionary annual leave "
         "(<i>me-time</i>), 25 are a wedding grant, and 2 are sick leave. The wedding block is an "
         "entitlement. The 31 discretionary days across two requests \u2014 one of them the 13 July "
         "to 21 August block he is on now \u2014 are the part that is genuinely a management "
         "question, and they sit alongside an appraisal already under discussion."),
        ("<b>Muzzammil Patel's 29 days are almost entirely entitlement.</b> 19 days paternity for "
         "the birth of his first child, 1 day sick, and 9 days annual leave, which he spent "
         "running health camps in Gilgit-Baltistan for a foundation he set up. His 4 work-from-home "
         "days cite a three-hour daily commute caused by construction. There is no discretionary "
         "concern visible here at all."),
        ("<b>Rahima Omar's pattern is work-from-home, not leave</b> \u2014 8 WFH days against 6 days of "
         "annual leave. Six of her eight WFH requests give a hybrid working arrangement as the "
         "reason. If that arrangement exists, filing each day as an exception is noise in the "
         "system; if it does not, the reason needs correcting. Administrative, not conduct."),
        ("<b>Nawal Khurram has 9 days, all annual leave</b>, split across her two user records \u2014 "
         "4 days in October 2025 on the archived account and 5 days now (17\u201321 August) on the "
         "active one. Neither record alone tells you that."),
        ("<b>Four of the eight have no records of any type.</b> Hamdan Ahmad (joined June 2026), "
         "Taimoor Abdullah in Impact &amp; Policy, Momina Raja (joined March 2024) and Osama Ahmad "
         "(joined February 2022). Two to four years with not one leave, sick day or WFH request is "
         "far more likely to mean leave is not being logged than that none was taken. "
         "<b>For these four the report cannot tell you what they took.</b>"),
        ("<b>Org-wide, the categories tell you what the culture actually uses.</b> Annual "
         "<i>me-time</i> dominates (515 requests, 138 people, 1,243 days) and ordinary sick leave "
         "is second (434 requests, 129 people). Notably, <b>mental-health leave has been used 51 "
         "times by 33 people</b> \u2014 the category is real and people use it. Study leave is mostly "
         "half-days (29 of 84 requests). The longest categories are maternity (avg 67 days), "
         "sabbatical (avg 23) and wedding (avg 18)."),
        ("<b>Nothing was refused, in any category.</b> Every request on record for these eight was "
         "approved. Org-wide in 2026 only 8 requests out of 1,153 were rejected."),
        ("<b>Approvals are often recorded after the leave began</b> \u2014 marked red. Muzzammil's "
         "April work-from-home days and his 27 April sick day were all approved on 21 May. "
         "Rahima's 3 and 8 July days were both approved on 21 July. Usman's October sick leave was "
         "approved after he returned. \u201cApproved\u201d here means recorded, not decided in advance."),
        ("<b>Not one request in any category names a cover person.</b> The backup-assignee field "
         "exists in Markaz and is empty on every record for all eight."),
    ]
    for i, f in enumerate(findings, 1):
        story += [Paragraph(f, BODY, bulletText=f"{i}."), Spacer(1, 4)]

    # per person
    for lab in ORDER:
        entries = person_reqs(lab)
        story.append(PageBreak())
        allrs = [r for _, _, _, rs in entries for r in rs]
        e, d, w = split_days(allrs)
        prof = entries[0][2]
        sub = []
        if prof:
            sub = [x for x in [prof.get("department"), prof.get("job_title"),
                               f'joined {prof["joined"]}' if prof.get("joined") else None,
                               f'LM {prof["line_manager"]}' if prof.get("line_manager") else None,
                               None if prof.get("status") == "active" else (prof.get("status") or "").upper()]
                   if x]
        story.append(section_bar(
            f'<b>{lab}</b><font size="8">   ·   {len(allrs)} request(s)   ·   '
            f'{d} discretionary + {e} entitlement = <b>{e+d}</b> leave days '
            f'({(e+d)/5:.1f} weeks)   ·   {w} WFH days</font>', SLATE))
        if sub:
            story.append(Paragraph(f'<font size="7.6" color="#6b7a90">{" · ".join(sub)}</font>', TC))
        story.append(Spacer(1, 5))
        for uid, note, prof2, rs in entries:
            if len(entries) > 1:
                story.append(Paragraph(
                    f'<font size="8.2" color="#34495e"><b>{note}</b> \u2014 '
                    f'{prof2["email"] if prof2 else uid}</font>', TC))
                story.append(Spacer(1, 3))
            if rs:
                story.append(request_table(rs))
            else:
                story.append(Paragraph(
                    '<font color="#c62828"><b>No records of any leave type in Markaz.</b></font> '
                    'This is an absence of data, not evidence that no leave was taken.', BODY))
            story.append(Spacer(1, 6))

    # data quality
    story.append(PageBreak())
    story.append(Paragraph("4 · Data quality — needs fixing in Markaz", H1))
    story.append(Paragraph(
        "Four records carry mistyped years. Left in, they would report as millions of days and "
        "make any type-level total meaningless \u2014 the raw <i>annual/me-time</i> figure comes out at "
        "4.7 million working days because of two of them. They are excluded from every number in "
        "this report and should be corrected at source. None belong to the eight named people.", BODY))
    story.append(Spacer(1, 5))
    rows = [[Paragraph(x, TH) for x in ["Record", "Person", "Type", "Start", "End", "Status",
                                        "What is wrong"]]]
    fixes = {1532: "End year typed 42026", 952: "End year typed 20226",
             1078: "Start year typed 0026", 1015: "Start year typed 2016, should be 2026"}
    for b in BAD:
        rows.append([Paragraph(str(b["id"]), TCS), Paragraph(b["name"], TCS),
                     Paragraph(b["leave_type"].replace("_", " "), TCS),
                     Paragraph(b["start_d"], TCS), Paragraph(b["end_d"], TCS),
                     Paragraph(b["status"], TCS),
                     Paragraph(fixes.get(b["id"], "Out of plausible range"), TCS)])
    story.append(nogrid(rows, [16 * mm, 40 * mm, 30 * mm, 28 * mm, 28 * mm, 24 * mm, 90 * mm]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "<b>Three further limits.</b> Working days are Monday to Friday; public holidays are not "
        "in Markaz, so every figure runs slightly high. Nawal Khurram's history is split across "
        "two user records and any per-person view reading only one will undercount her \u2014 worth "
        "merging. And two different people are called Taimoor Abdullah; the Impact &amp; Policy "
        "colleague named in the call has no records, while the archived NIETE ICT employee has "
        "one from July 2025.", NOTE))

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
    for lab in ORDER:
        assert lab in txt, f"MISSING {lab}"
    for t in ["me-time", "paternity", "under-weather", "wedding", "mental-health", "dragon",
              "sabbatical", "work from home"]:
        assert t in txt, f"MISSING type {t}"
    assert "ENTITLEMENT" in txt and "DISCRETIONARY" in txt
    print(f"PDF: {path}\n  pages={len(d)} size={os.path.getsize(path):,}B chars={len(txt):,}")
    print(f"  catalogue rows={len(CATALOGUE)}  corrupt records listed={len(BAD)}")
    print("  all 8 people + all leave types present; entitlement/discretionary split applied")
    print("  NOTE: structural check only - no PDF viewer here (CLAUDE.md Rule 14)")

    body = (
        "Hi Ayesha,\n\n"
        "Leave report by type, attached - rebuilt properly.\n\n"
        "What is new versus yesterday's version:\n\n"
        "1. The full leave-type catalogue from Markaz - all 21 type/sub-category combinations "
        "including ones these eight never used, with what each one is for and how the whole org "
        "uses it. Four families (annual, medical, grant, WFH) plus one legacy type.\n\n"
        "2. Every type classified ENTITLEMENT vs DISCRETIONARY, and each person's days split that "
        "way. This matters: Muzzammil's 29 days are 19 paternity + 1 sick + 9 annual, so almost "
        "all entitlement. Usman's 58 are 31 discretionary annual + 25 wedding grant + 2 sick. "
        "Ranking people on a combined total would be misleading and I have not done it.\n\n"
        "3. A person-by-type matrix so you can see the pattern at a glance.\n\n"
        "4. A data-quality page. Four records have mistyped years (42026, 20226, 0026, 2016). "
        "Left in, annual me-time reports as 4.7 MILLION working days. They are excluded here and "
        "need correcting at source - none belong to your eight.\n\n"
        "Formatting follows the locked P&C report conventions - pastel stat boxes, slate headers, "
        "no grid lines.\n\n"
        "Unchanged and still the biggest caveat: four of the eight (Hamdan, Taimoor, Momina, "
        "Osama) have no records of any type, two of them with 2-4 years' tenure. That is almost "
        "certainly a logging gap, so the report cannot tell you what they took.\n\n"
        "Please eyeball the layout before it goes anywhere - landscape, and I have no PDF viewer "
        "here so I can only verify contents structurally, not appearance.\n\n"
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
    safe_sendmail(s, SENDER, RECIPIENTS, msg.as_string(), context="leave_report_by_type_v2")
    s.quit()
    print(f"Sent to {RECIPIENTS}")


if __name__ == "__main__":
    main()
