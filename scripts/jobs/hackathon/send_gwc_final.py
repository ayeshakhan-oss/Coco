"""
Send GWC Warm Tone Emails - FINAL EXACT FORMAT
Logo, blue header, blue title, blue subtitle, blue line, Georgia justified text
NO asterisks in headings
"""
import os, sys
sys.path.insert(0, "c:/Agent Coco")

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from dotenv import load_dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

load_dotenv()

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
pdf_path = "c:/Agent Coco/scripts/jobs/hackathon/GWC_Hackathon_2026_Final.pdf"
doc = SimpleDocTemplate(pdf_path, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.75*inch, leftMargin=0.75*inch, rightMargin=0.75*inch)

styles = getSampleStyleSheet()

small_header_style = ParagraphStyle(
    'SmallHeader',
    parent=styles['Normal'],
    fontSize=10,
    textColor=colors.HexColor('#1565c0'),
    alignment=TA_CENTER,
    letterSpacing=2,
    spaceAfter=8
)

title_style = ParagraphStyle(
    'TitleStyle',
    parent=styles['Normal'],
    fontSize=18,
    textColor=colors.HexColor('#1565c0'),
    fontName='Helvetica-Bold',
    alignment=TA_CENTER,
    spaceAfter=4
)

subtitle_style = ParagraphStyle(
    'SubtitleStyle',
    parent=styles['Normal'],
    fontSize=12,
    textColor=colors.HexColor('#1565c0'),
    alignment=TA_CENTER,
    spaceAfter=12
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
    'HeadingBlue',
    parent=styles['Normal'],
    fontSize=11,
    fontFamily='Georgia',
    fontName='Helvetica-Bold',
    textColor=colors.HexColor('#1565c0'),
    spaceAfter=8,
    spaceBefore=12
)

logo_path = "c:/Agent Coco/assets/logo_taleemabad.png"

story = []

for i, (name, body) in enumerate(emails):
    # Logo
    if os.path.exists(logo_path):
        img = Image(logo_path, width=0.8*inch, height=0.8*inch)
        story.append(img)
        story.append(Spacer(1, 0.1*inch))

    # Small header
    story.append(Paragraph("PEOPLE &amp; CULTURE • REJECTION DECISION", small_header_style))
    story.append(Spacer(1, 0.06*inch))

    # Title (main position)
    story.append(Paragraph(f"We're reflecting on your Hackathon 2026 application", title_style))

    # Subtitle
    story.append(Paragraph("Hackathon 2026", subtitle_style))

    # Blue horizontal line
    line_table = Table([[""]], colWidths=[7*inch])
    line_table.setStyle(TableStyle([
        ('LINEBELOW', (0, 0), (-1, 0), 2, colors.HexColor('#1565c0')),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(line_table)
    story.append(Spacer(1, 0.15*inch))

    # Body paragraphs - remove asterisks from headings
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
print(f"[OK] PDF generated: {pdf_path}")

# Send email
SENDER = os.getenv('EMAIL_USER')
PASSWORD = os.getenv('EMAIL_PASSWORD')
RECIPIENT = 'ayesha.khan@taleemabad.com'

s = smtplib.SMTP('smtp.gmail.com', 587)
s.starttls()
s.login(SENDER, PASSWORD)

msg = MIMEMultipart()
msg['Subject'] = '[HACKATHON] GWC Warm Tone Rejection Emails - Final'
msg['From'] = SENDER
msg['To'] = RECIPIENT

body = '''Hi Ayesha,

Attached: Final GWC rejection emails with exact format.

3 candidates:
1. Ali Jawad
2. Umair Solangi
3. Sultan Muhammad Hamad Sheharyar

Format: Logo, blue header, blue title/subtitle, blue line, justified Georgia text. Warm tone, 800+ words, "we" voice.

Ready to go live.

Thanks,
Coco'''

msg.attach(MIMEText(body, 'plain'))

with open(pdf_path, 'rb') as attachment:
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename= GWC_Hackathon_2026_Final.pdf')
    msg.attach(part)

s.sendmail(SENDER, RECIPIENT, msg.as_string())
s.quit()

print('[OK] Final PDF sent to ayesha.khan@taleemabad.com')
