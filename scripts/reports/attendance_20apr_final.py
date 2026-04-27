from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT

pdf_file = "Attendance_20Apr2026_I10.pdf"
doc = SimpleDocTemplate(pdf_file, pagesize=A4, topMargin=0.35*inch, bottomMargin=0.35*inch)
story = []

styles = getSampleStyleSheet()

# === HEADER ===
header_para = Paragraph(
    "<font size=11 color='white'><b>PEOPLE &amp; CULTURE · ATTENDANCE MONITOR</b></font>",
    styles['Normal']
)
header_table = Table([[header_para]], colWidths=[7.5*inch])
header_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#34495e")),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('LEFTPADDING', (0, 0), (-1, -1), 14),
    ('TOPPADDING', (0, 0), (-1, -1), 12),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
]))
story.append(header_table)

# === TITLE & DATE ===
title_para = Paragraph(
    "<font size=22 color='white'><b>I-10 Head Office Attendance Record</b></font>",
    styles['Normal']
)
date_para = Paragraph(
    "<font size=10 color='#b3c6d9'>20 April 2026 (Monday) · Onsite Day (Mon–Thu)</font>",
    styles['Normal']
)
title_table = Table([[title_para], [Spacer(1, 0.02*inch)], [date_para]], colWidths=[7.5*inch])
title_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#34495e")),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('LEFTPADDING', (0, 0), (-1, -1), 14),
    ('TOPPADDING', (0, 0), (-1, -1), 14),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 14),
]))
story.append(title_table)

story.append(Spacer(1, 0.12*inch))

# === STAT BOXES - NO GRID LINES ===
stat_values = ["84", "47", "6", "17", "7", "6", "1"]
stat_labels = ["Total Active", "Onsite Today", "On Leave", "WFH", "WFH Confirmed", "Additional", "Flagged"]
stat_colors = [
    colors.HexColor("#f5f5f5"),
    colors.HexColor("#e8f5e9"),
    colors.HexColor("#ffe0b2"),
    colors.HexColor("#e3f2fd"),
    colors.HexColor("#f3e5f5"),
    colors.HexColor("#f3e5f5"),
    colors.HexColor("#ffebee"),
]

stat_cells = []
for val, lbl in zip(stat_values, stat_labels):
    cell_text = f"<b><font size=16>{val}</font></b><br/><font size=9>{lbl}</font>"
    stat_cells.append(Paragraph(cell_text, ParagraphStyle('Stat', parent=styles['Normal'], alignment=TA_CENTER)))

stat_table = Table([stat_cells], colWidths=[1.07*inch]*7)
stat_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (0, 0), stat_colors[0]),
    ('BACKGROUND', (1, 0), (1, 0), stat_colors[1]),
    ('BACKGROUND', (2, 0), (2, 0), stat_colors[2]),
    ('BACKGROUND', (3, 0), (3, 0), stat_colors[3]),
    ('BACKGROUND', (4, 0), (4, 0), stat_colors[4]),
    ('BACKGROUND', (5, 0), (5, 0), stat_colors[5]),
    ('BACKGROUND', (6, 0), (6, 0), stat_colors[6]),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('TOPPADDING', (0, 0), (-1, -1), 10),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ('LEFTPADDING', (0, 0), (-1, -1), 3),
    ('RIGHTPADDING', (0, 0), (-1, -1), 3),
]))
story.append(stat_table)

story.append(Spacer(1, 0.18*inch))

# === ONSITE SECTION ===
onsite_header = Paragraph(
    "<font size=12 color='white'><b>Present Onsite — I-10 Head Office (47)</b></font>",
    styles['Normal']
)
onsite_header_table = Table([[onsite_header]], colWidths=[7.5*inch])
onsite_header_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#2e7a4f")),
    ('LEFTPADDING', (0, 0), (-1, -1), 12),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
]))
story.append(onsite_header_table)

onsite_list = [
    "Aymen", "Ayesha Raza Khan", "Javariya",
    "Taloot", "Zeshan Ali", "Babar Khan", "Zeeshan Zahoor",
    "Shoaib Khan", "Kamal",
    "Fatima Rehman", "Shoaib ud din", "Mahnoor Shafique", "Mah Noor",
    "Zeeshan Usaid", "Iqra Zanib", "Afifa", "Hareem",
    "Fatima Khan", "Muzammil Patel", "Osama Ahmed", "Jalal",
    "Mashhood", "Talha", "Aroma",
    "Jahan Zaib", "Jahanzeb Ahmed", "Omer Rana",
    "Laraib", "Zunaira", "Hammad Sarfaraz", "Mahrah",
    "Zeest", "Hassan Shehzad", "Saleh", "Saim",
    "Mehdi", "Abdul Rehman Siddiqi", "Junaid Zaidi", "Shujaan",
    "Haris", "Nimra", "Kamran", "Usman Mughal",
    "Hataf", "Ali Sipra", "Salman Ahmed", "Ahmed Javed",
    "Haroon Ali", "Tayyaba Hamna", "Mavia", "Haya", "Sabeen Fatima"
]

onsite_data = []
for i in range(0, len(onsite_list), 2):
    row = [onsite_list[i]]
    if i+1 < len(onsite_list):
        row.append(onsite_list[i+1])
    else:
        row.append("")
    onsite_data.append(row)

onsite_table = Table(onsite_data, colWidths=[3.75*inch, 3.75*inch])
onsite_table.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor("#e8f5e9")]),
]))
story.append(onsite_table)

story.append(Spacer(1, 0.12*inch))

# === ON LEAVE ===
leave_header = Paragraph(
    "<font size=12 color='white'><b>On Leave (6)</b></font>",
    styles['Normal']
)
leave_header_table = Table([[leave_header]], colWidths=[7.5*inch])
leave_header_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f57c00")),
    ('LEFTPADDING', (0, 0), (-1, -1), 12),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
]))
story.append(leave_header_table)

leave_data = [
    ["Name", "Status"],
    ["Abdur Rehman", "Annual leave"],
    ["Ahsan Javed", "Medical leave"],
    ["Muhammad Danish Iqbal", "Grant Leave — Wedding"],
    ["Ramsha Khurshid", "Medical leave"],
    ["Samra Tariq", "Medical leave"],
    ["Tariq Asim", "Grant Leave — Wedding"],
]

leave_table = Table(leave_data, colWidths=[3.75*inch, 3.75*inch])
leave_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#34495e")),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#ffe0b2")]),
]))
story.append(leave_table)

story.append(Spacer(1, 0.12*inch))

# === WFH (ANNOUNCED ON TEAMS) ===
wfh_header = Paragraph(
    "<font size=12 color='white'><b>WFH — Announced on Teams (7)</b></font>",
    styles['Normal']
)
wfh_header_table = Table([[wfh_header]], colWidths=[7.5*inch])
wfh_header_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#1565c0")),
    ('LEFTPADDING', (0, 0), (-1, -1), 12),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
]))
story.append(wfh_header_table)

wfh_data = [
    ["Name", "Status"],
    ["Rida Nayyab", "Working remotely — road situation"],
    ["Muqadas Saleem", "Working remotely"],
    ["Saima Bibi", "Working remotely"],
    ["Ramisha Riaz", "Working from H9"],
    ["Unsa Umar", "WFH this week"],
    ["amena ahmed", "Will be remote today"],
    ["Umar Raza", "Working remotely"],
]

wfh_table = Table(wfh_data, colWidths=[3.75*inch, 3.75*inch])
wfh_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#34495e")),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#e3f2fd")]),
]))
story.append(wfh_table)

story.append(Spacer(1, 0.12*inch))

# === WFH CONFIRMED ===
wfh_header = Paragraph(
    "<font size=12 color='white'><b>WFH — Confirmed (7)</b></font>",
    styles['Normal']
)
wfh_header_table = Table([[wfh_header]], colWidths=[7.5*inch])
wfh_header_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#1565c0")),
    ('LEFTPADDING', (0, 0), (-1, -1), 12),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
]))
story.append(wfh_header_table)

wfh_data = [
    ["Name", "Status"],
    ["Amina Tayyub", "Permanent remote arrangement"],
    ["Zuhaib Shaikh", "Permanent remote arrangement (on-site)"],
    ["Ajlal Hasan", "Permanent remote arrangement"],
    ["Ahwaz Akhtar", "Permanent remote arrangement"],
    ["Shayan Ahmad", "Permanent remote arrangement"],
    ["ABDUL AHAD", "Permanent remote arrangement"],
    ["Zulfiqar Ahmed Mughal", "Permanent remote arrangement"],
]

wfh_table = Table(wfh_data, colWidths=[3.75*inch, 3.75*inch])
wfh_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#34495e")),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#e3f2fd")]),
]))
story.append(wfh_table)

story.append(Spacer(1, 0.12*inch))

# === FLAGGED ===
flagged_header = Paragraph(
    "<font size=12 color='white'><b>Flagged — No Attendance Record (1)</b></font>",
    styles['Normal']
)
flagged_header_table = Table([[flagged_header]], colWidths=[7.5*inch])
flagged_header_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#c62828")),
    ('LEFTPADDING', (0, 0), (-1, -1), 12),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
]))
story.append(flagged_header_table)

flagged_data = [
    ["Name", "Status"],
    ["Muhammad Usman Javed", "No attendance record"],
]

flagged_table = Table(flagged_data, colWidths=[3.75*inch, 3.75*inch])
flagged_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#34495e")),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#ffebee")]),
]))
story.append(flagged_table)

story.append(Spacer(1, 0.12*inch))

# === AWAY ===
away_header = Paragraph(
    "<font size=12 color='white'><b>Away</b></font>",
    styles['Normal']
)
away_header_table = Table([[away_header]], colWidths=[7.5*inch])
away_header_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#7b68ee")),
    ('LEFTPADDING', (0, 0), (-1, -1), 12),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
]))
story.append(away_header_table)

away_data = [
    ["Name", "Status"],
    ["Haroon Yasin", "Away for fundraising"],
]

away_table = Table(away_data, colWidths=[3.75*inch, 3.75*inch])
away_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#34495e")),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#f0e6ff")]),
]))
story.append(away_table)

story.append(Spacer(1, 0.12*inch))

# === ADDITIONAL ===
additional_header = Paragraph(
    "<font size=12 color='white'><b>Additional in Attendance — Not OPL+OWT (6)</b></font>",
    styles['Normal']
)
additional_header_table = Table([[additional_header]], colWidths=[7.5*inch])
additional_header_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#6a1b9a")),
    ('LEFTPADDING', (0, 0), (-1, -1), 12),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
]))
story.append(additional_header_table)

additional_data = [
    ["Name", "Status"],
    ["Jawwad Ali Rizvi", "NIETE — Archived/Parked · Onsite I-10"],
    ["Hareem", "NIETE — Archived/Parked · Onsite I-10"],
    ["Hamza shahid", "NIETE — Archived/Parked · Onsite I-10"],
    ["Zain", "NIETE — Archived/Parked · Onsite I-10"],
    ["Rifat", "NIETE — Archived/Parked · Onsite I-10"],
    ["Shumaila", "NIETE — Archived/Parked · Onsite I-10"],
]

additional_table = Table(additional_data, colWidths=[3.75*inch, 3.75*inch])
additional_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#34495e")),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#f3e5f5")]),
]))
story.append(additional_table)

story.append(Spacer(1, 0.12*inch))

# === FOOTER ===
footer_text = Paragraph(
    "<font size=8 color='#999'>Taleemabad People &amp; Culture · hiring@taleemabad.com · 20 April 2026 (Monday)<br/>Compiled by Coco, Nugget &amp; Noah · People &amp; Culture AI Assistants</font>",
    ParagraphStyle('Footer', parent=styles['Normal'], alignment=TA_CENTER)
)
story.append(footer_text)

doc.build(story)
