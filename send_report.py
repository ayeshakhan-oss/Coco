import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()

EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = int(os.getenv('EMAIL_PORT'))
EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

TO = "ayesha.khan@taleemabad.com"
SUBJECT = "Candidate Screening Report — Fundraising & Partnerships Manager | 2026-02-27"

# Read the main report
with open("output/2026-02-27-fundraising-partnerships-manager-screening-report.md", encoding="utf-8") as f:
    report_md = f.read()

HTML = """
<html><body style="font-family: Arial, sans-serif; font-size: 14px; color: #1a1a1a; max-width: 900px; margin: auto;">

<h1 style="color:#1d3557; border-bottom: 3px solid #1d3557; padding-bottom:8px;">
  Candidate Screening Report<br>
  <span style="font-size:18px; font-weight:normal;">Fundraising &amp; Partnerships Manager &nbsp;|&nbsp; 2026-02-27</span>
</h1>

<table style="width:100%; border-collapse:collapse; margin-bottom:24px;">
  <tr><td style="padding:4px 8px;"><strong>Total Applications</strong></td><td>23</td></tr>
  <tr style="background:#f0f4f8;"><td style="padding:4px 8px;"><strong>CVs Parsed</strong></td><td>18 &nbsp;(4 no resume; 1 unreadable)</td></tr>
  <tr><td style="padding:4px 8px;"><strong>Shortlisted</strong></td><td>5</td></tr>
  <tr style="background:#f0f4f8;"><td style="padding:4px 8px;"><strong>Over-Budget Flags</strong></td><td>2</td></tr>
  <tr><td style="padding:4px 8px;"><strong>Budget Range</strong></td><td>PKR 150,000 – 270,000 / month</td></tr>
  <tr style="background:#f0f4f8;"><td style="padding:4px 8px;"><strong>Hiring Manager</strong></td><td>Sabeena Abbasi &lt;sabeena.abbasi@taleemabad.com&gt;</td></tr>
  <tr><td style="padding:4px 8px;"><strong>Scoring Method</strong></td><td>JD Match 40% | Experience 30% | Skills 20% | Budget Fit 10%</td></tr>
</table>

<!-- TOP RECOMMENDATION -->
<div style="background:#e8f4fd; border-left:5px solid #1d7fd4; padding:16px; margin-bottom:28px; border-radius:4px;">
  <h2 style="margin:0 0 8px 0; color:#1d3557;">⭐ Top Recommendation: Arsim Tariq &nbsp;—&nbsp; 68.5%</h2>
  <p style="margin:0;">Arsim is the strongest fit for this specific role at this moment. He is Islamabad-based, led the <strong>ASPIRE DLR 9.2 teacher-training assessment at NIETE</strong> — the same federal programme Taleemabad partners with — and has secured <strong>10+ development sector projects</strong> through proposal design. His cover letter was the most analytically specific of all 23 applicants: he referenced the scale-and-cost paradox, the bilateral compliance requirements (FCDO, USAID), and Taleemabad's evidence base by name. At 26, he is young, but he is already active in the exact Islamabad donor circles the JD describes. Estimated salary expectation: <strong>PKR 100,000 – 180,000/month</strong> — firmly within budget.<br><br>
  <em>Gap to probe in interview: Has not yet independently closed a $500K+ institutional funding deal. Ask for a specific example.</em></p>
</div>

<!-- SHORTLIST TABLE -->
<h2 style="color:#1d3557;">Shortlisted Candidates (Ranked)</h2>
<table style="width:100%; border-collapse:collapse; margin-bottom:28px; font-size:13px;">
  <thead>
    <tr style="background:#1d3557; color:white;">
      <th style="padding:8px; text-align:left;">Rank</th>
      <th style="padding:8px; text-align:left;">Name</th>
      <th style="padding:8px; text-align:left;">Location</th>
      <th style="padding:8px; text-align:center;">Score</th>
      <th style="padding:8px; text-align:left;">Est. Salary (PKR/mo)</th>
      <th style="padding:8px; text-align:left;">Budget Status</th>
    </tr>
  </thead>
  <tbody>
    <tr style="background:#f9f9f9;">
      <td style="padding:8px;">1</td>
      <td style="padding:8px;"><strong>Arsim Tariq</strong></td>
      <td style="padding:8px;">Islamabad ✓</td>
      <td style="padding:8px; text-align:center;"><strong>68.5%</strong></td>
      <td style="padding:8px;">100,000 – 180,000</td>
      <td style="padding:8px; color:green;"><strong>Within budget</strong></td>
    </tr>
    <tr>
      <td style="padding:8px;">2</td>
      <td style="padding:8px;"><strong>Arsalan Ashraf</strong></td>
      <td style="padding:8px;">Karachi ✗</td>
      <td style="padding:8px; text-align:center;"><strong>67.5%</strong></td>
      <td style="padding:8px;">200,000 – 350,000</td>
      <td style="padding:8px; color:orange;"><strong>Borderline / unknown</strong></td>
    </tr>
    <tr style="background:#f9f9f9;">
      <td style="padding:8px;">3</td>
      <td style="padding:8px;"><strong>Abdul Salam</strong></td>
      <td style="padding:8px;">Islamabad ✓</td>
      <td style="padding:8px; text-align:center;"><strong>67.3%</strong></td>
      <td style="padding:8px;">400,000 – 600,000</td>
      <td style="padding:8px; color:red;"><strong>Likely over budget</strong></td>
    </tr>
    <tr>
      <td style="padding:8px;">4</td>
      <td style="padding:8px;"><strong>Mizhgan Kirmani</strong></td>
      <td style="padding:8px;">Islamabad ✓</td>
      <td style="padding:8px; text-align:center;"><strong>64.9%</strong></td>
      <td style="padding:8px;">150,000 – 260,000</td>
      <td style="padding:8px; color:green;"><strong>Likely within budget</strong></td>
    </tr>
    <tr style="background:#f9f9f9;">
      <td style="padding:8px;">5</td>
      <td style="padding:8px;"><strong>Sameen Amjad Ali</strong></td>
      <td style="padding:8px;">Islamabad ✓</td>
      <td style="padding:8px; text-align:center;"><strong>52.9%</strong></td>
      <td style="padding:8px;">200,000 – 320,000</td>
      <td style="padding:8px; color:orange;"><strong>Borderline / unknown</strong></td>
    </tr>
  </tbody>
</table>

<!-- OVER BUDGET FLAGS -->
<h2 style="color:#c0392b;">Over-Budget Strong Matches — Flag for Manager Review</h2>
<table style="width:100%; border-collapse:collapse; margin-bottom:28px; font-size:13px;">
  <thead>
    <tr style="background:#c0392b; color:white;">
      <th style="padding:8px; text-align:left;">Name</th>
      <th style="padding:8px; text-align:left;">Location</th>
      <th style="padding:8px; text-align:center;">Score</th>
      <th style="padding:8px; text-align:left;">Est. Salary (PKR/mo)</th>
      <th style="padding:8px; text-align:left;">Key Flag</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding:8px;"><strong>Danish Hussain</strong></td>
      <td style="padding:8px;">Hyderabad ✗</td>
      <td style="padding:8px; text-align:center;"><strong>79.7%</strong></td>
      <td style="padding:8px;">500,000 – 800,000</td>
      <td style="padding:8px;">20+ yrs, GM-level. Highest score. Hyderabad-based. Duplicate application (applied twice).</td>
    </tr>
    <tr style="background:#f9f9f9;">
      <td style="padding:8px;"><strong>Ahmed Al-Mayadeen</strong></td>
      <td style="padding:8px;">Yemen ✗</td>
      <td style="padding:8px; text-align:center;"><strong>58.2%</strong></td>
      <td style="padding:8px;">USD 3,000 – 6,000/mo</td>
      <td style="padding:8px;">10+ yrs UN (UNHCR, UNESCO). Not Pakistan-based. UN salary scale — well above budget.</td>
    </tr>
  </tbody>
</table>

<!-- WHY DIDN'T THEY MAKE IT -->
<h2 style="color:#1d3557;">Why Each Candidate Did Not Make the Shortlist</h2>
<p style="color:#555; margin-bottom:16px;"><em>Salary estimates are based on Pakistan market benchmarks for 2026. No candidate explicitly stated their salary expectation in their application.</em></p>

<table style="width:100%; border-collapse:collapse; font-size:13px; margin-bottom:32px;">
  <thead>
    <tr style="background:#2c3e50; color:white;">
      <th style="padding:8px; text-align:left;">Name</th>
      <th style="padding:8px; text-align:left;">Score</th>
      <th style="padding:8px; text-align:left;">Est. Salary (PKR/mo)</th>
      <th style="padding:8px; text-align:left;">Primary Reason(s) Not Shortlisted</th>
    </tr>
  </thead>
  <tbody>

    <tr style="background:#fef9e7;">
      <td style="padding:8px;"><strong>Zain Ul Abideen</strong><br><small>Islamabad | M.Phil IR</small></td>
      <td style="padding:8px;">N/A</td>
      <td style="padding:8px;">80,000 – 150,000</td>
      <td style="padding:8px;"><strong>CV unreadable</strong> — PDF could not be parsed by the system. Background (M.Phil IR, Islamabad) suggests possible relevance. <strong>Recommend HR review the file manually before dismissing.</strong></td>
    </tr>

    <tr>
      <td style="padding:8px;"><strong>Bareera Rauf</strong><br><small>Karachi | HopeWorks Founder | Sussex IDS</small></td>
      <td style="padding:8px;">44.5%</td>
      <td style="padding:8px;">120,000 – 200,000</td>
      <td style="padding:8px;"><strong>1. Location</strong> — Based in Karachi; role is in-person Islamabad.<br><strong>2. Limited track record</strong> — Founder of HopeWorks (founded Jan 2025, barely 1 year old). No large-scale institutional fundraising demonstrated.<br><strong>3. Seniority</strong> — Early career; strong academic credentials (Sussex IDS) but limited practical fundraising results.</td>
    </tr>

    <tr style="background:#f9f9f9;">
      <td style="padding:8px;"><strong>Samana Qaseem</strong><br><small>Karachi | USEFP / US Embassy</small></td>
      <td style="padding:8px;">44.3%</td>
      <td style="padding:8px;">100,000 – 180,000</td>
      <td style="padding:8px;"><strong>1. Location</strong> — Based in Karachi; role is Islamabad.<br><strong>2. Wrong fundraising type</strong> — USEFP role is alumni outreach and small grant evaluation, not institutional fundraising from bilateral/multilateral donors.<br><strong>3. Fundraising scale</strong> — No evidence of proposing, winning, or managing large grants. Education sector background is a positive but not sufficient alone.</td>
    </tr>

    <tr>
      <td style="padding:8px;"><strong>Anita Kanwal</strong><br><small>Islamabad | Digital Marketing | Islamic Charities UK</small></td>
      <td style="padding:8px;">39.1%</td>
      <td style="padding:8px;">100,000 – 180,000</td>
      <td style="padding:8px;"><strong>1. Wrong type of fundraising</strong> — Her PKR 30M+ fundraising was through <em>digital marketing campaigns</em> (Google Ads, Meta Ads) for UK Islamic charities. This is consumer/charity digital fundraising, which is fundamentally different from institutional fundraising (grant proposals, donor relationships, multilateral engagement).<br><strong>2. No development sector experience</strong> — No exposure to USAID, FCDO, World Bank, or bilateral donor processes.<br><strong>3. Title mismatch</strong> — She is a Creative/Digital Marketing Manager, not a fundraising professional.</td>
    </tr>

    <tr style="background:#f9f9f9;">
      <td style="padding:8px;"><strong>Mahnoor Mellu</strong><br><small>Lahore | SaaS / Digital Ocean | LUMS</small></td>
      <td style="padding:8px;">39.8%</td>
      <td style="padding:8px;">150,000 – 250,000</td>
      <td style="padding:8px;"><strong>1. Wrong domain</strong> — 5 years of B2B SaaS partnerships (Digital Ocean / Cloudways). Commercial tech partnerships are structurally different from institutional development fundraising.<br><strong>2. Location</strong> — Based in Lahore; role is Islamabad.<br><strong>3. Aspirational pivot</strong> — Cover letter explicitly states this is a "strategic pivot" into social impact. She has zero development sector experience. The JD requires someone who already knows the donor landscape, not someone learning it on the job.</td>
    </tr>

    <tr>
      <td style="padding:8px;"><strong>Fahad Khan</strong><br><small>Islamabad | Real Estate | Masters Economics</small></td>
      <td style="padding:8px;">33.0%</td>
      <td style="padding:8px;">80,000 – 150,000</td>
      <td style="padding:8px;"><strong>1. Wrong domain</strong> — Career spans real estate sales (Pak Advisors, Graana.com, Pixarch), logistics (Cheetay), and hospital QA (Shaukat Khanum). No connection to development sector, education, or institutional fundraising.<br><strong>2. "Associate Manager Fundraising" title misleading</strong> — This was a B2B/B2C sales role, not development sector fundraising from donors.</td>
    </tr>

    <tr style="background:#f9f9f9;">
      <td style="padding:8px;"><strong>Muhammad Taqi</strong><br><small>Islamabad | IT Sales | O3 Interfaces</small></td>
      <td style="padding:8px;">25.2%</td>
      <td style="padding:8px;">150,000 – 250,000</td>
      <td style="padding:8px;"><strong>1. Completely wrong domain</strong> — 8 years in IT industry business development (software, enterprise sales, international tech clients). No crossover with development sector, education, or donor relations.<br><strong>2. No development sector exposure</strong> — His pipeline management and CRM skills are transferable in theory but the sector knowledge gap is too large.</td>
    </tr>

    <tr>
      <td style="padding:8px;"><strong>Muhammad Sumraiz Kundi</strong><br><small>Islamabad | Telenor / Jazz B2B</small></td>
      <td style="padding:8px;">26.1%</td>
      <td style="padding:8px;">80,000 – 130,000</td>
      <td style="padding:8px;"><strong>1. Completely wrong domain</strong> — Telecom B2B sales (GSM, cloud corporate solutions) at Telenor and Jazz. No development sector, NGO, or donor experience.<br><strong>2. Commercial-sector mindset</strong> — Good pipeline and sales metrics, but institutional fundraising requires understanding of grant cycles, compliance, due diligence, and funder relationships — none of which appear in his background.</td>
    </tr>

    <tr style="background:#f9f9f9;">
      <td style="padding:8px;"><strong>Moeen Hassan</strong><br><small>Lahore | AutoCAD Engineer / Real Estate</small></td>
      <td style="padding:8px;">16.5%</td>
      <td style="padding:8px;">60,000 – 120,000</td>
      <td style="padding:8px;"><strong>1. Completely unrelated background</strong> — AutoCAD engineer, construction operations manager, real estate advisor. No fundraising, development sector, or donor experience of any kind.<br><strong>2. Location</strong> — Lahore-based.<br><strong>3. Aspirational only</strong> — Cover letter is well-written but based entirely on ambition, not track record. Cannot be considered for this role without relevant experience.</td>
    </tr>

    <tr>
      <td style="padding:8px;"><strong>Arooj Irfan</strong><br><small>Islamabad | Clinical Psychologist | 12 yrs PIMS</small></td>
      <td style="padding:8px;">11.5%</td>
      <td style="padding:8px;">100,000 – 200,000</td>
      <td style="padding:8px;"><strong>1. Completely unrelated profession</strong> — 12 years as a clinical psychologist at Pakistan Institute of Medical Sciences (DR-TB GFATM Project). Excellent professional in her field, but has zero overlap with fundraising, partnerships, or development sector donor engagement.<br><strong>2. No explanation for career pivot</strong> — No cover letter provided to explain why she is applying for a fundraising role.</td>
    </tr>

    <tr style="background:#f9f9f9;">
      <td style="padding:8px;"><strong>Muhammad Sheraz Khan</strong><br><small>Islamabad | IT/Cloud | via internal email</small></td>
      <td style="padding:8px;">11.0%</td>
      <td style="padding:8px;">150,000 – 250,000</td>
      <td style="padding:8px;"><strong>1. Wrong CV / Possible test application</strong> — Application was submitted via <em>aymen.abid@taleemabad.com</em> (internal Taleemabad email), but the CV belongs to "Muhammad Sheraz Khan" — a Microsoft Account Manager and cloud engineer at ZONES, INC. (U.S.-based company).<br><strong>2. Completely wrong domain</strong> — AWS, Kubernetes, Microsoft licensing. No fundraising or development sector experience.</td>
    </tr>

  </tbody>
</table>

<!-- NO RESUME SECTION -->
<h2 style="color:#7f8c8d;">No Resume Submitted — Auto-Excluded (4 Candidates)</h2>
<table style="width:100%; border-collapse:collapse; font-size:13px; margin-bottom:32px;">
  <thead>
    <tr style="background:#7f8c8d; color:white;">
      <th style="padding:8px;">Name</th>
      <th style="padding:8px;">Source</th>
      <th style="padding:8px;">Reason Excluded</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="padding:8px;">umair Applicant</td><td style="padding:8px;">LinkedIn Quick Apply</td><td style="padding:8px;">No CV. Temporary LinkedIn email. No usable information.</td></tr>
    <tr style="background:#f9f9f9;"><td style="padding:8px;">anitakanwal Applicant</td><td style="padding:8px;">LinkedIn Quick Apply</td><td style="padding:8px;">No CV. Temporary LinkedIn email. (Different from Anita Kanwal who applied separately.)</td></tr>
    <tr><td style="padding:8px;">mahnoor Applicant</td><td style="padding:8px;">LinkedIn Quick Apply</td><td style="padding:8px;">No CV. Temporary LinkedIn email. (Different from Mahnoor Mellu who applied separately.)</td></tr>
    <tr style="background:#f9f9f9;"><td style="padding:8px;">abeernoorbano Applicant</td><td style="padding:8px;">LinkedIn Quick Apply</td><td style="padding:8px;">No CV. Temporary LinkedIn email. No usable information.</td></tr>
  </tbody>
</table>

<!-- KEY INSIGHT BOX -->
<div style="background:#eafaf1; border-left:5px solid #27ae60; padding:16px; margin-bottom:28px; border-radius:4px;">
  <h3 style="margin:0 0 8px 0; color:#1e8449;">Operational Insight — LinkedIn Quick Apply</h3>
  <p style="margin:0;">All 4 LinkedIn Quick Apply submissions contained zero useful information — no CV, no cover letter, temporary email addresses. This is consistent with typical Quick Apply quality. <strong>Recommendation: Disable LinkedIn Quick Apply for this job posting</strong>, or configure it to require CV upload and a written note before submission is accepted. This will save screening time in future rounds.</p>
</div>

<!-- DUPLICATE ALERT -->
<div style="background:#fef9e7; border-left:5px solid #f39c12; padding:16px; margin-bottom:28px; border-radius:4px;">
  <h3 style="margin:0 0 8px 0; color:#d68910;">Duplicate Application Alert — Danish Hussain</h3>
  <p style="margin:0;">Danish Hussain applied <strong>twice</strong> (application IDs 1346 and 1347, identical CV). Please merge or remove the duplicate record from your HRIS. His estimated salary expectation is <strong>PKR 500,000 – 800,000/month</strong> based on his GM-level seniority and 20+ years of experience — well above the PKR 270K ceiling. However, if budget flexibility exists for an exceptional hire, he is worth a conversation about relocation from Hyderabad.</p>
</div>

<!-- NEXT STEPS -->
<h2 style="color:#1d3557;">Recommended Next Steps</h2>
<ol>
  <li style="margin-bottom:8px;"><strong>Interview Arsim Tariq first</strong> — Probe: "Give me a specific example of a proposal you wrote that was funded, and how did you manage the funder relationship afterwards?" Confirm salary expectation (expect PKR 100K–180K).</li>
  <li style="margin-bottom:8px;"><strong>Ask Abdul Salam and Arsalan Ashraf for salary expectations before scheduling</strong> — Both have strong backgrounds but are potentially over budget or need relocation.</li>
  <li style="margin-bottom:8px;"><strong>Quick 20-min call with Mizhgan Kirmani</strong> — Clarify: "When you say you worked with FCDO/USAID, were you fundraising from them, or delivering projects they funded?" The distinction is critical.</li>
  <li style="margin-bottom:8px;"><strong>Manually review Zain Ul Abideen's CV</strong> — File could not be parsed. M.Phil IR, Islamabad-based. May be worth reviewing directly.</li>
  <li style="margin-bottom:8px;"><strong>Disable LinkedIn Quick Apply</strong> for this posting — 4 empty applications wasted screening time.</li>
</ol>

<hr style="margin:32px 0; border:none; border-top:1px solid #ddd;">
<p style="color:#888; font-size:12px;">
  Report generated by <strong>Taleemabad Talent Acquisition Agent</strong> on 2026-02-27<br>
  Position: Fundraising &amp; Partnerships Manager (Job ID 32)<br>
  Hiring Manager: Sabeena Abbasi &mdash; sabeena.abbasi@taleemabad.com<br>
  Sent from: ayesha.khan@taleemabad.com
</p>

</body></html>
"""

msg = MIMEMultipart('alternative')
msg['From'] = EMAIL_USER
msg['To'] = TO
msg['Subject'] = SUBJECT
msg.attach(MIMEText(HTML, 'html'))

try:
    with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        server.send_message(msg)
    print(f"SUCCESS: Email sent to {TO}")
except Exception as e:
    print(f"FAILED: {e}")
