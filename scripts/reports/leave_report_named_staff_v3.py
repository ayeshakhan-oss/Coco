"""
Leave Report v3 — 8 named staff ONLY. Ayesha 2026-08-19.

Her correction: v2 was wrong. She did not ask for the org-wide catalogue of every leave type,
the entitlement/discretionary analysis, the org context or the data-quality pages. She asked
for these eight people only: which type of leave they took, when they took it, and a total
count. Nothing else.

So v3 is: summary table (totals per person) + one small table per person listing each leave
with its dates, type and days. Approval status kept because "were they approved or not" was
part of the original ask.

Kept (both are facts, not padding): the four people with no records at all are shown as such
rather than as zero, and Nawal's two user records are combined.

Formatting per memory/attendance_report_complete_template.md - slate headers, alternating row
fills, NO GRID LINES.
No PDF viewer here -> structural verification only (CLAUDE.md Rule 14).
"""

import os
import smtplib
import sys
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests
from dotenv import load_dotenv
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, KeepTogether, PageTemplate,
                               Paragraph, Spacer, Table, TableStyle)

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from scripts.utils.safe_send import safe_sendmail  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
load_dotenv(os.path.join(ROOT, ".env"))
URL = os.environ["DATABASE_URL"]
HOST = URL.split("@")[1].split("/")[0]

SENDER = "ayesha.khan@taleemabad.com"
RECIPIENTS = ["ayesha.khan@taleemabad.com"]
SUBJECT = "[PILOT - ] Leave Report - 8 named staff | as at 19 August 2026"
OUT_PDF = os.path.join(ROOT, "output", "reports", "Leave_Report_8_Staff_2026-08-19.pdf")

TARGETS = {
    "user-1751134210030-cast609wa": ("Muhammad Usman Javed", ""),
    "user-1767619173370-k06b07avk": ("Muhammad Muzzammil Patel", ""),
    "user-1777985545895-r5avvx2xr": ("Rahima Omar", ""),
    "user-1784531629947-rhid5j0rj": ("Nawal Khurram", "current account"),
    "user-1752813207085-r82vkp1ys": ("Nawal Khurram", "older account"),
    "user-1783805300065-dxzh6ey44": ("Taimoor Abdullah", ""),
    "user-1781766933165-6bennbn5a": ("Hamdan Ahmad", ""),
    "user-1751134178503-lxckgoywv": ("Momina Raja", ""),
    "user-1751134200553-okyuusi6c": ("Osama Ahmad", ""),
}
ORDER = ["Muhammad Usman Javed", "Muhammad Muzzammil Patel", "Rahima Omar", "Nawal Khurram",
         "Taimoor Abdullah", "Hamdan Ahmad", "Momina Raja", "Osama Ahmad"]

LABEL = {
    ("annual", "me-time"): "Annual leave",
    ("annual", "big-day"): "Annual - big day",
    ("annual", "(unset)"): "Annual leave",
    ("medical", "under-weather"): "Sick leave",
    ("medical", "family-support"): "Family care",
    ("medical", "mental-health"): "Mental health",
    ("medical", "paternity"): "Paternity leave",
    ("medical", "maternity"): "Maternity leave",
    ("medical", "(unset)"): "Sick leave",
    ("grant", "wedding"): "Wedding leave",
    ("grant", "religious"): "Religious leave",
    ("grant", "education"): "Study leave",
    ("grant", "dragon"): "Grant - 1 day",
    ("grant", "sabbatical"): "Sabbatical",
    ("grant", "(unset)"): "Grant leave",
    ("work_from_home", "wfh"): "Work from home",
    ("Time-Off", "(unset)"): "Time off",
}

TODAY = "2026-08-19"
# booked = whole request; taken = only days up to and including today. Two people are mid-leave
# right now (Usman to 21 Aug, Nawal to 21 Aug) so counting booked days as taken overstates them.
WD = ("(SELECT count(*) FROM generate_series(lr.start_date, lr.end_date, '1 day') d "
      "WHERE extract(isodow FROM d) < 6)")
WD_TAKEN = (f"(SELECT count(*) FROM generate_series(lr.start_date, "
            f"least(lr.end_date,'{TODAY}'::date), '1 day') d WHERE extract(isodow FROM d) < 6)")


def q(sql, params=None):
    r = requests.post(f"https://{HOST}/sql",
                      headers={"Neon-Connection-String": URL, "Content-Type": "application/json"},
                      json={"query": sql, "params": params or []}, timeout=120)
    r.raise_for_status()
    return r.json()["rows"]


IDS = list(TARGETS)
PROFILES = q("""SELECT u.id, ep.department, ep.job_title, ep.joining_date::date::text AS joined
FROM users u LEFT JOIN employee_profiles ep ON ep.user_id=u.id WHERE u.id = ANY($1)""", [IDS])
REQS = q(f"""
SELECT lr.user_id, lr.leave_type, COALESCE(lr.sub_category,'(unset)') AS sub_category,
       lr.is_half_day, lr.start_date::text AS start_d, lr.end_date::text AS end_d,
       {WD} AS days, {WD_TAKEN} AS days_taken,
       (lr.end_date > '{TODAY}'::date) AS ongoing, lr.status
FROM leave_requests lr
WHERE lr.user_id = ANY($1) AND (lr.end_date - lr.start_date) BETWEEN 0 AND 365
ORDER BY lr.start_date""", [IDS])

SLATE = colors.HexColor("#34495e")
L_ORANGE = colors.HexColor("#ffe0b2")
L_BLUE = colors.HexColor("#e3f2fd")
GREY = colors.HexColor("#6b7a90")

FONTS = r"C:\Windows\Fonts"
for nm, fn in [("Georgia", "georgia.ttf"), ("Georgia-Bold", "georgiab.ttf"),
               ("Georgia-Italic", "georgiai.ttf")]:
    pdfmetrics.registerFont(TTFont(nm, os.path.join(FONTS, fn)))
pdfmetrics.registerFontFamily("Georgia", normal="Georgia", bold="Georgia-Bold",
                              italic="Georgia-Italic")

BODY = ParagraphStyle("b", fontName="Georgia", fontSize=9.4, leading=14, alignment=TA_JUSTIFY,
                      textColor=colors.HexColor("#22303f"))
NOTE = ParagraphStyle("n", fontName="Georgia-Italic", fontSize=8.6, leading=12.5,
                      alignment=TA_JUSTIFY, textColor=colors.HexColor("#5a4632"))
H1 = ParagraphStyle("h", fontName="Georgia-Bold", fontSize=12.5, leading=16, textColor=SLATE,
                    spaceBefore=4, spaceAfter=6)
NAME = ParagraphStyle("nm", fontName="Georgia-Bold", fontSize=10.5, leading=14,
                      textColor=colors.white)
TC = ParagraphStyle("tc", fontName="Georgia", fontSize=8.6, leading=12)
TH = ParagraphStyle("th", fontName="Georgia-Bold", fontSize=8.4, leading=11,
                    textColor=colors.white)


def nogrid(rows, widths, tint, repeat=1, align_from=1):
    t = Table(rows, colWidths=widths, repeatRows=repeat)
    st = [("BACKGROUND", (0, 0), (-1, repeat - 1), SLATE),
          ("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("ALIGN", (align_from, 0), (-1, -1), "CENTER"),
          ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
          ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 7)]
    for i in range(repeat, len(rows)):
        if (i - repeat) % 2 == 1:
            st.append(("BACKGROUND", (0, i), (-1, i), tint))
    t.setStyle(TableStyle(st))
    return t


def rows_for(label):
    ids = [u for u, (l, _) in TARGETS.items() if l == label]
    return [r for r in REQS if r["user_id"] in ids]


def leave_only(rs):
    return [r for r in rs if r["leave_type"] != "work_from_home"]


def wfh_only(rs):
    return [r for r in rs if r["leave_type"] == "work_from_home"]


def days(rs, field="days_taken"):
    return sum(int(r[field]) for r in rs if r["status"] == "approved")


def type_summary(rs):
    agg = {}
    for r in rs:
        if r["status"] != "approved":
            continue
        k = LABEL.get((r["leave_type"], r["sub_category"]), r["sub_category"])
        agg[k] = agg.get(k, 0) + int(r["days_taken"])
    return ", ".join(f"{k} {v}d" for k, v in sorted(agg.items(), key=lambda x: -x[1])) or "—"


def summary_table():
    rows = [[Paragraph(x, TH) for x in ["Person", "Leaves<br/>taken", "Leave days<br/>so far",
                                        "Booked<br/>total", "WFH<br/>days",
                                        "Types of leave taken"]]]
    for lab in ORDER:
        rs = rows_for(lab)
        lv, wf = leave_only(rs), wfh_only(rs)
        if not rs:
            rows.append([Paragraph(lab, TC)] +
                        [Paragraph('<font color="#c62828">0</font>', TC) for _ in range(4)] +
                        [Paragraph('<font color="#c62828">No leave recorded in Markaz</font>', TC)])
        else:
            taken, booked = days(lv), days(lv, "days")
            bk = (f'<font color="#f57c00"><b>{booked}</b></font>' if booked != taken
                  else str(booked))
            rows.append([Paragraph(lab, TC), Paragraph(f"<b>{len(lv)}</b>", TC),
                         Paragraph(f"<b>{taken}</b>", TC), Paragraph(bk, TC),
                         Paragraph(str(days(wf)) if wf else "0", TC),
                         Paragraph(type_summary(lv), TC)])
    return nogrid(rows, [43 * mm, 16 * mm, 20 * mm, 18 * mm, 15 * mm, 61 * mm], L_ORANGE)


def detail_table(rs):
    rows = [[Paragraph(x, TH) for x in ["When", "Type of leave", "Days", "Approved?"]]]
    for r in rs:
        when = (r["start_d"] if r["start_d"] == r["end_d"]
                else f'{r["start_d"]}  to  {r["end_d"]}')
        lab = LABEL.get((r["leave_type"], r["sub_category"]), r["sub_category"])
        if r["is_half_day"]:
            lab += " (half day)"
        col = {"approved": "#2e7a4f", "pending": "#f57c00",
               "rejected": "#c62828"}.get(r["status"], "#6b7a90")
        dcell = str(r["days"])
        if r["ongoing"]:
            dcell = (f'{r["days_taken"]} so far'
                     f'<br/><font size="7" color="#f57c00">of {r["days"]} booked</font>')
        rows.append([Paragraph(when, TC), Paragraph(lab, TC), Paragraph(dcell, TC),
                     Paragraph(f'<font color="{col}">{r["status"].title()}</font>', TC)])
    tint = L_BLUE if rs and rs[0]["leave_type"] == "work_from_home" else L_ORANGE
    return nogrid(rows, [58 * mm, 62 * mm, 20 * mm, 33 * mm], tint)


def person_bar(label, rs, prof):
    lv, wf = leave_only(rs), wfh_only(rs)
    meta = " · ".join(x for x in [prof.get("department") if prof else None,
                                  prof.get("job_title") if prof else None] if x)
    txt = (f'<b>{label}</b><font size="8.4">'
           f'   ·   {len(lv)} leave(s), {days(lv)} days'
           + (f'   ·   {days(wf)} WFH days' if wf else '') + '</font>')
    t = Table([[Paragraph(txt, NAME)]] + ([[Paragraph(
        f'<font size="7.6" color="#dfe6ef">{meta}</font>', TC)]] if meta else []),
        colWidths=[173 * mm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), SLATE),
                           ("LEFTPADDING", (0, 0), (-1, -1), 8),
                           ("TOPPADDING", (0, 0), (-1, 0), 5),
                           ("BOTTOMPADDING", (0, -1), (-1, -1), 5),
                           ("BOTTOMPADDING", (0, 0), (-1, 0), 1),
                           ("TOPPADDING", (0, -1), (-1, -1), 0)]))
    return t


def header_footer(canvas, doc):
    canvas.saveState()
    w, h = A4
    canvas.setFillColor(SLATE)
    canvas.rect(0, h - 22 * mm, w, 22 * mm, stroke=0, fill=1)
    canvas.setFillColor(colors.HexColor("#aebccd"))
    canvas.setFont("Georgia", 7.2)
    canvas.drawString(19 * mm, h - 9 * mm, "PEOPLE & CULTURE  ·  LEAVE REPORT")
    canvas.setFillColor(colors.white)
    canvas.setFont("Georgia-Bold", 12.5)
    canvas.drawString(19 * mm, h - 15.5 * mm, "Leave Report — 8 Staff")
    canvas.setFillColor(colors.HexColor("#c3d0e6"))
    canvas.setFont("Georgia", 7.6)
    canvas.drawRightString(w - 19 * mm, h - 15.5 * mm, "Markaz  ·  19 August 2026")
    canvas.setFillColor(GREY)
    canvas.setFont("Georgia", 7)
    canvas.drawString(19 * mm, 9 * mm, "Confidential — People & Culture")
    canvas.drawRightString(w - 19 * mm, 9 * mm, f"Page {canvas.getPageNumber()}")
    canvas.restoreState()


def build():
    os.makedirs(os.path.dirname(OUT_PDF), exist_ok=True)
    doc = BaseDocTemplate(OUT_PDF, pagesize=A4, leftMargin=19 * mm, rightMargin=19 * mm,
                          topMargin=28 * mm, bottomMargin=16 * mm,
                          title="Leave Report - 8 staff (19 Aug 2026)",
                          author="Taleemabad People & Culture")
    doc.addPageTemplates([PageTemplate(id="a", frames=[
        Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height)], onPage=header_footer)])

    story = [Paragraph("Summary", H1), summary_table(), Spacer(1, 5),
             Paragraph('<font size="8" color="#6b7a90">Days are working days (Mon–Fri). '
                       '<b>Leave days so far</b> counts only days up to and including today; '
                       '<b>booked total</b> includes days still to come, shown in orange where '
                       'the two differ — Usman Javed and Nawal Khurram are both on leave until '
                       '21 August. Work-from-home is separate and not counted as leave.</font>',
                       TC), Spacer(1, 12),
             Paragraph("Leave by person", H1)]

    for lab in ORDER:
        rs = rows_for(lab)
        prof = next((p for p in PROFILES if p["id"] in
                     [u for u, (l, _) in TARGETS.items() if l == lab]), None)
        block = [person_bar(lab, rs, prof), Spacer(1, 4)]
        lv, wf = leave_only(rs), wfh_only(rs)
        if not rs:
            block.append(Paragraph(
                '<font color="#c62828"><b>No leave recorded in Markaz.</b></font>', BODY))
        else:
            if lv:
                block.append(detail_table(lv))
            if wf:
                block += [Spacer(1, 4), Paragraph(
                    '<font size="8" color="#1565c0"><b>Work from home</b></font>', TC),
                    Spacer(1, 2), detail_table(wf)]
        block.append(Spacer(1, 11))
        story.append(KeepTogether(block))

    story.append(Paragraph(
        "<b>Three notes.</b> (1) Hamdan Ahmad, Taimoor Abdullah, Momina Raja and Osama Ahmad have "
        "no leave records in Markaz at all. Osama joined in February 2022 and Momina in March "
        "2024, so this most likely means their leave was never logged rather than that none was "
        "taken. Nawal Khurram's two entries come from her two user accounts and are combined "
        "above. (2) Markaz holds no public-holiday calendar, so any gazetted holiday falling "
        "inside a leave block is still counted as a leave day here. Muzzammil Patel's 12–24 June "
        "block is the one to check against the official holiday list. (3) Muzzammil's paternity "
        "figure is independently corroborated — his request asked for 19 working days and the "
        "calculation returns exactly 19.", NOTE))
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
    assert "dragon" not in txt and "ENTITLEMENT" not in txt, "v2 content leaked in"
    print(f"PDF: {path}\n  pages={len(d)} size={os.path.getsize(path):,}B")
    print("  8 people, leave types + dates + totals only")

    body = ("Hi Ayesha,\n\n"
            "Redone - just the eight people, which leave they took, when, and their totals.\n\n"
            "Summary table on page 1, then a small table per person showing each leave with its "
            "date, type and number of days. Work-from-home is listed separately so it is not "
            "counted as leave.\n\n"
            "Dropped everything you did not ask for - no org-wide leave-type catalogue, no "
            "department comparisons, no analysis pages.\n\n"
            "The one thing I kept: Hamdan, Taimoor, Momina and Osama have no leave records at all, "
            "so they show as 'no leave recorded' rather than as zero. Osama has been here since "
            "2022, so it is a logging gap rather than clean attendance.\n\n"
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
    safe_sendmail(s, SENDER, RECIPIENTS, msg.as_string(), context="leave_report_8_staff_v3")
    s.quit()
    print(f"Sent to {RECIPIENTS}")


if __name__ == "__main__":
    main()
