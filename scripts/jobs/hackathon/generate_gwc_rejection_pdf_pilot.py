"""
Generate combined GWC rejection PDF for all 6 candidates
Branded format - pilot to Ayesha + Jawwad
"""
import os, sys, smtplib
sys.path.insert(0, "c:/Agent Coco")

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from scripts.utils.safe_send import safe_sendmail

load_dotenv(dotenv_path="c:/Agent Coco/.env")

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

PILOT_RECIPIENTS = ["ayesha.khan@taleemabad.com", "jawwad.ali@taleemabad.com"]

# Candidate data with feedback
candidates = [
    {
        "name": "Moaz Nadeem",
        "email": "muazndm128@gmail.com",
        "gwc_scores": "Get: 3/3 | Want: 3/3 | Capacity: 3/3",
        "type": "Perfect Pass",
        "liked": "Exceptional GWC performance with crystal-clear understanding of the role. Genuine enthusiasm shone through in every conversation. Strong capacity to execute across technical and strategic dimensions.",
        "questioned": "Timing and bandwidth on our end. Team structure is still settling. While skills are exactly what we'd want, we're concerned we couldn't give the mentorship deserved. Honest assessment of team constraints.",
        "next": "Keep doing the work that excites you. In 3-6 months, we'd love to revisit this conversation. Door remains open."
    },
    {
        "name": "Alishba Ramzan",
        "email": "alishbaramzan1@gmail.com",
        "gwc_scores": "Get: 3/3 | Want: 3/3 | Capacity: 3/3",
        "type": "Perfect Pass",
        "liked": "Exceptional GWC performance with crystal-clear understanding of the role. Genuine enthusiasm shone through in every conversation. Strong capacity to execute across technical and strategic dimensions.",
        "questioned": "Timing and bandwidth on our end. Team structure is still settling. While skills are exactly what we'd want, we're concerned we couldn't give the mentorship deserved. Honest assessment of team constraints.",
        "next": "Keep doing the work that excites you. In 3-6 months, we'd love to revisit this conversation. Door remains open."
    },
    {
        "name": "Umair Solangi",
        "email": "bscs2112203@szabist.pk",
        "gwc_scores": "Get: 2/3 | Want: 1/3 | Capacity: 3/3",
        "type": "Low Want It",
        "liked": "Solid technical foundation. Methodical approach to assessment. Openness and self-awareness throughout process. Genuine energy and ambition about building skills.",
        "questioned": "Alignment between what you want and what this position offers wasn't quite clicking. Responses on 'Want It' suggested hesitation about investing energy in this particular space. Best matches need mutual excitement.",
        "next": "Clarify what you're genuinely excited about. What problems do you want to solve? Seek opportunities aligned with that clarity. Door remains open if interests shift."
    },
    {
        "name": "Ali Jawad",
        "email": "ali.jawad6204@gmail.com",
        "gwc_scores": "Get: 2/3 | Want: 2/3 | Capacity: 2/3",
        "type": "Mixed Gaps",
        "liked": "Real thoughtfulness in understanding the role. Solid technical capabilities and structure in thinking. Flexibility and openness—willing to stretch and learn. Growth mindset is genuine strength.",
        "questioned": "While you have real capability, ground to cover across all three GWC dimensions. Understanding, enthusiasm, and delivery confidence all need more development for this role. Not at place where you can hit ground running with full independence.",
        "next": "Seek opportunities where you deepen technical-strategic integration. Work on projects showing product-user-engineering connection. Once foundation built, we'd welcome another conversation. Not a 'no'—more a 'not yet'."
    },
    {
        "name": "Maryam Rafaqat",
        "email": "maryamrafaqat88@gmail.com",
        "gwc_scores": "Get: 1/3 | Want: 1/3 | Capacity: 3/3",
        "type": "Low Understanding",
        "liked": "Genuine interest and energy in exploring this opportunity. Capacity to learn and adapt—flexibility and willingness to think through problems from different angles. Intellectual honesty and self-awareness.",
        "questioned": "Full complexity of role—weaving technical execution with strategic thinking and organizational impact—wasn't crystallizing yet. 'Get It' dimension suggests deeper structure of role needs clarity. Domain clarity needed for this position.",
        "next": "Spend intentional time deepening understanding of how technical work connects to strategy and impact. Work on projects showing that connection. Read widely. Find mentors. This foundation will set you up for faster growth."
    },
    {
        "name": "Sultan Muhammad Hamad Sheharyar",
        "email": "pirzadahammadzakori@gmail.com",
        "gwc_scores": "Get: 0/3 | Want: 1/3 | Capacity: 1/3",
        "type": "Significant Gaps",
        "liked": "Willingness to step into challenging assessment. Genuine openness to try something new despite it being outside comfort zone—growth-oriented mindset. Brought authentic self to process without pretense.",
        "questioned": "Gaps across all three dimensions we evaluate—understanding role requirements, genuine enthusiasm for work, confidence in execution. This role is specialized fit requiring strong understanding, passion, and capability. Gaps on all fronts.",
        "next": "Take time to explore what kind of work genuinely excites you. Seek opportunities naturally aligned with where you are now. Build deeper understanding and confidence over time at sustainable pace."
    }
]

# Create PDF
pdf_path = "c:/Agent Coco/scripts/jobs/hackathon/GWC_Rejection_Emails_Pilot.pdf"
doc = SimpleDocTemplate(pdf_path, pagesize=landscape(A4), topMargin=0.5*inch, bottomMargin=0.5*inch, leftMargin=0.75*inch, rightMargin=0.75*inch)

# Styles
styles = getSampleStyleSheet()
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=16,
    textColor=colors.HexColor('#1565c0'),
    spaceAfter=12,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold'
)

candidate_style = ParagraphStyle(
    'CandidateHeader',
    parent=styles['Heading2'],
    fontSize=13,
    textColor=colors.HexColor('#1565c0'),
    spaceAfter=8,
    spaceBefore=12,
    fontName='Helvetica-Bold'
)

section_style = ParagraphStyle(
    'SectionHead',
    parent=styles['Heading3'],
    fontSize=11,
    textColor=colors.HexColor('#2e7d32'),
    spaceAfter=6,
    spaceBefore=6,
    fontName='Helvetica-Bold'
)

body_style = ParagraphStyle(
    'BodyText',
    parent=styles['Normal'],
    fontSize=10,
    alignment=TA_JUSTIFY,
    spaceAfter=8,
    leading=14
)

label_style = ParagraphStyle(
    'Label',
    parent=styles['Normal'],
    fontSize=9,
    textColor=colors.HexColor('#666'),
    spaceAfter=2,
    fontName='Helvetica'
)

# Build PDF content
story = []

# Title
story.append(Paragraph("GWC Rejection Emails — Hackathon 2026", title_style))
story.append(Paragraph(f"Pilot Review • {datetime.now().strftime('%B %d, %Y')}", label_style))
story.append(Spacer(1, 0.3*inch))

# Add each candidate email
for i, cand in enumerate(candidates):
    # Candidate header
    story.append(Paragraph(f"{cand['name']}", candidate_style))

    # Meta info
    meta_data = [
        [f"Email:", cand['email']],
        [f"GWC Scores:", cand['gwc_scores']],
        [f"Category:", cand['type']]
    ]
    meta_table = Table(meta_data, colWidths=[1.2*inch, 4*inch])
    meta_table.setStyle(TableStyle([
        ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 9),
        ('FONT', (1, 0), (1, -1), 'Helvetica', 9),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#666')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ROWBACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f9f9f9')),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 0.15*inch))

    # What We Liked
    story.append(Paragraph("What We Liked Most About You", section_style))
    story.append(Paragraph(cand['liked'], body_style))

    # Where We Questioned
    story.append(Paragraph("Where We Found Ourselves Sitting With Questions", section_style))
    story.append(Paragraph(cand['questioned'], body_style))

    # What Next
    story.append(Paragraph("What We Think You Should Do Next", section_style))
    story.append(Paragraph(cand['next'], body_style))

    # Separator
    if i < len(candidates) - 1:
        story.append(Spacer(1, 0.25*inch))
        story.append(Paragraph("_______________________________________________________________________________", label_style))
        story.append(Spacer(1, 0.25*inch))

# Build PDF
doc.build(story)
print(f"[OK] PDF generated: {pdf_path}")

# Send as pilot email attachment
print("\n=== SENDING PDF PILOT ===\n")

try:
    s = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    s.starttls()
    s.login(EMAIL_USER, EMAIL_PASSWORD)
    print("[OK] Connected to Gmail SMTP")

    # Create email
    msg = MIMEMultipart()
    msg["Subject"] = "[PILOT] GWC Rejection Emails (6 candidates) — Hackathon 2026"
    msg["From"] = EMAIL_USER
    msg["To"] = ", ".join(PILOT_RECIPIENTS)

    body = """Hi Ayesha & Jawwad,

Please review the attached PDF with all 6 GWC rejection emails for Hackathon 2026.

Candidates included:
1. Moaz Nadeem (Perfect Pass - timing)
2. Alishba Ramzan (Perfect Pass - timing)
3. Umair Solangi (Low Want It)
4. Ali Jawad (Mixed Gaps)
5. Maryam Rafaqat (Low Understanding)
6. Sultan Muhammad Hamad Sheharyar (Significant Gaps)

Please review and share feedback. Once approved, I'll send live with full HTML formatting + feedback widget.

Thanks,
Coco
"""

    msg.attach(MIMEText(body, "plain"))

    # Attach PDF
    with open(pdf_path, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename= GWC_Rejection_Emails_Pilot.pdf")
        msg.attach(part)

    # Send via safe_sendmail
    from scripts.utils.safe_send import safe_sendmail
    safe_sendmail(
        s,
        EMAIL_USER,
        PILOT_RECIPIENTS,
        msg.as_string(),
        context="GWC_rejection_emails_pilot_pdf"
    )

    s.quit()

    print(f"[OK] PDF pilot sent to {', '.join(PILOT_RECIPIENTS)}")
    print(f"\nPDF: {pdf_path}")

except Exception as e:
    print(f"[FAILED] {e}")
    sys.exit(1)
