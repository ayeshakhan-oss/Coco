"""
Job 36 — Field Coordinator, Research & Impact Studies
Decision Brief v2 — Current pipeline state (April 2026)
Pilot: Ayesha + Jawwad
"""

import os, sys, io, smtplib
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                 PageBreak, HRFlowable, Table, TableStyle,
                                 KeepTogether)
from scripts.utils.safe_send import safe_sendmail, allow_candidate_addresses

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../..", ".env"))

EMAIL_USER     = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
REPORT_PATH    = "c:/Agent Coco/output/Job36_Decision_Brief_v2.pdf"
PILOT_TO       = "ayesha.khan@taleemabad.com"
PILOT_CC       = "jawwad.ali@taleemabad.com"

POSITION  = "Field Coordinator, Research & Impact Studies"
BUDGET    = "PKR 200,000 – 250,000"

# ── PIPELINE STATE ────────────────────────────────────────────────────────────

OFFERS_OUT = [
    {"app_id": 1950, "name": "Jalal Ud Din",       "score": "8.3", "salary": "120,000",         "note": "Offer extended. Awaiting response."},
    {"app_id": 1430, "name": "Scheherazade Noor",  "score": "8.0", "salary": "150,000–175,000",  "note": "Offer extended. Awaiting response."},
    {"app_id": 1903, "name": "Muhammad Abubakr",   "score": "7.4", "salary": "250,000",          "note": "Over budget. Offer extended with negotiation."},
    {"app_id": 2017, "name": "Shazmina",            "score": "—",   "salary": "200,000",          "note": "Offer extended. Awaiting response."},
]

VALUES_PASS = [
    {"app_id": 1518, "name": "Zubair Hussain",     "score": "9.4", "salary": "220,000",         "note": "Strong values. Over budget. Decision pending."},
    {"app_id": 1700, "name": "Asad Farooq",        "score": "8.5", "salary": "140,000",         "note": "Values cleared. Within budget. Awaiting right-seat decision."},
    {"app_id": 1755, "name": "Usman Ahmed Khan",   "score": "8.1", "salary": "160,000",         "note": "Values cleared. Within budget."},
    {"app_id": 1857, "name": "Amina Batool",       "score": "7.4", "salary": "300,000–310,000", "note": "Values cleared. Over budget."},
    {"app_id": 1808, "name": "Mehwish",            "score": "7.0", "salary": "200,000",         "note": "Values cleared. Within budget."},
]

VALUES_FAIL = [
    {"app_id": 1602, "name": "Asif Khan",           "score": "10.0", "salary": "250,000", "note": "Highest CV score. Did not clear values."},
    {"app_id": 1442, "name": "Faryal Afridi",       "score": "8.1",  "salary": "100,000", "note": "Values failed."},
    {"app_id": 1789, "name": "Muhammad Omer Khan",  "score": "8.0",  "salary": "155,000", "note": "Values failed."},
    {"app_id": 1624, "name": "Muhammad Siddique",   "score": "7.9",  "salary": "120,000", "note": "Values failed."},
]

VALUES_PENDING = [
    {"app_id": 1720, "name": "Jawad Khan",      "score": "9.3", "salary": "200,000", "note": "Values interview not yet completed."},
    {"app_id": 1658, "name": "Fatima Razzaq",   "score": "9.1", "salary": "185,999", "note": "Values interview not yet completed."},
    {"app_id": 1864, "name": "Fatima Mughal",   "score": "8.8", "salary": "170,000", "note": "Values interview not yet completed."},
    {"app_id": 1839, "name": "HabibunNabi",     "score": "8.6", "salary": "80,000",  "note": "Values interview not yet completed."},
    {"app_id": 1513, "name": "Ali Zia",         "score": "8.1", "salary": "As per budget", "note": "Values interview not yet completed."},
]


# ── PDF ───────────────────────────────────────────────────────────────────────

BLUE   = colors.HexColor("#1565c0")
GREEN  = colors.HexColor("#2e7d32")
RED    = colors.HexColor("#c62828")
AMBER  = colors.HexColor("#e65100")
LGREY  = colors.HexColor("#f5f5f5")
DGREY  = colors.HexColor("#424242")


def build_pdf():
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
                             leftMargin=18*mm, rightMargin=18*mm,
                             topMargin=18*mm, bottomMargin=18*mm)
    styles = getSampleStyleSheet()

    H1   = ParagraphStyle("H1",   fontSize=20, textColor=BLUE,  spaceAfter=4,  alignment=TA_CENTER, fontName="Helvetica-Bold")
    H2   = ParagraphStyle("H2",   fontSize=13, textColor=BLUE,  spaceAfter=6,  fontName="Helvetica-Bold")
    BODY = ParagraphStyle("BODY", fontSize=9,  leading=14,      spaceAfter=4,  alignment=TA_JUSTIFY)
    SMLL = ParagraphStyle("SMLL", fontSize=8,  textColor=colors.HexColor("#666666"), leading=12)
    WARN = ParagraphStyle("WARN", fontSize=9,  textColor=RED,   spaceAfter=4)

    story = []

    # Cover
    story.append(Spacer(1, 20*mm))
    story.append(Paragraph("Hiring Decision Brief", H1))
    story.append(Paragraph(POSITION, ParagraphStyle("sub", fontSize=12, textColor=DGREY, alignment=TA_CENTER, spaceAfter=2)))
    story.append(Paragraph("April 2026 &nbsp;·&nbsp; Pipeline Status", ParagraphStyle("sub2", fontSize=10, textColor=colors.grey, alignment=TA_CENTER, spaceAfter=12)))
    story.append(HRFlowable(width="100%", thickness=1, color=BLUE, spaceAfter=12))

    # Stat row
    stat_data = [[
        Paragraph(f"<b><font size=20 color='#1565c0'>{len(OFFERS_OUT)}</font></b><br/><font size=8 color='grey'>Offers Out</font>", styles["Normal"]),
        Paragraph(f"<b><font size=20 color='#2e7d32'>{len(VALUES_PASS)}</font></b><br/><font size=8 color='grey'>Values Cleared</font>", styles["Normal"]),
        Paragraph(f"<b><font size=20 color='#e65100'>{len(VALUES_PENDING)}</font></b><br/><font size=8 color='grey'>Pending Values</font>", styles["Normal"]),
        Paragraph(f"<b><font size=20 color='#c62828'>{len(VALUES_FAIL)}</font></b><br/><font size=8 color='grey'>Values Failed</font>", styles["Normal"]),
    ]]
    stat_table = Table(stat_data, colWidths=[42*mm]*4)
    stat_table.setStyle(TableStyle([
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0,0), (-1,-1), [LGREY]),
        ("BOX", (0,0), (-1,-1), 0.5, colors.HexColor("#dddddd")),
        ("INNERGRID", (0,0), (-1,-1), 0.5, colors.HexColor("#dddddd")),
        ("TOPPADDING", (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
    ]))
    story.append(stat_table)
    story.append(Spacer(1, 10*mm))

    # Budget note
    story.append(Paragraph(f"<b>Budget:</b> {BUDGET}", BODY))
    story.append(Spacer(1, 6*mm))

    def candidate_table(candidates, header_color):
        rows = [["#", "Name", "CV Score", "Expected Salary", "Note"]]
        for i, c in enumerate(candidates, 1):
            rows.append([
                str(i),
                c["name"],
                c["score"],
                c["salary"],
                c["note"],
            ])
        t = Table(rows, colWidths=[8*mm, 45*mm, 20*mm, 38*mm, 56*mm])
        style = [
            ("BACKGROUND", (0,0), (-1,0), header_color),
            ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
            ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
            ("FONTSIZE",   (0,0), (-1,-1), 8),
            ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, LGREY]),
            ("GRID", (0,0), (-1,-1), 0.4, colors.HexColor("#cccccc")),
            ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
            ("TOPPADDING", (0,0), (-1,-1), 5),
            ("BOTTOMPADDING", (0,0), (-1,-1), 5),
            ("ALIGN", (2,0), (3,-1), "CENTER"),
        ]
        t.setStyle(TableStyle(style))
        return t

    # Section: Offers Out
    story.append(KeepTogether([
        Paragraph("Offers Extended", H2),
        HRFlowable(width="100%", thickness=0.5, color=BLUE, spaceAfter=6),
        candidate_table(OFFERS_OUT, BLUE),
        Spacer(1, 6*mm),
    ]))

    # Section: Values Cleared
    story.append(KeepTogether([
        Paragraph("Values Cleared — Awaiting Decision", H2),
        HRFlowable(width="100%", thickness=0.5, color=GREEN, spaceAfter=6),
        candidate_table(VALUES_PASS, GREEN),
        Spacer(1, 6*mm),
    ]))

    # Section: Pending Values
    story.append(KeepTogether([
        Paragraph("Values Interview Pending", H2),
        HRFlowable(width="100%", thickness=0.5, color=AMBER, spaceAfter=6),
        candidate_table(VALUES_PENDING, AMBER),
        Spacer(1, 6*mm),
    ]))

    # Section: Values Failed
    story.append(KeepTogether([
        Paragraph("Values Failed — Out of Pipeline", H2),
        HRFlowable(width="100%", thickness=0.5, color=RED, spaceAfter=6),
        candidate_table(VALUES_FAIL, RED),
        Spacer(1, 4*mm),
        Paragraph("These candidates will not proceed regardless of CV strength.", SMLL),
    ]))

    doc.build(story)
    buf.seek(0)
    return buf.read()


def build_html():
    def stat(val, label, color):
        return f"""<td style="padding:12px 20px;background:#f9f9f9;border-radius:4px;text-align:center;border:1px solid #e0e0e0;">
  <strong style="font-size:26px;color:{color};">{val}</strong><br>
  <span style="font-size:11px;color:#666;">{label}</span>
</td>"""

    rows36 = lambda lst, color: "".join(
        f"<tr style='background:{'#f9f9f9' if i%2==0 else '#fff'};'>"
        f"<td style='padding:6px 10px;font-weight:bold;color:{color};'>{i+1}</td>"
        f"<td style='padding:6px 10px;'>{c['name']}</td>"
        f"<td style='padding:6px 10px;text-align:center;'>{c['score']}</td>"
        f"<td style='padding:6px 10px;'>{c['salary']}</td>"
        f"<td style='padding:6px 10px;color:#555;font-size:12px;'>{c['note']}</td>"
        f"</tr>"
        for i, c in enumerate(lst)
    )

    table_head = """<tr style="background:#1565c0;color:#fff;">
      <th style="padding:8px 10px;">#</th>
      <th style="padding:8px 10px;text-align:left;">Name</th>
      <th style="padding:8px 10px;">CV Score</th>
      <th style="padding:8px 10px;text-align:left;">Salary Ask</th>
      <th style="padding:8px 10px;text-align:left;">Note</th>
    </tr>"""

    def section(title, color, candidates):
        return f"""
<h3 style="color:{color};margin:28px 0 8px;border-bottom:2px solid {color};padding-bottom:4px;">{title}</h3>
<table width="100%" cellpadding="0" cellspacing="0" style="border-collapse:collapse;font-size:13px;">
  {table_head}
  {rows36(candidates, color)}
</table>"""

    return f"""
<html><body style="font-family:Arial,sans-serif;font-size:14px;color:#222;max-width:700px;margin:auto;">
<div style="background:#1565c0;padding:22px 28px;border-radius:6px 6px 0 0;">
  <h2 style="color:#fff;margin:0;">Hiring Decision Brief</h2>
  <p style="color:#bbdefb;margin:4px 0 0;">{POSITION} &nbsp;·&nbsp; April 2026</p>
</div>
<div style="padding:24px 28px;background:#fff;border:1px solid #ddd;">
  <p>Hi Ayesha,</p>
  <p>Here is the current pipeline status for <strong>{POSITION}</strong>. PDF attached for full view.</p>
  <table cellpadding="0" cellspacing="8" style="margin:16px 0;">
    <tr>
      {stat(len(OFFERS_OUT), 'Offers Out', '#1565c0')}
      <td width="8"></td>
      {stat(len(VALUES_PASS), 'Values Cleared', '#2e7d32')}
      <td width="8"></td>
      {stat(len(VALUES_PENDING), 'Pending Values', '#e65100')}
      <td width="8"></td>
      {stat(len(VALUES_FAIL), 'Values Failed', '#c62828')}
    </tr>
  </table>
  <p style="font-size:12px;color:#555;"><strong>Budget:</strong> {BUDGET}</p>

  {section('Offers Extended', '#1565c0', OFFERS_OUT)}
  {section('Values Cleared — Awaiting Decision', '#2e7d32', VALUES_PASS)}
  {section('Values Interview Pending', '#e65100', VALUES_PENDING)}
  {section('Values Failed — Out', '#c62828', VALUES_FAIL)}
</div>
<div style="padding:10px 28px;background:#eee;font-size:11px;color:#666;">
  Taleemabad Talent Acquisition · hiring@taleemabad.com
</div>
</body></html>"""


def main():
    print("Building Job 36 Decision Brief v2...")
    pdf = build_pdf()
    with open(REPORT_PATH, "wb") as f:
        f.write(pdf)
    print(f"PDF saved: {REPORT_PATH} ({len(pdf):,} bytes)")

    msg = MIMEMultipart("mixed")
    msg["Subject"] = f"[PILOT] Job 36 Decision Brief — {POSITION} | Pipeline Update"
    msg["From"]    = EMAIL_USER
    msg["To"]      = PILOT_TO
    msg["CC"]      = PILOT_CC

    msg.attach(MIMEText(build_html(), "html", "utf-8"))

    pdf_part = MIMEBase("application", "pdf")
    pdf_part.set_payload(pdf)
    encoders.encode_base64(pdf_part)
    pdf_part.add_header("Content-Disposition", "attachment", filename="Job36_Decision_Brief_v2.pdf")
    msg.attach(pdf_part)

    recipients = [PILOT_TO, PILOT_CC]
    allow_candidate_addresses(recipients)
    import smtplib
    with smtplib.SMTP("smtp.gmail.com", 587) as s:
        s.ehlo(); s.starttls(); s.login(EMAIL_USER, EMAIL_PASSWORD)
        safe_sendmail(s, EMAIL_USER, recipients, msg.as_string(), context="job36_decision_brief_v2")
    print(f"Sent to {PILOT_TO} (CC: {PILOT_CC})")


if __name__ == "__main__":
    main()
