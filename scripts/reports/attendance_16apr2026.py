"""I-10 Head Office Attendance Record — 16 April 2026 (Thursday)"""
import os, sys, io
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from dotenv import load_dotenv

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

load_dotenv(os.path.join(os.path.dirname(__file__), "../..", ".env"))

DATE = "16 April 2026 (Thursday)"

ONSITE_LIST = sorted([
    "Mahrah Ashraf", "Saima Bibi", "Laraib Sarfraz", "Hassan Shahzad", "Muhammad Hammad Sarfraz",
    "Haroon Ali", "Haya Abid", "Osama Ahmad", "Muhammad Saim", "Saleh Muhammad",
    "Muhammad Usman Mughal", "Muhammad Kamal", "Muhammad Talha", "Ramsha Khurshid", "Usman Imtiaz",
    "Taloot Ahmad Malik", "Aymen Abid", "Zeest Hassan Qureshi", "Abdur Rehman", "Salman Ahmad",
    "Fatima Khan", "MUHAMMAD OMER MAZHAR RANA", "Amena Ahmed", "Mahnoor Shafique", "Sheikh Nimra Rasheed",
    "Mashhood Ali Rastgar", "Muhammad Zeeshan Usaid", "Muhammad Haris", "Mah Noor", "Fatima Rahman",
    "Muhammad Mehdi Abbas", "Zeeshan Zahoor", "MUHAMMAD SHOAIB KHAN", "Babar Khan", "Fahad Rao",
    "Shoaib Ud Din", "Zeshan Ali", "Ahmed Javed", "Mavia ", "Afifa Sultana",
    "Abdul Rehman Siddiqi", "Saad Zahid", "JAHAN ZAIB", "Aroma Tahir", "Samra Tariq",
    "Muhammad Raees Shujaan Azhar", "Hataf Bin Atif", "Ali Sipra", "Ahsan Javed", "Muhammad Jalal Khan",
    "Muhammad Kamran Taj", "Ramisha Riaz Sheikh", "Sabeen Fatima", "Rida Nayyab",
    "Ayesha Raza Khan", "Syed Junaid Ali Zaidi"
])

ON_LEAVE = [
    ("Gul Perwasha Cheema", "On leave · Mentioned on Teams"),
    ("Iqra Zanib", "On leave today · Informed on Teams"),
    ("Jahanzeb Ahmad", "On leave today · Informed on Teams"),
    ("Javariya Mufarrakh", "On leave · Informed by manager"),
    ("Muhammad Danish Iqbal", "Grant Leave — Wedding (23 Mar–23 Apr)"),
    ("Salman Iqbal", "On leave · Informed by manager"),
    ("Tariq Asim", "Grant Leave — Wedding (31 Mar–29 Apr)"),
    ("Umar Raza", "Sick leave today · Informed on Teams"),
    ("Unsa Umar", "Leave pending approval on Markaz"),
]

PERMANENT_WFH = [
    ("Amina Tayyub", "Permanent remote arrangement"),
    ("Zuhaib Shaikh", "Permanent remote arrangement"),
    ("Ajlal Hasan", "Permanent remote arrangement"),
    ("Ahwaz Akhtar", "Permanent remote arrangement"),
    ("Shayan Ahmad", "Permanent remote arrangement"),
    ("ABDUL AHAD", "Permanent remote arrangement"),
    ("Zulfiqar Ahmed Mughal", "Permanent remote arrangement"),
]

FLAGGED = [
    ("Muhammad Muzzammil Patel", "No attendance record"),
    ("Muhammad Usman Javed", "No attendance record"),
]

ADDITIONAL_ATTENDANCE = [
    ("Jawwad Ali", "NIETE — Archived/Parked · Onsite I-10"),
    ("Sameer Sheikh", "Additional Attendee — Not OPL+OWT"),
    ("Hareem Fatima", "NIETE — Archived/Parked · Onsite I-10"),
    ("Hamza Shahid", "NIETE — Archived/Parked · Onsite I-10"),
    ("Umama", "Additional Attendee — Not OPL+OWT"),
    ("Zain Ul Abideen", "NIETE — Archived/Parked · Onsite I-10"),
    ("Rifat", "NIETE — Archived/Parked · Onsite I-10"),
    ("Shumaila", "NIETE — Archived/Parked · Onsite I-10"),
    ("QURAT UL AIN", "NIETE — Archived/Parked · Onsite I-10"),
]

# Counts
TOTAL = 84
ONSITE_COUNT = len(ONSITE_LIST)
ON_LEAVE_CNT = len(ON_LEAVE)  # Now 9 (added Unsa Umar pending approval)
PERMANENT_WFH_CNT = len(PERMANENT_WFH)
FLAGGED_CNT = len(FLAGGED)  # Now 2 (removed Unsa Umar)
ADDITIONAL_CNT = len(ADDITIONAL_ATTENDANCE)


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
    LGREY = colors.HexColor("#f5f5f5")
    GREY  = colors.HexColor("#e0e0e0")
    PURPLE = colors.HexColor("#6a1b9a")
    LPURPLE = colors.HexColor("#f3e5f5")
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

    # Header
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
    story.append(Spacer(1, 5*mm))

    # Stat Boxes (7 boxes)
    stats = [
        (str(TOTAL), "Total Active", LGREY),
        (str(ONSITE_COUNT), "Onsite Today", LGREY),
        (str(ON_LEAVE_CNT), "On Leave", LAMBER),
        ("0", "WFH", colors.HexColor("#e3f2fd")),
        (str(PERMANENT_WFH_CNT), "WFH Confirmed", LBLUE),
        (str(ADDITIONAL_CNT), "Additional", LPURPLE),
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

    stats_tbl = Table([stat_cells], colWidths=[23*mm]*7)
    stats_tbl.setStyle(TableStyle([("ALIGN", (0,0), (-1,-1), "CENTER")]))
    story.append(stats_tbl)
    story.append(Spacer(1, 6*mm))

    # Onsite Section (2-column grid, names only)
    hdr_onsite = Table([[Paragraph(f"Present Onsite — I-10 Head Office ({ONSITE_COUNT})", styles['h2'])]], colWidths=[180*mm])
    hdr_onsite.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), GREEN),
        ("PADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING", (0,0), (-1,-1), 10),
    ]))
    story.append(hdr_onsite)

    pairs = []
    for i in range(0, len(ONSITE_LIST), 2):
        left = Paragraph(ONSITE_LIST[i], styles['bd'])
        right = Paragraph(ONSITE_LIST[i+1], styles['bd']) if i+1 < len(ONSITE_LIST) else Paragraph("", styles['bd'])
        pairs.append([left, right])

    onsite_tbl = Table(pairs, colWidths=[90*mm, 90*mm])
    onsite_style = [("BORDER", (0,0), (-1,-1), 0.5, GREY), ("PADDING", (0,0), (-1,-1), 7)]
    for i in range(len(pairs)):
        bg = LGREEN if i % 2 == 0 else WHITE
        onsite_style.append(("BACKGROUND", (0,i), (-1,i), bg))
    onsite_tbl.setStyle(TableStyle(onsite_style))
    story.append(onsite_tbl)
    story.append(Spacer(1, 3*mm))

    # Helper function for sections
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
        story.append(Spacer(1, 3*mm))

    # Add sections in order
    if ON_LEAVE_CNT > 0:
        make_section(f"On Leave ({ON_LEAVE_CNT})", AMBER, ON_LEAVE, LAMBER, WHITE)
    if PERMANENT_WFH_CNT > 0:
        make_section(f"WFH — Confirmed ({PERMANENT_WFH_CNT})", BLUE, PERMANENT_WFH, LBLUE, WHITE)
    if FLAGGED_CNT > 0:
        make_section(f"Flagged — No Attendance Record ({FLAGGED_CNT})", RED, FLAGGED, LRED, WHITE)
    if ADDITIONAL_CNT > 0:
        make_section(f"Additional in Attendance — Not OPL+OWT ({ADDITIONAL_CNT})", PURPLE, ADDITIONAL_ATTENDANCE, LPURPLE, WHITE)

    # Footer (2-column layout)
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
    ]))
    story.append(footer)

    doc.build(story)
    buf.seek(0)
    return buf.read()

if __name__ == "__main__":
    print("Building attendance report for 16 April 2026...")
    pdf = build_pdf()
    os.makedirs("scripts/reports", exist_ok=True)
    pdf_path = "scripts/reports/Attendance_16Apr2026_I10.pdf"
    with open(pdf_path, "wb") as f:
        f.write(pdf)
    print(f"[SUCCESS] PDF created: {pdf_path}")
