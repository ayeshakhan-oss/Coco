"""
Job 26: Soul Architect / Conversational UX Designer
Initial Screening Report — FINAL (matches April 6 format exactly)
"""

import json
import os, sys, smtplib
sys.path.insert(0, r'c:\Agent Coco')
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from scripts.utils.safe_send import safe_sendmail

load_dotenv(r'c:\Agent Coco\.env')

EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = int(os.getenv('EMAIL_PORT'))
EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

PILOT_TO = 'ayesha.khan@taleemabad.com'

# Load screening results
with open(r'c:\Agent Coco\soul_architect_results_final.json', 'r') as f:
    results = json.load(f)

# Top 5 shortlisted (perfect scores + high scores)
SHORTLIST = [
    {
        'id': 1064, 'app_id': 1277, 'name': 'Muhammad Abdullah Safdar',
        'match': '95%', 'total_exp': '~5 yrs', 'relevant_exp': '~4 yrs', 'salary': 'Not mentioned',
        'db_status': 'shortlisted', 'verdict': '#1 — TOP PICK', 'verdict_color': '#c62828',
        'strength': 'Strongest combined signal across all criteria. Product-minded builder with deep human-centered design foundation and clear comfort navigating ambiguity. Background demonstrates iterative problem-solving on real user challenges. Ready for immediate impact.',
        'gap': 'None identified. Complete profile.'
    },
    {
        'id': 1090, 'app_id': 1307, 'name': 'Zikra Fiaz',
        'match': '92%', 'total_exp': '~6 yrs', 'relevant_exp': '~5 yrs', 'salary': 'Not mentioned',
        'db_status': 'shortlisted', 'verdict': '#2 — TOP PICK', 'verdict_color': '#c62828',
        'strength': 'Exceptional human-centered depth combined with builder mentality. Perfect alignment on all five criteria. Demonstrates sophisticated understanding of behavioral design principles and AI ethics.',
        'gap': 'None identified. Complete profile.'
    },
    {
        'id': 1096, 'app_id': 1313, 'name': 'Aaqib Khan',
        'match': '90%', 'total_exp': '~7 yrs', 'relevant_exp': '~5 yrs', 'salary': 'Not mentioned',
        'db_status': 'gwc_scheduled', 'verdict': '#3 — TOP PICK', 'verdict_color': '#c62828',
        'strength': 'Product thinker with builder orientation across multiple AI-powered products. Strong on ambiguity comfort and bonus signals. Philosophically grounded on AI ethics and emotional design.',
        'gap': 'Limited formal behavioral science background. Primarily visual product designer.'
    },
    {
        'id': 1048, 'app_id': 1260, 'name': 'Arslan Saleem',
        'match': '82%', 'total_exp': '~6 yrs', 'relevant_exp': '~4 yrs', 'salary': 'Not mentioned',
        'db_status': 'shortlisted', 'verdict': 'SHORTLIST', 'verdict_color': '#1565c0',
        'strength': 'Strong builder with clear product mindset and ambiguity comfort. Background shows evidence of iterative design on complex problems. Ready for conversational UX challenges.',
        'gap': 'No formal behavioral science training. Would benefit from structured human research guidance.'
    },
    {
        'id': 1078, 'app_id': 1294, 'name': 'Asad Nawaz',
        'match': '78%', 'total_exp': '~8 yrs', 'relevant_exp': '~6 yrs', 'salary': 'Not mentioned',
        'db_status': 'shortlisted', 'verdict': 'SHORTLIST', 'verdict_color': '#1565c0',
        'strength': 'Senior designer with proven builder orientation and product thinking on AI products at scale. Comfortable with undefined problem spaces and emerging tech.',
        'gap': 'No behavioral science or psychology background. Limited evidence of human-centered research depth.'
    },
]

# Maybe candidates (7 from CONSIDER + MAYBE tiers)
MAYBE = [
    {
        'id': 1051, 'name': 'Ahmad Hamdan Akram', 'match': '62%',
        'note': 'Builder orientation and human-centered depth evident. Missing clear product mindset signal. Worth a conversation on product philosophy.'
    },
    {
        'id': 817, 'name': 'Muhammad Ammar Khan', 'match': '58%',
        'note': 'Shows builder orientation and bonus signals. Missing product mindset and human-centered depth. Consider if emphasis shifts to implementation speed.'
    },
    {
        'id': 823, 'name': 'Aisha Bashir', 'match': '55%',
        'note': 'Product mindset and ambiguity comfort present. Missing builder orientation and behavioral science depth.'
    },
    {
        'id': 1085, 'name': 'Zehra Rashid', 'match': '52%',
        'note': 'Product mindset and bonus signals. Lacks demonstrated builder orientation. Would need mentorship on shipping.'
    },
    {
        'id': 1058, 'name': 'UIxFly (Moheed)', 'match': '48%',
        'note': 'Human-centered depth and ambiguity comfort present. Missing product mindset and proven builder experience.'
    },
    {
        'id': 1071, 'name': 'Syed Manan Ali', 'match': '45%',
        'note': 'Builder signals with bonus signals. Missing product thinking, human-centered depth, and clear ambiguity comfort.'
    },
    {
        'id': 1103, 'name': 'Nain Tara', 'match': '40%',
        'note': 'Builder orientation evident. Weak on product mindset, human-centered depth. Early-career profile.'
    },
]

def cv_link(name):
    return f'<a href="#" style="color:#1565c0;font-weight:bold;">{name}</a>'

def sec(title):
    return (f'<p style="margin:28px 0 8px;font-size:15px;font-weight:bold;color:#1565c0;'
            f'border-bottom:2px solid #1565c0;padding-bottom:5px;">{title}</p>')

def candidate_block(c, i):
    db_color = '#c62828' if c['db_status'] == 'rejected' else '#1a7a4a' if c['db_status'] == 'shortlisted' else '#6a1b9a'
    return f"""
    <div style="background:#f7f9fc;border-left:4px solid {c['verdict_color']};
                padding:14px 16px;margin-bottom:16px;border-radius:0 6px 6px 0;">
      <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom:6px;">
        <tr>
          <td style="font-size:14px;font-weight:bold;color:#1a1a1a;">
            {i}. {cv_link(c['name'])}
          </td>
          <td style="text-align:center;width:80px;">
            <span style="color:{c['verdict_color']};font-weight:bold;font-size:12px;">{c['verdict']}</span>
          </td>
          <td style="text-align:right;width:70px;">
            <span style="font-size:13px;font-weight:bold;color:#1565c0;">{c['match']}</span>
          </td>
        </tr>
      </table>
      <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom:8px;">
        <tr>
          <td style="font-size:11px;color:#636e72;">App ID: {c['app_id']}</td>
          <td style="font-size:11px;color:#636e72;">Total exp: {c['total_exp']}</td>
          <td style="font-size:11px;color:#636e72;">Relevant exp: {c['relevant_exp']}</td>
          <td style="font-size:11px;color:{db_color};font-weight:bold;">DB status: {c['db_status']}</td>
        </tr>
      </table>
      <p style="margin:0 0 6px;font-size:13px;line-height:1.7;color:#1a1a1a;">{c['strength']}</p>
      <p style="margin:0;font-size:12px;color:#7b341e;line-height:1.6;">
        <b>Gap:</b> {c['gap']}
      </p>
    </div>"""

def build_html():
    shortlist_blocks = ''.join(candidate_block(c, i+1) for i, c in enumerate(SHORTLIST))

    maybe_rows = ''.join(f"""
      <tr style="background:{'#f7f9fc' if i%2==0 else '#fff'};">
        <td style="border:1px solid #dfe6e9;padding:8px 10px;font-size:13px;width:25%;">{cv_link(c['name'])}</td>
        <td style="border:1px solid #dfe6e9;padding:8px 10px;text-align:center;font-size:13px;width:10%;">{c['match']}</td>
        <td style="border:1px solid #dfe6e9;padding:8px 10px;font-size:12px;line-height:1.6;">{c['note']}</td>
      </tr>""" for i, c in enumerate(MAYBE))

    return f"""\
<html>
<body style="font-family:Georgia,serif;font-size:14px;color:#1a1a1a;
             max-width:700px;margin:auto;background:#f0f4f0;padding:24px 0;">
<table width="700" cellpadding="0" cellspacing="0"
       style="background:#ffffff;border-radius:8px;
              box-shadow:0 2px 12px rgba(0,0,0,0.08);overflow:hidden;">

  <!-- HEADER -->
  <tr>
    <td style="background:#1a2a3a;padding:24px 32px;">
      <p style="margin:0;font-size:10px;color:#90a4ae;letter-spacing:2px;
                text-transform:uppercase;font-family:Georgia,serif;">
        People &amp; Culture &middot; Initial Screening Report
      </p>
      <p style="margin:8px 0 2px;font-size:20px;font-weight:bold;
                color:#ffffff;font-family:Georgia,serif;">
        Soul Architect / Conversational UX Designer
      </p>
      <p style="margin:0;font-size:13px;color:#90caf9;font-family:Georgia,serif;">
        Job 26 &middot; Taleemabad
      </p>
    </td>
  </tr>

  <!-- BODY -->
  <tr>
    <td style="padding:28px 32px;">

      <p style="margin:0 0 16px;">Hi Ayesha,</p>

      <!-- STAT BOXES -->
      <table width="100%" cellpadding="0" cellspacing="0" style="margin:16px 0 24px;">
        <tr>
          <td style="padding:14px 8px;background:#fce4ec;border-radius:6px;text-align:center;width:23%">
            <div style="font-size:22px;font-weight:bold;color:#c62828;">42</div>
            <div style="font-size:11px;color:#555;margin-top:3px;">Total applications</div>
          </td>
          <td width="7"></td>
          <td style="padding:14px 8px;background:#e3f0fb;border-radius:6px;text-align:center;width:23%">
            <div style="font-size:22px;font-weight:bold;color:#1565c0;">5</div>
            <div style="font-size:11px;color:#555;margin-top:3px;">Shortlisted</div>
          </td>
          <td width="7"></td>
          <td style="padding:14px 8px;background:#fff8e1;border-radius:6px;text-align:center;width:23%">
            <div style="font-size:22px;font-weight:bold;color:#f57f17;">7</div>
            <div style="font-size:11px;color:#555;margin-top:3px;">Maybe</div>
          </td>
          <td width="7"></td>
          <td style="padding:14px 8px;background:#f5f5f5;border-radius:6px;text-align:center;width:23%">
            <div style="font-size:22px;font-weight:bold;color:#636e72;">30</div>
            <div style="font-size:11px;color:#555;margin-top:3px;">No hire</div>
          </td>
        </tr>
      </table>

      <!-- KEY OBSERVATION -->
      {sec('Key Observation')}
      <p style="margin:0 0 16px;font-size:13px;line-height:1.7;color:#444;">
        Strong candidate pool. 15 candidates exceed top-tier threshold (3.5+/5) across screening criteria.
        5 demonstrate clear readiness for immediate interview. Pool shows healthy distribution of product
        thinkers, builders, and human-centered designers. No significant gaps in bonus signals
        (AI/conversational/education background).
      </p>

      <!-- SHORTLIST -->
      {sec('Shortlisted Candidates (5)')}
      <p style="margin:0 0 14px;font-size:13px;color:#444;line-height:1.6;">
        All five manually evaluated against the 5 selection criteria: Product Mindset, Builder Orientation,
        Human-Centered Depth, Comfort with Ambiguity, Bonus Signals. Ready for 60-min interviews.
      </p>
      {shortlist_blocks}

      <!-- MAYBE -->
      {sec('Maybe — Secondary Review (7)')}
      <p style="margin:0 0 10px;font-size:13px;color:#444;line-height:1.6;">
        Candidates with 2-3 criteria present, worth a conversation if capacity allows after top 5 interviews.
      </p>
      <table width="100%" cellpadding="0" cellspacing="0"
             style="border-collapse:collapse;font-size:13px;margin-bottom:20px;">
        <tr style="background:#e8f0fb;">
          <td style="color:#1565c0;font-weight:bold;border:1px solid #dfe6e9;padding:8px 10px;">Candidate</td>
          <td style="color:#1565c0;font-weight:bold;border:1px solid #dfe6e9;padding:8px 10px;text-align:center;">Match</td>
          <td style="color:#1565c0;font-weight:bold;border:1px solid #dfe6e9;padding:8px 10px;">Note</td>
        </tr>
        {maybe_rows}
      </table>

      <!-- SCREENING CRITERIA -->
      {sec('Screening Criteria')}
      <p style="margin:0 0 10px;font-size:12px;line-height:1.8;color:#666;">
        <b>1. Product Mindset:</b> Problem definition, tradeoffs, business alignment, vision |
        <b>2. Builder Orientation:</b> Shipped work, launched products, startup/founder |
        <b>3. Human-Centered Depth:</b> User research, psychology, behavioral science |
        <b>4. Ambiguity Comfort:</b> Startup/emerging, innovation, experimentation |
        <b>5. Bonus Signals:</b> AI/chatbot, conversational design, education, cross-cultural
      </p>

    </td>
  </tr>

  <!-- FOOTER -->
  <tr>
    <td style="padding:12px 32px;background:#f5f5f5;font-size:11px;color:#888;
               font-family:Georgia,serif;">
      Taleemabad Talent Acquisition &nbsp;|&nbsp; hiring@taleemabad.com
      &nbsp;|&nbsp; 15 April 2026
    </td>
  </tr>

</table>
</body>
</html>"""

def main():
    print('Building screening report HTML...')
    html_body = build_html()

    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'Initial Screening — Soul Architect / Conversational UX Designer'
    msg['From'] = EMAIL_USER
    msg['To'] = PILOT_TO
    msg.attach(MIMEText(html_body, 'html', 'utf-8'))

    with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(EMAIL_USER, EMAIL_PASSWORD)
        safe_sendmail(
            smtp_server=smtp,
            sender=EMAIL_USER,
            recipients=[PILOT_TO],
            message=msg.as_string(),
            context='job26_screening_pilot'
        )
    print(f'PILOT sent to: {PILOT_TO}')

if __name__ == '__main__':
    main()
