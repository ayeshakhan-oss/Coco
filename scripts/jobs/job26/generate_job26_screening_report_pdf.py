"""
Job 26: Soul Architect — CV Screening Report PDF
Proper format: stat boxes, tiered candidates, professional layout
"""

import json
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime

# Load results
with open(r"c:\Agent Coco\soul_architect_results_final.json", 'r') as f:
    results = json.load(f)

# Output path
output_path = r"c:\Agent Coco\scripts\jobs\job26\JOB26_SOUL_ARCHITECT_SCREENING_REPORT.pdf"

# Create document
doc = SimpleDocTemplate(
    output_path,
    pagesize=landscape(A4),
    rightMargin=0.8*cm, leftMargin=0.8*cm,
    topMargin=0.8*cm, bottomMargin=0.8*cm
)

# Styles
styles = getSampleStyleSheet()
style_title = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=24,
    textColor=colors.HexColor('#1565c0'),
    spaceAfter=10,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold'
)

style_heading = ParagraphStyle(
    'CustomHeading',
    parent=styles['Heading2'],
    fontSize=13,
    textColor=colors.HexColor('#1565c0'),
    spaceAfter=8,
    fontName='Helvetica-Bold'
)

style_body = ParagraphStyle(
    'CustomBody',
    parent=styles['BodyText'],
    fontSize=10,
    textColor=colors.HexColor('#333333'),
    alignment=TA_LEFT,
    spaceAfter=6
)

# Build story
story = []

# ─── HEADER ───────────────────────────────────────────────────────────────
header_data = [['PEOPLE & CULTURE · INITIAL SCREENING REPORT']]
header_table = Table(header_data, colWidths=[19*cm])
header_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#0d47a1')),
    ('TEXTCOLOR', (0, 0), (-1, -1), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 11),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
]))
story.append(header_table)
story.append(Spacer(1, 0.3*cm))

# Title
story.append(Paragraph("Soul Architect / Conversational UX Designer", style_title))
story.append(Paragraph("Job 26 · Taleemabad", style_heading))
story.append(Spacer(1, 0.4*cm))

# ─── STAT BOXES ───────────────────────────────────────────────────────────
stat_data = [
    ['42', '15', '4', '8'],
    ['Total Screened', 'Top Tier', 'Consider', 'Maybe']
]

colors_list = [colors.HexColor('#d32f2f'), colors.HexColor('#1976d2'),
               colors.HexColor('#fbc02d'), colors.HexColor('#757575')]

stat_table = Table(stat_data, colWidths=[4.5*cm, 4.5*cm, 4.5*cm, 4.5*cm])
stat_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (0, 0), colors_list[0]),
    ('BACKGROUND', (1, 0), (1, 0), colors_list[1]),
    ('BACKGROUND', (2, 0), (2, 0), colors_list[2]),
    ('BACKGROUND', (3, 0), (3, 0), colors_list[3]),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 18),
    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
    ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
    ('TOPPADDING', (0, 0), (-1, 0), 10),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 10),

    ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#f5f5f5')),
    ('TEXTCOLOR', (0, 1), (-1, 1), colors.HexColor('#333333')),
    ('FONTNAME', (0, 1), (-1, 1), 'Helvetica'),
    ('FONTSIZE', (0, 1), (-1, 1), 10),
    ('ALIGN', (0, 1), (-1, 1), 'CENTER'),
    ('VALIGN', (0, 1), (-1, 1), 'MIDDLE'),
    ('TOPPADDING', (0, 1), (-1, 1), 6),
    ('BOTTOMPADDING', (0, 1), (-1, 1), 6),
    ('LINEBELOW', (0, 0), (-1, 1), 0.5, colors.HexColor('#cccccc')),
]))
story.append(stat_table)
story.append(Spacer(1, 0.4*cm))

# ─── KEY OBSERVATION ───────────────────────────────────────────────────────
story.append(Paragraph("<b>Key Observation</b>", style_heading))
obs_text = (
    "Strong candidate pool for Soul Architect role. 15 candidates meet top-tier criteria "
    "(3.5/5 or above), with 7 demonstrating perfect fit across all 5 selection criteria. "
    "4 additional candidates in 'Consider' tier warrant secondary review. Ready to move forward with interviews."
)
story.append(Paragraph(obs_text, style_body))
story.append(Spacer(1, 0.3*cm))

# ─── TOP TIER CANDIDATES ───────────────────────────────────────────────────
story.append(Paragraph("<b>Top Tier - Interview Ready (15)</b>", style_heading))

top_tier_data = [['#', 'Candidate', 'Score', 'Criteria Met', 'Status']]
for i, cand in enumerate(results['TOP_TIER'], 1):
    criteria = ', '.join(cand['criteria'][:2])
    top_tier_data.append([
        str(i),
        cand['name'],
        f"{cand['score']}/5",
        criteria,
        'Priority' if cand['score'] >= 4.0 else 'Next'
    ])

top_tier_table = Table(top_tier_data, colWidths=[0.6*cm, 4.2*cm, 1.4*cm, 7*cm, 1.8*cm])
top_tier_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1565c0')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 9),
    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
    ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
    ('TOPPADDING', (0, 0), (-1, 0), 6),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 6),

    ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f9f9f9')),
    ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#333333')),
    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 1), (-1, -1), 9),
    ('ALIGN', (0, 1), (0, -1), 'CENTER'),
    ('ALIGN', (2, 1), (2, -1), 'CENTER'),
    ('ALIGN', (4, 1), (4, -1), 'CENTER'),
    ('VALIGN', (0, 1), (-1, -1), 'MIDDLE'),
    ('TOPPADDING', (0, 1), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 1), (-1, -1), 4),
    ('LINEBELOW', (0, 1), (-1, -1), 0.5, colors.HexColor('#e0e0e0')),
]))
story.append(top_tier_table)
story.append(Spacer(1, 0.3*cm))

# Perfect scores
perfect_count = sum(1 for c in results['TOP_TIER'] if c['score'] == 5.0)
story.append(Paragraph(
    f"Perfect Scores (5.0/5): {perfect_count} candidates meet all criteria. Recommend expedited interviews.",
    style_body
))
story.append(Spacer(1, 0.3*cm))

# ─── CONSIDER TIER ───────────────────────────────────────────────────────
story.append(Paragraph("<b>Consider - Secondary Review (4)</b>", style_heading))

consider_data = [['Candidate', 'Score', 'Key Criteria']]
for cand in results['CONSIDER']:
    consider_data.append([
        cand['name'],
        f"{cand['score']}/5",
        ', '.join(cand['criteria'])
    ])

consider_table = Table(consider_data, colWidths=[5*cm, 1.5*cm, 8.5*cm])
consider_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1565c0')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 9),
    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
    ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
    ('TOPPADDING', (0, 0), (-1, 0), 6),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 6),

    ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#fffde7')),
    ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#333333')),
    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 1), (-1, -1), 9),
    ('ALIGN', (1, 1), (1, -1), 'CENTER'),
    ('VALIGN', (0, 1), (-1, -1), 'MIDDLE'),
    ('TOPPADDING', (0, 1), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 1), (-1, -1), 4),
    ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.HexColor('#e0e0e0')),
]))
story.append(consider_table)
story.append(Spacer(1, 0.3*cm))

# ─── FOOTER ───────────────────────────────────────────────────────────────
footer_text = f"Taleemabad Talent Acquisition | Job 26 | {datetime.now().strftime('%Y-%m-%d')} | Coco"
story.append(Spacer(1, 0.2*cm))
story.append(Paragraph(footer_text, ParagraphStyle(
    'Footer',
    parent=styles['Normal'],
    fontSize=8,
    textColor=colors.HexColor('#999999'),
    alignment=TA_CENTER
)))

# Build PDF
doc.build(story)
print(f"PDF created: {output_path}")
