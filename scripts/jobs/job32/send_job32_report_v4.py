import smtplib, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()
import sys as _sys
_sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from scripts.utils.safe_send import safe_sendmail, allow_candidate_addresses


RECIPIENT = "ayesha.khan@taleemabad.com"
SENDER    = os.getenv("EMAIL_USER")
PASSWORD  = os.getenv("EMAIL_PASSWORD")

html = """<!DOCTYPE html>
<html><head><meta charset="UTF-8"></head>
<body style="font-family:Arial,sans-serif;font-size:14px;color:#111827;max-width:1100px;margin:0 auto;padding:24px;background:#fafafa;">

<!-- HEADER -->
<table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom:8px;">
  <tr><td bgcolor="#4C1D95" style="background-color:#4C1D95;padding:20px 24px;border-radius:8px;">
    <span style="color:#ffffff;font-size:22px;font-weight:bold;">&#128203; Candidate Screening Report &mdash; Fundraising &amp; Partnerships Manager</span>
  </td></tr>
</table>
<p style="color:#6B21A8;font-weight:bold;margin-top:4px;">Updated Report v4 &bull; OCR-recovered candidate included (Zain Ul Abideen) &bull; Charts Fixed</p>

<!-- ══ 1. SCREENING SUMMARY ══ -->
<h2 style="color:#6B21A8;border-bottom:3px solid #EC4899;padding-bottom:6px;margin-top:40px;font-size:18px;">1. Screening Summary</h2>
<table cellpadding="0" cellspacing="0" border="0" width="100%">
  <tr><td bgcolor="#EDE9FE" style="background-color:#EDE9FE;border-left:5px solid #7C3AED;border-radius:6px;padding:16px 20px;">
    <table cellpadding="5" cellspacing="0" border="0">
      <tr><td style="color:#6B21A8;font-weight:bold;padding-right:20px;white-space:nowrap;">Job</td><td>Fundraising &amp; Partnerships Manager (Job ID 32)</td></tr>
      <tr><td style="color:#6B21A8;font-weight:bold;">Date</td><td>2026-03-02 (Updated v4 &mdash; Charts Fixed)</td></tr>
      <tr><td style="color:#6B21A8;font-weight:bold;">Pool size</td><td>48 applications</td></tr>
      <tr><td style="color:#6B21A8;font-weight:bold;">Shortlist</td><td>Top 20 (pool &ge;40 rule)</td></tr>
      <tr><td style="color:#6B21A8;font-weight:bold;">Budget</td><td>PKR 150,000 &ndash; 270,000 / month</td></tr>
      <tr><td style="color:#6B21A8;font-weight:bold;">Location</td><td>Islamabad &mdash; In-Person, Permanent</td></tr>
      <tr><td style="color:#6B21A8;font-weight:bold;">CVs readable</td><td>37 / 48 (36 standard PDF + 1 via OCR)</td></tr>
      <tr><td style="color:#6B21A8;font-weight:bold;">Scoring weights</td><td>Must-have 35% &bull; Experience 25% &bull; Domain 10% &bull; Responsibilities 10% &bull; Budget 15% &bull; Location 5%</td></tr>
    </table>
  </td></tr>
</table>

<p><b>Data gaps:</b></p>
<ul>
  <li><span style="color:#DC2626;font-weight:bold;">9 no-resume</span> (LinkedIn Quick Apply &mdash; empty submissions): apps 1332, 1336, 1348, 1350, 1366, 1372, 1386, 1407, 1515</li>
  <li><span style="color:#1D4ED8;font-weight:bold;">1 OCR-recovered</span>: Zain Ul Abideen (1333) &mdash; scanned PDF, extracted via Tesseract OCR. Strong candidate discovered.</li>
  <li><span style="color:#DC2626;font-weight:bold;">1 test/junk entry</span>: AAMIR SOHAIL (1393) &mdash; salary entered as &ldquo;1&rdquo;, .doc file unreadable</li>
  <li><span style="color:#DC2626;font-weight:bold;">2 duplicates</span>: Danish Hussain (1347 = 1346), AAMIR SOHAIL (1418 = 1393)</li>
</ul>

<!-- ══ 2. JD SCORECARD ══ -->
<h2 style="color:#6B21A8;border-bottom:3px solid #EC4899;padding-bottom:6px;margin-top:40px;font-size:18px;">2. JD Scorecard</h2>
<table width="100%" border="1" cellpadding="10" cellspacing="0" style="border-collapse:collapse;border-color:#E5E7EB;font-size:13px;">
  <tr>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;width:150px;text-align:left;">Category</th>
    <th bgcolor="#1D4ED8" style="background-color:#1D4ED8;color:#fff;text-align:left;">Detail</th>
  </tr>
  <tr>
    <td style="font-weight:bold;color:#6B21A8;">Must-haves</td>
    <td>1. Fundraising / partnerships / BD / institutional engagement experience<br>
        2. Knowledge of Pakistan donor landscape (USAID, World Bank, DFID/FCDO, JICA, EU, multilaterals, foundations)<br>
        3. Proposal / concept note / grant writing experience<br>
        4. Pipeline management (30&ndash;50+ opportunities simultaneously)<br>
        5. Islamabad-based <b>or willing to relocate</b><br>
        6. Strong written communication and presentation skills</td>
  </tr>
  <tr bgcolor="#F5F3FF" style="background-color:#F5F3FF;">
    <td style="font-weight:bold;color:#1D4ED8;">Nice-to-haves</td>
    <td>&bull; Existing donor relationships in Pakistan<br>
        &bull; Independently closed $500K+ funding deals<br>
        &bull; Education sector experience<br>
        &bull; Government/policy engagement in Islamabad</td>
  </tr>
  <tr>
    <td style="font-weight:bold;color:#DC2626;">Deal-breakers</td>
    <td>&bull; Zero fundraising/BD/partnerships experience<br>
        &bull; <b>Not Islamabad-based AND not willing to relocate</b> (willing to relocate = acceptable)</td>
  </tr>
  <tr bgcolor="#F5F3FF" style="background-color:#F5F3FF;">
    <td style="font-weight:bold;color:#DB2777;">Constraints</td>
    <td>Budget: PKR 150,000&ndash;270,000/month &bull; Islamabad in-person &bull; Year 1 target: $500K&ndash;$1M+</td>
  </tr>
</table>

<!-- ══ 3. RANKED SHORTLIST ══ -->
<h2 style="color:#6B21A8;border-bottom:3px solid #EC4899;padding-bottom:6px;margin-top:40px;font-size:18px;">3. Ranked Shortlist &mdash; Top 20</h2>
<p style="color:#6B21A8;font-style:italic;font-size:13px;">Pool: 48 &bull; Rule: pool &ge;40 &rarr; top 20. Ranked by total score &rarr; must-have strength &rarr; budget fit.</p>

<table width="100%" border="1" cellpadding="9" cellspacing="0" style="border-collapse:collapse;border-color:#E5E7EB;font-size:13px;">
  <tr>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">#</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">Candidate</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">Score /10</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">Must-have match</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">Salary (PKR/mo)</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">Budget</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">Key Strengths</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">Key Risks</th>
  </tr>
  <tr>
    <td style="font-weight:bold;color:#6B21A8;">1</td><td><b>Mizhgan Kirmani</b></td><td><b>8.0</b></td>
    <td>Donor relations &#10003; Proposals &#10003; FCDO/UNDP/USAID &#10003;</td>
    <td>250,000</td>
    <td><span style="background:#DCFCE7;color:#166534;font-weight:bold;padding:3px 10px;border-radius:12px;white-space:nowrap;">In Budget</span></td>
    <td>Manager Donor Relations TCF; PKR 72M closed FY; FCDO/UN Women/USAID/UNDP direct engagement; Islamabad</td>
    <td>No $500K+ deal independently closed yet</td>
  </tr>
  <tr bgcolor="#F5F3FF" style="background-color:#F5F3FF;">
    <td style="font-weight:bold;color:#DB2777;">2</td><td><b>Arsalan Ashraf</b></td><td><b>7.9</b></td>
    <td>Fundraising &#10003; Proposals &#10003; Pipeline &#10003;</td>
    <td>450,000</td>
    <td><span style="background:#FEE2E2;color:#991B1B;font-weight:bold;padding:3px 10px;border-radius:12px;white-space:nowrap;">Out of Budget</span></td>
    <td>Meta $100K, Chevron $250K, PKR 80M NAVTTC; built fundraising depts from scratch</td>
    <td>CSR/corporate focus; PKR 450K (67% over ceiling); Karachi-based (willing to relocate)</td>
  </tr>
  <tr>
    <td style="font-weight:bold;color:#1D4ED8;">3</td><td><b>Zain Ul Abideen</b> &#128269;</td><td><b>7.8</b></td>
    <td>Proposals &#10003; UNICEF/UNFPA/IRC/WaterAid &#10003; Pipeline &#10003;</td>
    <td>350,000</td>
    <td><span style="background:#FEE2E2;color:#991B1B;font-weight:bold;padding:3px 10px;border-radius:12px;white-space:nowrap;">Out of Budget</span></td>
    <td>US $50M in won proposals; PKR 2.36B at READ Foundation; PKR 1.23B at SPO; Islamabad-based</td>
    <td>PKR 350K over budget; M.Phil IR (not business); freelance periods in CV</td>
  </tr>
  <tr bgcolor="#F5F3FF" style="background-color:#F5F3FF;">
    <td>4</td><td><b>Sadia Sohail</b></td><td><b>7.5</b></td>
    <td>Donor relations &#10003; Proposals &#10003; Budget reporting &#10003;</td>
    <td>140,000</td>
    <td><span style="background:#DCFCE7;color:#166534;font-weight:bold;padding:3px 10px;border-radius:12px;white-space:nowrap;">In Budget</span></td>
    <td>8 yrs donor relations at READ Foundation; fundraising certifications; Islamabad-based</td>
    <td>Domestic NGO only &mdash; no multilateral (USAID/WB/FCDO) experience</td>
  </tr>
  <tr>
    <td>5</td><td><b>Ahad Ahsan Khan</b></td><td><b>7.4</b></td>
    <td>Grants mgmt &#10003; USAID/WB &#10003; $134M portfolio &#10003;</td>
    <td>550,000</td>
    <td><span style="background:#FEE2E2;color:#991B1B;font-weight:bold;padding:3px 10px;border-radius:12px;white-space:nowrap;">Out of Budget</span></td>
    <td>Manager Grants AKU ($134M, 210 grants); World Bank HEDP lead; Islamabad hometown</td>
    <td>Grants compliance &ne; fundraising acquisition; PKR 550K far over budget</td>
  </tr>
  <tr bgcolor="#F5F3FF" style="background-color:#F5F3FF;">
    <td>6</td><td><b>Danish Hussain</b></td><td><b>7.3</b></td>
    <td>Fundraising &#10003; FCDO/EU/WB &#10003; Grant writing &#10003;</td>
    <td>550,000</td>
    <td><span style="background:#FEE2E2;color:#991B1B;font-weight:bold;padding:3px 10px;border-radius:12px;white-space:nowrap;">Out of Budget</span></td>
    <td>20 yrs development; PKR 1B+ mobilized; Head Grants &amp; Partnerships; FCDO/WB/UNDP/ADB</td>
    <td>Hyderabad-based (willing to relocate); PKR 550K (2x ceiling); WASH focus not EdTech</td>
  </tr>
  <tr>
    <td>7</td><td><b>Faheem Baig</b></td><td><b>6.7</b></td>
    <td>Donor networks &#10003; Dev sector &#10003; M.Phil PIDE &#10003;</td>
    <td>145,000</td>
    <td><span style="background:#DCFCE7;color:#166534;font-weight:bold;padding:3px 10px;border-radius:12px;white-space:nowrap;">In Budget</span></td>
    <td>DG-ECHO, GIZ, UN Women, USAID, AKDN networks; CEO/COO prog lead; Islamabad</td>
    <td>Programme implementation &mdash; no quantified proposal wins</td>
  </tr>
  <tr bgcolor="#F5F3FF" style="background-color:#F5F3FF;">
    <td>8</td><td><b>Hamdan Ahmad</b></td><td><b>6.6</b></td>
    <td>WB partnership &#10003; Dev sector &#10003; Education &#10003;</td>
    <td>320,000</td>
    <td><span style="background:#FEE2E2;color:#991B1B;font-weight:bold;padding:3px 10px;border-radius:12px;white-space:nowrap;">Out of Budget</span></td>
    <td>World Bank ESFCD consultant ($100M project); Islamabad; education sector</td>
    <td>Programme mgmt not resource mobilisation; PKR 320K (PKR 50K over &mdash; closest gap)</td>
  </tr>
  <tr>
    <td>9</td><td><b>Mushahid Hussain</b></td><td><b>6.6</b></td>
    <td>Donor reporting &#10003; Fundraising &#10003; Dev sector &#10003;</td>
    <td>170,000</td>
    <td><span style="background:#DCFCE7;color:#166534;font-weight:bold;padding:3px 10px;border-radius:12px;white-space:nowrap;">In Budget</span></td>
    <td>Donor Reporting Officer READ Foundation; fundraising, financial proposals; Islamabad</td>
    <td>4 yrs experience &mdash; junior for Manager; reporting not acquisition lead</td>
  </tr>
  <tr bgcolor="#F5F3FF" style="background-color:#F5F3FF;">
    <td>10</td><td><b>Shakir Manzoor Khan</b></td><td><b>6.5</b></td>
    <td>Resource mobilisation &#10003; Grant proposals &#10003; PPP &#10003;</td>
    <td>350,000</td>
    <td><span style="background:#FEE2E2;color:#991B1B;font-weight:bold;padding:3px 10px;border-radius:12px;white-space:nowrap;">Out of Budget</span></td>
    <td>15 yrs resource mobilization; Commonwealth Foundation, WHO, AEIF proposals; Rawalpindi</td>
    <td>Health/pharma focus; grant contributions appear supporting not lead; PKR 350K over</td>
  </tr>
  <tr>
    <td>11</td><td><b>Ahmed Al-Mayadeen</b></td><td><b>6.4</b></td>
    <td>UN fundraising &#10003; Multi-million campaigns &#10003;</td>
    <td>~PKR 980K ($3,500/mo)</td>
    <td><span style="background:#FEE2E2;color:#991B1B;font-weight:bold;padding:3px 10px;border-radius:12px;white-space:nowrap;">Out of Budget</span></td>
    <td>10+ yrs UN/NGO fundraising; UNESCO roster; Harvard Business diploma</td>
    <td>Yemen-based; PKR 980K (3.6x ceiling); Pakistan donor relationships unclear</td>
  </tr>
  <tr bgcolor="#F5F3FF" style="background-color:#F5F3FF;">
    <td>12</td><td><b>Muhammad Usman</b></td><td><b>6.1</b></td>
    <td>Partnerships &#10003; Fundraising (competency) &#10003;</td>
    <td>350,000</td>
    <td><span style="background:#FEE2E2;color:#991B1B;font-weight:bold;padding:3px 10px;border-radius:12px;white-space:nowrap;">Out of Budget</span></td>
    <td>18 yrs stakeholder mgmt; international development alliances; Rawalpindi/Islamabad</td>
    <td>Fundraising listed but not quantified; PKR 350K over budget</td>
  </tr>
  <tr>
    <td>13</td><td><b>Abdul Salam</b></td><td><b>5.9</b></td>
    <td>Donor projects &#10003; WB/USAID/DFID &#10003;</td>
    <td>400,000</td>
    <td><span style="background:#FEE2E2;color:#991B1B;font-weight:bold;padding:3px 10px;border-radius:12px;white-space:nowrap;">Out of Budget</span></td>
    <td>21 yrs development; managed WB/USAID/DFID/GIZ/UNICEF programmes; Islamabad</td>
    <td>WASH implementation not resource mobilisation; PKR 400K over budget</td>
  </tr>
  <tr bgcolor="#F5F3FF" style="background-color:#F5F3FF;">
    <td>14</td><td><b>Zubair Hussain</b></td><td><b>5.6</b></td>
    <td>Dev sector &#10003; SEF education &#10003;</td>
    <td>30,000 &#9888;</td>
    <td><span style="background:#FEF9C3;color:#854D0E;font-weight:bold;padding:3px 10px;border-radius:12px;white-space:nowrap;">Unknown*</span></td>
    <td>PPAF-ITC-EU project; education programme; gender/rights-based</td>
    <td>Salary anomaly (30K desired vs 250K current &mdash; likely typo); field specialist not BD</td>
  </tr>
  <tr>
    <td>15</td><td><b>Arsim Tariq</b></td><td><b>5.4</b></td>
    <td>Proposals &#10003; FCDO/WB contracts &#10003; Education &#10003;</td>
    <td>280,000&ndash;300,000</td>
    <td><span style="background:#FEE2E2;color:#991B1B;font-weight:bold;padding:3px 10px;border-radius:12px;white-space:nowrap;">Out of Budget</span></td>
    <td>10+ dev sector proposals won; FCDO/WB contracts; Islamabad; NUST MS</td>
    <td>Programme mgmt/M&amp;E role; PKR 280K&ndash;300K marginally over 270K ceiling</td>
  </tr>
  <tr bgcolor="#F5F3FF" style="background-color:#F5F3FF;">
    <td>16</td><td><b>Fahad Khan</b></td><td><b>5.0</b></td>
    <td>Fundraising role &#10003; Pipeline &#10003;</td>
    <td>350,000</td>
    <td><span style="background:#FEE2E2;color:#991B1B;font-weight:bold;padding:3px 10px;border-radius:12px;white-space:nowrap;">Out of Budget</span></td>
    <td>Associate Manager Fundraising Shaukat Khanum; BD experience; Islamabad</td>
    <td>Hospital charity &ne; institutional donors; PKR 350K over budget</td>
  </tr>
  <tr>
    <td>17</td><td><b>Mahnoor Mellu</b></td><td><b>5.0</b></td>
    <td>Partnerships &#10003; B2B pipeline &#10003;</td>
    <td>350,000</td>
    <td><span style="background:#FEE2E2;color:#991B1B;font-weight:bold;padding:3px 10px;border-radius:12px;white-space:nowrap;">Out of Budget</span></td>
    <td>Partnerships Manager DigitalOcean-Cloudways; LUMS graduate</td>
    <td>Tech/SaaS &ne; dev sector fundraising; Lahore (willing to relocate); PKR 350K over</td>
  </tr>
  <tr bgcolor="#F5F3FF" style="background-color:#F5F3FF;">
    <td>18</td><td><b>Imran Haider</b></td><td><b>4.9</b></td>
    <td>Education policy &#10003; WB/MoFEPT &#10003;</td>
    <td>350,000</td>
    <td><span style="background:#FEE2E2;color:#991B1B;font-weight:bold;padding:3px 10px;border-radius:12px;white-space:nowrap;">Out of Budget</span></td>
    <td>LUMS; education policy &amp; M&amp;E; WB PHCIP consultant; strong edu alignment</td>
    <td>Policy/implementation not resource mobilisation; PKR 350K over; Lahore (willing to relocate)</td>
  </tr>
  <tr>
    <td>19</td><td><b>Sameen Amjad Ali</b></td><td><b>3.6</b></td>
    <td>Stakeholder engagement &#10003;</td>
    <td>650,000</td>
    <td><span style="background:#FEE2E2;color:#991B1B;font-weight:bold;padding:3px 10px;border-radius:12px;white-space:nowrap;">Out of Budget</span></td>
    <td>Senior marketing/comms; investor-facing materials; ministerial engagement</td>
    <td>No donor/dev sector fundraising; PKR 650K (2.4x budget)</td>
  </tr>
  <tr bgcolor="#F5F3FF" style="background-color:#F5F3FF;">
    <td>20</td><td><b>Syeda Kainat</b></td><td><b>3.3</b></td>
    <td>Education &#10003; M&amp;E &#10003; Islamabad &#10003;</td>
    <td>110,000</td>
    <td><span style="background:#DCFCE7;color:#166534;font-weight:bold;padding:3px 10px;border-radius:12px;white-space:nowrap;">In Budget</span></td>
    <td>Education sector; WB TEACH certified; Islamabad; within budget</td>
    <td>M&amp;E/comms officer &mdash; missing all core fundraising must-haves for Manager</td>
  </tr>
</table>
<p style="font-size:12px;color:#6B7280;">&#128269; = OCR-recovered candidate (scanned PDF, read via Tesseract OCR)</p>

<!-- ══ 4. STRONGEST 3 — DEEP COMPARE ══ -->
<h2 style="color:#6B21A8;border-bottom:3px solid #EC4899;padding-bottom:6px;margin-top:40px;font-size:18px;">4. Strongest 3 Candidates &mdash; Deep Comparison</h2>

<table cellpadding="0" cellspacing="0" border="0" width="100%" style="margin-bottom:16px;">
  <tr><td bgcolor="#ffffff" style="background:#fff;border:1px solid #DDD6FE;border-left:5px solid #7C3AED;border-radius:6px;padding:16px;">
    <p style="margin:0 0 6px 0;font-size:15px;color:#1D4ED8;font-weight:bold;">&#127947; Mizhgan Kirmani &nbsp;
      <span style="background:linear-gradient(135deg,#7C3AED,#EC4899);color:#fff;border-radius:20px;padding:4px 14px;font-weight:bold;font-size:14px;">8.0 / 10</span>
      &nbsp;<span style="background:#DCFCE7;color:#166534;font-weight:bold;padding:3px 10px;border-radius:12px;">In Budget &bull; PKR 250,000</span>
    </p>
    <p style="margin:6px 0;"><b style="color:#6B21A8;">Why she&rsquo;s top:</b></p>
    <ul style="margin:4px 0;padding-left:20px;">
      <li>Currently <b>Manager Donor Relations at Citizens Foundation</b> &mdash; closed the FY at PKR 72M. Live, active institutional fundraising in Pakistan&rsquo;s education sector.</li>
      <li>Direct named relationships with <b>FCDO, UN Women, UNDP, USAID, Green Climate Fund</b> &mdash; the exact donor ecosystem in the JD.</li>
      <li>Islamabad-based, proposal writing active, within budget at PKR 250K &mdash; no location or budget risk.</li>
    </ul>
    <p style="margin:6px 0;"><b style="color:#DC2626;">Risks:</b></p>
    <ul style="margin:4px 0;padding-left:20px;">
      <li>PKR 72M track record is strong but below the JD&rsquo;s Year 1 target of $500K&ndash;$1M+ (PKR 140M&ndash;280M).</li>
      <li>Probe in interview: has she independently won large competitive grants, or supported senior leads?</li>
    </ul>
  </td></tr>
</table>

<table cellpadding="0" cellspacing="0" border="0" width="100%" style="margin-bottom:16px;">
  <tr><td bgcolor="#ffffff" style="background:#fff;border:1px solid #DDD6FE;border-left:5px solid #DB2777;border-radius:6px;padding:16px;">
    <p style="margin:0 0 6px 0;font-size:15px;color:#1D4ED8;font-weight:bold;">&#127948; Zain Ul Abideen &#128269; &nbsp;
      <span style="background:linear-gradient(135deg,#7C3AED,#EC4899);color:#fff;border-radius:20px;padding:4px 14px;font-weight:bold;font-size:14px;">7.8 / 10</span>
      &nbsp;<span style="background:#FEE2E2;color:#991B1B;font-weight:bold;padding:3px 10px;border-radius:12px;">Out of Budget &bull; PKR 350,000</span>
    </p>
    <p style="margin:6px 0;"><b style="color:#1D4ED8;">Why he&rsquo;s strong (flag for HM):</b></p>
    <ul style="margin:4px 0;padding-left:20px;">
      <li><b>US $50M lifetime in won proposals</b>: PKR 2.36B (US $8.44M) at READ Foundation alone; PKR 1.23B (US $4.42M) at SPO. These are actual closed funding relationships with UNICEF, UNFPA, US Embassy, British Council, Oxfam, IRC, WaterAid, Save the Children.</li>
      <li><b>Islamabad-based with direct NGO fundraising leadership</b> &mdash; Deputy Manager at READ Foundation (exactly the kind of organisation Taleemabad competes with for the same donors).</li>
      <li>Strong proposal writer with 16+ years experience &mdash; including RFP/RFI/RFQ wins for US government contracts.</li>
    </ul>
    <p style="margin:6px 0;"><b style="color:#DC2626;">Risks:</b></p>
    <ul style="margin:4px 0;padding-left:20px;">
      <li>PKR 350K &mdash; PKR 80K over budget ceiling. Gap is the smallest among the strong-but-over-budget group.</li>
      <li>CV was scanned and originally missed &mdash; process gap now fixed with OCR.</li>
    </ul>
  </td></tr>
</table>

<table cellpadding="0" cellspacing="0" border="0" width="100%" style="margin-bottom:16px;">
  <tr><td bgcolor="#ffffff" style="background:#fff;border:1px solid #DDD6FE;border-left:5px solid #1D4ED8;border-radius:6px;padding:16px;">
    <p style="margin:0 0 6px 0;font-size:15px;color:#1D4ED8;font-weight:bold;">&#127949; Sadia Sohail &nbsp;
      <span style="background:linear-gradient(135deg,#7C3AED,#EC4899);color:#fff;border-radius:20px;padding:4px 14px;font-weight:bold;font-size:14px;">7.5 / 10</span>
      &nbsp;<span style="background:#DCFCE7;color:#166534;font-weight:bold;padding:3px 10px;border-radius:12px;">In Budget &bull; PKR 140,000</span>
    </p>
    <p style="margin:6px 0;"><b style="color:#16A34A;">Best in-budget safety option:</b></p>
    <ul style="margin:4px 0;padding-left:20px;">
      <li><b>8 dedicated years in donor relations at READ Foundation</b> &mdash; proposal writing, donor database, budget reporting, funder communications. Most sustained in-budget donor relations experience.</li>
      <li>Fundraising-specific certifications: Major Donor Fundraising, NGO Boot Camp, Fundraising Essentials.</li>
      <li>Islamabad-based at PKR 140K &mdash; most affordable senior option with genuine donor relations background.</li>
    </ul>
    <p style="margin:6px 0;"><b style="color:#DC2626;">Risks:</b></p>
    <ul style="margin:4px 0;padding-left:20px;">
      <li>READ Foundation is domestic NGO &mdash; no multilateral (USAID/WB/FCDO/EU) experience. Step-up to international donor landscape is material.</li>
      <li>No evidence of 30&ndash;50 opportunity pipeline at scale.</li>
    </ul>
  </td></tr>
</table>

<h3 style="color:#1D4ED8;margin-top:20px;">Comparison Matrix &mdash; Top 3</h3>
<table width="100%" border="1" cellpadding="9" cellspacing="0" style="border-collapse:collapse;border-color:#E5E7EB;font-size:13px;">
  <tr>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">Criteria</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">Mizhgan Kirmani</th>
    <th bgcolor="#BE185D" style="background-color:#BE185D;color:#fff;">Zain Ul Abideen &#128269;</th>
    <th bgcolor="#1D4ED8" style="background-color:#1D4ED8;color:#fff;">Sadia Sohail</th>
  </tr>
  <tr><td><b>Score</b></td><td>8.0</td><td>7.8</td><td>7.5</td></tr>
  <tr bgcolor="#F5F3FF" style="background-color:#F5F3FF;"><td><b>Budget</b></td><td>&#10003; PKR 250K</td><td>&#10007; PKR 350K (+80K)</td><td>&#10003; PKR 140K</td></tr>
  <tr><td><b>Location</b></td><td>&#10003; Islamabad</td><td>&#10003; Islamabad</td><td>&#10003; Rawalpindi/Isb</td></tr>
  <tr bgcolor="#F5F3FF" style="background-color:#F5F3FF;"><td><b>Fundraising track record</b></td><td>PKR 72M closed (FY)</td><td>US $50M+ in won proposals</td><td>Donor relations (no $ stated)</td></tr>
  <tr><td><b>Multilateral donors</b></td><td>&#10003; FCDO/UN Women/USAID/UNDP</td><td>&#10003; UNICEF/UNFPA/US Embassy/IRC</td><td>&#10007; Domestic NGO only</td></tr>
  <tr bgcolor="#F5F3FF" style="background-color:#F5F3FF;"><td><b>Proposal writing</b></td><td>&#10003; Active</td><td>&#10003; Core career skill</td><td>&#10003; Active</td></tr>
  <tr><td><b>$500K+ closed independently</b></td><td>&#10007; Not evidenced</td><td>&#10003; Multiple ($4.42M, $8.44M)</td><td>&#10007; Not evidenced</td></tr>
  <tr bgcolor="#F5F3FF" style="background-color:#F5F3FF;"><td><b>Education sector</b></td><td>&#10003; TCF/EdTech</td><td>&#10003; READ Foundation</td><td>&#10003; READ Foundation</td></tr>
  <tr><td><b>Seniority</b></td><td>Senior (8yr)</td><td>Senior (16yr)</td><td>Mid (10yr)</td></tr>
  <tr bgcolor="#F5F3FF" style="background-color:#F5F3FF;">
    <td><b>Recommended action</b></td>
    <td style="color:#16A34A;font-weight:bold;">Interview first</td>
    <td style="color:#D97706;font-weight:bold;">HM decision on budget</td>
    <td style="color:#16A34A;font-weight:bold;">Interview (backup)</td>
  </tr>
</table>

<!-- ══ 5. STRONG BUT OUT OF BUDGET ══ -->
<h2 style="color:#6B21A8;border-bottom:3px solid #EC4899;padding-bottom:6px;margin-top:40px;font-size:18px;">5. Strong Match but Out of Budget</h2>
<table cellpadding="0" cellspacing="0" border="0" width="100%">
  <tr><td bgcolor="#FEF3C7" style="background-color:#FEF3C7;border-left:5px solid #D97706;border-radius:6px;padding:16px 20px;margin-bottom:16px;">
    These candidates scored &ge;6.5/10 but are above the PKR 270K ceiling. Do not exclude silently &mdash; flagged for hiring manager review.
  </td></tr>
</table>
<br>
<table width="100%" border="1" cellpadding="9" cellspacing="0" style="border-collapse:collapse;border-color:#E5E7EB;font-size:13px;">
  <tr>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">Candidate</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">Score</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">Salary Desired</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">Budget Gap</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">Why They&rsquo;re Strong</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">Notes</th>
  </tr>
  <tr>
    <td><b>Arsalan Ashraf</b></td><td>7.9</td><td>PKR 450,000</td>
    <td><span style="color:#DC2626;font-weight:bold;">+PKR 180,000</span></td>
    <td>Highest fundraising deal-closing in pool: Meta $100K, Chevron $250K, PKR 80M NAVTTC; built fundraising functions at 3 orgs</td>
    <td>Karachi-based, willing to relocate; has existing Islamabad office. Budget negotiation required.</td>
  </tr>
  <tr bgcolor="#F5F3FF" style="background-color:#F5F3FF;">
    <td><b>Zain Ul Abideen &#128269;</b></td><td>7.8</td><td>PKR 350,000</td>
    <td><span style="color:#DC2626;font-weight:bold;">+PKR 80,000</span></td>
    <td>US $50M in won proposals; UNICEF/UNFPA/IRC/WaterAid/US Embassy direct donor relationships; Islamabad-based; 16+ years</td>
    <td>Smallest budget gap in this group. Islamabad-based &mdash; no relocation risk. Strong candidate to negotiate with.</td>
  </tr>
  <tr>
    <td><b>Ahad Ahsan Khan</b></td><td>7.4</td><td>PKR 550,000</td>
    <td><span style="color:#DC2626;font-weight:bold;">+PKR 280,000</span></td>
    <td>$134M grants portfolio (AKU, 210 grants); World Bank HEDP; Islamabad hometown</td>
    <td>Grants compliance role &mdash; fundraising acquisition needs probing. Large salary gap.</td>
  </tr>
  <tr bgcolor="#F5F3FF" style="background-color:#F5F3FF;">
    <td><b>Danish Hussain</b></td><td>7.3</td><td>PKR 550,000</td>
    <td><span style="color:#DC2626;font-weight:bold;">+PKR 280,000</span></td>
    <td>20 yrs dev sector; PKR 1B+ mobilized; Head Grants &amp; Partnerships; FCDO/WB/UNDP/ADB; applied twice</td>
    <td>Hyderabad-based, willing to relocate. WASH focus not EdTech. Duplicate application (1346+1347).</td>
  </tr>
  <tr>
    <td><b>Hamdan Ahmad</b></td><td>6.6</td><td>PKR 320,000</td>
    <td><span style="color:#DC2626;font-weight:bold;">+PKR 50,000</span></td>
    <td>World Bank ESFCD consultant ($100M project); Islamabad-based; education/social sector</td>
    <td>Closest to budget in group &mdash; PKR 50K gap may be negotiable. Programme mgmt not BD.</td>
  </tr>
  <tr bgcolor="#F5F3FF" style="background-color:#F5F3FF;">
    <td><b>Shakir Manzoor Khan</b></td><td>6.5</td><td>PKR 350,000</td>
    <td><span style="color:#DC2626;font-weight:bold;">+PKR 80,000</span></td>
    <td>15 yrs resource mobilization; Commonwealth Foundation, WHO, AEIF grant contributions; PPP experience</td>
    <td>Rawalpindi-based; pharma/health focus; grant role appears supporting not lead.</td>
  </tr>
</table>

<!-- ══ 6. WHY OTHERS DIDN'T MAKE THE CUT ══ -->
<h2 style="color:#6B21A8;border-bottom:3px solid #EC4899;padding-bottom:6px;margin-top:40px;font-size:18px;">6. Why Others Didn&rsquo;t Make the Cut</h2>
<table width="100%" border="1" cellpadding="9" cellspacing="0" style="border-collapse:collapse;border-color:#E5E7EB;font-size:13px;">
  <tr>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">Bucket</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">Count</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">Candidates</th>
  </tr>
  <tr>
    <td><b style="color:#DC2626;">Missing must-have skills</b><br>(no fundraising/BD/donor exp)</td><td>14</td>
    <td>Muhammad Taqi (IT SaaS BD), Aqsa Gul (customer service), Muhammad Akmal (admin), Asim Ur Rehman (rural volunteer), Hasan Shahid (marketing/PR), Sheraz Khan (Microsoft licensing), Anita Kanwal (UK charity digital), Muhammad Ali Zafar (research intern), Laveeza Shah (HR/admin), Moeen Hassan (AutoCAD/real estate), Zainab (early career HR), Muhammad Sumraiz Kundi (telecom sales), Sani Muhammad (IT/ops), Arooj Irfan (clinical psychologist)</td>
  </tr>
  <tr bgcolor="#F5F3FF" style="background-color:#F5F3FF;">
    <td><b style="color:#DC2626;">No resume submitted</b><br>(LinkedIn Quick Apply)</td><td>9</td>
    <td>umair (1332), anitakanwal (1336), mahnoor (1348), abeernoorbano (1350), tanveeralamm (1366), usmaanq (1372), imran (1386), saad (1407), hassansajjadkhan (1515)</td>
  </tr>
  <tr>
    <td><b style="color:#DC2626;">Budget too high + weak function match</b></td><td>3</td>
    <td>Sameen Amjad Ali (PKR 650K, marketing/comms), Samana Qaseem (PKR 430K, alumni admin), Bareera Rauf (USD 2K/mo, dev research)</td>
  </tr>
  <tr bgcolor="#F5F3FF" style="background-color:#F5F3FF;">
    <td><b style="color:#DC2626;">Test/junk data</b></td><td>1</td>
    <td>AAMIR SOHAIL (1393) &mdash; salary &ldquo;1&rdquo;, .doc format unreadable</td>
  </tr>
  <tr>
    <td><b style="color:#DC2626;">Duplicate application</b></td><td>2</td>
    <td>Danish Hussain (1347 = 1346), AAMIR SOHAIL (1418 = 1393)</td>
  </tr>
</table>

<!-- ══ 7. CHARTS & VISUALS ══ -->
<h2 style="color:#6B21A8;border-bottom:3px solid #EC4899;padding-bottom:6px;margin-top:40px;font-size:18px;">7. Charts &amp; Visuals</h2>

<!-- ── A. Score Bar Chart ── -->
<h3 style="color:#6B21A8;margin-top:20px;">A. Score Distribution &mdash; Top 14 Candidates</h3>
<table cellpadding="0" cellspacing="0" border="0" width="100%">
  <tr><td bgcolor="#ffffff" style="background:#fff;border:1px solid #DDD6FE;border-radius:8px;padding:16px;">

    <table width="100%" cellpadding="0" cellspacing="4" border="0">

      <tr>
        <td width="190" align="right" style="font-size:12px;color:#374151;padding-right:8px;white-space:nowrap;">Mizhgan Kirmani</td>
        <td><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
          <td width="80%" bgcolor="#7C3AED" height="22" style="background-color:#7C3AED;color:#fff;font-size:11px;font-weight:bold;padding:0 8px;white-space:nowrap;">8.0 &nbsp;&#10003; In Budget</td>
          <td bgcolor="#F3F4F6" height="22" style="background-color:#F3F4F6;width:20%;"></td>
        </tr></table></td>
      </tr>

      <tr>
        <td width="190" align="right" style="font-size:12px;color:#374151;padding-right:8px;white-space:nowrap;">Arsalan Ashraf</td>
        <td><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
          <td width="79%" bgcolor="#DC2626" height="22" style="background-color:#DC2626;color:#fff;font-size:11px;font-weight:bold;padding:0 8px;white-space:nowrap;">7.9 &nbsp;Out of Budget</td>
          <td bgcolor="#F3F4F6" height="22" style="background-color:#F3F4F6;width:21%;"></td>
        </tr></table></td>
      </tr>

      <tr>
        <td width="190" align="right" style="font-size:12px;color:#374151;padding-right:8px;white-space:nowrap;">Zain Ul Abideen &#128269;</td>
        <td><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
          <td width="78%" bgcolor="#DB2777" height="22" style="background-color:#DB2777;color:#fff;font-size:11px;font-weight:bold;padding:0 8px;white-space:nowrap;">7.8 &nbsp;Out of Budget</td>
          <td bgcolor="#F3F4F6" height="22" style="background-color:#F3F4F6;width:22%;"></td>
        </tr></table></td>
      </tr>

      <tr>
        <td width="190" align="right" style="font-size:12px;color:#374151;padding-right:8px;white-space:nowrap;">Sadia Sohail</td>
        <td><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
          <td width="75%" bgcolor="#7C3AED" height="22" style="background-color:#7C3AED;color:#fff;font-size:11px;font-weight:bold;padding:0 8px;white-space:nowrap;">7.5 &nbsp;&#10003; In Budget</td>
          <td bgcolor="#F3F4F6" height="22" style="background-color:#F3F4F6;width:25%;"></td>
        </tr></table></td>
      </tr>

      <tr>
        <td width="190" align="right" style="font-size:12px;color:#374151;padding-right:8px;white-space:nowrap;">Ahad Ahsan Khan</td>
        <td><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
          <td width="74%" bgcolor="#DC2626" height="22" style="background-color:#DC2626;color:#fff;font-size:11px;font-weight:bold;padding:0 8px;white-space:nowrap;">7.4 &nbsp;Out of Budget</td>
          <td bgcolor="#F3F4F6" height="22" style="background-color:#F3F4F6;width:26%;"></td>
        </tr></table></td>
      </tr>

      <tr>
        <td width="190" align="right" style="font-size:12px;color:#374151;padding-right:8px;white-space:nowrap;">Danish Hussain</td>
        <td><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
          <td width="73%" bgcolor="#DC2626" height="22" style="background-color:#DC2626;color:#fff;font-size:11px;font-weight:bold;padding:0 8px;white-space:nowrap;">7.3 &nbsp;Out of Budget</td>
          <td bgcolor="#F3F4F6" height="22" style="background-color:#F3F4F6;width:27%;"></td>
        </tr></table></td>
      </tr>

      <tr>
        <td width="190" align="right" style="font-size:12px;color:#374151;padding-right:8px;white-space:nowrap;">Faheem Baig</td>
        <td><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
          <td width="67%" bgcolor="#16A34A" height="22" style="background-color:#16A34A;color:#fff;font-size:11px;font-weight:bold;padding:0 8px;white-space:nowrap;">6.7 &nbsp;&#10003; In Budget</td>
          <td bgcolor="#F3F4F6" height="22" style="background-color:#F3F4F6;width:33%;"></td>
        </tr></table></td>
      </tr>

      <tr>
        <td width="190" align="right" style="font-size:12px;color:#374151;padding-right:8px;white-space:nowrap;">Hamdan Ahmad</td>
        <td><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
          <td width="66%" bgcolor="#D97706" height="22" style="background-color:#D97706;color:#fff;font-size:11px;font-weight:bold;padding:0 8px;white-space:nowrap;">6.6 &nbsp;Out (-PKR 50K)</td>
          <td bgcolor="#F3F4F6" height="22" style="background-color:#F3F4F6;width:34%;"></td>
        </tr></table></td>
      </tr>

      <tr>
        <td width="190" align="right" style="font-size:12px;color:#374151;padding-right:8px;white-space:nowrap;">Mushahid Hussain</td>
        <td><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
          <td width="66%" bgcolor="#16A34A" height="22" style="background-color:#16A34A;color:#fff;font-size:11px;font-weight:bold;padding:0 8px;white-space:nowrap;">6.6 &nbsp;&#10003; In Budget</td>
          <td bgcolor="#F3F4F6" height="22" style="background-color:#F3F4F6;width:34%;"></td>
        </tr></table></td>
      </tr>

      <tr>
        <td width="190" align="right" style="font-size:12px;color:#374151;padding-right:8px;white-space:nowrap;">Shakir Manzoor Khan</td>
        <td><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
          <td width="65%" bgcolor="#DC2626" height="22" style="background-color:#DC2626;color:#fff;font-size:11px;font-weight:bold;padding:0 8px;white-space:nowrap;">6.5 &nbsp;Out of Budget</td>
          <td bgcolor="#F3F4F6" height="22" style="background-color:#F3F4F6;width:35%;"></td>
        </tr></table></td>
      </tr>

      <tr>
        <td width="190" align="right" style="font-size:12px;color:#374151;padding-right:8px;white-space:nowrap;">Ahmed Al-Mayadeen</td>
        <td><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
          <td width="64%" bgcolor="#DC2626" height="22" style="background-color:#DC2626;color:#fff;font-size:11px;font-weight:bold;padding:0 8px;white-space:nowrap;">6.4 &nbsp;Out of Budget</td>
          <td bgcolor="#F3F4F6" height="22" style="background-color:#F3F4F6;width:36%;"></td>
        </tr></table></td>
      </tr>

      <tr>
        <td width="190" align="right" style="font-size:12px;color:#374151;padding-right:8px;white-space:nowrap;">Muhammad Usman</td>
        <td><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
          <td width="61%" bgcolor="#DC2626" height="22" style="background-color:#DC2626;color:#fff;font-size:11px;font-weight:bold;padding:0 8px;white-space:nowrap;">6.1 &nbsp;Out of Budget</td>
          <td bgcolor="#F3F4F6" height="22" style="background-color:#F3F4F6;width:39%;"></td>
        </tr></table></td>
      </tr>

      <tr>
        <td width="190" align="right" style="font-size:12px;color:#374151;padding-right:8px;white-space:nowrap;">Abdul Salam</td>
        <td><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
          <td width="59%" bgcolor="#DC2626" height="22" style="background-color:#DC2626;color:#fff;font-size:11px;font-weight:bold;padding:0 8px;white-space:nowrap;">5.9 &nbsp;Out of Budget</td>
          <td bgcolor="#F3F4F6" height="22" style="background-color:#F3F4F6;width:41%;"></td>
        </tr></table></td>
      </tr>

      <tr>
        <td width="190" align="right" style="font-size:12px;color:#374151;padding-right:8px;white-space:nowrap;">Arsim Tariq</td>
        <td><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
          <td width="54%" bgcolor="#D97706" height="22" style="background-color:#D97706;color:#fff;font-size:11px;font-weight:bold;padding:0 8px;white-space:nowrap;">5.4 &nbsp;Borderline (+10K)</td>
          <td bgcolor="#F3F4F6" height="22" style="background-color:#F3F4F6;width:46%;"></td>
        </tr></table></td>
      </tr>

    </table>

    <p style="font-size:12px;color:#6B7280;margin-top:10px;">
      <b style="color:#7C3AED;">&#9632; Purple</b> = In Budget &nbsp;|&nbsp;
      <b style="color:#16A34A;">&#9632; Green</b> = In Budget (lower score) &nbsp;|&nbsp;
      <b style="color:#DC2626;">&#9632; Red</b> = Out of Budget &nbsp;|&nbsp;
      <b style="color:#D97706;">&#9632; Amber</b> = Borderline / closest gap &nbsp;|&nbsp;
      <b style="color:#DB2777;">&#9632; Pink</b> = OCR candidate
    </p>
  </td></tr>
</table>

<!-- ── B. Budget Distribution Stacked Bar ── -->
<h3 style="color:#6B21A8;margin-top:30px;">B. Budget Fit Overview &mdash; All 48 Applications</h3>
<table cellpadding="0" cellspacing="0" border="0" width="100%">
  <tr><td bgcolor="#ffffff" style="background:#fff;border:1px solid #DDD6FE;border-radius:8px;padding:20px;">

    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="border-radius:6px;overflow:hidden;">
      <tr>
        <td width="25%" bgcolor="#16A34A" height="52" style="background-color:#16A34A;color:#ffffff;text-align:center;font-size:12px;font-weight:bold;vertical-align:middle;padding:4px;">
          &#10003; In Budget<br>~12 candidates<br>(25%)
        </td>
        <td width="52%" bgcolor="#DC2626" height="52" style="background-color:#DC2626;color:#ffffff;text-align:center;font-size:12px;font-weight:bold;vertical-align:middle;padding:4px;">
          &#10007; Out of Budget<br>~25 candidates<br>(52%)
        </td>
        <td width="23%" bgcolor="#7C3AED" height="52" style="background-color:#7C3AED;color:#ffffff;text-align:center;font-size:12px;font-weight:bold;vertical-align:middle;padding:4px;">
          &#9654; No Data / Excluded<br>~11 candidates<br>(23%)
        </td>
      </tr>
    </table>

    <table cellpadding="6" cellspacing="0" border="0" style="margin-top:16px;font-size:13px;">
      <tr>
        <td><span style="display:inline-block;width:14px;height:14px;background-color:#16A34A;vertical-align:middle;margin-right:6px;">&nbsp;</span><b style="color:#16A34A;">In Budget (&le;PKR 270K)</b> &mdash; ~12 candidates</td>
      </tr>
      <tr>
        <td><span style="display:inline-block;width:14px;height:14px;background-color:#DC2626;vertical-align:middle;margin-right:6px;">&nbsp;</span><b style="color:#DC2626;">Out of Budget (&gt;PKR 270K)</b> &mdash; ~25 candidates</td>
      </tr>
      <tr>
        <td><span style="display:inline-block;width:14px;height:14px;background-color:#7C3AED;vertical-align:middle;margin-right:6px;">&nbsp;</span><b style="color:#6B21A8;">No data / Excluded</b> &mdash; ~11 candidates <span style="color:#6B7280;">(9 no-resume, 1 test data, 1 anomalous salary)</span></td>
      </tr>
    </table>

  </td></tr>
</table>

<!-- ── C. Dimension Score Comparison (replaces radar) ── -->
<h3 style="color:#6B21A8;margin-top:30px;">C. Top 3 Candidates &mdash; Score by Dimension</h3>
<table cellpadding="0" cellspacing="0" border="0" width="100%">
  <tr><td bgcolor="#ffffff" style="background:#fff;border:1px solid #DDD6FE;border-radius:8px;padding:20px;">

    <table width="100%" border="1" cellpadding="10" cellspacing="0" style="border-collapse:collapse;border-color:#E5E7EB;font-size:13px;">
      <tr>
        <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;width:200px;text-align:left;">Scoring Dimension</th>
        <th bgcolor="#7C3AED" style="background-color:#7C3AED;color:#fff;text-align:center;">Mizhgan Kirmani<br><span style="font-size:11px;font-weight:normal;">Total: 8.0 / 10</span></th>
        <th bgcolor="#BE185D" style="background-color:#BE185D;color:#fff;text-align:center;">Zain Ul Abideen &#128269;<br><span style="font-size:11px;font-weight:normal;">Total: 7.8 / 10</span></th>
        <th bgcolor="#1D4ED8" style="background-color:#1D4ED8;color:#fff;text-align:center;">Sadia Sohail<br><span style="font-size:11px;font-weight:normal;">Total: 7.5 / 10</span></th>
      </tr>
      <tr>
        <td style="font-weight:bold;padding:10px;">Must-have Match<br><span style="font-size:11px;color:#6B7280;font-weight:normal;">(35% weight)</span></td>
        <td bgcolor="#16A34A" style="background-color:#16A34A;color:#fff;text-align:center;padding:10px;">&#9733;&#9733;&#9733;&#9733;&#9733;<br><span style="font-size:11px;">91% &mdash; FCDO/UNDP/USAID active</span></td>
        <td bgcolor="#16A34A" style="background-color:#16A34A;color:#fff;text-align:center;padding:10px;">&#9733;&#9733;&#9733;&#9733;&#9733;<br><span style="font-size:11px;">94% &mdash; US $50M in won proposals</span></td>
        <td bgcolor="#22C55E" style="background-color:#22C55E;color:#fff;text-align:center;padding:10px;">&#9733;&#9733;&#9733;&#9733;&#9734;<br><span style="font-size:11px;">80% &mdash; Donor relations, proposals</span></td>
      </tr>
      <tr bgcolor="#F9FAFB" style="background-color:#F9FAFB;">
        <td style="font-weight:bold;padding:10px;">Experience<br><span style="font-size:11px;color:#6B7280;font-weight:normal;">(25% weight)</span></td>
        <td bgcolor="#EAB308" style="background-color:#EAB308;color:#111;text-align:center;padding:10px;">&#9733;&#9733;&#9733;&#9734;&#9734;<br><span style="font-size:11px;">72% &mdash; 8 yrs, strong domain</span></td>
        <td bgcolor="#22C55E" style="background-color:#22C55E;color:#fff;text-align:center;padding:10px;">&#9733;&#9733;&#9733;&#9733;&#9734;<br><span style="font-size:11px;">84% &mdash; 16 yrs, large-scale wins</span></td>
        <td bgcolor="#EAB308" style="background-color:#EAB308;color:#111;text-align:center;padding:10px;">&#9733;&#9733;&#9733;&#9734;&#9734;<br><span style="font-size:11px;">72% &mdash; 10 yrs donor relations</span></td>
      </tr>
      <tr>
        <td style="font-weight:bold;padding:10px;">Domain / Industry<br><span style="font-size:11px;color:#6B7280;font-weight:normal;">(10% weight)</span></td>
        <td bgcolor="#22C55E" style="background-color:#22C55E;color:#fff;text-align:center;padding:10px;">&#9733;&#9733;&#9733;&#9733;&#9734;<br><span style="font-size:11px;">80% &mdash; TCF / EdTech</span></td>
        <td bgcolor="#EAB308" style="background-color:#EAB308;color:#111;text-align:center;padding:10px;">&#9733;&#9733;&#9733;&#9734;&#9734;<br><span style="font-size:11px;">70% &mdash; NGO/development</span></td>
        <td bgcolor="#EAB308" style="background-color:#EAB308;color:#111;text-align:center;padding:10px;">&#9733;&#9733;&#9733;&#9734;&#9734;<br><span style="font-size:11px;">70% &mdash; READ Foundation</span></td>
      </tr>
      <tr bgcolor="#F9FAFB" style="background-color:#F9FAFB;">
        <td style="font-weight:bold;padding:10px;">Responsibilities Fit<br><span style="font-size:11px;color:#6B7280;font-weight:normal;">(10% weight)</span></td>
        <td bgcolor="#EAB308" style="background-color:#EAB308;color:#111;text-align:center;padding:10px;">&#9733;&#9733;&#9733;&#9734;&#9734;<br><span style="font-size:11px;">70% &mdash; Pipeline scale unproven</span></td>
        <td bgcolor="#22C55E" style="background-color:#22C55E;color:#fff;text-align:center;padding:10px;">&#9733;&#9733;&#9733;&#9733;&#9734;<br><span style="font-size:11px;">80% &mdash; Large pipeline managed</span></td>
        <td bgcolor="#22C55E" style="background-color:#22C55E;color:#fff;text-align:center;padding:10px;">&#9733;&#9733;&#9733;&#9733;&#9734;<br><span style="font-size:11px;">75% &mdash; Donor comms &amp; reporting</span></td>
      </tr>
      <tr>
        <td style="font-weight:bold;padding:10px;">Budget Fit<br><span style="font-size:11px;color:#6B7280;font-weight:normal;">(15% weight)</span></td>
        <td bgcolor="#16A34A" style="background-color:#16A34A;color:#fff;text-align:center;padding:10px;">&#9733;&#9733;&#9733;&#9733;&#9733;<br><span style="font-size:11px;">&#10003; PKR 250K &mdash; in budget</span></td>
        <td bgcolor="#DC2626" style="background-color:#DC2626;color:#fff;text-align:center;padding:10px;">&#9733;&#9734;&#9734;&#9734;&#9734;<br><span style="font-size:11px;">&#10007; PKR 350K &mdash; over by 80K</span></td>
        <td bgcolor="#16A34A" style="background-color:#16A34A;color:#fff;text-align:center;padding:10px;">&#9733;&#9733;&#9733;&#9733;&#9733;<br><span style="font-size:11px;">&#10003; PKR 140K &mdash; well in budget</span></td>
      </tr>
      <tr bgcolor="#F9FAFB" style="background-color:#F9FAFB;">
        <td style="font-weight:bold;padding:10px;">Location<br><span style="font-size:11px;color:#6B7280;font-weight:normal;">(5% weight)</span></td>
        <td bgcolor="#16A34A" style="background-color:#16A34A;color:#fff;text-align:center;padding:10px;">&#9733;&#9733;&#9733;&#9733;&#9733;<br><span style="font-size:11px;">&#10003; Islamabad</span></td>
        <td bgcolor="#16A34A" style="background-color:#16A34A;color:#fff;text-align:center;padding:10px;">&#9733;&#9733;&#9733;&#9733;&#9733;<br><span style="font-size:11px;">&#10003; Islamabad</span></td>
        <td bgcolor="#16A34A" style="background-color:#16A34A;color:#fff;text-align:center;padding:10px;">&#9733;&#9733;&#9733;&#9733;&#9733;<br><span style="font-size:11px;">&#10003; Rawalpindi / Islamabad</span></td>
      </tr>
    </table>

    <p style="font-size:11px;color:#6B7280;margin-top:8px;">
      &#9733;&#9733;&#9733;&#9733;&#9733; Excellent (&ge;90%) &nbsp;|&nbsp;
      &#9733;&#9733;&#9733;&#9733;&#9734; Good (75&ndash;89%) &nbsp;|&nbsp;
      &#9733;&#9733;&#9733;&#9734;&#9734; Moderate (60&ndash;74%) &nbsp;|&nbsp;
      &#9733;&#9734;&#9734;&#9734;&#9734; Weak (&lt;45%)
      &nbsp;&bull;&nbsp; * Sub-scores are approximate breakdowns. Total scores are authoritative.
    </p>
  </td></tr>
</table>

<!-- ── D. Must-have Heatmap ── -->
<h3 style="color:#6B21A8;margin-top:30px;">D. Must-have Coverage Heatmap &mdash; Top 8 Candidates</h3>
<table width="100%" border="1" cellpadding="9" cellspacing="0" style="border-collapse:collapse;border-color:#E5E7EB;font-size:12px;">
  <tr>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;text-align:left;padding:10px 12px;">Must-have skill</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;text-align:center;">Mizhgan</th>
    <th bgcolor="#BE185D" style="background-color:#BE185D;color:#fff;text-align:center;">Zain &#128269;</th>
    <th bgcolor="#B45309" style="background-color:#B45309;color:#fff;text-align:center;">Arsalan</th>
    <th bgcolor="#155E75" style="background-color:#155E75;color:#fff;text-align:center;">Sadia</th>
    <th bgcolor="#065F46" style="background-color:#065F46;color:#fff;text-align:center;">Faheem</th>
    <th bgcolor="#1D4ED8" style="background-color:#1D4ED8;color:#fff;text-align:center;">Mushahid</th>
    <th bgcolor="#92400E" style="background-color:#92400E;color:#fff;text-align:center;">Danish</th>
    <th bgcolor="#6B21A8" style="background-color:#6B21A8;color:#fff;text-align:center;">Hamdan</th>
  </tr>
  <tr>
    <td style="padding:9px 12px;">Fundraising / BD / partnerships</td>
    <td bgcolor="#DCFCE7" style="background-color:#DCFCE7;text-align:center;">&#9989;</td>
    <td bgcolor="#DCFCE7" style="background-color:#DCFCE7;text-align:center;">&#9989;</td>
    <td bgcolor="#DCFCE7" style="background-color:#DCFCE7;text-align:center;">&#9989;</td>
    <td bgcolor="#DCFCE7" style="background-color:#DCFCE7;text-align:center;">&#9989;</td>
    <td bgcolor="#FEF9C3" style="background-color:#FEF9C3;text-align:center;">&#9888;</td>
    <td bgcolor="#FEF9C3" style="background-color:#FEF9C3;text-align:center;">&#9888;</td>
    <td bgcolor="#DCFCE7" style="background-color:#DCFCE7;text-align:center;">&#9989;</td>
    <td bgcolor="#FEF9C3" style="background-color:#FEF9C3;text-align:center;">&#9888;</td>
  </tr>
  <tr bgcolor="#F9FAFB" style="background-color:#F9FAFB;">
    <td style="padding:9px 12px;">Pakistan donor landscape knowledge</td>
    <td bgcolor="#DCFCE7" style="background-color:#DCFCE7;text-align:center;">&#9989;</td>
    <td bgcolor="#DCFCE7" style="background-color:#DCFCE7;text-align:center;">&#9989;</td>
    <td bgcolor="#FEF9C3" style="background-color:#FEF9C3;text-align:center;">&#9888;</td>
    <td bgcolor="#FEF9C3" style="background-color:#FEF9C3;text-align:center;">&#9888;</td>
    <td bgcolor="#DCFCE7" style="background-color:#DCFCE7;text-align:center;">&#9989;</td>
    <td bgcolor="#FEF9C3" style="background-color:#FEF9C3;text-align:center;">&#9888;</td>
    <td bgcolor="#DCFCE7" style="background-color:#DCFCE7;text-align:center;">&#9989;</td>
    <td bgcolor="#DCFCE7" style="background-color:#DCFCE7;text-align:center;">&#9989;</td>
  </tr>
  <tr>
    <td style="padding:9px 12px;">Proposal / grant writing</td>
    <td bgcolor="#DCFCE7" style="background-color:#DCFCE7;text-align:center;">&#9989;</td>
    <td bgcolor="#DCFCE7" style="background-color:#DCFCE7;text-align:center;">&#9989;</td>
    <td bgcolor="#DCFCE7" style="background-color:#DCFCE7;text-align:center;">&#9989;</td>
    <td bgcolor="#DCFCE7" style="background-color:#DCFCE7;text-align:center;">&#9989;</td>
    <td bgcolor="#FEF9C3" style="background-color:#FEF9C3;text-align:center;">&#9888;</td>
    <td bgcolor="#FEF9C3" style="background-color:#FEF9C3;text-align:center;">&#9888;</td>
    <td bgcolor="#DCFCE7" style="background-color:#DCFCE7;text-align:center;">&#9989;</td>
    <td bgcolor="#FEF9C3" style="background-color:#FEF9C3;text-align:center;">&#9888;</td>
  </tr>
  <tr bgcolor="#F9FAFB" style="background-color:#F9FAFB;">
    <td style="padding:9px 12px;">Pipeline management (30&ndash;50+ opps)</td>
    <td bgcolor="#FEF9C3" style="background-color:#FEF9C3;text-align:center;">&#9888;</td>
    <td bgcolor="#DCFCE7" style="background-color:#DCFCE7;text-align:center;">&#9989;</td>
    <td bgcolor="#DCFCE7" style="background-color:#DCFCE7;text-align:center;">&#9989;</td>
    <td bgcolor="#FEF9C3" style="background-color:#FEF9C3;text-align:center;">&#9888;</td>
    <td bgcolor="#FEE2E2" style="background-color:#FEE2E2;text-align:center;">&#10060;</td>
    <td bgcolor="#FEE2E2" style="background-color:#FEE2E2;text-align:center;">&#10060;</td>
    <td bgcolor="#DCFCE7" style="background-color:#DCFCE7;text-align:center;">&#9989;</td>
    <td bgcolor="#FEE2E2" style="background-color:#FEE2E2;text-align:center;">&#10060;</td>
  </tr>
  <tr>
    <td style="padding:9px 12px;">Islamabad / willing to relocate</td>
    <td bgcolor="#DCFCE7" style="background-color:#DCFCE7;text-align:center;">&#9989;</td>
    <td bgcolor="#DCFCE7" style="background-color:#DCFCE7;text-align:center;">&#9989;</td>
    <td bgcolor="#FEF9C3" style="background-color:#FEF9C3;text-align:center;">&#9888;</td>
    <td bgcolor="#DCFCE7" style="background-color:#DCFCE7;text-align:center;">&#9989;</td>
    <td bgcolor="#DCFCE7" style="background-color:#DCFCE7;text-align:center;">&#9989;</td>
    <td bgcolor="#DCFCE7" style="background-color:#DCFCE7;text-align:center;">&#9989;</td>
    <td bgcolor="#FEF9C3" style="background-color:#FEF9C3;text-align:center;">&#9888;</td>
    <td bgcolor="#DCFCE7" style="background-color:#DCFCE7;text-align:center;">&#9989;</td>
  </tr>
  <tr bgcolor="#F9FAFB" style="background-color:#F9FAFB;">
    <td style="padding:9px 12px;">Strong written / presentation skills</td>
    <td bgcolor="#DCFCE7" style="background-color:#DCFCE7;text-align:center;">&#9989;</td>
    <td bgcolor="#DCFCE7" style="background-color:#DCFCE7;text-align:center;">&#9989;</td>
    <td bgcolor="#DCFCE7" style="background-color:#DCFCE7;text-align:center;">&#9989;</td>
    <td bgcolor="#DCFCE7" style="background-color:#DCFCE7;text-align:center;">&#9989;</td>
    <td bgcolor="#DCFCE7" style="background-color:#DCFCE7;text-align:center;">&#9989;</td>
    <td bgcolor="#FEF9C3" style="background-color:#FEF9C3;text-align:center;">&#9888;</td>
    <td bgcolor="#DCFCE7" style="background-color:#DCFCE7;text-align:center;">&#9989;</td>
    <td bgcolor="#DCFCE7" style="background-color:#DCFCE7;text-align:center;">&#9989;</td>
  </tr>
  <tr>
    <td style="padding:9px 12px;">$500K+ deal closed independently</td>
    <td bgcolor="#FEE2E2" style="background-color:#FEE2E2;text-align:center;">&#10060;</td>
    <td bgcolor="#DCFCE7" style="background-color:#DCFCE7;text-align:center;">&#9989;</td>
    <td bgcolor="#DCFCE7" style="background-color:#DCFCE7;text-align:center;">&#9989;</td>
    <td bgcolor="#FEE2E2" style="background-color:#FEE2E2;text-align:center;">&#10060;</td>
    <td bgcolor="#FEE2E2" style="background-color:#FEE2E2;text-align:center;">&#10060;</td>
    <td bgcolor="#FEE2E2" style="background-color:#FEE2E2;text-align:center;">&#10060;</td>
    <td bgcolor="#DCFCE7" style="background-color:#DCFCE7;text-align:center;">&#9989;</td>
    <td bgcolor="#FEE2E2" style="background-color:#FEE2E2;text-align:center;">&#10060;</td>
  </tr>
</table>
<p style="font-size:12px;color:#6B7280;margin-top:6px;">&#9989; Present &nbsp;|&nbsp; &#9888; Partial / Adjacent &nbsp;|&nbsp; &#10060; Absent</p>

<!-- ══ RECOMMENDED NEXT STEPS ══ -->
<h2 style="color:#6B21A8;border-bottom:3px solid #EC4899;padding-bottom:6px;margin-top:40px;font-size:18px;">Recommended Next Steps</h2>
<table cellpadding="0" cellspacing="0" border="0" width="100%">
  <tr><td bgcolor="#DCFCE7" style="background-color:#DCFCE7;border-left:5px solid #16A34A;border-radius:6px;padding:16px 20px;">
    <ol style="margin:0;padding-left:20px;line-height:2.0;">
      <li><b style="color:#6B21A8;">Interview Mizhgan Kirmani first</b> &mdash; strongest in-budget candidate. Probe: what did you personally win vs. support? Largest grant independently closed?</li>
      <li><b style="color:#DB2777;">HM decision on Zain Ul Abideen</b> &mdash; PKR 350K (PKR 80K over ceiling). US $50M in won proposals. Smallest budget gap among all strong-but-out-of-budget candidates. Worth a call to discuss.</li>
      <li><b style="color:#1D4ED8;">Interview Sadia Sohail</b> &mdash; 8 yrs donor relations, in budget. Probe: has she engaged multilateral/bilateral donors directly or only domestic NGOs?</li>
      <li><b style="color:#16A34A;">Interview Faheem Baig and Mushahid Hussain</b> &mdash; both Islamabad-based, within budget. Probe grant writing experience specifically.</li>
      <li><b style="color:#DC2626;">HM decision on Arsalan Ashraf</b> &mdash; strongest fundraising closer in pool but PKR 450K. Budget negotiation required.</li>
      <li><b style="color:#D97706;">Consider Hamdan Ahmad</b> &mdash; PKR 320K, only PKR 50K over ceiling. World Bank background. Closest to negotiability.</li>
      <li><b style="color:#6B7280;">Disable LinkedIn Quick Apply</b> &mdash; 9/48 applications (19%) were empty submissions with temp emails and no CVs.</li>
    </ol>
  </td></tr>
</table>

<!-- FOOTER -->
<table cellpadding="0" cellspacing="0" border="0" width="100%" style="margin-top:48px;">
  <tr><td style="border-top:2px solid #DDD6FE;padding-top:16px;color:#6B7280;font-size:12px;">
    Report generated by Taleemabad Talent Acquisition Agent &bull; 2026-03-02 (v4 &mdash; Email-Safe Charts)<br>
    Job ID 32 &bull; Fundraising &amp; Partnerships Manager &bull; Budget: PKR 150,000&ndash;270,000/month<br>
    Scoring: Must-have 35% &bull; Experience 25% &bull; Domain 10% &bull; Responsibilities 10% &bull; Budget 15% &bull; Location 5%<br>
    Sent to: ayesha.khan@taleemabad.com only &bull; &#128269; = OCR-recovered via Tesseract
  </td></tr>
</table>

</body></html>"""

msg = MIMEMultipart("alternative")
msg["Subject"] = "CORRECTED: Screening Report — Fundraising & Partnerships Manager (v4 · Charts Fixed)"
msg["From"]    = SENDER
msg["To"]      = RECIPIENT
msg.attach(MIMEText(html, "html"))

with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.starttls()
    server.login(SENDER, PASSWORD)
    allow_candidate_addresses(RECIPIENT if isinstance(RECIPIENT, list) else [RECIPIENT])
        safe_sendmail(server, SENDER, RECIPIENT, msg.as_string(), context='send_job32_report_v4')

print(f"SUCCESS: v4 report sent to {RECIPIENT}")
