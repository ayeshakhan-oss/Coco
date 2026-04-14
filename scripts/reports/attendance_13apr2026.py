"""I-10 Head Office Attendance Record — 13 April 2026 (Monday)"""
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

DATE = "13 April 2026 (Monday)"

# All 84 OPL+OWT employees (payroll)
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

PAYROLL_TOTAL = 88

# User-provided on-site list for Monday, 13 April 2026 (59 active employees - removed 7 archived/parked)
ONSITE = [
    "MUHAMMAD OMER MAZHAR RANA", "Afifa Sultana", "Saima Bibi", "Ahmed Javed", "Salman Iqbal", "Samra Tariq",
    "Abdul Rehman Siddiqi", "Ayesha Raza Khan", "Muhammad Kamal", "Saleh Muhammad", "Iqra Zanib",
    "Ali Sipra", "Hataf Bin Atif", "Mashhood Ali Rastgar", "Aroma Tahir", "Amena Ahmed", "Fahad Rao",
    "Saad Zahid", "Muhammad Haris", "Mahrah Ashraf", "Zunaira Shahid", "Muhammad Jalal Khan", "Aymen Abid",
    "Javariya Mufarrakh", "Mah Noor", "Fatima Rahman", "Ahsan Javed", "Salman Ahmad", "Osama Ahmad",
    "Jahanzeb Ahmad", "Haroon Ali", "Taloot Ahmad Malik", "Zeshan Ali", "Hassan Shahzad", "Muhammad Talha",
    "Haya Abid", "Muqadas Saleem", "Muhammad Usman Mughal", "Muhammad Muzzammil Patel", "Haroon Ali",
    "Shoaib Ud Din", "Muhammad Umar Raza", "Muhammad Kamran Taj", "Muhammad Hammad Sarfraz", "Laraib Sarfraz",
    "JAHAN ZAIB", "Muhammad Raees Shujaan Azhar", "Fatima Khan", "Mahnoor Shafique", "Unsa Umar",
    "Ahmed Javed", "Sheikh Nimra Rasheed", "Muhammad Mehdi Abbas", "Zeeshan Zahoor", "MUHAMMAD SHOAIB KHAN",
    "Babar Khan", "Ramisha Riaz Sheikh", "Rida Nayyab", "Sabeen Fatima", "Muhammad Zeeshan Usaid",
    "Muhammad Saim"
]

# Teams updates for 13 April 2026
ARRIVING_LATER = [
    ("Hassan Shahzad", "Traveling - Will reach office around 11:30"),
    ("Osama Ahmad", "Traveling - Will join office after 1pm"),
    ("Abdur Rehman", "Joining in second half today"),
]

ON_LEAVE = [
    ("Gul Perwasha Cheema", "On visit to Lahore - Limited availability this week"),
    ("Mavia ", "Annual Leave — Me-Time (Apr 1–15) · Approved on Markaz"),
    ("Muhammad Danish Iqbal", "Grant Leave — Wedding (Mar 24–Apr 24) · Approved on Markaz"),
    ("Tariq Asim", "Grant Leave — Wedding (Apr 1–30) · Approved on Markaz"),
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

WFH_NO_MARKAZ = []
OUT_OF_OFFICE = []
REMOTE = []

# Compute accounting
accounted = set(
    [n for n in ONSITE] +
    [ln[0] for ln in ON_LEAVE] +
    [w[0] for w in WFH_NO_MARKAZ] +
    [pwfh[0] for pwfh in PERMANENT_WFH] +
    [r[0] for r in REMOTE] +
    [o[0] for o in OUT_OF_OFFICE] +
    [al[0] for al in ARRIVING_LATER]
)

FLAGGED_NOTES = {
    "Mavia ": "No sign-in",
    "Muhammad Danish Iqbal": "No sign-in",
    "Syed Junaid Ali Zaidi": "No sign-in",
    "Tariq Asim": "No sign-in",
    "Razia Kausar": "No sign-in",
    "Iffat Maab Akhtar": "No sign-in - RWP Team",
    "Muhammad Usman Javed": "No sign-in - No Markaz record",
    "Raheela Akhtar": "No sign-in - RWP Team",
    "Sohaib Danish": "No sign-in - RWP Team",
    "Summaya Shakur": "No sign-in - RWP Team",
    "Syed Zaamin Abbas": "No sign-in - No Markaz record",
    "Tehniat Taqdees Masood": "No sign-in - RWP Team",
    "Alishba Anam": "No sign-in",
}

FLAGGED = [(name, FLAGGED_NOTES.get(name, "No sign-in - No Markaz record"))
           for name in ALL_PAYROLL if name not in accounted]

onsite_list = [n for n in ONSITE if n not in [ln[0] for ln in ON_LEAVE] +
               [w[0] for w in WFH_NO_MARKAZ] + [pwfh[0] for pwfh in PERMANENT_WFH] +
               [r[0] for r in REMOTE] + [o[0] for o in OUT_OF_OFFICE] + [al[0] for al in ARRIVING_LATER]]

# Counts
TOTAL        = PAYROLL_TOTAL
ONSITE_COUNT = len(onsite_list)
ON_LEAVE_CNT = len(ON_LEAVE)
WFH_CNT      = len(WFH_NO_MARKAZ)
PERMANENT_WFH_CNT = len(PERMANENT_WFH)
ARRIVING_LATER_CNT = len(ARRIVING_LATER)
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
    story.append(Spacer(1, 8*mm))

    # Stat Boxes
    stats = [
        (str(TOTAL), "Total Active", LGREY),
        (str(ONSITE_COUNT), "Onsite Today", LGREEN),
        (str(ON_LEAVE_CNT), "On Leave", LAMBER),
        (str(WFH_CNT), "WFH", LBROWN),
        (str(PERMANENT_WFH_CNT), "WFH Confirmed", LBLUE),
        (str(ARRIVING_LATER_CNT), "Arriving Later", colors.HexColor("#fffde7")),
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

    # Onsite Section
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

    # Make Section Helper
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

    if ARRIVING_LATER_CNT > 0:
        make_section(f"Arriving Later — Teams Update ({ARRIVING_LATER_CNT})", AMBER, ARRIVING_LATER, LAMBER, WHITE)
    if ON_LEAVE_CNT > 0:
        make_section(f"On Leave ({ON_LEAVE_CNT})", AMBER, ON_LEAVE, LAMBER, WHITE)
    if WFH_CNT > 0:
        make_section(f"Working From Home ({WFH_CNT})", BROWN, WFH_NO_MARKAZ, LBROWN, WHITE)
    if PERMANENT_WFH_CNT > 0:
        make_section(f"WFH — Confirmed ({PERMANENT_WFH_CNT})", BLUE, PERMANENT_WFH, LBLUE, WHITE)
    if FLAGGED_CNT > 0:
        make_section(f"Flagged — No Attendance Record ({FLAGGED_CNT})", RED, FLAGGED, LRED, WHITE)

    # Notes Section
    story.append(Spacer(1, 8*mm))
    notes_header = Table([[Paragraph("NOTES — EMPLOYEE RECONCILIATION", styles['h2'])]], colWidths=[180*mm])
    notes_header.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), NAVY),
        ("PADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING", (0,0), (-1,-1), 10),
    ]))
    story.append(notes_header)
    story.append(Spacer(1, 4*mm))

    # Build notes content with better formatting
    notes_content = []
    notes_content.append(Paragraph("<b>Attendance Reconciliation — Total 91 People</b>", ParagraphStyle("notesTitle", fontSize=8, leading=10, textColor=colors.HexColor("#333333"), spaceAfter=4, fontName="Helvetica-Bold")))
    notes_content.append(Paragraph("Active OPL+OWT Employees: <b>88</b>", ParagraphStyle("notesCount", fontSize=8, leading=10, textColor=colors.HexColor("#1a7a4a"), spaceAfter=2, fontName="Helvetica-Bold")))
    notes_content.append(Spacer(1, 3*mm))

    notes_content.append(Paragraph("<b>7 Archived/Separated Employees—Parked in NIETE entity:</b>", ParagraphStyle("notesSubtitle", fontSize=8, leading=10, textColor=colors.HexColor("#333333"), spaceAfter=3, fontName="Helvetica-Bold")))

    archived_names = [
        "Umama Gul Siddiqui",
        "Shumaila Aslam",
        "Jawwad Ali",
        "QURAT UL AIN",
        "Hareem Fatima",
        "Humna Tayaba",
        "Momina Raja"
    ]

    for name in archived_names:
        notes_content.append(Paragraph(f"• <b>{name}</b>", ParagraphStyle("notesBullet", fontSize=8, leading=9, leftIndent=10, textColor=colors.HexColor("#333333"), spaceAfter=1)))

    notes_content.append(Spacer(1, 4*mm))
    notes_content.append(Paragraph("<b>Additional People in Attendance (Not OPL+OWT):</b>", ParagraphStyle("notesSubtitle2", fontSize=8, leading=10, textColor=colors.HexColor("#333333"), spaceAfter=3, fontName="Helvetica-Bold")))
    notes_content.append(Paragraph("• <b>Sabeena Abbasi</b> — Taleemabad Inc. (WFH Confirmed)", ParagraphStyle("notesBullet", fontSize=8, leading=9, leftIndent=10, textColor=colors.HexColor("#333333"), spaceAfter=1)))
    notes_content.append(Paragraph("• <b>Zeest Hassan Qureshi</b> — Unassigned Entity (WFH Confirmed)", ParagraphStyle("notesBullet", fontSize=8, leading=9, leftIndent=10, textColor=colors.HexColor("#333333"), spaceAfter=1)))
    notes_content.append(Paragraph("• <b>Haroon Yasin</b> — Away for Fundraising", ParagraphStyle("notesBullet", fontSize=8, leading=9, leftIndent=10, textColor=colors.HexColor("#c62828"), spaceAfter=1, fontName="Helvetica-Bold")))

    notes_content.append(Spacer(1, 4*mm))
    notes_content.append(Paragraph("<b>Summary: 88 (Active OPL+OWT) + 3 (Other) = 91 Total in Attendance</b>", ParagraphStyle("notesSummary", fontSize=8, leading=10, textColor=colors.HexColor("#1a2a3a"), fontName="Helvetica-Bold", spaceAfter=2, borderPadding=5)))

    notes_box = Table([[notes_content]], colWidths=[170*mm])
    notes_box.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#f9f9f9")),
        ("BORDER", (0,0), (-1,-1), 0.5, GREY),
        ("PADDING", (0,0), (-1,-1), 10),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
    ]))
    story.append(notes_box)

    # Footer
    story.append(Spacer(1, 6*mm))
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

if __name__ == "__main__":
    print("Building PDF...")
    pdf = build_pdf()
    os.makedirs("output", exist_ok=True)
    pdf_path = "output/Attendance_Record_13Apr2026.pdf"
    with open(pdf_path, "wb") as f:
        f.write(pdf)
    print(f"PDF generated: {pdf_path}")
    print(f"Stats: Onsite={ONSITE_COUNT}, Arriving Later={ARRIVING_LATER_CNT}, On Leave={ON_LEAVE_CNT}, WFH Confirmed={PERMANENT_WFH_CNT}, Flagged={FLAGGED_CNT}")
