"""
Generate GWC Warm Tone PDF - EXACT Email Template Format
Logo, header, yellow position box, horizontal line, body text
"""
import os, sys
sys.path.insert(0, "c:/Agent Coco")

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY

# Read warm tone emails
def extract_email_body(filepath):
    with open(filepath, "r") as f:
        content = f.read()
    parts = content.split("---")
    if len(parts) >= 2:
        return parts[1].strip()
    return content

ali_body = extract_email_body("c:/Agent Coco/scripts/jobs/hackathon/ali_jawad_warm_800.txt")
umair_body = extract_email_body("c:/Agent Coco/scripts/jobs/hackathon/umair_solangi_warm_800.txt")
sultan_body = extract_email_body("c:/Agent Coco/scripts/jobs/hackathon/sultan_sheharyar_warm_800.txt")

emails = [
    ("Ali Jawad", ali_body),
    ("Umair Solangi", umair_body),
    ("Sultan Muhammad Hamad Sheharyar", sultan_body),
]

# Create PDF
pdf_path = "c:/Agent Coco/scripts/jobs/hackathon/GWC_Warm_Tone_Exact_Format.pdf"
doc = SimpleDocTemplate(pdf_path, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.75*inch, leftMargin=0.75*inch, rightMargin=0.75*inch)

# Styles
styles = getSampleStyleSheet()

header_style = ParagraphStyle(
    'HeaderText',
    parent=styles['Normal'],
    fontSize=9,
    textColor=colors.HexColor('#1565c0'),
    alignment=TA_CENTER,
    letterSpacing=1,
    spaceAfter=6
)

position_style = ParagraphStyle(
    'PositionStyle',
    parent=styles['Normal'],
    fontSize=12,
    textColor=colors.HexColor('#1565c0'),
    fontName='Helvetica-Bold',
    alignment=TA_CENTER,
    spaceAfter=0
)

greeting_style = ParagraphStyle(
    'Greeting',
    parent=styles['Normal'],
    fontSize=11,
    fontFamily='Georgia',
    spaceAfter=12,
    leading=16
)

body_style = ParagraphStyle(
    'BodyText',
    parent=styles['Normal'],
    fontSize=11,
    alignment=TA_JUSTIFY,
    fontFamily='Georgia',
    spaceAfter=12,
    leading=16
)

heading_style = ParagraphStyle(
    'Heading',
    parent=styles['Normal'],
    fontSize=11,
    fontFamily='Georgia',
    fontName='Helvetica-Bold',
    textColor=colors.HexColor('#1565c0'),
    spaceAfter=8,
    spaceBefore=12
)

logo_path = "c:/Agent Coco/assets/logo_taleemabad.png"

# Build story
story = []

for i, (name, body) in enumerate(emails):
    # Logo
    if os.path.exists(logo_path):
        img = Image(logo_path, width=0.8*inch, height=0.8*inch)
        story.append(img)
        story.append(Spacer(1, 0.1*inch))

    # Header
    story.append(Paragraph("PEOPLE &amp; CULTURE • REJECTION DECISION", header_style))
    story.append(Spacer(1, 0.08*inch))

    # Yellow Position Box
    pos_table = Table([
        [Paragraph(f"Hackathon 2026", position_style)]
    ], colWidths=[7*inch])
    pos_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#FDD835')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('BORDER', (0, 0), (-1, -1), 0),
    ]))
    story.append(pos_table)
    story.append(Spacer(1, 0.08*inch))

    # Horizontal line
    line_table = Table([[""]], colWidths=[7*inch])
    line_table.setStyle(TableStyle([
        ('LINEBELOW', (0, 0), (-1, 0), 2, colors.HexColor('#333333')),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(line_table)
    story.append(Spacer(1, 0.15*inch))

    # Greeting
    story.append(Paragraph(f"Hi {name.split()[0]},", greeting_style))

    # Body paragraphs
    paragraphs = body.split("\n\n")
    for para_text in paragraphs:
        para = para_text.strip()
        if para.startswith("**") and para.endswith("**"):
            heading = para.replace("**", "")
            story.append(Paragraph(heading, heading_style))
        elif para:
            story.append(Paragraph(para, body_style))

    if i < len(emails) - 1:
        story.append(PageBreak())

doc.build(story)
print(f"[OK] PDF generated with exact format: {pdf_path}")
