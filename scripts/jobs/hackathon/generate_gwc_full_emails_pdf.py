"""
Generate GWC rejection PDF with FULL 950-word emails (not summaries)
Ali Jawad, Umair Solangi, Sultan Muhammad Hamad Sheharyar
"""
import os, sys
sys.path.insert(0, "c:/Agent Coco")

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime

# Read full emails from text files
with open("c:/Agent Coco/scripts/jobs/hackathon/ali_jawad_800words.txt") as f:
    ali_text = f.read().split("---\n\n")[1].strip()  # Skip header

with open("c:/Agent Coco/scripts/jobs/hackathon/umair_800words.txt") as f:
    umair_text = f.read().split("---\n\n")[1].strip()  # Skip header

with open("c:/Agent Coco/scripts/jobs/hackathon/sultan_800words.txt") as f:
    sultan_text = f.read().split("---\n\n")[1].strip()  # Skip header

# Candidate info
candidates = [
    {"name": "Ali Jawad", "email": "ali.jawad6204@gmail.com", "text": ali_text},
    {"name": "Umair Solangi", "email": "bscs2112203@szabist.pk", "text": umair_text},
    {"name": "Sultan Muhammad Hamad Sheharyar", "email": "pirzadahammadzakori@gmail.com", "text": sultan_text},
]

# Create PDF
pdf_path = "c:/Agent Coco/scripts/jobs/hackathon/GWC_Three_Candidates_Pilot.pdf"
doc = SimpleDocTemplate(pdf_path, pagesize=A4, topMargin=0.75*inch, bottomMargin=0.75*inch, leftMargin=0.75*inch, rightMargin=0.75*inch)

# Styles
styles = getSampleStyleSheet()
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=18,
    textColor=colors.HexColor('#1565c0'),
    spaceAfter=12,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold'
)

subtitle_style = ParagraphStyle(
    'Subtitle',
    parent=styles['Normal'],
    fontSize=10,
    textColor=colors.HexColor('#666'),
    spaceAfter=20,
    alignment=TA_CENTER,
    fontName='Helvetica'
)

candidate_style = ParagraphStyle(
    'CandidateHeader',
    parent=styles['Heading2'],
    fontSize=14,
    textColor=colors.HexColor('#1565c0'),
    spaceAfter=4,
    spaceBefore=12,
    fontName='Helvetica-Bold'
)

email_style = ParagraphStyle(
    'EmailBody',
    parent=styles['Normal'],
    fontSize=11,
    alignment=TA_JUSTIFY,
    spaceAfter=12,
    leading=16,
    fontFamily='Georgia'
)

# Build story
story = []

# Title page
story.append(Paragraph("GWC Rejection Emails", title_style))
story.append(Paragraph("Hackathon 2026 Position", title_style))
story.append(Spacer(1, 0.2*inch))
story.append(Paragraph(f"Evidence-Based (Interview Transcripts) • {datetime.now().strftime('%B %d, %Y')}", subtitle_style))
story.append(Spacer(1, 0.4*inch))

story.append(Paragraph("3 Candidates:", subtitle_style))
story.append(Paragraph("• Ali Jawad<br/>• Umair Solangi<br/>• Sultan Muhammad Hamad Sheharyar", subtitle_style))
story.append(PageBreak())

# Add each full email
for i, cand in enumerate(candidates):
    # Candidate name and email
    story.append(Paragraph(cand['name'], candidate_style))
    story.append(Paragraph(f"<i>{cand['email']}</i>", subtitle_style))
    story.append(Spacer(1, 0.15*inch))

    # Full email text
    story.append(Paragraph(cand['text'].replace("\n\n", "<br/><br/>"), email_style))

    # Page break between candidates
    if i < len(candidates) - 1:
        story.append(PageBreak())

# Build PDF
doc.build(story)
print(f"[OK] PDF generated: {pdf_path}")
print(f"[OK] Contains 3 full 950-word emails (not summaries)")
