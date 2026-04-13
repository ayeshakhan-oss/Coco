"""
Job 35 — Junior Research Associate, Impact & Policy
Decision Brief — Pipeline Status (April 2026)
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
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                 PageBreak, HRFlowable, Table, TableStyle,
                                 KeepTogether)
from scripts.utils.safe_send import safe_sendmail, allow_candidate_addresses

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../..", ".env"))

EMAIL_USER     = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
REPORT_PATH    = "c:/Agent Coco/output/Job35_Decision_Brief.pdf"
PILOT_TO       = "ayesha.khan@taleemabad.com"
PILOT_CC       = "jawwad.ali@taleemabad.com"

POSITION = "Junior Research Associate, Impact & Policy"
BUDGET   = "PKR 150,000 – 200,000"

# ── PIPELINE STATE ────────────────────────────────────────────────────────────
# Budget note: Nain Tara salary ask PKR 55,000 — well below budget. Verify this is correct.
# Mariam Rehman has 2 apps (1944 + 1945); deduplicated — using app 1944 (correct salary 120k).

VALUES_PASS = [
    {"app_id": 1534, "name": "Nain Tara",      "score": "8.6", "salary": "55,000",   "budget": "IN",  "note": "Values cleared. Salary ask unusually low — verify before offer."},
    {"app_id": 1558, "name": "Hadiyah Shaheen","score": "8.4", "salary": "90–100k",  "budget": "IN",  "note": "Values cleared. Within budget."},
    {"app_id": 1949, "name": "Maria Malik",    "score": "7.8", "salary": "70,000",   "budget": "IN",  "note": "Values cleared. Within budget."},
]

VALUES_FAIL = [
    {"app_id": 1569, "name": "Rabia Zafar",  "score": "9.4", "salary": "125,000", "budget": "IN",  "note": "Highest CV score in cohort. Did not clear values. Out of pipeline."},
    {"app_id": 1663, "name": "Zeeshan Ali",  "score": "9.0", "salary": "100,000", "budget": "IN",  "note": "Strong CV. Did not clear values. Out of pipeline."},
    {"app_id": 1445, "name": "Faryal Afridi", "score": "9.5", "salary": "100,000", "budget": "IN",  "note": "Highest AI score. Values interview done (host: Jawwad). proceedToRightSeat: No. Status now updated to rejected."},
]

VALUES_PENDING = [
    {"app_id": 1771, "name": "Wasif Mehdi",       "score": "9.1", "salary": "100,000", "budget": "IN",   "note": "Values interview not yet completed."},
    {"app_id": 1550, "name": "Ali Muhammad",      "score": "8.9", "salary": "120,000", "budget": "IN",   "note": "Values interview not yet completed."},
    {"app_id": 1456, "name": "Shahid Kamal",      "score": "8.6", "salary": "150,000", "budget": "IN",   "note": "Values interview not yet completed."},
    {"app_id": 1944, "name": "Mariam Rehman",     "score": "8.5", "salary": "120,000", "budget": "IN",   "note": "Values interview not yet completed."},
    {"app_id": 1774, "name": "Fatima Tu Zahra",   "score": "8.3", "salary": "70–80k",  "budget": "IN",   "note": "Values interview not yet completed."},
    {"app_id": 1878, "name": "Rameez Wasif",      "score": "8.0", "salary": "130,000", "budget": "IN",   "note": "Values interview not yet completed."},
    {"app_id": 1947, "name": "Daniyah Noor",      "score": "7.5", "salary": "120,000", "budget": "IN",   "note": "Values interview not yet completed."},
    {"app_id": 1821, "name": "Ayesha Nadeem",     "score": "7.0", "salary": "70,000",  "budget": "IN",   "note": "Values interview not yet completed."},
]


# ── PDF ───────────────────────────────────────────────────────────────────────

BLUE  = colors.HexColor("#1565c0")
GREEN = colors.HexColor("#2e7d32")
RED   = colors.HexColor("#c62828")
AMBER = colors.HexColor("#e65100")
LGREY = colors.HexColor("#f5f5f5")
DGREY = colors.HexColor("#424242")


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

    story = []

    story.append(Spacer(1, 20*mm))
    story.append(Paragraph("Hiring Decision Brief", H1))
    story.append(Paragraph(POSITION, ParagraphStyle("sub", fontSize=12, textColor=DGREY, alignment=TA_CENTER, spaceAfter=2)))
    story.append(Paragraph("April 2026 &nbsp;·&nbsp; Values Stage", ParagraphStyle("sub2", fontSize=10, textColor=colors.grey, alignment=TA_CENTER, spaceAfter=12)))
    story.append(HRFlowable(width="100%", thickness=1, color=BLUE, spaceAfter=12))

    # Stats
    stat_data = [[
        Paragraph(f"<b><font size=20 color='#2e7d32'>{len(VALUES_PASS)}</font></b><br/><font size=8 color='grey'>Values Cleared</font>", styles["Normal"]),
        Paragraph(f"<b><font size=20 color='#e65100'>{len(VALUES_PENDING)}</font></b><br/><font size=8 color='grey'>Pending Values</font>", styles["Normal"]),
        Paragraph(f"<b><font size=20 color='#c62828'>{len(VALUES_FAIL)}</font></b><br/><font size=8 color='grey'>Values Failed</font>", styles["Normal"]),
        Paragraph(f"<b><font size=20 color='#1565c0'>{len(VALUES_PASS)+len(VALUES_PENDING)+len(VALUES_FAIL)}</font></b><br/><font size=8 color='grey'>Total Pipeline</font>", styles["Normal"]),
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
    story.append(Spacer(1, 6*mm))
    story.append(Paragraph(f"<b>Budget:</b> {BUDGET} &nbsp;·&nbsp; <b>Status:</b> Values stage in progress. No case study issued yet.", BODY))
    story.append(Spacer(1, 6*mm))

    def candidate_table(candidates, header_color):
        rows = [["#", "Name", "CV Score", "Salary Ask", "Note"]]
        for i, c in enumerate(candidates, 1):
            rows.append([str(i), c["name"], c["score"], c["salary"], c["note"]])
        t = Table(rows, colWidths=[8*mm, 42*mm, 20*mm, 30*mm, 66*mm])
        t.setStyle(TableStyle([
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
        ]))
        return t

    story.append(KeepTogether([
        Paragraph("Values Cleared — Ready for Next Stage", H2),
        HRFlowable(width="100%", thickness=0.5, color=GREEN, spaceAfter=6),
        candidate_table(VALUES_PASS, GREEN),
        Spacer(1, 3*mm),
        Paragraph("These three candidates have cleared values. Ready for case study or right-seat decision.", SMLL),
        Spacer(1, 8*mm),
    ]))

    story.append(KeepTogether([
        Paragraph("Values Interview Pending", H2),
        HRFlowable(width="100%", thickness=0.5, color=AMBER, spaceAfter=6),
        candidate_table(VALUES_PENDING, AMBER),
        Spacer(1, 3*mm),
        Paragraph("8 candidates shortlisted with values interview not yet completed. Wasif Mehdi (9.1) leads this group.", SMLL),
        Spacer(1, 8*mm),
    ]))

    story.append(KeepTogether([
        Paragraph("Values Failed — Out of Pipeline", H2),
        HRFlowable(width="100%", thickness=0.5, color=RED, spaceAfter=6),
        candidate_table(VALUES_FAIL, RED),
        Spacer(1, 3*mm),
        Paragraph("Note: Faryal Afridi (9.5) was the highest AI-scored candidate and also did not clear values (host: Jawwad, 2 Apr). Rabia Zafar (9.4) and Zeeshan Ali (9.0) also out. All three rejection emails pending.", SMLL),
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

    def rows_html(lst, color):
        out = ""
        for i, c in enumerate(lst):
            bg = "#f9f9f9" if i % 2 == 0 else "#fff"
            out += (f"<tr style='background:{bg};'>"
                    f"<td style='padding:6px 10px;font-weight:bold;color:{color};'>{i+1}</td>"
                    f"<td style='padding:6px 10px;'>{c['name']}</td>"
                    f"<td style='padding:6px 10px;text-align:center;'>{c['score']}</td>"
                    f"<td style='padding:6px 10px;'>{c['salary']}</td>"
                    f"<td style='padding:6px 10px;color:#555;font-size:12px;'>{c['note']}</td>"
                    f"</tr>")
        return out

    thead = """<tr style="background:#1565c0;color:#fff;">
      <th style="padding:8px 10px;">#</th><th style="padding:8px 10px;text-align:left;">Name</th>
      <th style="padding:8px 10px;">Score</th><th style="padding:8px 10px;text-align:left;">Salary Ask</th>
      <th style="padding:8px 10px;text-align:left;">Note</th></tr>"""

    def section(title, color, lst):
        return f"""
<h3 style="color:{color};margin:28px 0 8px;border-bottom:2px solid {color};padding-bottom:4px;">{title}</h3>
<table width="100%" cellpadding="0" cellspacing="0" style="border-collapse:collapse;font-size:13px;">
  {thead}{rows_html(lst, color)}</table>"""

    return f"""
<html><body style="font-family:Arial,sans-serif;font-size:14px;color:#222;max-width:700px;margin:auto;">
<div style="background:#1565c0;padding:22px 28px;border-radius:6px 6px 0 0;">
  <h2 style="color:#fff;margin:0;">Hiring Decision Brief</h2>
  <p style="color:#bbdefb;margin:4px 0 0;">{POSITION} &nbsp;·&nbsp; April 2026 · Values Stage</p>
</div>
<div style="padding:24px 28px;background:#fff;border:1px solid #ddd;">
  <p>Hi Ayesha,</p>
  <p>Here is the current pipeline status for <strong>{POSITION}</strong>. PDF attached with full view.</p>
  <table cellpadding="0" cellspacing="8" style="margin:16px 0;"><tr>
    {stat(len(VALUES_PASS), 'Values Cleared', '#2e7d32')}
    <td width="8"></td>
    {stat(len(VALUES_PENDING), 'Pending Values', '#e65100')}
    <td width="8"></td>
    {stat(len(VALUES_FAIL), 'Values Failed', '#c62828')}
    <td width="8"></td>
    {stat(len(VALUES_PASS)+len(VALUES_PENDING)+len(VALUES_FAIL), 'Total Pipeline', '#1565c0')}
  </tr></table>
  <p style="font-size:12px;color:#555;"><strong>Budget:</strong> {BUDGET} &nbsp;·&nbsp; Values stage in progress. No case study issued yet.</p>
  {section('Values Cleared — Ready for Next Stage', '#2e7d32', VALUES_PASS)}
  {section('Values Interview Pending', '#e65100', VALUES_PENDING)}
  {section('Values Failed — Out', '#c62828', VALUES_FAIL)}
</div>
<div style="padding:10px 28px;background:#eee;font-size:11px;color:#666;">
  Taleemabad Talent Acquisition · hiring@taleemabad.com
</div>
</body></html>"""


def main():
    print("Building Job 35 Decision Brief...")
    pdf = build_pdf()
    with open(REPORT_PATH, "wb") as f:
        f.write(pdf)
    print(f"PDF saved: {REPORT_PATH} ({len(pdf):,} bytes)")

    msg = MIMEMultipart("mixed")
    msg["Subject"] = f"[PILOT] Job 35 Decision Brief — {POSITION} | Pipeline Update"
    msg["From"]    = EMAIL_USER
    msg["To"]      = PILOT_TO
    msg["CC"]      = PILOT_CC

    msg.attach(MIMEText(build_html(), "html", "utf-8"))

    pdf_part = MIMEBase("application", "pdf")
    pdf_part.set_payload(pdf)
    encoders.encode_base64(pdf_part)
    pdf_part.add_header("Content-Disposition", "attachment", filename="Job35_Decision_Brief.pdf")
    msg.attach(pdf_part)

    recipients = [PILOT_TO, PILOT_CC]
    allow_candidate_addresses(recipients)
    with smtplib.SMTP("smtp.gmail.com", 587) as s:
        s.ehlo(); s.starttls(); s.login(EMAIL_USER, EMAIL_PASSWORD)
        safe_sendmail(s, EMAIL_USER, recipients, msg.as_string(), context="job35_decision_brief_pilot")
    print(f"Sent to {PILOT_TO} (CC: {PILOT_CC})")


if __name__ == "__main__":
    main()
