"""I-10 Head Office Attendance Record — 9 April 2026 — Exact Pattern Match"""
import os, sys, smtplib, io
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
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak

load_dotenv(os.path.join(os.path.dirname(__file__), "../..", ".env"))

EMAIL_USER     = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
DATE = "9 April 2026 (Thursday)"

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
    "Ahmed Javed", "Muhammad Omer Mazhar Rana",
]

ON_LEAVE = [
    ("Mavia ", "Annual Leave — Me-Time (Apr 1–15) · Approved on Markaz"),
    ("Muhammad Danish Iqbal", "Grant Leave — Wedding (Mar 24–Apr 24) · Approved on Markaz"),
    ("Salman Ahmad", "Grant Leave — Religious (Mar 30–Apr 12) · Approved on Markaz"),
    ("Shumaila Aslam", "Annual Leave"),
    ("Syed Junaid Ali Zaidi", "Medical Leave"),
    ("Tariq Asim", "Grant Leave — Wedding (Apr 1–30) · Approved on Markaz"),
    ("Rida Nayyab", "On leave — mentioned on Teams channel. Not marked on Markaz."),
]

WFH_NO_MARKAZ = [
    ("Iqra Zanib", "Not feeling well — joined remotely"),
    ("Fatima Khan", "Not feeling well — left to WFH"),
]

REMOTE = [
    ("Kamran Taj", "Confirmed remote arrangement"),
]

OUT_OF_OFFICE = [
    ("Mashhood Ali Rastgar", "Out of office — conducting training in Lahore"),
]

PARTIAL = [
    ("Muhammad Omer Mazhar Rana", "Running a bit late"),
]

FLAGGED = []

onsite_list = [n for n in ONSITE if n not in [ln[0] for ln in ON_LEAVE] + [w[0] for w in WFH_NO_MARKAZ] + [r[0] for r in REMOTE] + [o[0] for o in OUT_OF_OFFICE] + [p[0] for p in PARTIAL]]

TOTAL        = len(onsite_list) + len(ON_LEAVE) + len(WFH_NO_MARKAZ) + len(REMOTE) + len(OUT_OF_OFFICE) + len(PARTIAL)
ONSITE_COUNT = len(onsite_list)
ON_LEAVE_CNT = len(ON_LEAVE)
WFH_CNT      = len(WFH_NO_MARKAZ)
REMOTE_CNT   = len(REMOTE)
OOO_CNT      = len(OUT_OF_OFFICE)
PARTIAL_CNT  = len(PARTIAL)
FLAGGED_CNT  = len(FLAGGED)


def build_pdf():
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=15*mm, rightMargin=15*mm,
                            topMargin=15*mm, bottomMargin=15*mm)

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

    LBL = ParagraphStyle("LBL", fontSize=8, textColor=colors.HexColor("#999999"), fontName="Helvetica")
    H1  = ParagraphStyle("H1",  fontSize=24, textColor=colors.white, fontName="Helvetica-Bold")
    H1s = ParagraphStyle("H1s", fontSize=11, textColor=colors.HexColor("#90caf9"), fontName="Helvetica")
    H2  = ParagraphStyle("H2",  fontSize=11, textColor=colors.white, fontName="Helvetica-Bold")
    BD  = ParagraphStyle("BD",  fontSize=9, fontName="Helvetica-Bold")
    TH  = ParagraphStyle("TH",  fontSize=9, textColor=colors.white, fontName="Helvetica-Bold")
    SM  = ParagraphStyle("SM",  fontSize=8)

    story = []

    # Header
    hdr_data = [
        [Paragraph("PEOPLE &amp; CULTURE · ATTENDANCE MONITOR", LBL)],
        [Paragraph("I-10 Head Office Attendance Record", H1)],
        [Paragraph(f"{DATE} · Onsite Day (Mon–Thu)", H1s)],
    ]
    hdr = Table(hdr_data, colWidths=[160*mm])
    hdr.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), NAVY),
        ("TOPPADDING",    (0,0), (-1,-1), 14),
        ("BOTTOMPADDING", (0,0), (-1,-1), 14),
        ("LEFTPADDING",   (0,0), (-1,-1), 14),
    ]))
    story.append(hdr)
    story.append(Spacer(1, 8*mm))

    # Stat Boxes - Match reference exactly
    stat_boxes = [
        (str(TOTAL), "Total Active", LGREY),
        (str(ONSITE_COUNT), "Onsite Today", LGREEN),
        (str(ON_LEAVE_CNT), "On Leave", LAMBER),
        (str(WFH_CNT), "WFH", LBROWN),
        (str(PARTIAL_CNT), "Arriving Later", colors.HexColor("#fffde7")),
        (str(REMOTE_CNT), "Remote", LBLUE),
        (str(FLAGGED_CNT), "Flagged", LRED),
    ]

    stat_cells = []
    for val, label, bg_color in stat_boxes:
        cell_para = Paragraph(f"<b><font size='24'>{val}</font></b><br/><font size='8'>{label}</font>",
                              ParagraphStyle("stat", alignment=TA_CENTER, leading=20))
        cell = Table([[cell_para]], colWidths=[20*mm])
        cell.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,-1), bg_color),
            ("BORDER", (0,0), (-1,-1), 0.5, GREY),
            ("TOPPADDING",    (0,0), (-1,-1), 8),
            ("BOTTOMPADDING", (0,0), (-1,-1), 8),
            ("ALIGN", (0,0), (-1,-1), "CENTER"),
            ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ]))
        stat_cells.append(cell)

    stats_row = Table([stat_cells], colWidths=[20*mm]*7, hAlign='LEFT')
    stats_row.setStyle(TableStyle([("ALIGN", (0,0), (-1,-1), "CENTER")]))
    story.append(stats_row)
    story.append(Spacer(1, 10*mm))

    # Onsite Section - 2 column grid
    hdr_onsite = Table([[Paragraph(f"Present Onsite — I-10 Head Office ({ONSITE_COUNT})", H2)]], colWidths=[160*mm])
    hdr_onsite.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), GREEN),
        ("TOPPADDING",    (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
    ]))
    story.append(hdr_onsite)

    pairs = []
    for i in range(0, len(onsite_list), 2):
        left = Paragraph(onsite_list[i], BD)
        right = Paragraph(onsite_list[i+1], BD) if i+1 < len(onsite_list) else Paragraph("", BD)
        pairs.append([left, right])

    onsite_tbl = Table(pairs, colWidths=[80*mm, 80*mm])
    style = [("BORDER", (0,0), (-1,-1), 0.5, GREY), ("PADDING", (0,0), (-1,-1), 7)]
    for i in range(len(pairs)):
        bg = LGREEN if i % 2 == 0 else colors.white
        style.append(("BACKGROUND", (0,i), (-1,i), bg))
    onsite_tbl.setStyle(TableStyle(style))
    story.append(onsite_tbl)
    story.append(Spacer(1, 8*mm))

    # Sections
    def make_section(title, header_color, rows):
        if not rows:
            return
        hdr = Table([[Paragraph(title, H2)]], colWidths=[160*mm])
        hdr.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,-1), header_color),
            ("TOPPADDING",    (0,0), (-1,-1), 8),
            ("BOTTOMPADDING", (0,0), (-1,-1), 8),
            ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ]))
        story.append(hdr)

        data = [[Paragraph("<b>Name</b>", TH), Paragraph("<b>Status</b>", TH)]]
        for name, status in rows:
            data.append([Paragraph(name, BD), Paragraph(status, SM)])

        tbl = Table(data, colWidths=[65*mm, 95*mm])
        style = [
            ("BACKGROUND", (0,0), (-1,0), NAVY),
            ("BORDER", (0,0), (-1,-1), 0.5, GREY),
            ("TOPPADDING",    (0,0), (-1,-1), 6),
            ("BOTTOMPADDING", (0,0), (-1,-1), 6),
            ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ]
        for i in range(1, len(data)):
            bg = colors.HexColor("#f9f9f9") if i % 2 == 0 else colors.white
            style.append(("BACKGROUND", (0,i), (-1,i), bg))
        tbl.setStyle(TableStyle(style))
        story.append(tbl)
        story.append(Spacer(1, 6*mm))

    if PARTIAL_CNT > 0:
        make_section(f"Arriving Later — Teams Update ({PARTIAL_CNT})", AMBER, PARTIAL)
    if ON_LEAVE_CNT > 0:
        make_section(f"On Leave ({ON_LEAVE_CNT})", AMBER, ON_LEAVE)
    if WFH_CNT > 0:
        make_section(f"Working From Home ({WFH_CNT})", BROWN, WFH_NO_MARKAZ)
    if REMOTE_CNT > 0:
        make_section(f"Remote — Confirmed ({REMOTE_CNT})", BLUE, REMOTE)
    if OOO_CNT > 0:
        make_section(f"Out of Office ({OOO_CNT})", RED, OUT_OF_OFFICE)
    if FLAGGED_CNT > 0:
        make_section(f"Flagged — No Attendance Record ({FLAGGED_CNT})", RED, FLAGGED)

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
        safe_sendmail(s, EMAIL_USER, recipients, msg.as_string(), context="attendance_9apr2026_corrected")
    print(f"PDF sent to {recipients}")

if __name__ == "__main__":
    main()
