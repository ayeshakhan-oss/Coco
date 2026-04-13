"""I-10 Head Office Attendance Record — 9 April 2026 (Markaz + Teams integrated)"""
import os, sys, smtplib, io
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from scripts.utils.safe_send import safe_sendmail, allow_candidate_addresses

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, KeepTogether)

load_dotenv(os.path.join(os.path.dirname(__file__), "../..", ".env"))

EMAIL_USER     = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
DATE = "9 April 2026 (Thursday)"

# Onsite list from user's sheet (with full Markaz names matched)
ONSITE = [
    "Salman Iqbal", "Osama Ahmad", "Ramsha Khurshid", "Aroma Tahir", "Abdul Rehman Siddiqi",
    "Muhammad Kamal", "Hassan Shahzad", "Saleh Muhammad", "Fatima Rahman", "Mah Noor",
    "Haya Abid", "Sheikh Nimra Rasheed", "Mahrah Ashraf", "Muhammad Saim", "Rifat Yasmeen",
    "Umama Gul Siddiqui", "QURAT UL AIN", "Muhammad Umar Raza", "Afifa Sultana", "Haroon Ali",
    "Saima Bibi", "Zunaira Shahid", "Mahnoor Shafique", "Taloot Ahmad Malik", "Ahsan Javed",
    "Zeshan Ali", "Jawwad Ali", "Ayesha Raza Khan", "Javariya Mufarrakh", "Muhammad Talha",
    "Usman Imtiaz", "Muhammad Hammad Sarfraz", "Muhammad Zain ul Abadin", "Jahanzeb Ahmad",
    "Hamza Shahid", "Shoaib Ud Din", "Saad Zahid", "Muhammad Usman Mughal", "Hataf Bin Atif",
    "Amena Ahmed", "Abdur Rehman", "Muhammad Zeeshan Usaid", "Hareem Fatima", "Ramisha Riaz Sheikh",
    "Laraib Sarfraz", "Sabeen Fatima", "Muhammad Jalal Khan", "Muhammad Raees Shujaan Azhar",
    "Muhammad Haris", "Samra Tariq", "Babar Khan", "Zeeshan Zahoor", "Shoaib Ud Din",
    "Ahmed Javed", "Muhammad Omer Mazhar Rana",  # Added: Ahmed Javed + Omer Rana
]

# Markaz approved leave for 09-04-2026 (including those expected onsite but have approved leave)
ON_LEAVE = [
    ("Mavia ", "OPL", "Annual", "Leave approved on Markaz (Annual)"),
    ("Muhammad Danish Iqbal", "OPL", "Grant", "Leave approved on Markaz (Grant)"),
    ("Salman Ahmad", "OPL", "Grant", "Leave approved on Markaz (Grant)"),
    ("Shumaila Aslam", "OPL", "Annual", "Leave approved on Markaz (Annual)"),
    ("Syed Junaid Ali Zaidi", "OPL", "Medical", "Leave approved on Markaz (Medical)"),
    ("Tariq Asim", "OPL", "Grant", "Leave approved on Markaz (Grant)"),
    ("Rida Nayyab", "OPL", "Unspecified", "Mentioned on Teams: On leave"),
]

# Teams Presence updates (not on Markaz leave)
WFH_NO_MARKAZ = [
    ("Iqra Zanib", "OPL", "Remote", "Not feeling well — joined remotely via Teams"),
    ("Fatima Khan", "OPL", "WFH", "Not feeling well — left to WFH via Teams"),
]

# Remote/Out of office (Teams)
REMOTE = [
    ("Kamran Taj", "OPL", "H-9", "Working from H-9 — mentioned on Teams"),
]

# Out of office (Teams)
OUT_OF_OFFICE = [
    ("Mashhood Ali Rastgar", "OPL", "Training", "Out of office — conducting training in Lahore"),
]

# Arriving late (Teams)
PARTIAL = [
    ("Muhammad Omer Mazhar Rana", "OPL", "Late", "Running a bit late — mentioned on Teams"),
]

FLAGGED = []

# Calculate counts
ONSITE_COUNT = len([n for n in ONSITE if n not in [ln[0] for ln in ON_LEAVE] + [w[0] for w in WFH_NO_MARKAZ] + [r[0] for r in REMOTE] + [o[0] for o in OUT_OF_OFFICE] + [p[0] for p in PARTIAL]])
ON_LEAVE_CNT = len(ON_LEAVE)
WFH_CNT      = len(WFH_NO_MARKAZ)
REMOTE_CNT   = len(REMOTE)
OOO_CNT      = len(OUT_OF_OFFICE)
PARTIAL_CNT  = len(PARTIAL)
FLAGGED_CNT  = len(FLAGGED)
TOTAL        = ONSITE_COUNT + ON_LEAVE_CNT + WFH_CNT + REMOTE_CNT + OOO_CNT + PARTIAL_CNT

# ... (rest is same format as yesterday)

def stat(val, label, color):
    return (f'<td style="padding:14px 10px;background:#f9f9f9;border-radius:6px;'
            f'text-align:center;border:1px solid #e0e0e0;min-width:90px;">'
            f'<div style="font-size:22px;font-weight:bold;color:{color};">{val}</div>'
            f'<div style="font-size:11px;color:#666;margin-top:3px;">{label}</div></td>')

THEAD = ('<tr style="background:#1a2a3a;color:#fff;">'
         '<th style="padding:10px 16px;text-align:left;width:50%;">Name</th>'
         '<th style="padding:10px 16px;text-align:left;">Status</th></tr>')

def data_row(name, badge, badge_color, note, bg):
    return (f'<tr style="background:{bg};">'
            f'<td style="padding:9px 16px;border:1px solid #e8e8e8;font-weight:bold;">{name}</td>'
            f'<td style="padding:9px 16px;border:1px solid #e8e8e8;font-size:13px;">'
            f'<span style="color:{badge_color};font-weight:bold;">{badge}</span>'
            f'{"&nbsp;&nbsp;" + note if note else ""}</td></tr>')

def sec(title, color):
    return (f'<table width="100%" cellpadding="0" cellspacing="0" style="margin:24px 0 10px;">'
            f'<tr><td style="background:{color};padding:10px 14px;border-radius:4px 4px 0 0;">'
            f'<span style="font-size:13px;font-weight:bold;color:#ffffff;'
            f'font-family:Georgia,serif;">{title}</span>'
            f'</td></tr></table>')

leave_rows = "".join(
    data_row(n, "ON LEAVE", "#e65100", note, "#fff8e1" if i%2==0 else "#fff")
    for i, (n,_,_,note) in enumerate(ON_LEAVE))

wfh_rows = "".join(
    data_row(n, "WFH", "#7b341e", note, "#fff8f0" if i%2==0 else "#fff")
    for i, (n,_,_,note) in enumerate(WFH_NO_MARKAZ))

remote_rows = "".join(
    data_row(n, "REMOTE", "#1565c0", note, "#e3f0fb" if i%2==0 else "#fff")
    for i, (n,_,_,note) in enumerate(REMOTE))

ooo_rows = "".join(
    data_row(n, "OUT OF OFFICE", "#d32f2f", note, "#ffebee" if i%2==0 else "#fff")
    for i, (n,_,_,note) in enumerate(OUT_OF_OFFICE))

onsite_list = [n for n in ONSITE if n not in [ln[0] for ln in ON_LEAVE] + [w[0] for w in WFH_NO_MARKAZ] + [r[0] for r in REMOTE] + [o[0] for o in OUT_OF_OFFICE] + [p[0] for p in PARTIAL]]
onsite_rows = "".join(
    data_row(n, "ONSITE", "#1a7a4a", "", "#f1f8e9" if i%2==0 else "#fff")
    for i, n in enumerate(onsite_list))

partial_rows = "".join(
    data_row(n, "ARRIVING LATER", "#e65100", note, "#fff8e1" if i%2==0 else "#fff")
    for i, (n,_,_,note) in enumerate(PARTIAL))

html = f"""
<html><body style="font-family:Georgia,serif;font-size:14px;color:#1a1a1a;
     max-width:760px;margin:auto;background:#f0f4f0;padding:24px 0;">
<table width="760" cellpadding="0" cellspacing="0"
       style="background:#fff;border-radius:8px;
              box-shadow:0 2px 12px rgba(0,0,0,0.08);overflow:hidden;">
<tr><td style="background:#1a2a3a;padding:22px 32px;">
  <p style="margin:0 0 6px;font-size:10px;color:#90a4ae;letter-spacing:2px;
            text-transform:uppercase;font-family:Georgia,serif;">
    People &amp; Culture &nbsp;&middot;&nbsp; Attendance Monitor</p>
  <p style="margin:0 0 2px;font-size:19px;font-weight:bold;color:#fff;font-family:Georgia,serif;">
    I-10 Head Office Attendance Record</p>
  <p style="margin:0;font-size:13px;color:#90caf9;font-family:Georgia,serif;">
    {DATE} &nbsp;&middot;&nbsp; Onsite Day (Mon–Thu)</p>
</td></tr>
<tr><td style="padding:28px 32px;">

<p style="margin:0 0 6px;">Hi Ayesha,</p>
<p style="margin:0 0 20px;font-size:13px;color:#444;line-height:1.7;">
  Today's attendance record cross-referenced against Markaz leave records, Markaz payroll list,
  and Teams Presence channel updates. Data sources: Markaz DB + Teams channel.
</p>

<table cellpadding="0" cellspacing="8" style="margin:0 0 24px;"><tr>
  {stat(ONSITE_COUNT, "Onsite Today",      "#1a7a4a")}
  <td width="6"></td>
  {stat(ON_LEAVE_CNT, "On Leave (Markaz)", "#e65100")}
  <td width="6"></td>
  {stat(WFH_CNT,      "WFH",               "#7b341e")}
  <td width="6"></td>
  {stat(PARTIAL_CNT,  "Arriving Later",    "#f59e0b")}
  <td width="6"></td>
  {stat(OOO_CNT,      "Out of Office",     "#d32f2f")}
</tr></table>

{sec(f"Present Onsite — I-10 Head Office ({ONSITE_COUNT})", "#1a7a4a")}
<p style="margin:-6px 0 8px;font-size:13px;color:#444;">
  {ONSITE_COUNT} employees onsite today (Markaz + sheet verified).
</p>
<table width="100%" cellpadding="0" cellspacing="0"
       style="border-collapse:collapse;font-size:13px;margin-bottom:20px;">
  {THEAD}{onsite_rows}</table>

{sec(f"Arriving Later — Teams Update ({PARTIAL_CNT})", "#e65100") if PARTIAL_CNT > 0 else ""}
{f'<p style="margin:-6px 0 8px;font-size:13px;color:#444;">Mentioned on Teams they are coming in but not yet onsite.</p>' if PARTIAL_CNT > 0 else ""}
{f'<table width="100%" cellpadding="0" cellspacing="0" style="border-collapse:collapse;font-size:13px;margin-bottom:20px;">{THEAD}{partial_rows}</table>' if PARTIAL_CNT > 0 else ""}

{sec(f"On Leave — Markaz Approved ({ON_LEAVE_CNT})", "#e65100")}
<p style="margin:-6px 0 8px;font-size:13px;color:#444;">Employees on leave today (approved on Markaz + Teams updates).</p>
<table width="100%" cellpadding="0" cellspacing="0"
       style="border-collapse:collapse;font-size:13px;margin-bottom:20px;">
  {THEAD}{leave_rows}</table>

{sec(f"Working From Home ({WFH_CNT})", "#7b341e") if WFH_CNT > 0 else ""}
{f'<p style="margin:-6px 0 8px;font-size:13px;color:#444;">Mentioned on Teams channel — WFH not formally logged on Markaz.</p>' if WFH_CNT > 0 else ""}
{f'<table width="100%" cellpadding="0" cellspacing="0" style="border-collapse:collapse;font-size:13px;margin-bottom:20px;">{THEAD}{wfh_rows}</table>' if WFH_CNT > 0 else ""}

{sec(f"Remote — Confirmed ({REMOTE_CNT})", "#1565c0") if REMOTE_CNT > 0 else ""}
{f'<p style="margin:-6px 0 8px;font-size:13px;color:#444;">Confirmed remote working arrangement.</p>' if REMOTE_CNT > 0 else ""}
{f'<table width="100%" cellpadding="0" cellspacing="0" style="border-collapse:collapse;font-size:13px;margin-bottom:20px;">{THEAD}{remote_rows}</table>' if REMOTE_CNT > 0 else ""}

{sec(f"Out of Office ({OOO_CNT})", "#d32f2f") if OOO_CNT > 0 else ""}
{f'<p style="margin:-6px 0 8px;font-size:13px;color:#444;">Out of office for official business.</p>' if OOO_CNT > 0 else ""}
{f'<table width="100%" cellpadding="0" cellspacing="0" style="border-collapse:collapse;font-size:13px;margin-bottom:20px;">{THEAD}{ooo_rows}</table>' if OOO_CNT > 0 else ""}

</td></tr>
<tr><td style="padding:12px 32px;background:#f5f5f5;font-size:11px;color:#888;
               font-family:Georgia,serif;">
  Taleemabad People &amp; Culture &nbsp;|&nbsp; hiring@taleemabad.com
  &nbsp;|&nbsp; Compiled by Coco, Nugget &amp; Noah &nbsp;|&nbsp; {DATE}
</td></tr>
</table></body></html>"""


def build_pdf():
    buf = io.BytesIO()
    PAGE = landscape(A4)
    W = PAGE[0] - 36*mm

    doc = SimpleDocTemplate(buf, pagesize=PAGE,
                             leftMargin=18*mm, rightMargin=18*mm,
                             topMargin=14*mm, bottomMargin=14*mm)

    NAVY  = colors.HexColor("#1a2a3a")
    GREEN = colors.HexColor("#1a7a4a")
    LGREEN= colors.HexColor("#e8f5e9")
    AMBER = colors.HexColor("#e65100")
    LAMBER= colors.HexColor("#fff3e0")
    BLUE  = colors.HexColor("#1565c0")
    LBLUE = colors.HexColor("#e3f2fd")
    RED   = colors.HexColor("#c62828")
    LRED  = colors.HexColor("#ffebee")
    BROWN = colors.HexColor("#7b341e")
    LBROWN= colors.HexColor("#fff8f0")
    LGREY = colors.HexColor("#f5f5f5")
    MGREY = colors.HexColor("#e0e0e0")
    DGREY = colors.HexColor("#757575")

    LBL   = ParagraphStyle("LBL",  fontSize=7,  textColor=colors.HexColor("#90a4ae"), fontName="Helvetica")
    H1    = ParagraphStyle("H1",   fontSize=18, textColor=colors.white, fontName="Helvetica-Bold", leading=22)
    H1sub = ParagraphStyle("sub",  fontSize=10, textColor=colors.HexColor("#90caf9"), fontName="Helvetica")
    H2    = ParagraphStyle("H2",   fontSize=9,  textColor=colors.white, fontName="Helvetica-Bold")
    BODY  = ParagraphStyle("BODY", fontSize=8,  leading=12, fontName="Helvetica-Bold")
    NOTE  = ParagraphStyle("NOTE", fontSize=7,  textColor=DGREY, leading=10, fontName="Helvetica")
    TH    = ParagraphStyle("TH",   fontSize=8,  textColor=colors.white, fontName="Helvetica-Bold")

    def section_header(title, color):
        t = Table([[Paragraph(title, H2)]], colWidths=[W])
        t.setStyle(TableStyle([
            ("BACKGROUND",    (0,0), (-1,-1), color),
            ("TOPPADDING",    (0,0), (-1,-1), 8),
            ("BOTTOMPADDING", (0,0), (-1,-1), 8),
            ("LEFTPADDING",   (0,0), (-1,-1), 12),
        ]))
        return t

    def two_col_table(names, bg_light, bg_alt):
        pairs = []
        for i in range(0, len(names), 2):
            left  = Paragraph(f"<b>{names[i]}</b>", BODY)
            right = Paragraph(f"<b>{names[i+1]}</b>", BODY) if i+1 < len(names) else Paragraph("", BODY)
            pairs.append([left, right])
        col = W / 2
        t = Table(pairs, colWidths=[col, col])
        style_cmds = [
            ("GRID",         (0,0), (-1,-1), 0.3, MGREY),
            ("TOPPADDING",   (0,0), (-1,-1), 5),
            ("BOTTOMPADDING",(0,0), (-1,-1), 5),
            ("LEFTPADDING",  (0,0), (-1,-1), 10),
            ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
        ]
        for i in range(len(pairs)):
            bg = bg_light if i % 2 == 0 else bg_alt
            style_cmds.append(("BACKGROUND", (0,i), (-1,i), bg))
        t.setStyle(TableStyle(style_cmds))
        return t

    def data_table(rows, bg_light, bg_alt):
        header = [Paragraph("Name", TH), Paragraph("Status", TH)]
        table_data = [header]
        for name, status in rows:
            table_data.append([
                Paragraph(f"<b>{name}</b>", BODY),
                Paragraph(status, NOTE),
            ])
        col1 = W * 0.38
        col2 = W * 0.62
        t = Table(table_data, colWidths=[col1, col2])
        style_cmds = [
            ("BACKGROUND",    (0,0), (-1,0),  NAVY),
            ("GRID",          (0,0), (-1,-1),  0.3, MGREY),
            ("TOPPADDING",    (0,0), (-1,-1),  5),
            ("BOTTOMPADDING", (0,0), (-1,-1),  5),
            ("LEFTPADDING",   (0,0), (-1,-1),  10),
            ("VALIGN",        (0,0), (-1,-1),  "MIDDLE"),
        ]
        for i in range(1, len(table_data)):
            bg = bg_light if i % 2 == 1 else bg_alt
            style_cmds.append(("BACKGROUND", (0,i), (-1,i), bg))
        t.setStyle(TableStyle(style_cmds))
        return t

    def stat_table():
        stats = [
            (str(ONSITE_COUNT), "Onsite Today",   GREEN, LGREEN),
            (str(ON_LEAVE_CNT), "On Leave",       AMBER, LAMBER),
            (str(WFH_CNT),      "WFH",            BROWN, LBROWN),
            (str(PARTIAL_CNT),  "Arriving Later", colors.HexColor("#f59e0b"), colors.HexColor("#fffde7")),
            (str(REMOTE_CNT),   "Remote",         BLUE,  LBLUE),
        ]
        cells = []
        for val, label, fg, bg in stats:
            p = Paragraph(
                f'<font size="22" color="{fg.hexval()}"><b>{val}</b></font><br/>'
                f'<font size="7" color="#666666">{label}</font>',
                ParagraphStyle("sc", alignment=TA_CENTER, leading=16))
            inner = Table([[p]], colWidths=[W/5 - 3*mm])
            inner.setStyle(TableStyle([
                ("BACKGROUND",    (0,0), (-1,-1), bg),
                ("BOX",           (0,0), (-1,-1), 0.5, MGREY),
                ("TOPPADDING",    (0,0), (-1,-1), 12),
                ("BOTTOMPADDING", (0,0), (-1,-1), 12),
                ("ALIGN",         (0,0), (-1,-1), "CENTER"),
            ]))
            cells.append(inner)
        t = Table([cells], colWidths=[W/5]*5)
        t.setStyle(TableStyle([
            ("ALIGN",  (0,0), (-1,-1), "CENTER"),
            ("VALIGN", (0,0), (-1,-1), "TOP"),
            ("LEFTPADDING",  (0,0), (-1,-1), 2),
            ("RIGHTPADDING", (0,0), (-1,-1), 2),
        ]))
        return t

    story = []
    hdr = Table([
        [Paragraph("PEOPLE &amp; CULTURE  ·  ATTENDANCE MONITOR", LBL)],
        [Paragraph("I-10 Head Office Attendance Record", H1)],
        [Paragraph(f"{DATE}  ·  Onsite Day (Mon–Thu)", H1sub)],
    ], colWidths=[W])
    hdr.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), NAVY),
        ("TOPPADDING",    (0,0), (0,0),   14),
        ("BOTTOMPADDING", (0,2), (0,2),   14),
        ("LEFTPADDING",   (0,0), (-1,-1), 16),
    ]))
    story.append(hdr)
    story.append(Spacer(1, 5*mm))
    story.append(stat_table())
    story.append(Spacer(1, 6*mm))

    onsite_list = [n for n in ONSITE if n not in [ln[0] for ln in ON_LEAVE] + [w[0] for w in WFH_NO_MARKAZ] + [r[0] for r in REMOTE] + [o[0] for o in OUT_OF_OFFICE] + [p[0] for p in PARTIAL]]

    sections = [
        (f"Present Onsite — I-10 Head Office ({len(onsite_list)})", GREEN,
         [(n, "ONSITE") for n in onsite_list]),
        (f"Arriving Later — Teams Update ({PARTIAL_CNT})", AMBER,
         [(n, note) for n,_,_,note in PARTIAL]),
        (f"On Leave ({ON_LEAVE_CNT})", AMBER,
         [(n, note) for n,_,_,note in ON_LEAVE]),
        (f"Working From Home ({WFH_CNT})", BROWN,
         [(n, note) for n,_,_,note in WFH_NO_MARKAZ]),
        (f"Remote — Confirmed ({REMOTE_CNT})", BLUE,
         [(n, note) for n,_,_,note in REMOTE]),
        (f"Out of Office ({OOO_CNT})", RED,
         [(n, note) for n,_,_,note in OUT_OF_OFFICE]),
    ]

    for title, color, rows in sections:
        if not rows:
            continue
        story.append(KeepTogether([
            section_header(title, color),
            two_col_table([r[0] for r in rows], color, colors.white) if len(rows) > 10 else data_table(rows, color, colors.white),
            Spacer(1, 4*mm),
        ]))

    footer = Table([[
        Paragraph(f"Taleemabad People &amp; Culture  ·  hiring@taleemabad.com  ·  {DATE}",
                  ParagraphStyle("ft", fontSize=7, textColor=DGREY, fontName="Helvetica")),
        Paragraph("Compiled by Coco, Nugget &amp; Noah",
                  ParagraphStyle("ft2", fontSize=7, textColor=DGREY, fontName="Helvetica-Oblique",
                                 alignment=TA_CENTER)),
    ]], colWidths=[W*0.55, W*0.45])
    footer.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), LGREY),
        ("TOPPADDING",    (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING",   (0,0), (-1,-1), 12),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ]))
    story.append(footer)

    doc.build(story)
    buf.seek(0)
    return buf.read()


def main():
    print("Building PDF...")
    pdf = build_pdf()
    pdf_path = "c:/Agent Coco/output/Attendance_Record_9Apr2026.pdf"
    os.makedirs("c:/Agent Coco/output", exist_ok=True)
    with open(pdf_path, "wb") as f:
        f.write(pdf)
    print(f"PDF saved: {pdf_path} ({len(pdf):,} bytes)")

    msg = MIMEMultipart("mixed")
    msg["Subject"] = "I-10 Head Office Attendance Record — 9 April 2026"
    msg["From"]    = EMAIL_USER
    msg["To"]      = "ayesha.khan@taleemabad.com"
    msg["Cc"]      = "jawwad.ali@taleemabad.com"
    msg.attach(MIMEText(html, "html", "utf-8"))

    pdf_part = MIMEBase("application", "pdf")
    pdf_part.set_payload(pdf)
    encoders.encode_base64(pdf_part)
    pdf_part.add_header("Content-Disposition", "attachment",
                        filename="Attendance_Record_9Apr2026.pdf")
    msg.attach(pdf_part)

    recipients = ["ayesha.khan@taleemabad.com", "jawwad.ali@taleemabad.com"]
    allow_candidate_addresses(recipients)
    with smtplib.SMTP("smtp.gmail.com", 587) as s:
        s.ehlo(); s.starttls(); s.login(EMAIL_USER, EMAIL_PASSWORD)
        safe_sendmail(s, EMAIL_USER, recipients, msg.as_string(),
                      context="attendance_9apr2026_markaz")
    print(f"Email + PDF sent to {recipients}")
    print(f"Total: {TOTAL} | Onsite: {ONSITE_COUNT} | Leave: {ON_LEAVE_CNT} | WFH: {WFH_CNT} | Remote: {REMOTE_CNT} | OOO: {OOO_CNT} | Arriving: {PARTIAL_CNT}")

if __name__ == "__main__":
    main()
