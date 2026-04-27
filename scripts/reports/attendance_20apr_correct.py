from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT

pdf_file = "Attendance_20Apr2026_I10.pdf"
doc = SimpleDocTemplate(pdf_file, pagesize=A4, topMargin=0.4*inch, bottomMargin=0.4*inch)
story = []

styles = getSampleStyleSheet()

# === HEADER ===
header_para = Paragraph(
    "<font size=12 color='white'><b>PEOPLE &amp; CULTURE · ATTENDANCE MONITOR</b></font>",
    styles['Normal']
)
header_table = Table([[header_para]], colWidths=[7.5*inch])
header_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#2c3e50")),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('LEFTPADDING', (0, 0), (-1, -1), 14),
    ('TOPPADDING', (0, 0), (-1, -1), 10),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
]))
story.append(header_table)

# === TITLE & DATE ===
title_para = Paragraph(
    "<font size=20 color='white'><b>I-10 Head Office Attendance Record</b></font>",
    styles['Normal']
)
date_para = Paragraph(
    "<font size=11 color='white'>20 April 2026 (Monday) · Onsite Day (Mon–Thu)</font>",
    styles['Normal']
)
title_table = Table([[title_para], [date_para]], colWidths=[7.5*inch])
title_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#34495e")),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('LEFTPADDING', (0, 0), (-1, -1), 14),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
]))
story.append(title_table)

story.append(Spacer(1, 0.18*inch))

# === STAT BOXES (7 boxes) - April 20 actual data ===
stat_values = ["84", "51", "6", "11", "7", "6", "3"]
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
for val, lbl, col in zip(stat_values, stat_labels, stat_colors):
    cell_text = f"<b><font size=18>{val}</font></b><br/><font size=9>{lbl}</font>"
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
    ('TOPPADDING', (0, 0), (-1, -1), 12),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ('LEFTPADDING', (0, 0), (-1, -1), 2),
    ('RIGHTPADDING', (0, 0), (-1, -1), 2),
]))
story.append(stat_table)

story.append(Spacer(1, 0.25*inch))

# === ONSITE SECTION - 51 OPL+OWT (excluding 6 NIETE) ===
onsite_header = Paragraph(
    "<font size=12 color='white'><b>Present Onsite — I-10 Head Office (51)</b></font>",
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

# 51 OPL+OWT on-site from the user's 57, excluding 6 NIETE
onsite_list = [
    "Abdul Rehman Siddiqi", "Abdur Rehman", "Afifa", "Ahmed Javed",
    "Ahsan Javed", "Ali Sipra", "Aroma", "Ayesha Raza Khan",
    "Aymen", "Babar Khan", "Fahad Rao", "Fatima Khan",
    "Fatima Rehman", "Haroon Ali", "Hassan Shehzad", "Hataf",
    "Haya", "Jahan Zaib", "Laraib", "Muhammad Omer Mazhar Rana",
    "Muhammad Shoaib Khan", "Mah Noor", "Mahnoor Shafique", "Mahrah",
    "Mavia", "Muhammad Hammad Sarfraz", "Muhammad Haris", "Muhammad Jalal Khan",
    "Muhammad Kamal", "Muhammad Kamran Taj", "Muhammad Mehdi", "Muhammad Raees Shujaan",
    "Muhammad Saim", "Muhammad Talha", "Muhammad Usman Mughal", "Muhammad Zeeshan Usaid",
    "Osama Ahmad", "Ramisha Riaz Sheikh", "Ramsha Khurshid", "Rida Nayyab",
    "Saad Zahid", "Sabeen Fatima", "Saima Bibi", "Saleh",
    "Salman Ahmad", "Samra Tariq", "Sheikh Nimra Rasheed", "Shoaib Ud Din",
    "Syed Junaid Ali Zaidi", "Taloot", "Usman Imtiaz", "Zeeshan Zahoor", "Zeest", "Zeshan Ali"
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
onsite_style = [
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('LEFTPADDING', (0, 0), (-1, -1), 10),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor("#ddd")),
]
for i in range(len(onsite_data)):
    if i % 2 == 1:
        onsite_style.append(('BACKGROUND', (0, i), (-1, i), colors.HexColor("#e8f5e9")))
    else:
        onsite_style.append(('BACKGROUND', (0, i), (-1, i), colors.white))
onsite_table.setStyle(TableStyle(onsite_style))
story.append(onsite_table)

story.append(Spacer(1, 0.18*inch))

# === ON LEAVE - 6 people ===
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
leave_style = [
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2c3e50")),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('LEFTPADDING', (0, 0), (-1, -1), 10),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor("#ddd")),
]
for i in range(1, len(leave_data)):
    if i % 2 == 1:
        leave_style.append(('BACKGROUND', (0, i), (-1, i), colors.HexColor("#ffe0b2")))
    else:
        leave_style.append(('BACKGROUND', (0, i), (-1, i), colors.white))
leave_table.setStyle(TableStyle(leave_style))
story.append(leave_table)

story.append(Spacer(1, 0.18*inch))

# === WFH CONFIRMED - 7 people ===
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
wfh_style = [
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2c3e50")),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('LEFTPADDING', (0, 0), (-1, -1), 10),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor("#ddd")),
]
for i in range(1, len(wfh_data)):
    if i % 2 == 1:
        wfh_style.append(('BACKGROUND', (0, i), (-1, i), colors.HexColor("#e3f2fd")))
    else:
        wfh_style.append(('BACKGROUND', (0, i), (-1, i), colors.white))
wfh_table.setStyle(TableStyle(wfh_style))
story.append(wfh_table)

story.append(Spacer(1, 0.18*inch))

# === FLAGGED - 3 people ===
flagged_header = Paragraph(
    "<font size=12 color='white'><b>Flagged — No Attendance Record (3)</b></font>",
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
    ["Muhammad Muzzammil Patel", "No attendance record"],
    ["Muhammad Usman Javed", "No attendance record"],
    ["Unsa Umar", "No attendance record"],
]

flagged_table = Table(flagged_data, colWidths=[3.75*inch, 3.75*inch])
flagged_style = [
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2c3e50")),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('LEFTPADDING', (0, 0), (-1, -1), 10),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor("#ddd")),
]
for i in range(1, len(flagged_data)):
    if i % 2 == 1:
        flagged_style.append(('BACKGROUND', (0, i), (-1, i), colors.HexColor("#ffebee")))
    else:
        flagged_style.append(('BACKGROUND', (0, i), (-1, i), colors.white))
flagged_table.setStyle(TableStyle(flagged_style))
story.append(flagged_table)

story.append(Spacer(1, 0.18*inch))

# === ADDITIONAL - 6 NIETE people ===
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
additional_style = [
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2c3e50")),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('LEFTPADDING', (0, 0), (-1, -1), 10),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor("#ddd")),
]
for i in range(1, len(additional_data)):
    if i % 2 == 1:
        additional_style.append(('BACKGROUND', (0, i), (-1, i), colors.HexColor("#f3e5f5")))
    else:
        additional_style.append(('BACKGROUND', (0, i), (-1, i), colors.white))
additional_table.setStyle(TableStyle(additional_style))
story.append(additional_table)

story.append(Spacer(1, 0.2*inch))

# === FOOTER ===
footer_text = Paragraph(
    "<font size=8 color='#666'>Taleemabad People &amp; Culture · hiring@taleemabad.com · 20 April 2026 (Monday)<br/>Compiled by Coco, Nugget &amp; Noah · People &amp; Culture AI Assistants</font>",
    ParagraphStyle('Footer', parent=styles['Normal'], alignment=TA_CENTER)
)
story.append(footer_text)

doc.build(story)
print("Report complete")
