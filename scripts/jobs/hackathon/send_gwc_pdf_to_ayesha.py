"""
Send GWC Three Candidates PDF to Ayesha only
"""
import os, sys, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv

sys_path = os.path.join(os.path.dirname(__file__), "../../..")
sys.path.insert(0, sys_path)

load_dotenv()

SENDER = os.getenv("EMAIL_USER")
PASSWORD = os.getenv("EMAIL_PASSWORD")
RECIPIENT = "ayesha.khan@taleemabad.com"
PDF_PATH = "c:/Agent Coco/scripts/jobs/hackathon/GWC_Three_Candidates_Pilot.pdf"

print("\n=== SENDING GWC THREE CANDIDATES PDF TO AYESHA ===\n")

try:
    s = smtplib.SMTP("smtp.gmail.com", 587)
    s.starttls()
    s.login(SENDER, PASSWORD)
    print("[OK] Connected to Gmail SMTP\n")

    msg = MIMEMultipart()
    msg["Subject"] = "[HACKATHON] GWC Rejection Emails - 3 Candidates (Evidence-Based)"
    msg["From"] = SENDER
    msg["To"] = RECIPIENT

    body = """Hi Ayesha,

Please review the attached PDF with GWC rejection emails for 3 Hackathon 2026 candidates:

1. Ali Jawad (Mixed Gaps) - Cricket prediction system, Gemini reliance, mid-interview pivot
2. Umair Solangi (Frontend Gap/Alignment) - Strong Laravel backend, weak React, backend preference
3. Sultan Muhammad Hamad Sheharyar (Significant Gaps) - Breadth without depth, fundamentals missing

All emails are evidence-based from interview transcripts (800-1100 words each).

Please review and share feedback. Ready to go live once approved.

Thanks,
Coco
"""

    msg.attach(MIMEText(body, "plain"))

    # Attach PDF
    with open(PDF_PATH, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename= GWC_Three_Candidates_Pilot.pdf")
        msg.attach(part)

    s.sendmail(SENDER, RECIPIENT, msg.as_string())
    s.quit()

    print(f"[OK] PDF sent to {RECIPIENT}")
    print(f"PDF: {PDF_PATH}")
    print("\n" + "="*60)

except Exception as e:
    print(f"[FAILED] {e}")
    import traceback
    traceback.print_exc()
