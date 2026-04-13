"""I-10 Head Office Attendance Record — 9 April 2026 — EXACT MATCH to 8 Apr reference"""
import os, sys, smtplib, io, json, subprocess
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from scripts.utils.safe_send import safe_sendmail, allow_candidate_addresses

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

load_dotenv(os.path.join(os.path.dirname(__file__), "../..", ".env"))

EMAIL_USER     = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
DATE = "9 April 2026 (Thursday)"

# All 84 OPL+OWT employees (from database query)
ALL_PAYROLL = [
    "ABDUL AHAD", "Abdul Rehman", "Abdul Rehman Siddiqi", "Abdur Rehman", "Afifa Sultana", "Ahmed Javed", "Ahsan Javed",
    "Ahwaz Akhtar", "Ajlal Hasan", "Ali Sipra", "Alishba Anam", "Amena Ahmed", "Amina Tayyub", "Aroma Tahir",
    "Ayesha Raza Khan", "Aymen Abid", "Babar Khan", "Fahad Rao", "Fatima Khan", "Fatima Rahman", "Gul Perwasha Cheema",
    "Haroon Ali", "Hassan Shahzad", "Hataf Bin Atif", "Haya Abid", "Iffat Maab Akhtar", "Iqra Zanib", "JAHAN ZAIB",
    "Jahanzeb Ahmad", "Javariya Mufarrakh", "Laraib Sarfraz", "MUHAMMAD OMER MAZHAR RANA", "MUHAMMAD SHOAIB KHAN",
    "Mah Noor", "Mahnoor Shafique", "Mahrah Ashraf", "Mashhood Ali Rastgar", "Mavia ", "Muhammad Danish Iqbal",
    "Muhammad Hammad Sarfraz", "Muhammad Haris", "Muhammad Jalal Khan", "Muhammad Kamal", "Muhammad Kamran Taj",
    "Muhammad Mehdi Abbas", "Muhammad Muzzammil Patel", "Muhammad Raees Shujaan Azhar", "Muhammad Saim", "Muhammad Talha",
    "Muhammad Umar Raza", "Muhammad Usman Javed", "Muhammad Usman Mughal", "Muhammad Zeeshan Usaid", "Muqadas Saleem",
    "Osama Ahmad", "Raheela Akhtar", "Ramisha Riaz Sheikh", "Ramsha Khurshid", "Razia Kausar", "Rida Nayyab",
    "Saad Zahid", "Sabeen Fatima", "Saima Bibi", "Saleh Muhammad", "Salman Ahmad", "Salman Iqbal", "Samra Tariq",
    "Shayan Ahmad", "Sheikh Nimra Rasheed", "Shoaib Ud Din", "Sohaib Danish", "Summaya Shakur", "Syed Junaid Ali Zaidi",
    "Syed Zaamin Abbas", "Taloot Ahmad Malik", "Tariq Asim", "Tehniat Taqdees Masood", "Unsa Umar", "Usman Imtiaz",
    "Zeeshan Zahoor", "Zeest Hassan Qureshi", "Zeshan Ali", "Zulfiqar Ahmed Mughal", "Zunaira Shahid"
]

# Total active employees in OPL + OWT payroll entities (verified from database)
PAYROLL_TOTAL = 84

ONSITE = [
    "Salman Iqbal", "Osama Ahmad", "Ramsha Khurshid", "Aroma Tahir", "Abdul Rehman Siddiqi",
    "Muhammad Kamal", "Hassan Shahzad", "Saleh Muhammad", "Fatima Rahman", "Mah Noor",
    "Haya Abid", "Sheikh Nimra Rasheed", "Mahrah Ashraf", "Muhammad Saim", "Rifat Yasmeen",
    "Umama Gul Siddiqui", "QURAT UL AIN", "Muhammad Umar Raza", "MUHAMMAD OMER MAZHAR RANA", "Afifa Sultana",
    "Haroon Ali", "Saima Bibi", "Zunaira Shahid", "Mahnoor Shafique", "Taloot Ahmad Malik",
    "Ahsan Javed", "Zeshan Ali", "Jawwad Ali", "Ayesha Raza Khan", "Javariya Mufarrakh",
    "Muhammad Talha", "Usman Imtiaz", "Muhammad Hammad Sarfraz", "Muhammad Zain ul Abadin", "Jahanzeb Ahmad",
    "Hamza Shahid", "Shoaib Ud Din", "Saad Zahid", "Muhammad Usman Mughal", "Hataf Bin Atif", "JAHAN ZAIB",
    "Amena Ahmed", "Abdur Rehman", "Abdul Rehman", "Muhammad Zeeshan Usaid", "Hareem Fatima", "Ramisha Riaz Sheikh",
    "Laraib Sarfraz", "Sabeen Fatima", "Muhammad Jalal Khan", "Muhammad Raees Shujaan Azhar",
    "Muhammad Haris", "Samra Tariq", "Babar Khan", "Zeeshan Zahoor",
    "Ahmed Javed", "MUHAMMAD SHOAIB KHAN", "Muhammad Mehdi Abbas", "Muhammad Kamran Taj",
    "Ali Sipra", "Fahad Rao", "Gul Perwasha Cheema",
]

ON_LEAVE = [
    ("Mavia ", "Annual Leave — Me-Time (Apr 1–15) · Approved on Markaz"),
    ("Muhammad Danish Iqbal", "Grant Leave — Wedding (Mar 24–Apr 24) · Approved on Markaz"),
    ("Salman Ahmad", "Grant Leave — Religious (Mar 30–Apr 12) · Approved on Markaz"),
    ("Tariq Asim", "Grant Leave — Wedding (Apr 1–30) · Approved on Markaz"),
    ("Shumaila Aslam", "Annual Leave"),
    ("Syed Junaid Ali Zaidi", "Medical Leave"),
    ("Rida Nayyab", "On leave — mentioned on Teams channel. Not marked on Markaz."),
    ("Aymen Abid", "On leave — mentioned on Teams"),
]

WFH_NO_MARKAZ = [
    ("Iqra Zanib", "Not feeling well — joined remotely"),
    ("Fatima Khan", "Not feeling well — left to WFH"),
]

PERMANENT_WFH = [
    ("Amina Tayyub", "Permanent remote arrangement"),
    ("Zuhaib Shaikh", "Permanent remote arrangement"),
    ("Ajlal Hasan", "Permanent remote arrangement"),
    ("Zeest Hassan Qureshi", "Permanent remote arrangement"),
    ("Ahwaz Akhtar", "Permanent remote arrangement"),
    ("Shayan Ahmad", "Permanent remote arrangement"),
    ("ABDUL AHAD", "Permanent remote arrangement"),
    ("Zulfiqar Ahmed Mughal", "Permanent remote arrangement"),
    ("Sabeena Abbasi", "Permanent remote arrangement"),
]

REMOTE = []

OUT_OF_OFFICE = [
    ("Mashhood Ali Rastgar", "Out of office — conducting training in Lahore"),
    ("Haroon Yasin", "Out of office"),
]

PARTIAL = [
    ("Muhammad Omer Mazhar Rana", "Running a bit late"),
]

# Compute FLAGGED: all payroll employees not in any attendance category with specific notes
accounted = set(
    [n for n in ONSITE] +
    [ln[0] for ln in ON_LEAVE] +
    [w[0] for w in WFH_NO_MARKAZ] +
    [pwfh[0] for pwfh in PERMANENT_WFH] +
    [r[0] for r in REMOTE] +
    [o[0] for o in OUT_OF_OFFICE] +
    [p[0] for p in PARTIAL]
)

FLAGGED_NOTES = {
    "Alishba Anam": "No sign-in · (last month)",
    "Iffat Maab Akhtar": "No sign-in · RWP Team",
    "Muhammad Muzzammil Patel": "No sign-in · No Markaz record · No Teams update",
    "Muhammad Usman Javed": "No sign-in · No Markaz record · No Teams update",
    "Muqadas Saleem": "No sign-in · RWP Team",
    "Raheela Akhtar": "No sign-in · RWP Team",
    "Razia Kausar": "No sign-in · (on severance)",
    "Sohaib Danish": "RWP Team",
    "Summaya Shakur": "RWP Team",
    "Syed Zaamin Abbas": "No sign-in · No Markaz record · No Teams update",
    "Tehniat Taqdees Masood": "RWP Team",
    "Unsa Umar": "No sign-in · No Markaz record · No Teams update",
}

FLAGGED = [(name, FLAGGED_NOTES.get(name, "No sign-in · No Markaz record · No Teams update"))
           for name in ALL_PAYROLL if name not in accounted]

onsite_list = [n for n in ONSITE if n not in [ln[0] for ln in ON_LEAVE] + [w[0] for w in WFH_NO_MARKAZ] + [pwfh[0] for pwfh in PERMANENT_WFH] + [r[0] for r in REMOTE] + [o[0] for o in OUT_OF_OFFICE] + [p[0] for p in PARTIAL]]

# TOTAL is from payroll headcount, not sum of attendance categories
TOTAL        = PAYROLL_TOTAL  # 84 for OPL + OWT
ONSITE_COUNT = len(onsite_list)
ON_LEAVE_CNT = len(ON_LEAVE)
WFH_CNT      = len(WFH_NO_MARKAZ)
PERMANENT_WFH_CNT = len(PERMANENT_WFH)
REMOTE_CNT   = len(REMOTE)
OOO_CNT      = len(OUT_OF_OFFICE)
PARTIAL_CNT  = len(PARTIAL)
FLAGGED_CNT  = len(FLAGGED)


def build_pdf():
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=10*mm, rightMargin=10*mm,
                            topMargin=10*mm, bottomMargin=10*mm)

    NAVY  = colors.HexColor("#1a2a3a")
    GREEN = colors.HexColor("#1a7a4a")
    LGREEN = colors.HexColor("#e8f5e9")
    AMBER = colors.HexColor("#e65100")
    LAMBER = colors.HexColor("#fff3e0")
    BLUE  = colors.HexColor("#1565c0")
    LBLUE = colors.HexColor("#e3f2fd")
    RED   = colors.HexColor("#c62828")
    LRED  = colors.HexColor("#ffebee")
    BROWN = colors.HexColor("#7b341e")
    LBROWN = colors.HexColor("#fff8f0")
    LGREY = colors.HexColor("#f5f5f5")
    GREY  = colors.HexColor("#e0e0e0")
    WHITE = colors.white

    styles = {
        'lbl': ParagraphStyle("lbl", fontSize=7, textColor=colors.HexColor("#999999"), fontName="Helvetica"),
        'h1': ParagraphStyle("h1", fontSize=24, textColor=WHITE, fontName="Helvetica-Bold", leading=30),
        'h1s': ParagraphStyle("h1s", fontSize=11, textColor=colors.HexColor("#90caf9"), fontName="Helvetica", leading=14),
        'h2': ParagraphStyle("h2", fontSize=11, textColor=WHITE, fontName="Helvetica-Bold", leading=14),
        'bd': ParagraphStyle("bd", fontSize=9, fontName="Helvetica-Bold", leading=11),
        'th': ParagraphStyle("th", fontSize=9, textColor=WHITE, fontName="Helvetica-Bold", leading=11),
        'sm': ParagraphStyle("sm", fontSize=8, leading=10),
    }

    story = []

    # ─── Header ──────────────────────────────────────────
    hdr_data = [
        [Paragraph("PEOPLE &amp; CULTURE · ATTENDANCE MONITOR", styles['lbl'])],
        [Paragraph("I-10 Head Office Attendance Record", styles['h1'])],
        [Paragraph(f"{DATE} · Onsite Day (Mon–Thu)", styles['h1s'])],
    ]
    hdr = Table(hdr_data, colWidths=[180*mm])
    hdr.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), NAVY),
        ("TOPPADDING",    (0,0), (-1,-1), 12),
        ("BOTTOMPADDING", (0,0), (-1,-1), 12),
        ("LEFTPADDING",   (0,0), (-1,-1), 12),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ]))
    story.append(hdr)
    story.append(Spacer(1, 8*mm))

    # ─── Stat Boxes ──────────────────────────────────────
    stats = [
        (str(TOTAL), "Total Active", LGREY),
        (str(ONSITE_COUNT), "Onsite Today", LGREEN),
        (str(ON_LEAVE_CNT), "On Leave", LAMBER),
        (str(WFH_CNT), "WFH", LBROWN),
        (str(PERMANENT_WFH_CNT), "WFH Confirmed", LBLUE),
        (str(PARTIAL_CNT), "Arriving Later", colors.HexColor("#fffde7")),
        (str(FLAGGED_CNT), "Flagged", LRED),
    ]

    stat_cells = []
    for val, lbl, bg in stats:
        p = Paragraph(f"<b><font size='20'>{val}</font></b><br/><font size='7'>{lbl}</font>",
                      ParagraphStyle("s", alignment=TA_CENTER, leading=18))
        cell = Table([[p]], colWidths=[23*mm])
        cell.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,-1), bg),
            ("BORDER", (0,0), (-1,-1), 0.5, GREY),
            ("PADDING", (0,0), (-1,-1), 7),
            ("ALIGN", (0,0), (-1,-1), "CENTER"),
            ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ]))
        stat_cells.append(cell)

    stats_tbl = Table([stat_cells], colWidths=[23*mm]*8)
    stats_tbl.setStyle(TableStyle([("ALIGN", (0,0), (-1,-1), "CENTER")]))
    story.append(stats_tbl)
    story.append(Spacer(1, 10*mm))

    # ─── Onsite Section (2-column grid) ──────────────────
    hdr_onsite = Table([[Paragraph(f"Present Onsite — I-10 Head Office ({ONSITE_COUNT})", styles['h2'])]], colWidths=[180*mm])
    hdr_onsite.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), GREEN),
        ("PADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING", (0,0), (-1,-1), 10),
    ]))
    story.append(hdr_onsite)

    pairs = []
    for i in range(0, len(onsite_list), 2):
        left = Paragraph(onsite_list[i], styles['bd'])
        right = Paragraph(onsite_list[i+1], styles['bd']) if i+1 < len(onsite_list) else Paragraph("", styles['bd'])
        pairs.append([left, right])

    onsite_tbl = Table(pairs, colWidths=[90*mm, 90*mm])
    onsite_style = [("BORDER", (0,0), (-1,-1), 0.5, GREY), ("PADDING", (0,0), (-1,-1), 7)]
    for i in range(len(pairs)):
        bg = LGREEN if i % 2 == 0 else WHITE
        onsite_style.append(("BACKGROUND", (0,i), (-1,i), bg))
    onsite_tbl.setStyle(TableStyle(onsite_style))
    story.append(onsite_tbl)
    story.append(Spacer(1, 8*mm))

    # ─── Sections ────────────────────────────────────────
    def make_section(title, hdr_color, rows, alt_bg_light, alt_bg_dark):
        if not rows:
            return
        hdr = Table([[Paragraph(title, styles['h2'])]], colWidths=[180*mm])
        hdr.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,-1), hdr_color),
            ("PADDING", (0,0), (-1,-1), 8),
            ("LEFTPADDING", (0,0), (-1,-1), 10),
        ]))
        story.append(hdr)

        data = [[Paragraph("Name", styles['th']), Paragraph("Status", styles['th'])]]
        for name, status in rows:
            data.append([Paragraph(name, styles['bd']), Paragraph(status, styles['sm'])])

        tbl = Table(data, colWidths=[70*mm, 110*mm])
        tbl_style = [
            ("BACKGROUND", (0,0), (-1,0), NAVY),
            ("BORDER", (0,0), (-1,-1), 0.5, GREY),
            ("PADDING", (0,0), (-1,-1), 6),
            ("LEFTPADDING", (0,0), (-1,-1), 8),
        ]
        for i in range(1, len(data)):
            bg = alt_bg_light if i % 2 == 1 else alt_bg_dark
            tbl_style.append(("BACKGROUND", (0,i), (-1,i), bg))
        tbl.setStyle(TableStyle(tbl_style))
        story.append(tbl)
        story.append(Spacer(1, 6*mm))

    if PARTIAL_CNT > 0:
        make_section(f"Arriving Later — Teams Update ({PARTIAL_CNT})", AMBER, PARTIAL, LAMBER, WHITE)
    if ON_LEAVE_CNT > 0:
        make_section(f"On Leave ({ON_LEAVE_CNT})", AMBER, ON_LEAVE, LAMBER, WHITE)
    if WFH_CNT > 0:
        make_section(f"Working From Home ({WFH_CNT})", BROWN, WFH_NO_MARKAZ, LBROWN, WHITE)
    if PERMANENT_WFH_CNT > 0:
        make_section(f"WFH — Confirmed ({PERMANENT_WFH_CNT})", BLUE, PERMANENT_WFH, LBLUE, WHITE)
    if REMOTE_CNT > 0:
        make_section(f"Remote — Confirmed ({REMOTE_CNT})", BLUE, REMOTE, LBLUE, WHITE)
    if OOO_CNT > 0:
        make_section(f"Out of Office ({OOO_CNT})", RED, OUT_OF_OFFICE, LRED, WHITE)
    if FLAGGED_CNT > 0:
        make_section(f"Flagged — No Attendance Record ({FLAGGED_CNT})", RED, FLAGGED, LRED, WHITE)

    # ─── Footer ──────────────────────────────────────────
    footer = Table([[
        Paragraph(f"Taleemabad People &amp; Culture · hiring@taleemabad.com · {DATE}",
                  ParagraphStyle("ft", fontSize=8, textColor=colors.HexColor("#666666"))),
        Paragraph("Compiled by Coco, Nugget &amp; Noah · People &amp; Culture AI Assistants",
                  ParagraphStyle("ft2", fontSize=8, textColor=colors.HexColor("#666666"),
                                alignment=TA_RIGHT)),
    ]], colWidths=[90*mm, 90*mm])
    footer.setStyle(TableStyle([
        ("BORDER", (0,0), (-1,-1), 0.5, GREY),
        ("PADDING", (0,0), (-1,-1), 6),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
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

    pdf_part = MIMEBase("application", "pdf")
    pdf_part.set_payload(pdf)
    encoders.encode_base64(pdf_part)
    pdf_part.add_header("Content-Disposition", "attachment", filename="Attendance_Record_9Apr2026.pdf")
    msg.attach(pdf_part)

    recipients = ["ayesha.khan@taleemabad.com", "jawwad.ali@taleemabad.com"]
    allow_candidate_addresses(recipients)
    with smtplib.SMTP("smtp.gmail.com", 587) as s:
        s.ehlo(); s.starttls(); s.login(EMAIL_USER, EMAIL_PASSWORD)
        safe_sendmail(s, EMAIL_USER, recipients, msg.as_string(), context="attendance_9apr2026_exact")
    print(f"PDF sent to {recipients}")

if __name__ == "__main__":
    main()
