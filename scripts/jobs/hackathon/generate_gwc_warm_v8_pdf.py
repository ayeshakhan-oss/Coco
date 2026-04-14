"""
Generate GWC Warm Tone PDF with v8 Email Template Format
Blue header, proper styling, Georgia serif, matching email design
"""
import os, sys
sys.path.insert(0, "c:/Agent Coco")

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT

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
    ("Ali Jawad", "ali.jawad6204@gmail.com", "We enjoyed meeting you - and here's what we saw", ali_body),
    ("Umair Solangi", "bscs2112203@szabist.pk", "Your foundation is strong - here's what we saw", umair_body),
    ("Sultan Muhammad Hamad Sheharyar", "pirzadahammadzakori@gmail.com", "Your curiosity is a strength - here's what we learned about you", sultan_body),
]

# Create PDF
pdf_path = "c:/Agent Coco/scripts/jobs/hackathon/GWC_Warm_Tone_v8_Format.pdf"
doc = SimpleDocTemplate(pdf_path, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.75*inch, leftMargin=0.75*inch, rightMargin=0.75*inch)

# Styles
styles = getSampleStyleSheet()

# v8 Header style
header_style = ParagraphStyle(
    'HeaderStyle',
    parent=styles['Normal'],
    fontSize=11,
    textColor=colors.HexColor('#1565c0'),
    alignment=TA_CENTER,
    fontName='Helvetica-Bold',
    letterSpacing=2,
    spaceAfter=4
)

subject_style = ParagraphStyle(
    'SubjectStyle',
    parent=styles['Heading2'],
    fontSize=14,
    textColor=colors.HexColor('#1565c0'),
    fontName='Helvetica-Bold',
    alignment=TA_CENTER,
    spaceAfter=2
)

role_style = ParagraphStyle(
    'RoleStyle',
    parent=styles['Normal'],
    fontSize=10,
    textColor=colors.HexColor('#5c85c7'),
    alignment=TA_CENTER,
    spaceAfter=12
)

candidate_style = ParagraphStyle(
    'CandidateName',
    parent=styles['Heading2'],
    fontSize=12,
    textColor=colors.HexColor('#1565c0'),
    spaceAfter=2,
    spaceBefore=18,
    fontName='Helvetica-Bold'
)

email_meta_style = ParagraphStyle(
    'Meta',
    parent=styles['Normal'],
    fontSize=9,
    textColor=colors.HexColor('#666'),
    spaceAfter=12,
)

email_body_style = ParagraphStyle(
    'EmailBody',
    parent=styles['Normal'],
    fontSize=10,
    alignment=TA_JUSTIFY,
    spaceAfter=10,
    leading=15,
    fontFamily='Georgia'
)

heading_style = ParagraphStyle(
    'EmailHeading',
    parent=styles['Heading3'],
    fontSize=11,
    textColor=colors.HexColor('#1565c0'),
    spaceAfter=8,
    spaceBefore=12,
    fontName='Helvetica-Bold'
)

# Build story
story = []

for i, (name, email_addr, subject, body) in enumerate(emails):
    # v8 Header Band
    header_data = [
        [Paragraph("PEOPLE &amp; CULTURE &nbsp;&bull;&nbsp; REJECTION DECISION", header_style)],
        [Paragraph(subject, subject_style)],
        [Paragraph("Hackathon 2026", role_style)],
    ]
    header_table = Table(header_data, colWidths=[7.5*inch])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f0f4f0')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 28),
        ('RIGHTPADDING', (0, 0), (-1, -1), 28),
        ('TOPPADDING', (0, 0), (-1, -1), 20),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 20),
        ('BORDER', (0, 0), (-1, -1), 2, colors.HexColor('#1565c0')),
        ('ROUNDED', (0, 0), (-1, -1), 8),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 0.2*inch))

    # Candidate name and email
    story.append(Paragraph(name, candidate_style))
    story.append(Paragraph(email_addr, email_meta_style))

    # Email body with headings
    paragraphs = body.split("\n\n")
    for para_text in paragraphs:
        para = para_text.strip()
        if para.startswith("**") and para.endswith("**"):
            heading = para.replace("**", "")
            story.append(Paragraph(heading, heading_style))
        elif para:
            story.append(Paragraph(para, email_body_style))

    # Footer
    story.append(Spacer(1, 0.3*inch))
    footer_text = Paragraph("Warm regards,<br/><strong>People and Culture Team</strong><br/><strong>Taleemabad</strong><br/>hiring@taleemabad.com | www.taleemabad.com<br/><i>Sent on behalf of Talent Acquisition Team by Coco</i>", email_meta_style)
    story.append(footer_text)

    if i < len(emails) - 1:
        story.append(PageBreak())

doc.build(story)
print(f"[OK] PDF generated with v8 format: {pdf_path}")
