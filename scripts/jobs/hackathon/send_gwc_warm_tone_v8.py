"""
Send GWC Rejection Emails - Warm Tone v8 Format
Ali Jawad, Umair Solangi, Sultan Muhammad Hamad Sheharyar
HTML branded email with logo, blue header, Georgia serif
"""
import os, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from dotenv import load_dotenv

load_dotenv()
import sys as _sys
_sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
from scripts.utils.safe_send import safe_sendmail

SENDER = os.getenv("EMAIL_USER")
PASSWORD = os.getenv("EMAIL_PASSWORD")
RECIPIENT = "ayesha.khan@taleemabad.com"
ROLE = "Hackathon 2026"
LOGO_PATH = os.path.join(os.path.dirname(__file__), "../../..", "assets", "logo_taleemabad.png")

# HTML HELPERS (v8 design)
H   = lambda t: f'<h2 style="color:#1565c0;font-size:17px;font-weight:bold;margin:36px 0 6px 0;letter-spacing:0.3px;">{t}</h2>'
P   = lambda t: f'<p style="margin:0 0 18px 0;text-align:justify;font-family:Georgia,serif;font-size:15px;line-height:1.8;">{t}</p>'

FOOTER = """<table width="100%" cellpadding="0" cellspacing="0" style="margin-top:40px;border-top:1px solid #e0e0e0;padding-top:20px;"><tr><td style="font-family:Georgia,serif;font-size:13px;color:#555;line-height:1.9;">Warm regards,<br><strong style="color:#1a1a1a;">People and Culture Team</strong><br><strong style="color:#1565c0;">Taleemabad</strong><br><a href="mailto:hiring@taleemabad.com" style="color:#1565c0;text-decoration:none;">hiring@taleemabad.com</a> &nbsp;|&nbsp; <a href="http://www.taleemabad.com" style="color:#1565c0;text-decoration:none;">www.taleemabad.com</a><br><span style="font-size:12px;color:#aaa;margin-top:4px;display:block;"></span></td></tr></table>"""

def header_block(subject_line):
    return f"""<table width="100%" cellpadding="0" cellspacing="0" style="border-radius:8px 8px 0 0;overflow:hidden;border-bottom:2px solid #1565c0;"><tr><td align="center" bgcolor="#ffffff" style="background-color:#ffffff;padding:28px 40px 22px 40px;"><img src="cid:taleemabad_logo" height="38" alt="Taleemabad" style="display:block;margin:0 auto 14px auto;"><p style="margin:0;font-family:Georgia,serif;font-size:11px;color:#1565c0;letter-spacing:2px;text-transform:uppercase;">People &amp; Culture &nbsp;&bull;&nbsp; Rejection Decision</p><p style="margin:10px 0 4px 0;font-family:Georgia,serif;font-size:17px;font-weight:bold;color:#1565c0;line-height:1.4;">{subject_line}</p><p style="margin:0;font-family:Georgia,serif;font-size:12px;color:#5c85c7;">{ROLE}</p></td></tr></table>"""

def wrap(subject_line, body_html):
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8"></head><body style="margin:0;padding:0;background-color:#f0f4f0;"><table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f0f4f0;padding:32px 0;"><tr><td align="center"><table width="620" cellpadding="0" cellspacing="0" style="max-width:620px;border-radius:8px;box-shadow:0 2px 12px rgba(0,0,0,0.08);"><tr><td>{header_block(subject_line)}</td></tr><tr><td style="background:#ffffff;padding:40px 52px 48px 52px;border-radius:0 0 8px 8px;font-family:Georgia,serif;font-size:15px;line-height:1.8;color:#1a1a1a;">{body_html}</td></tr></table></td></tr></table></body></html>"""

# Read warm tone emails
def extract_email_body(filepath):
    with open(filepath, "r") as f:
        content = f.read()
    parts = content.split("---")
    if len(parts) >= 2:
        return parts[1].strip()
    return content

ali_body_text = extract_email_body("c:/Agent Coco/scripts/jobs/hackathon/ali_jawad_warm_800.txt")
umair_body_text = extract_email_body("c:/Agent Coco/scripts/jobs/hackathon/umair_solangi_warm_800.txt")
sultan_body_text = extract_email_body("c:/Agent Coco/scripts/jobs/hackathon/sultan_sheharyar_warm_800.txt")

# Convert to HTML paragraphs
def text_to_html(text):
    paragraphs = text.split("\n\n")
    html = ""
    for para in paragraphs:
        if para.strip().startswith("**"):
            heading = para.strip().replace("**", "").replace("\n", " ")
            html += H(heading)
        elif para.strip():
            html += P(para.strip())
    return html

ALI_HTML = wrap("We enjoyed meeting you - and here's what we saw", text_to_html(ali_body_text))
UMAIR_HTML = wrap("Your foundation is strong - here's what we saw", text_to_html(umair_body_text))
SULTAN_HTML = wrap("Your curiosity is a strength - here's what we learned about you", text_to_html(sultan_body_text))

EMAILS = [
    ("Ali Jawad", ALI_HTML),
    ("Umair Solangi", UMAIR_HTML),
    ("Sultan Muhammad Hamad Sheharyar", SULTAN_HTML),
]

print("\n=== SENDING GWC WARM TONE EMAILS - v8 FORMAT ===\n")

try:
    s = smtplib.SMTP("smtp.gmail.com", 587)
    s.starttls()
    s.login(SENDER, PASSWORD)
    print("[OK] Connected to Gmail SMTP\n")

    for name, html_body in EMAILS:
        msg = MIMEMultipart("related")
        msg["Subject"] = f"[PILOT] {name} — We're reflecting on your Hackathon 2026 application"
        msg["From"] = SENDER
        msg["To"] = RECIPIENT

        # Attach logo as CID
        try:
            with open(LOGO_PATH, "rb") as logo_file:
                logo = MIMEImage(logo_file.read())
                logo.add_header("Content-ID", "<taleemabad_logo>")
                logo.add_header("Content-Disposition", "inline")
                msg.attach(logo)
        except FileNotFoundError:
            print(f"[WARNING] Logo not found at {LOGO_PATH}")

        # Add body
        msg_alt = MIMEMultipart("alternative")
        msg.attach(msg_alt)
        msg_alt.attach(MIMEText(html_body, "html"))

        # Send via safe_sendmail
        safe_sendmail(
            s,
            SENDER,
            RECIPIENT,
            msg.as_string(),
            context=f"GWC_warm_tone_pilot_{name.replace(' ', '_')}"
        )
        print(f"[OK] Sent warm tone email for {name}")

    s.quit()
    print(f"\n" + "="*60)
    print(f"Sent 3 warm tone emails (v8 format)")
    print(f"="*60)

except Exception as e:
    print(f"[FAILED] {e}")
    import traceback
    traceback.print_exc()
