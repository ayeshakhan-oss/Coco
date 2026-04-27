"""
Attendance Report for April 20, 2026 — I-10 Head Office
Following exact format from April 16, 2026 report
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from datetime import datetime

# === DATA ===
onsite_list = [
    "Abdul Rehman Siddiqi", "Abdur Rehman", "Afifa", "Ahmed Javed",
    "Ahsan Javed", "Ali Sipra", "Aroma", "Ayesha Raza Khan",
    "Aymen", "Babar Khan", "Fahad Rao", "Fatima Khan",
    "Fatima Rehman", "Haroon Ali", "Hassan Shehzad", "Hataf",
    "Haya", "Jahan Zaib", "Laraib", "Muhammad Omer Mazhar Rana",
    "Muhammad Shoaib Khan", "Mah Noor", "Mahnoor Shafique", "Mahrah",
    "Mashhood", "Mavia", "Muhammad Hammad Sarfraz", "Muhammad Haris",
    "Muhammad Jalal Khan", "Muhammad Kamal", "Muhammad Kamran Taj",
    "Muhammad Mehdi", "Muhammad Raees Shujaan", "Muhammad Saim",
    "Muhammad Talha", "Muhammad Usman Mughal", "Muhammad Zeeshan Usaid",
    "Osama Ahmed", "Ramisha Riaz Sheikh", "Ramsha Khurshid",
    "Rida Nayyab", "Saad Zahid", "Sabeen Fatima", "Saima Bibi",
    "Saleh", "Salman Ahmad", "Samra Tariq", "Sheikh Nimra Rasheed",
    "Shoaib Ud Din", "Syed Junaid Ali Zaidi", "Taloot", "Usman Imtiaz",
    "Zeeshan Zahoor", "Zeest", "Zeshan Ali", "Omer Rana",
    "Zunaira", "Hammad Sarfaraz", "Mehdi", "Shujaan", "Junaid Zaidi", "Haris"
]

# 57 - subtract known additional/NIETE
additional_onsite = [
    ("Jawwad Ali Rizvi", "NIETE — Archived/Parked · Onsite I-10"),
    ("Hareem", "NIETE — Archived/Parked · Onsite I-10"),
    ("Hamza shahid", "NIETE — Archived/Parked · Onsite I-10"),
    ("Zain", "NIETE — Archived/Parked · Onsite I-10"),
    ("Rifat", "NIETE — Archived/Parked · Onsite I-10"),
    ("Shumaila", "NIETE — Archived/Parked · Onsite I-10"),
]

on_leave = [
    ("Abdur Rehman", "Annual leave"),
    ("Ahsan Javed", "Medical leave"),
    ("Muhammad Danish Iqbal", "Grant Leave"),
    ("Ramsha Khurshid", "Medical leave"),
    ("Samra Tariq", "Medical leave"),
    ("Tariq Asim", "Grant Leave"),
]

wfh_confirmed = [
    ("Amina Tayyub", "Permanent remote arrangement"),
    ("Zuhaib Shaikh", "Permanent remote arrangement (on-site)"),
    ("Ajlal Hasan", "Permanent remote arrangement"),
    ("Ahwaz Akhtar", "Permanent remote arrangement"),
    ("Shayan Ahmad", "Permanent remote arrangement"),
    ("ABDUL AHAD", "Permanent remote arrangement"),
    ("Zulfiqar Ahmed Mughal", "Permanent remote arrangement"),
]

away = [
    ("Mashhood", "Away for training"),
    ("Haroon Yasin", "Away for fundraising"),
]

flagged = [
    ("Muhammad Muzzammil Patel", "No attendance record"),
    ("Muhammad Usman Javed", "No attendance record"),
    ("Unsa Umar", "No attendance record"),
]

# === COUNTS ===
total_active = 84
onsite_count = 57 - len(additional_onsite)  # 51 OPL+OWT
on_leave_count = len(on_leave)  # 6
wfh_count = 0  # No temporary WFH today
wfh_confirmed_count = len(wfh_confirmed)  # 7
away_count = len(away)  # 2
additional_count = len(additional_onsite)  # 6
flagged_count = len(flagged)  # 3

# === PDF SETUP ===
pdf_file = "Attendance_20Apr2026_I10.pdf"
doc = SimpleDocTemplate(pdf_file, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
story = []

styles = getSampleStyleSheet()
style_heading = ParagraphStyle(
    'CustomHeading',
    parent=styles['Normal'],
    fontSize=24,
    textColor=colors.HexColor("#FFFFFF"),
    spaceAfter=6,
    fontName='Helvetica-Bold',
)

style_subtitle = ParagraphStyle(
    'SubtitleStyle',
    parent=styles['Normal'],
    fontSize=11,
    textColor=colors.HexColor("#FFFFFF"),
    spaceAfter=12,
)

# Header section with dark background
header_data = [
    [Paragraph("PEOPLE & CULTURE · ATTENDANCE MONITOR", style_heading)],
]
header_table = Table(header_data, colWidths=[7.5*inch])
header_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#2c3e50")),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('LEFTPADDING', (0, 0), (-1, -1), 12),
    ('TOPPADDING', (0, 0), (-1, -1), 12),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
]))
story.append(header_table)

# Title and date section
title_data = [
    [Paragraph("I-10 Head Office Attendance Record", style_heading),
     Paragraph("20 April 2026 (Monday) · Onsite Day (Mon–Thu)", style_subtitle)],
]
title_table = Table(title_data, colWidths=[7.5*inch])
title_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#34495e")),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('LEFTPADDING', (0, 0), (-1, -1), 12),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
]))
story.append(title_table)

story.append(Spacer(1, 0.2*inch))

# Stat boxes
stat_data = [
    [
        Paragraph(f"<b>{total_active}</b><br/>Total Active", styles['Normal']),
        Paragraph(f"<b>{onsite_count}</b><br/>Onsite Today", styles['Normal']),
        Paragraph(f"<b>{on_leave_count}</b><br/>On Leave", styles['Normal']),
        Paragraph(f"<b>{wfh_count}</b><br/>WFH", styles['Normal']),
        Paragraph(f"<b>{wfh_confirmed_count}</b><br/>WFH Confirmed", styles['Normal']),
        Paragraph(f"<b>{additional_count}</b><br/>Additional", styles['Normal']),
        Paragraph(f"<b>{flagged_count}</b><br/>Flagged", styles['Normal']),
    ]
]
stat_table = Table(stat_data, colWidths=[1.05*inch]*7)
stat_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (0, 0), colors.HexColor("#f5f5f5")),
    ('BACKGROUND', (1, 0), (1, 0), colors.HexColor("#e8f5e9")),
    ('BACKGROUND', (2, 0), (2, 0), colors.HexColor("#ffe0b2")),
    ('BACKGROUND', (3, 0), (3, 0), colors.HexColor("#e3f2fd")),
    ('BACKGROUND', (4, 0), (4, 0), colors.HexColor("#f3e5f5")),
    ('BACKGROUND', (5, 0), (5, 0), colors.HexColor("#f3e5f5")),
    ('BACKGROUND', (6, 0), (6, 0), colors.HexColor("#ffebee")),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 11),
    ('TOPPADDING', (0, 0), (-1, -1), 10),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ('LEFTPADDING', (0, 0), (-1, -1), 4),
    ('RIGHTPADDING', (0, 0), (-1, -1), 4),
]))
story.append(stat_table)

story.append(Spacer(1, 0.3*inch))

# === PRESENT ONSITE ===
header_style = ParagraphStyle(
    'SectionHeader',
    parent=styles['Normal'],
    fontSize=12,
    textColor=colors.HexColor("#FFFFFF"),
    fontName='Helvetica-Bold',
)

section_header = Paragraph(f"Present Onsite — I-10 Head Office ({onsite_count})", header_style)
section_table = Table([[section_header]], colWidths=[7.5*inch])
section_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#2e7a4f")),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('LEFTPADDING', (0, 0), (-1, -1), 12),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
]))
story.append(section_table)

# Onsite names in 2-column layout
onsite_filtered = [n for n in onsite_list if n not in [x[0] for x in additional_onsite]]
onsite_data = []
for i in range(0, len(onsite_filtered), 2):
    row = [onsite_filtered[i]]
    if i+1 < len(onsite_filtered):
        row.append(onsite_filtered[i+1])
    else:
        row.append("")
    onsite_data.append(row)

onsite_table = Table(onsite_data, colWidths=[3.75*inch, 3.75*inch])
onsite_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#e8f5e9")),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#ddd")),
]))
story.append(onsite_table)

story.append(Spacer(1, 0.2*inch))

# === ON LEAVE ===
leave_header = Paragraph("On Leave (6)", header_style)
leave_table_header = Table([[leave_header]], colWidths=[7.5*inch])
leave_table_header.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f57c00")),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('LEFTPADDING', (0, 0), (-1, -1), 12),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
]))
story.append(leave_table_header)

leave_data = [["Name", "Status"]] + list(on_leave)
leave_details = Table(leave_data, colWidths=[3.75*inch, 3.75*inch])
leave_details.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2c3e50")),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor("#FFFFFF")),
    ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#ffe0b2")),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#ddd")),
]))
story.append(leave_details)

story.append(Spacer(1, 0.2*inch))

# === AWAY ===
if away:
    away_header = Paragraph("Away (2)", header_style)
    away_table_header = Table([[away_header]], colWidths=[7.5*inch])
    away_table_header.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#ff9800")),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(away_table_header)

    away_data = [["Name", "Status"]] + list(away)
    away_details = Table(away_data, colWidths=[3.75*inch, 3.75*inch])
    away_details.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2c3e50")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor("#FFFFFF")),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#ffe0b2")),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#ddd")),
    ]))
    story.append(away_details)

    story.append(Spacer(1, 0.2*inch))

# === WFH CONFIRMED ===
wfh_header = Paragraph("WFH — Confirmed (7)", header_style)
wfh_table_header = Table([[wfh_header]], colWidths=[7.5*inch])
wfh_table_header.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#1565c0")),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('LEFTPADDING', (0, 0), (-1, -1), 12),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
]))
story.append(wfh_table_header)

wfh_data = [["Name", "Status"]] + list(wfh_confirmed)
wfh_details = Table(wfh_data, colWidths=[3.75*inch, 3.75*inch])
wfh_details.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2c3e50")),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor("#FFFFFF")),
    ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#e3f2fd")),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#ddd")),
]))
story.append(wfh_details)

story.append(Spacer(1, 0.2*inch))

# === FLAGGED ===
flagged_header = Paragraph("Flagged — No Attendance Record (3)", header_style)
flagged_table_header = Table([[flagged_header]], colWidths=[7.5*inch])
flagged_table_header.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#c62828")),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('LEFTPADDING', (0, 0), (-1, -1), 12),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
]))
story.append(flagged_table_header)

flagged_data = [["Name", "Status"]] + list(flagged)
flagged_details = Table(flagged_data, colWidths=[3.75*inch, 3.75*inch])
flagged_details.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2c3e50")),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor("#FFFFFF")),
    ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#ffebee")),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#ddd")),
]))
story.append(flagged_details)

story.append(Spacer(1, 0.2*inch))

# === ADDITIONAL ===
additional_header = Paragraph("Additional in Attendance — Not OPL+OWT (6)", header_style)
additional_table_header = Table([[additional_header]], colWidths=[7.5*inch])
additional_table_header.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#6a1b9a")),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('LEFTPADDING', (0, 0), (-1, -1), 12),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
]))
story.append(additional_table_header)

additional_data = [["Name", "Status"]] + list(additional_onsite)
additional_details = Table(additional_data, colWidths=[3.75*inch, 3.75*inch])
additional_details.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2c3e50")),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor("#FFFFFF")),
    ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#f3e5f5")),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#ddd")),
]))
story.append(additional_details)

story.append(Spacer(1, 0.3*inch))

# Footer
footer_style = ParagraphStyle(
    'Footer',
    parent=styles['Normal'],
    fontSize=8,
    textColor=colors.HexColor("#666"),
    alignment=1,
)
footer = Paragraph("Taleemabad People & Culture · hiring@taleemabad.com · 20 April 2026 (Monday)<br/>Compiled by Coco, Nugget & Noah · People & Culture AI Assistants", footer_style)
story.append(footer)

# Build PDF
doc.build(story)
print(f"PDF generated: {pdf_file}")
