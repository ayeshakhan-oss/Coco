"""
Generate GWC rejection PDF - proper extraction and formatting
"""
import os, sys
sys.path.insert(0, "c:/Agent Coco")

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY

# Read and extract email bodies properly
def extract_email_body(filepath):
    with open(filepath, "r") as f:
        content = f.read()
    # Split on "---" separator and get content after it
    parts = content.split("---")
    if len(parts) >= 2:
        return parts[1].strip()
    return content

ali_body = extract_email_body("c:/Agent Coco/scripts/jobs/hackathon/ali_jawad_800words.txt")
umair_body = extract_email_body("c:/Agent Coco/scripts/jobs/hackathon/umair_800words.txt")
sultan_body = extract_email_body("c:/Agent Coco/scripts/jobs/hackathon/sultan_800words.txt")

# Email metadata
emails = [
    ("Ali Jawad", "ali.jawad6204@gmail.com", ali_body),
    ("Umair Solangi", "bscs2112203@szabist.pk", umair_body),
    ("Sultan Muhammad Hamad Sheharyar", "pirzadahammadzakori@gmail.com", sultan_body),
]

# Create PDF
pdf_path = "c:/Agent Coco/scripts/jobs/hackathon/GWC_Three_Candidates_Pilot.pdf"
doc = SimpleDocTemplate(pdf_path, pagesize=letter, topMargin=0.75*inch, bottomMargin=0.75*inch, leftMargin=0.75*inch, rightMargin=0.75*inch)

# Styles
styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    'Title',
    parent=styles['Heading1'],
    fontSize=14,
    textColor=colors.HexColor('#1565c0'),
    spaceAfter=4,
    fontName='Helvetica-Bold'
)

candidate_style = ParagraphStyle(
    'CandidateName',
    parent=styles['Heading2'],
    fontSize=12,
    textColor=colors.HexColor('#1565c0'),
    spaceAfter=2,
    fontName='Helvetica-Bold'
)

email_meta_style = ParagraphStyle(
    'Meta',
    parent=styles['Normal'],
    fontSize=9,
    textColor=colors.HexColor('#666'),
    spaceAfter=10,
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

# Build story
story = []

# Add each email
for i, (name, email_addr, body) in enumerate(emails):
    # Candidate header
    story.append(Paragraph(name, candidate_style))
    story.append(Paragraph(email_addr, email_meta_style))

    # Email body - break into paragraphs
    paragraphs = body.split("\n\n")
    for para_text in paragraphs:
        if para_text.strip():
            story.append(Paragraph(para_text.strip(), email_body_style))

    # Page break between candidates
    if i < len(emails) - 1:
        story.append(PageBreak())

# Build PDF
doc.build(story)
print(f"[OK] PDF generated correctly: {pdf_path}")
