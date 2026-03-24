import smtplib, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

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
<p style="color:#6B21A8;font-weight:bold;margin-top:4px;">v5 &bull; Re-screened with 7-Dimension Evidence-Based Framework &bull; 2026-03-03</p>

<!-- ══ 1. SCREENING SUMMARY ══ -->
<h2 style="color:#6B21A8;border-bottom:3px solid #EC4899;padding-bottom:6px;margin-top:40px;font-size:18px;">1. Screening Summary</h2>
<table cellpadding="0" cellspacing="0" border="0" width="100%">
  <tr><td bgcolor="#EDE9FE" style="background-color:#EDE9FE;border-left:5px solid #7C3AED;border-radius:6px;padding:16px 20px;">
    <table cellpadding="5" cellspacing="0" border="0">
      <tr><td style="color:#6B21A8;font-weight:bold;padding-right:20px;white-space:nowrap;">Job</td><td>Fundraising &amp; Partnerships Manager (Job ID JOB-0032)</td></tr>
      <tr><td style="color:#6B21A8;font-weight:bold;">Date</td><td>2026-03-03</td></tr>
      <tr><td style="color:#6B21A8;font-weight:bold;">Pool</td><td>48 applications</td></tr>
      <tr><td style="color:#6B21A8;font-weight:bold;">CVs assessed</td><td>37 (36 standard PDF + 1 OCR-recovered) &bull; 11 excluded (9 no-resume, 1 test/junk, 1 duplicate)</td></tr>
      <tr><td style="color:#6B21A8;font-weight:bold;">Budget</td><td>PKR 150,000 &ndash; 270,000 / month</td></tr>
      <tr><td style="color:#6B21A8;font-weight:bold;">Scoring framework</td><td>7-Dimension Evidence-Based Model (scores 0&ndash;100)</td></tr>
      <tr><td style="color:#6B21A8;font-weight:bold;">Viable candidates</td><td><b style="color:#16A34A;">Tier A (85+): 2</b> &bull; <b style="color:#1D4ED8;">Tier B (70&ndash;84): 2</b> &bull; <b style="color:#D97706;">Tier C (55&ndash;69): 1</b> &bull; No-Hire (&lt;55): 32</td></tr>
    </table>
  </td></tr>
</table>

<p><b>Data gaps:</b></p>
<ul>
  <li><span style="color:#DC2626;font-weight:bold;">9 no-resume</span> (LinkedIn Quick Apply): apps 1332, 1336, 1348, 1350, 1366, 1372, 1386, 1407, 1515</li>
  <li><span style="color:#1D4ED8;font-weight:bold;">1 OCR-recovered</span>: Zain Ul Abideen (1333) &mdash; scanned PDF, read via Tesseract OCR. Tier A candidate discovered.</li>
  <li><span style="color:#DC2626;font-weight:bold;">1 test/junk</span>: AAMIR SOHAIL (1393) &mdash; salary entered as &ldquo;1&rdquo;</li>
  <li><span style="color:#DC2626;font-weight:bold;">1 duplicate</span>: Danish Hussain (1347 = 1346)</li>
</ul>

<!-- ══ 2. JD SCORECARD ══ -->
<h2 style="color:#6B21A8;border-bottom:3px solid #EC4899;padding-bottom:6px;margin-top:40px;font-size:18px;">2. Role Deconstruction &amp; JD Scorecard</h2>

<table cellpadding="0" cellspacing="0" border="0" width="100%" style="margin-bottom:12px;">
  <tr><td bgcolor="#F5F3FF" style="background-color:#F5F3FF;border-left:5px solid #7C3AED;border-radius:6px;padding:14px 18px;">
    <b style="color:#6B21A8;">Role Mission:</b> Build and run Taleemabad&rsquo;s institutional fundraising function from Islamabad. Find, develop, and close funding from multilateral donors (USAID, World Bank, FCDO, JICA, EU, UN agencies), foundations, and bilateral partners to hit $500K&ndash;$1M+ in Year 1.
  </td></tr>
</table>

<table width="100%" border="1" cellpadding="10" cellspacing="0" style="border-collapse:collapse;border-color:#E5E7EB;font-size:13px;">
  <tr>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;width:160px;text-align:left;">Element</th>
    <th bgcolor="#1D4ED8" style="background-color:#1D4ED8;color:#fff;text-align:left;">Detail</th>
  </tr>
  <tr>
    <td style="font-weight:bold;color:#6B21A8;">Must-Haves<br><span style="font-size:11px;font-weight:normal;">(double weight)</span></td>
    <td>
      1. Direct fundraising / BD / institutional donor engagement (not programme delivery)<br>
      2. Pakistan donor landscape knowledge &mdash; USAID, World Bank, DFID/FCDO, JICA, EU, multilaterals<br>
      3. Proposal / concept note / grant writing &mdash; submitted and won<br>
      4. Pipeline management: 30&ndash;50+ live opportunities simultaneously<br>
      5. Islamabad-based <b>or explicitly willing to relocate</b> (deal-breaker if neither)<br>
      6. Strong written communication and presentation
    </td>
  </tr>
  <tr bgcolor="#F5F3FF" style="background-color:#F5F3FF;">
    <td style="font-weight:bold;color:#1D4ED8;">Nice-to-Haves</td>
    <td>
      &bull; Independently closed $500K+ deals<br>
      &bull; Named bilateral/multilateral donor relationships in Pakistan<br>
      &bull; Education sector experience<br>
      &bull; Government/policy engagement in Islamabad
    </td>
  </tr>
  <tr>
    <td style="font-weight:bold;color:#DC2626;">Deal-Breakers</td>
    <td>
      &bull; Zero fundraising acquisition experience (delivery/implementation &ne; fundraising)<br>
      &bull; Not Islamabad-based AND not willing to relocate<br>
      &bull; No evidence of winning grants (managing existing grants &ne; fundraising)
    </td>
  </tr>
  <tr bgcolor="#F5F3FF" style="background-color:#F5F3FF;">
    <td style="font-weight:bold;color:#DB2777;">Success in 12 Months</td>
    <td>
      &bull; $500K&ndash;$1M+ in closed or near-close funding<br>
      &bull; Active pipeline of 30&ndash;50+ opportunities at various stages<br>
      &bull; Named relationships with 10+ Pakistan-based donor programme officers<br>
      &bull; Taleemabad known and trusted by FCDO, USAID, and at least 2 other multilaterals
    </td>
  </tr>
</table>

<!-- ══ 3. SCORING FRAMEWORK ══ -->
<h2 style="color:#6B21A8;border-bottom:3px solid #EC4899;padding-bottom:6px;margin-top:40px;font-size:18px;">3. Scoring Framework</h2>
<table width="100%" border="1" cellpadding="9" cellspacing="0" style="border-collapse:collapse;border-color:#E5E7EB;font-size:13px;">
  <tr>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">#</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">Dimension</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">Weight</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">What it measures</th>
  </tr>
  <tr><td>D1</td><td><b>Functional Match</b></td><td>25%</td><td>Does the candidate directly own fundraising/BD/donor engagement? Same scope and complexity?</td></tr>
  <tr bgcolor="#F5F3FF" style="background-color:#F5F3FF;"><td>D2</td><td><b>Demonstrated Outcomes</b></td><td>20%</td><td>Quantified results: grants won, $ raised, donors closed. Cap at 2/4 if no measurable outcomes.</td></tr>
  <tr><td>D3</td><td><b>Environment Fit</b></td><td>15%</td><td>Pakistan development/NGO/donor-funded sector? Islamabad proximity? Similar constraints?</td></tr>
  <tr bgcolor="#F5F3FF" style="background-color:#F5F3FF;"><td>D4</td><td><b>Ownership &amp; Execution</b></td><td>15%</td><td>Built from scratch? Led independently? Closed deals? Or supporting/participating only?</td></tr>
  <tr><td>D5</td><td><b>Stakeholder &amp; Communication</b></td><td>10%</td><td>Named donor/executive/government relationships? Cross-org leadership?</td></tr>
  <tr bgcolor="#F5F3FF" style="background-color:#F5F3FF;"><td>D6</td><td><b>Hard Skills / Technical</b></td><td>10%</td><td>Proposal writing, donor frameworks, grant systems, presentation skills</td></tr>
  <tr><td>D7</td><td><b>Growth &amp; Leadership</b></td><td>5%</td><td>Career progression, team leadership, increasing scope</td></tr>
</table>
<p style="font-size:12px;color:#6B7280;margin-top:6px;">Score scale: 0=Missing &bull; 1=Weak/Adjacent &bull; 2=Partial &bull; 3=Strong &bull; 4=Exceptional with evidence. Missing a must-have = &minus;15% penalty per gap. Decision tiers: 85+ Tier A &bull; 70&ndash;84 Tier B &bull; 55&ndash;69 Tier C &bull; &lt;55 No-Hire.</p>

<!-- ══ 4. RANKED SHORTLIST ══ -->
<h2 style="color:#6B21A8;border-bottom:3px solid #EC4899;padding-bottom:6px;margin-top:40px;font-size:18px;">4. Ranked Results &mdash; All Viable Candidates</h2>
<p style="color:#6B21A8;font-style:italic;font-size:13px;">Only 5 of 37 assessed candidates reached Tier C or above. Pool of 48 with 37 assessable CVs.</p>

<table width="100%" border="1" cellpadding="9" cellspacing="0" style="border-collapse:collapse;border-color:#E5E7EB;font-size:13px;">
  <tr>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">#</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">Candidate</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">Score</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">Tier</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">D1</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">D2</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">D3</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">D4</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">D5</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">D6</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">D7</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">Salary</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">Budget</th>
  </tr>
  <tr>
    <td><b style="color:#6B21A8;">1</b></td>
    <td><b>Danish Hussain</b></td>
    <td><b>97.5</b></td>
    <td bgcolor="#16A34A" style="background-color:#16A34A;color:#fff;font-weight:bold;text-align:center;">Tier A</td>
    <td style="text-align:center;font-weight:bold;color:#16A34A;">4</td><td style="text-align:center;font-weight:bold;color:#16A34A;">4</td>
    <td style="text-align:center;font-weight:bold;color:#16A34A;">3</td><td style="text-align:center;font-weight:bold;color:#16A34A;">4</td>
    <td style="text-align:center;font-weight:bold;color:#16A34A;">4</td><td style="text-align:center;font-weight:bold;color:#16A34A;">4</td>
    <td style="text-align:center;font-weight:bold;color:#16A34A;">4</td>
    <td>PKR 550,000</td>
    <td><span style="background:#FEE2E2;color:#991B1B;font-weight:bold;padding:2px 8px;border-radius:10px;">Out +280K</span></td>
  </tr>
  <tr bgcolor="#F5F3FF" style="background-color:#F5F3FF;">
    <td><b style="color:#DB2777;">2</b></td>
    <td><b>Zain Ul Abideen</b> &#128269;</td>
    <td><b>95.0</b></td>
    <td bgcolor="#16A34A" style="background-color:#16A34A;color:#fff;font-weight:bold;text-align:center;">Tier A</td>
    <td style="text-align:center;font-weight:bold;color:#16A34A;">4</td><td style="text-align:center;font-weight:bold;color:#16A34A;">4</td>
    <td style="text-align:center;font-weight:bold;color:#16A34A;">4</td><td style="text-align:center;font-weight:bold;color:#16A34A;">4</td>
    <td style="text-align:center;font-weight:bold;color:#22C55E;">3</td><td style="text-align:center;font-weight:bold;color:#16A34A;">4</td>
    <td style="text-align:center;font-weight:bold;color:#22C55E;">3</td>
    <td>PKR 350,000</td>
    <td><span style="background:#FEE2E2;color:#991B1B;font-weight:bold;padding:2px 8px;border-radius:10px;">Out +80K</span></td>
  </tr>
  <tr>
    <td><b style="color:#1D4ED8;">3</b></td>
    <td><b>Mizhgan Kirmani</b></td>
    <td><b>78.8</b></td>
    <td bgcolor="#1D4ED8" style="background-color:#1D4ED8;color:#fff;font-weight:bold;text-align:center;">Tier B</td>
    <td style="text-align:center;font-weight:bold;color:#22C55E;">3</td><td style="text-align:center;font-weight:bold;color:#22C55E;">3</td>
    <td style="text-align:center;font-weight:bold;color:#16A34A;">4</td><td style="text-align:center;font-weight:bold;color:#22C55E;">3</td>
    <td style="text-align:center;font-weight:bold;color:#22C55E;">3</td><td style="text-align:center;font-weight:bold;color:#22C55E;">3</td>
    <td style="text-align:center;font-weight:bold;color:#22C55E;">3</td>
    <td>PKR 250,000</td>
    <td><span style="background:#DCFCE7;color:#166534;font-weight:bold;padding:2px 8px;border-radius:10px;">In Budget</span></td>
  </tr>
  <tr bgcolor="#F5F3FF" style="background-color:#F5F3FF;">
    <td><b style="color:#D97706;">4</b></td>
    <td><b>Arsalan Ashraf</b></td>
    <td><b>72.2</b></td>
    <td bgcolor="#1D4ED8" style="background-color:#1D4ED8;color:#fff;font-weight:bold;text-align:center;">Tier B</td>
    <td style="text-align:center;font-weight:bold;color:#16A34A;">4</td><td style="text-align:center;font-weight:bold;color:#22C55E;">3</td>
    <td style="text-align:center;font-weight:bold;color:#22C55E;">3</td><td style="text-align:center;font-weight:bold;color:#16A34A;">4</td>
    <td style="text-align:center;font-weight:bold;color:#22C55E;">3</td><td style="text-align:center;font-weight:bold;color:#22C55E;">3</td>
    <td style="text-align:center;font-weight:bold;color:#16A34A;">4</td>
    <td>PKR 450,000</td>
    <td><span style="background:#FEE2E2;color:#991B1B;font-weight:bold;padding:2px 8px;border-radius:10px;">Out +180K</span></td>
  </tr>
  <tr>
    <td><b style="color:#DC2626;">5</b></td>
    <td><b>Sadia Sohail</b></td>
    <td><b>57.3</b></td>
    <td bgcolor="#D97706" style="background-color:#D97706;color:#fff;font-weight:bold;text-align:center;">Tier C</td>
    <td style="text-align:center;font-weight:bold;color:#22C55E;">3</td><td style="text-align:center;font-weight:bold;color:#EAB308;">2</td>
    <td style="text-align:center;font-weight:bold;color:#22C55E;">3</td><td style="text-align:center;font-weight:bold;color:#22C55E;">3</td>
    <td style="text-align:center;font-weight:bold;color:#EAB308;">2</td><td style="text-align:center;font-weight:bold;color:#22C55E;">3</td>
    <td style="text-align:center;font-weight:bold;color:#EAB308;">2</td>
    <td>PKR 140,000</td>
    <td><span style="background:#DCFCE7;color:#166534;font-weight:bold;padding:2px 8px;border-radius:10px;">In Budget</span></td>
  </tr>
</table>
<p style="font-size:12px;color:#6B7280;">D1=Functional Match &bull; D2=Demonstrated Outcomes &bull; D3=Environment Fit &bull; D4=Ownership &amp; Execution &bull; D5=Stakeholder &amp; Communication &bull; D6=Hard Skills &bull; D7=Growth. &#128269;=OCR-recovered.</p>

<!-- ══ 5. TIER A PROFILES ══ -->
<h2 style="color:#6B21A8;border-bottom:3px solid #EC4899;padding-bottom:6px;margin-top:40px;font-size:18px;">5. Tier A Profiles &mdash; Strong Move Forward</h2>

<!-- Danish Hussain -->
<table cellpadding="0" cellspacing="0" border="0" width="100%" style="margin-bottom:20px;">
  <tr><td bgcolor="#ffffff" style="background:#fff;border:1px solid #DDD6FE;border-left:5px solid #16A34A;border-radius:6px;padding:16px;">
    <p style="margin:0 0 8px 0;font-size:15px;font-weight:bold;color:#111827;">
      &#127947; Danish Hussain &nbsp;
      <span style="background-color:#16A34A;color:#fff;border-radius:20px;padding:4px 14px;font-weight:bold;font-size:14px;">97.5 / 100 &mdash; Tier A</span>
      &nbsp;<span style="background:#FEE2E2;color:#991B1B;font-weight:bold;padding:3px 10px;border-radius:12px;">Out of Budget &bull; PKR 550,000 (+280K)</span>
    </p>
    <table width="100%" border="1" cellpadding="7" cellspacing="0" style="border-collapse:collapse;border-color:#E5E7EB;font-size:12px;margin-bottom:10px;">
      <tr>
        <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;text-align:center;">D1 Functional</th>
        <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;text-align:center;">D2 Outcomes</th>
        <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;text-align:center;">D3 Environment</th>
        <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;text-align:center;">D4 Ownership</th>
        <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;text-align:center;">D5 Stakeholder</th>
        <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;text-align:center;">D6 Hard Skills</th>
        <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;text-align:center;">D7 Growth</th>
      </tr>
      <tr>
        <td bgcolor="#16A34A" style="background-color:#16A34A;color:#fff;text-align:center;font-weight:bold;">4 / 4</td>
        <td bgcolor="#16A34A" style="background-color:#16A34A;color:#fff;text-align:center;font-weight:bold;">4 / 4</td>
        <td bgcolor="#22C55E" style="background-color:#22C55E;color:#fff;text-align:center;font-weight:bold;">3 / 4</td>
        <td bgcolor="#16A34A" style="background-color:#16A34A;color:#fff;text-align:center;font-weight:bold;">4 / 4</td>
        <td bgcolor="#16A34A" style="background-color:#16A34A;color:#fff;text-align:center;font-weight:bold;">4 / 4</td>
        <td bgcolor="#16A34A" style="background-color:#16A34A;color:#fff;text-align:center;font-weight:bold;">4 / 4</td>
        <td bgcolor="#16A34A" style="background-color:#16A34A;color:#fff;text-align:center;font-weight:bold;">4 / 4</td>
      </tr>
    </table>
    <p style="margin:6px 0;"><b style="color:#16A34A;">Top 3 Strengths (Evidence-based):</b></p>
    <ul style="margin:4px 0;padding-left:20px;font-size:13px;">
      <li><b>PKR 1B+ mobilised</b> across FCDO, World Bank, UNDP, ADB &mdash; highest quantified fundraising track record in pool. <span style="color:#6B7280;">[FACT &mdash; stated in CV]</span></li>
      <li><b>Head of Grants &amp; Partnerships at INGO, 20 years</b> &mdash; most senior fundraising title in pool at exactly the right functional level. <span style="color:#6B7280;">[FACT]</span></li>
      <li><b>Named active donor relationships:</b> FCDO Pakistan, UNDP Pakistan, ADB &mdash; the exact bilateral/multilateral network the JD requires. <span style="color:#6B7280;">[FACT]</span></li>
    </ul>
    <p style="margin:6px 0;"><b style="color:#DC2626;">Top 3 Risks:</b></p>
    <ul style="margin:4px 0;padding-left:20px;font-size:13px;">
      <li>Hyderabad-based &mdash; states willing to relocate. Must be confirmed as firm commitment with timeline.</li>
      <li>WASH/humanitarian sector focus &mdash; EdTech fundraising is a pivot. Donor base overlaps significantly but EdTech positioning needs building.</li>
      <li>PKR 550,000 desired is 2x the budget ceiling &mdash; significant exception required from leadership.</li>
    </ul>
    <p style="margin:6px 0;"><b style="color:#1D4ED8;">5 Interview Questions:</b></p>
    <ol style="margin:4px 0;padding-left:20px;font-size:13px;">
      <li>You have stated willingness to relocate &mdash; what is your realistic timeline and are there conditions on that?</li>
      <li>Walk me through the largest single grant you personally closed &mdash; your exact role from inception to award letter.</li>
      <li>Your background is WASH/humanitarian &mdash; how would you reposition Taleemabad to FCDO, UNDP, and ADB as an EdTech investment priority?</li>
      <li>Which programme officers at FCDO Pakistan, UNDP Pakistan, and ADB are you currently in active relationship with?</li>
      <li>The budget ceiling is PKR 270,000/month. Your ask is 550,000. Is there a package structure &mdash; base + performance &mdash; that works for both sides?</li>
    </ol>
    <p style="font-size:12px;color:#6B7280;margin:6px 0;"><b>Confidence:</b> High &bull; <b>Missing must-haves:</b> 0 &bull; <b>Applied twice:</b> yes (1346 + duplicate 1347)</p>
  </td></tr>
</table>

<!-- Zain Ul Abideen -->
<table cellpadding="0" cellspacing="0" border="0" width="100%" style="margin-bottom:20px;">
  <tr><td bgcolor="#ffffff" style="background:#fff;border:1px solid #DDD6FE;border-left:5px solid #16A34A;border-radius:6px;padding:16px;">
    <p style="margin:0 0 8px 0;font-size:15px;font-weight:bold;color:#111827;">
      &#127948; Zain Ul Abideen &#128269; &nbsp;
      <span style="background-color:#16A34A;color:#fff;border-radius:20px;padding:4px 14px;font-weight:bold;font-size:14px;">95.0 / 100 &mdash; Tier A</span>
      &nbsp;<span style="background:#FEE2E2;color:#991B1B;font-weight:bold;padding:3px 10px;border-radius:12px;">Out of Budget &bull; PKR 350,000 (+80K)</span>
    </p>
    <table width="100%" border="1" cellpadding="7" cellspacing="0" style="border-collapse:collapse;border-color:#E5E7EB;font-size:12px;margin-bottom:10px;">
      <tr>
        <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;text-align:center;">D1 Functional</th>
        <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;text-align:center;">D2 Outcomes</th>
        <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;text-align:center;">D3 Environment</th>
        <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;text-align:center;">D4 Ownership</th>
        <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;text-align:center;">D5 Stakeholder</th>
        <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;text-align:center;">D6 Hard Skills</th>
        <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;text-align:center;">D7 Growth</th>
      </tr>
      <tr>
        <td bgcolor="#16A34A" style="background-color:#16A34A;color:#fff;text-align:center;font-weight:bold;">4 / 4</td>
        <td bgcolor="#16A34A" style="background-color:#16A34A;color:#fff;text-align:center;font-weight:bold;">4 / 4</td>
        <td bgcolor="#16A34A" style="background-color:#16A34A;color:#fff;text-align:center;font-weight:bold;">4 / 4</td>
        <td bgcolor="#16A34A" style="background-color:#16A34A;color:#fff;text-align:center;font-weight:bold;">4 / 4</td>
        <td bgcolor="#22C55E" style="background-color:#22C55E;color:#fff;text-align:center;font-weight:bold;">3 / 4</td>
        <td bgcolor="#16A34A" style="background-color:#16A34A;color:#fff;text-align:center;font-weight:bold;">4 / 4</td>
        <td bgcolor="#22C55E" style="background-color:#22C55E;color:#fff;text-align:center;font-weight:bold;">3 / 4</td>
      </tr>
    </table>
    <p style="margin:6px 0;"><b style="color:#16A34A;">Top 3 Strengths:</b></p>
    <ul style="margin:4px 0;padding-left:20px;font-size:13px;">
      <li><b>Lifetime US $50M in won proposals</b> &mdash; US $8.44M at READ Foundation (UNICEF, UNFPA, US Embassy, British Council, Oxfam, IRC, WaterAid, Save the Children); US $4.42M at SPO. Dual-organisation track record confirms pattern not luck. <span style="color:#6B7280;">[FACT]</span></li>
      <li><b>Deputy Manager Resource Mobilisation, Islamabad-based</b> &mdash; senior direct ownership of fundraising function + no relocation risk. <span style="color:#6B7280;">[FACT]</span></li>
      <li><b>Breadth of donor portfolio</b> &mdash; UNICEF, UNFPA, US Embassy, British Council, Oxfam, IRC, WaterAid, Save the Children &mdash; strongest donor network in pool. <span style="color:#6B7280;">[FACT]</span></li>
    </ul>
    <p style="margin:6px 0;"><b style="color:#DC2626;">Top 3 Risks:</b></p>
    <ul style="margin:4px 0;padding-left:20px;font-size:13px;">
      <li>Freelance periods in CV &mdash; reasons and continuity of focus need probing.</li>
      <li>WASH/humanitarian sector dominant &mdash; EdTech fundraising is a pivot, though skill transfer is high.</li>
      <li>PKR 350,000 is PKR 80,000 above ceiling &mdash; smallest budget gap among all out-of-budget candidates. Negotiable.</li>
    </ul>
    <p style="margin:6px 0;"><b style="color:#1D4ED8;">5 Interview Questions:</b></p>
    <ol style="margin:4px 0;padding-left:20px;font-size:13px;">
      <li>Walk me through the single largest proposal you wrote and won &mdash; your exact role from first draft to award.</li>
      <li>Which specific donor programme officers at UNICEF, USAID, FCDO have you worked with in Pakistan &mdash; are these relationships still active?</li>
      <li>You have raised predominantly in WASH/humanitarian &mdash; how would you position Taleemabad to the same donor base?</li>
      <li>What caused the freelance periods in your CV, and what were you working on during those times?</li>
      <li>The budget is PKR 150K&ndash;270K/month. Your ask is 350K. Is there flexibility, and what would make this worth the difference for you?</li>
    </ol>
    <p style="font-size:12px;color:#6B7280;margin:6px 0;"><b>Confidence:</b> High &bull; <b>Missing must-haves:</b> 0 &bull; &#128269; CV was scanned &mdash; recovered via OCR. Would have been missed entirely without OCR capability.</p>
  </td></tr>
</table>

<!-- ══ 6. TIER B PROFILES ══ -->
<h2 style="color:#6B21A8;border-bottom:3px solid #EC4899;padding-bottom:6px;margin-top:40px;font-size:18px;">6. Tier B Profiles &mdash; Interview with Focused Validation</h2>

<!-- Mizhgan -->
<table cellpadding="0" cellspacing="0" border="0" width="100%" style="margin-bottom:20px;">
  <tr><td bgcolor="#ffffff" style="background:#fff;border:1px solid #DDD6FE;border-left:5px solid #1D4ED8;border-radius:6px;padding:16px;">
    <p style="margin:0 0 8px 0;font-size:15px;font-weight:bold;color:#111827;">
      &#127949; Mizhgan Kirmani &nbsp;
      <span style="background-color:#1D4ED8;color:#fff;border-radius:20px;padding:4px 14px;font-weight:bold;font-size:14px;">78.8 / 100 &mdash; Tier B</span>
      &nbsp;<span style="background:#DCFCE7;color:#166534;font-weight:bold;padding:3px 10px;border-radius:12px;">In Budget &bull; PKR 250,000</span>
    </p>
    <table width="100%" border="1" cellpadding="7" cellspacing="0" style="border-collapse:collapse;border-color:#E5E7EB;font-size:12px;margin-bottom:10px;">
      <tr>
        <th bgcolor="#1D4ED8" style="background-color:#1D4ED8;color:#fff;text-align:center;">D1 Functional</th>
        <th bgcolor="#1D4ED8" style="background-color:#1D4ED8;color:#fff;text-align:center;">D2 Outcomes</th>
        <th bgcolor="#1D4ED8" style="background-color:#1D4ED8;color:#fff;text-align:center;">D3 Environment</th>
        <th bgcolor="#1D4ED8" style="background-color:#1D4ED8;color:#fff;text-align:center;">D4 Ownership</th>
        <th bgcolor="#1D4ED8" style="background-color:#1D4ED8;color:#fff;text-align:center;">D5 Stakeholder</th>
        <th bgcolor="#1D4ED8" style="background-color:#1D4ED8;color:#fff;text-align:center;">D6 Hard Skills</th>
        <th bgcolor="#1D4ED8" style="background-color:#1D4ED8;color:#fff;text-align:center;">D7 Growth</th>
      </tr>
      <tr>
        <td bgcolor="#22C55E" style="background-color:#22C55E;color:#fff;text-align:center;font-weight:bold;">3 / 4</td>
        <td bgcolor="#22C55E" style="background-color:#22C55E;color:#fff;text-align:center;font-weight:bold;">3 / 4</td>
        <td bgcolor="#16A34A" style="background-color:#16A34A;color:#fff;text-align:center;font-weight:bold;">4 / 4</td>
        <td bgcolor="#22C55E" style="background-color:#22C55E;color:#fff;text-align:center;font-weight:bold;">3 / 4</td>
        <td bgcolor="#22C55E" style="background-color:#22C55E;color:#fff;text-align:center;font-weight:bold;">3 / 4</td>
        <td bgcolor="#22C55E" style="background-color:#22C55E;color:#fff;text-align:center;font-weight:bold;">3 / 4</td>
        <td bgcolor="#22C55E" style="background-color:#22C55E;color:#fff;text-align:center;font-weight:bold;">3 / 4</td>
      </tr>
    </table>
    <p style="margin:6px 0;"><b style="color:#16A34A;">Top 3 Strengths:</b></p>
    <ul style="margin:4px 0;padding-left:20px;font-size:13px;">
      <li>Manager Donor Relations at TCF &mdash; live fundraising role with FCDO, UN Women, UNDP, USAID, Green Climate Fund. PKR 72M closed in FY. <span style="color:#6B7280;">[FACT]</span></li>
      <li>Islamabad-based, within budget at PKR 250K &mdash; zero location or budget risk. Best risk-adjusted in-budget option. <span style="color:#6B7280;">[FACT]</span></li>
      <li>8 years fundraising + Aga Khan Foundation background &mdash; deep education sector donor pedigree. <span style="color:#6B7280;">[FACT]</span></li>
    </ul>
    <p style="margin:6px 0;"><b style="color:#DC2626;">Top 3 Risks:</b></p>
    <ul style="margin:4px 0;padding-left:20px;font-size:13px;">
      <li>PKR 72M (~$260K) is below the Year 1 target of $500K&ndash;$1M+. Scale of ambition needs validating.</li>
      <li>Largest single deal size unclear &mdash; no $500K+ independently closed grant evidenced.</li>
      <li>Government/policy engagement not evidenced &mdash; Islamabad ministry relationships missing from CV.</li>
    </ul>
    <p style="margin:6px 0;"><b style="color:#1D4ED8;">5 Interview Questions:</b></p>
    <ol style="margin:4px 0;padding-left:20px;font-size:13px;">
      <li>What is the largest single grant you personally closed &mdash; walk through from identification to signature?</li>
      <li>How do you manage a pipeline of 30&ndash;50 opportunities simultaneously &mdash; tools and cadence?</li>
      <li>Which named donor officers at USAID, FCDO, or UNDP Pakistan have you built active relationships with?</li>
      <li>Have you written winning proposals without a dedicated proposal writer &mdash; can you share a sample or describe your writing process?</li>
      <li>The Year 1 target is $500K&ndash;$1M+ from cold. What would your 90-day plan look like at Taleemabad?</li>
    </ol>
    <p style="font-size:12px;color:#6B7280;margin:6px 0;"><b>Confidence:</b> High &bull; <b>Missing must-haves:</b> 0 &bull; <b>Best in-budget candidate</b></p>
  </td></tr>
</table>

<!-- Arsalan Ashraf -->
<table cellpadding="0" cellspacing="0" border="0" width="100%" style="margin-bottom:20px;">
  <tr><td bgcolor="#ffffff" style="background:#fff;border:1px solid #DDD6FE;border-left:5px solid #1D4ED8;border-radius:6px;padding:16px;">
    <p style="margin:0 0 8px 0;font-size:15px;font-weight:bold;color:#111827;">
      &#127948; Arsalan Ashraf &nbsp;
      <span style="background-color:#1D4ED8;color:#fff;border-radius:20px;padding:4px 14px;font-weight:bold;font-size:14px;">72.2 / 100 &mdash; Tier B</span>
      &nbsp;<span style="background:#FEE2E2;color:#991B1B;font-weight:bold;padding:3px 10px;border-radius:12px;">Out of Budget &bull; PKR 450,000 (+180K)</span>
    </p>
    <p style="font-size:12px;color:#D97706;margin:4px 0;"><b>Note: 1 missing must-have applied (&minus;15% penalty)</b> &mdash; Limited multilateral/bilateral (USAID, World Bank, FCDO, EU) donor experience.</p>
    <p style="margin:6px 0;"><b style="color:#16A34A;">Top 3 Strengths:</b></p>
    <ul style="margin:4px 0;padding-left:20px;font-size:13px;">
      <li>Director of Fundraising/BD at multiple NGOs &mdash; built departments from scratch at 3 orgs. Closed Meta $100K, Chevron $250K, PKR 80M NAVTTC. <span style="color:#6B7280;">[FACT]</span></li>
      <li>Pipeline of 15&ndash;20 active opportunities managed simultaneously. <span style="color:#6B7280;">[FACT]</span></li>
      <li>Builder mentality &mdash; built fundraising functions from zero at 3 organisations &mdash; strong Taleemabad fit. <span style="color:#6B7280;">[FACT]</span></li>
    </ul>
    <p style="margin:6px 0;"><b style="color:#DC2626;">Top 3 Risks:</b></p>
    <ul style="margin:4px 0;padding-left:20px;font-size:13px;">
      <li>Corporate CSR and foundation focus &mdash; limited multilateral/bilateral donor experience (USAID, World Bank, FCDO, EU). This is a missing must-have.</li>
      <li>Karachi-based &mdash; willing to relocate stated, but must be confirmed as firm commitment.</li>
      <li>PKR 450,000 ask is PKR 180K above ceiling &mdash; significant budget exception required.</li>
    </ul>
    <p style="margin:6px 0;"><b style="color:#1D4ED8;">5 Interview Questions:</b></p>
    <ol style="margin:4px 0;padding-left:20px;font-size:13px;">
      <li>Your background is primarily corporate CSR &mdash; have you directly engaged USAID, FCDO, World Bank, or EU as a prime grantee?</li>
      <li>Walk me through the USAID sub-grantee experience &mdash; what was your specific role in that funding relationship?</li>
      <li>Which Pakistan-based multilateral donor programme officers are you currently in active relationship with?</li>
      <li>You have built fundraising functions from scratch at 3 orgs &mdash; what would your first 90 days look like here?</li>
      <li>Budget ceiling is 270K. Your ask is 450K. Is there a base + performance structure that bridges this?</li>
    </ol>
    <p style="font-size:12px;color:#6B7280;margin:6px 0;"><b>Confidence:</b> High &bull; <b>Missing must-haves:</b> 1 (multilateral experience)</p>
  </td></tr>
</table>

<!-- ══ 7. TIER C PROFILE ══ -->
<h2 style="color:#6B21A8;border-bottom:3px solid #EC4899;padding-bottom:6px;margin-top:40px;font-size:18px;">7. Tier C Profile &mdash; Risky / Backup Only</h2>

<table cellpadding="0" cellspacing="0" border="0" width="100%" style="margin-bottom:20px;">
  <tr><td bgcolor="#ffffff" style="background:#fff;border:1px solid #DDD6FE;border-left:5px solid #D97706;border-radius:6px;padding:16px;">
    <p style="margin:0 0 8px 0;font-size:15px;font-weight:bold;color:#111827;">
      &#127949; Sadia Sohail &nbsp;
      <span style="background-color:#D97706;color:#fff;border-radius:20px;padding:4px 14px;font-weight:bold;font-size:14px;">57.3 / 100 &mdash; Tier C</span>
      &nbsp;<span style="background:#DCFCE7;color:#166534;font-weight:bold;padding:3px 10px;border-radius:12px;">In Budget &bull; PKR 140,000</span>
    </p>
    <p style="font-size:12px;color:#D97706;margin:4px 0;"><b>Note: 1 missing must-have applied (&minus;15% penalty)</b> &mdash; No multilateral/bilateral donor experience. Proceed only if Tier A and B candidates do not work out.</p>
    <p style="margin:6px 0;"><b style="color:#16A34A;">Top 3 Strengths:</b></p>
    <ul style="margin:4px 0;padding-left:20px;font-size:13px;">
      <li>8 dedicated years in donor relations at READ Foundation &mdash; proposal writing, donor comms, budget reporting. <span style="color:#6B7280;">[FACT]</span></li>
      <li>Fundraising-specific certifications: Major Donor Fundraising, NGO Boot Camp, Fundraising Essentials. <span style="color:#6B7280;">[FACT]</span></li>
      <li>Islamabad-based, within budget at PKR 140K &mdash; most affordable option with genuine donor relations background. <span style="color:#6B7280;">[FACT]</span></li>
    </ul>
    <p style="margin:6px 0;"><b style="color:#DC2626;">Top 3 Risks:</b></p>
    <ul style="margin:4px 0;padding-left:20px;font-size:13px;">
      <li>READ Foundation is a domestic NGO &mdash; no multilateral or bilateral (USAID/WB/FCDO/EU) experience. Missing must-have.</li>
      <li>No quantified outcomes stated &mdash; grants won and amounts raised not cited anywhere in CV. Scored 2/4 on D2.</li>
      <li>8 years at Donor Relations Officer level without progression to Senior BD &mdash; management readiness unproven.</li>
    </ul>
    <p style="margin:6px 0;"><b style="color:#1D4ED8;">5 Interview Questions:</b></p>
    <ol style="margin:4px 0;padding-left:20px;font-size:13px;">
      <li>Have you engaged with any international donors &mdash; USAID, FCDO, World Bank, UNDP, EU &mdash; in a fundraising capacity?</li>
      <li>What is the largest single grant you personally helped close &mdash; amount, donor, and your role?</li>
      <li>What is your understanding of how USAID or FCDO Pakistan structures competitive grant rounds?</li>
      <li>How would you approach building relationships with international donors you have not previously worked with?</li>
      <li>What has kept you at Donor Relations Officer level for 8 years &mdash; and what changed that you are seeking a Manager role?</li>
    </ol>
    <p style="font-size:12px;color:#6B7280;margin:6px 0;"><b>Confidence:</b> High &bull; <b>Missing must-haves:</b> 1 (multilateral experience)</p>
  </td></tr>
</table>

<!-- ══ 8. NO-HIRE SUMMARY ══ -->
<h2 style="color:#6B21A8;border-bottom:3px solid #EC4899;padding-bottom:6px;margin-top:40px;font-size:18px;">8. No-Hire &mdash; Why Others Were Excluded</h2>
<table width="100%" border="1" cellpadding="9" cellspacing="0" style="border-collapse:collapse;border-color:#E5E7EB;font-size:13px;">
  <tr>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">Category</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">Count</th>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;">Candidates &amp; Reason</th>
  </tr>
  <tr>
    <td><b style="color:#DC2626;">Development sector adjacent — no fundraising acquisition</b></td><td>6</td>
    <td>Faheem Baig (programme implementation), Hamdan Ahmad (World Bank programme management), Mushahid Hussain (donor reporting not acquisition), Shakir Manzoor (supporting role), Abdul Salam (WASH delivery), Ahad Ahsan Khan (grants compliance) &mdash; all scored &lt;42</td>
  </tr>
  <tr bgcolor="#F5F3FF" style="background-color:#F5F3FF;">
    <td><b style="color:#DC2626;">Completely unrelated background</b></td><td>15</td>
    <td>Sheraz Khan (Microsoft licensing), Muhammad Taqi (SaaS sales), Sameen Amjad Ali (marketing/comms), Hasan Shahid (digital marketing), Moeen Hassan (AutoCAD/real estate), Sani Muhammad (IT ops), Muhammad Akmal (admin), Arooj Irfan (clinical psychologist), Aqsa Gul (customer service), Laveeza Shah (HR), Asim Ur Rehman (rural volunteer), Muhammad Sumraiz Kundi (telecom sales), Muhammad Ali Zafar (research intern), Zainab (early career HR), Syeda Kainat (M&amp;E/comms)</td>
  </tr>
  <tr>
    <td><b style="color:#DC2626;">Wrong sector / geography</b></td><td>5</td>
    <td>Fahad Khan (hospital charity fundraising), Mahnoor Mellu (SaaS partnerships), Imran Haider (education policy not BD), Anita Kanwal (digital charity campaigns UK), Ahmed Al-Mayadeen (Yemen-based, wrong geography)</td>
  </tr>
  <tr bgcolor="#F5F3FF" style="background-color:#F5F3FF;">
    <td><b style="color:#DC2626;">Borderline / anomalous data</b></td><td>2</td>
    <td>Arsim Tariq (M&amp;E lead, not fundraising owner &mdash; 49.2), Zubair Hussain (salary anomaly, field specialist &mdash; 20.6), Bareera Rauf (researcher not fundraiser &mdash; 18.8), Samana Qaseem (alumni admin &mdash; 8.6)</td>
  </tr>
  <tr>
    <td><b style="color:#DC2626;">No resume / excluded</b></td><td>9</td>
    <td>Apps 1332, 1336, 1348, 1350, 1366, 1372, 1386, 1407, 1515 &mdash; LinkedIn Quick Apply, no CV submitted</td>
  </tr>
</table>

<!-- ══ 9. CHARTS ══ -->
<h2 style="color:#6B21A8;border-bottom:3px solid #EC4899;padding-bottom:6px;margin-top:40px;font-size:18px;">9. Charts &amp; Visuals</h2>

<!-- A. Score Bar Chart -->
<h3 style="color:#6B21A8;margin-top:20px;">A. Score Distribution &mdash; Viable Candidates</h3>
<table cellpadding="0" cellspacing="0" border="0" width="100%">
  <tr><td bgcolor="#ffffff" style="background:#fff;border:1px solid #DDD6FE;border-radius:8px;padding:16px;">
    <table width="100%" cellpadding="0" cellspacing="5" border="0">

      <tr>
        <td width="190" align="right" style="font-size:12px;color:#374151;padding-right:8px;white-space:nowrap;">Danish Hussain <b style="color:#16A34A;">&#9650;A</b></td>
        <td><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
          <td width="97%" bgcolor="#16A34A" height="26" style="background-color:#16A34A;color:#fff;font-size:11px;font-weight:bold;padding:0 8px;white-space:nowrap;">97.5 &nbsp;Out of Budget +280K</td>
          <td bgcolor="#F3F4F6" height="26" style="background-color:#F3F4F6;width:3%;"></td>
        </tr></table></td>
      </tr>

      <tr>
        <td width="190" align="right" style="font-size:12px;color:#374151;padding-right:8px;white-space:nowrap;">Zain Ul Abideen &#128269; <b style="color:#16A34A;">&#9650;A</b></td>
        <td><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
          <td width="95%" bgcolor="#22C55E" height="26" style="background-color:#22C55E;color:#fff;font-size:11px;font-weight:bold;padding:0 8px;white-space:nowrap;">95.0 &nbsp;Out of Budget +80K &mdash; Smallest gap</td>
          <td bgcolor="#F3F4F6" height="26" style="background-color:#F3F4F6;width:5%;"></td>
        </tr></table></td>
      </tr>

      <tr>
        <td width="190" align="right" style="font-size:12px;color:#374151;padding-right:8px;white-space:nowrap;">Mizhgan Kirmani <b style="color:#1D4ED8;">&#9650;B</b></td>
        <td><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
          <td width="79%" bgcolor="#1D4ED8" height="26" style="background-color:#1D4ED8;color:#fff;font-size:11px;font-weight:bold;padding:0 8px;white-space:nowrap;">78.8 &nbsp;&#10003; In Budget</td>
          <td bgcolor="#F3F4F6" height="26" style="background-color:#F3F4F6;width:21%;"></td>
        </tr></table></td>
      </tr>

      <tr>
        <td width="190" align="right" style="font-size:12px;color:#374151;padding-right:8px;white-space:nowrap;">Arsalan Ashraf <b style="color:#1D4ED8;">&#9650;B</b></td>
        <td><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
          <td width="72%" bgcolor="#7C3AED" height="26" style="background-color:#7C3AED;color:#fff;font-size:11px;font-weight:bold;padding:0 8px;white-space:nowrap;">72.2 &nbsp;Out of Budget +180K</td>
          <td bgcolor="#F3F4F6" height="26" style="background-color:#F3F4F6;width:28%;"></td>
        </tr></table></td>
      </tr>

      <tr>
        <td width="190" align="right" style="font-size:12px;color:#374151;padding-right:8px;white-space:nowrap;">Sadia Sohail <b style="color:#D97706;">&#9650;C</b></td>
        <td><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
          <td width="57%" bgcolor="#D97706" height="26" style="background-color:#D97706;color:#fff;font-size:11px;font-weight:bold;padding:0 8px;white-space:nowrap;">57.3 &nbsp;&#10003; In Budget &mdash; Backup only</td>
          <td bgcolor="#F3F4F6" height="26" style="background-color:#F3F4F6;width:43%;"></td>
        </tr></table></td>
      </tr>

    </table>
    <p style="font-size:12px;color:#6B7280;margin-top:10px;">
      <b style="color:#16A34A;">&#9632; Green</b> = Tier A &nbsp;|&nbsp;
      <b style="color:#1D4ED8;">&#9632; Blue</b> = Tier B (in budget) &nbsp;|&nbsp;
      <b style="color:#7C3AED;">&#9632; Purple</b> = Tier B (out of budget) &nbsp;|&nbsp;
      <b style="color:#D97706;">&#9632; Amber</b> = Tier C
    </p>
  </td></tr>
</table>

<!-- B. Pool Distribution -->
<h3 style="color:#6B21A8;margin-top:30px;">B. Pool Distribution &mdash; All 48 Applications</h3>
<table cellpadding="0" cellspacing="0" border="0" width="100%">
  <tr><td bgcolor="#ffffff" style="background:#fff;border:1px solid #DDD6FE;border-radius:8px;padding:20px;">
    <table width="100%" cellpadding="0" cellspacing="0" border="0">
      <tr>
        <td width="4%" bgcolor="#16A34A" height="50" style="background-color:#16A34A;color:#fff;text-align:center;font-size:11px;font-weight:bold;vertical-align:middle;padding:2px;">A</td>
        <td width="4%" bgcolor="#1D4ED8" height="50" style="background-color:#1D4ED8;color:#fff;text-align:center;font-size:11px;font-weight:bold;vertical-align:middle;padding:2px;">B</td>
        <td width="2%" bgcolor="#D97706" height="50" style="background-color:#D97706;color:#fff;text-align:center;font-size:11px;font-weight:bold;vertical-align:middle;padding:2px;">C</td>
        <td width="69%" bgcolor="#DC2626" height="50" style="background-color:#DC2626;color:#fff;text-align:center;font-size:12px;font-weight:bold;vertical-align:middle;padding:2px;">No-Hire &mdash; 32 candidates (69%)</td>
        <td width="21%" bgcolor="#7C3AED" height="50" style="background-color:#7C3AED;color:#fff;text-align:center;font-size:11px;font-weight:bold;vertical-align:middle;padding:2px;">No CV / Excluded<br>11 (23%)</td>
      </tr>
    </table>
    <table cellpadding="6" cellspacing="0" border="0" style="margin-top:14px;font-size:13px;">
      <tr><td><span style="display:inline-block;width:14px;height:14px;background-color:#16A34A;vertical-align:middle;margin-right:6px;">&nbsp;</span><b style="color:#16A34A;">Tier A (85+)</b> &mdash; 2 candidates (4%)</td></tr>
      <tr><td><span style="display:inline-block;width:14px;height:14px;background-color:#1D4ED8;vertical-align:middle;margin-right:6px;">&nbsp;</span><b style="color:#1D4ED8;">Tier B (70&ndash;84)</b> &mdash; 2 candidates (4%)</td></tr>
      <tr><td><span style="display:inline-block;width:14px;height:14px;background-color:#D97706;vertical-align:middle;margin-right:6px;">&nbsp;</span><b style="color:#D97706;">Tier C (55&ndash;69)</b> &mdash; 1 candidate (2%)</td></tr>
      <tr><td><span style="display:inline-block;width:14px;height:14px;background-color:#DC2626;vertical-align:middle;margin-right:6px;">&nbsp;</span><b style="color:#DC2626;">No-Hire (&lt;55)</b> &mdash; 32 candidates (69%)</td></tr>
      <tr><td><span style="display:inline-block;width:14px;height:14px;background-color:#7C3AED;vertical-align:middle;margin-right:6px;">&nbsp;</span><b style="color:#6B21A8;">Excluded</b> &mdash; 11 candidates (23%) (9 no-resume, 1 test, 1 duplicate)</td></tr>
    </table>
  </td></tr>
</table>

<!-- C. Dimension Comparison Top 3 -->
<h3 style="color:#6B21A8;margin-top:30px;">C. Top 3 Candidates &mdash; Dimension Score Grid</h3>
<table cellpadding="0" cellspacing="0" border="0" width="100%">
  <tr><td bgcolor="#ffffff" style="background:#fff;border:1px solid #DDD6FE;border-radius:8px;padding:20px;">
    <table width="100%" border="1" cellpadding="10" cellspacing="0" style="border-collapse:collapse;border-color:#E5E7EB;font-size:13px;">
      <tr>
        <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;width:200px;text-align:left;">Dimension</th>
        <th bgcolor="#16A34A" style="background-color:#16A34A;color:#fff;text-align:center;">Danish Hussain<br><span style="font-size:11px;font-weight:normal;">97.5 / 100 &mdash; Tier A</span></th>
        <th bgcolor="#22C55E" style="background-color:#22C55E;color:#fff;text-align:center;">Zain Ul Abideen &#128269;<br><span style="font-size:11px;font-weight:normal;">95.0 / 100 &mdash; Tier A</span></th>
        <th bgcolor="#1D4ED8" style="background-color:#1D4ED8;color:#fff;text-align:center;">Mizhgan Kirmani<br><span style="font-size:11px;font-weight:normal;">78.8 / 100 &mdash; Tier B</span></th>
      </tr>
      <tr>
        <td style="font-weight:bold;padding:10px;">D1 Functional Match (25%)</td>
        <td bgcolor="#16A34A" style="background-color:#16A34A;color:#fff;text-align:center;padding:10px;">&#9733;&#9733;&#9733;&#9733;&#9733;<br><span style="font-size:11px;">4/4 &mdash; Head Grants &amp; Partnerships, INGO</span></td>
        <td bgcolor="#16A34A" style="background-color:#16A34A;color:#fff;text-align:center;padding:10px;">&#9733;&#9733;&#9733;&#9733;&#9733;<br><span style="font-size:11px;">4/4 &mdash; Deputy Manager Resource Mobilisation</span></td>
        <td bgcolor="#22C55E" style="background-color:#22C55E;color:#fff;text-align:center;padding:10px;">&#9733;&#9733;&#9733;&#9733;&#9734;<br><span style="font-size:11px;">3/4 &mdash; Manager Donor Relations, TCF</span></td>
      </tr>
      <tr bgcolor="#F9FAFB" style="background-color:#F9FAFB;">
        <td style="font-weight:bold;padding:10px;">D2 Demonstrated Outcomes (20%)</td>
        <td bgcolor="#16A34A" style="background-color:#16A34A;color:#fff;text-align:center;padding:10px;">&#9733;&#9733;&#9733;&#9733;&#9733;<br><span style="font-size:11px;">4/4 &mdash; PKR 1B+ across FCDO/WB/UNDP/ADB</span></td>
        <td bgcolor="#16A34A" style="background-color:#16A34A;color:#fff;text-align:center;padding:10px;">&#9733;&#9733;&#9733;&#9733;&#9733;<br><span style="font-size:11px;">4/4 &mdash; US $50M in won proposals</span></td>
        <td bgcolor="#22C55E" style="background-color:#22C55E;color:#fff;text-align:center;padding:10px;">&#9733;&#9733;&#9733;&#9733;&#9734;<br><span style="font-size:11px;">3/4 &mdash; PKR 72M closed FY</span></td>
      </tr>
      <tr>
        <td style="font-weight:bold;padding:10px;">D3 Environment Fit (15%)</td>
        <td bgcolor="#22C55E" style="background-color:#22C55E;color:#fff;text-align:center;padding:10px;">&#9733;&#9733;&#9733;&#9733;&#9734;<br><span style="font-size:11px;">3/4 &mdash; INGO/dev sector; WASH vs EdTech gap</span></td>
        <td bgcolor="#16A34A" style="background-color:#16A34A;color:#fff;text-align:center;padding:10px;">&#9733;&#9733;&#9733;&#9733;&#9733;<br><span style="font-size:11px;">4/4 &mdash; Islamabad, NGO, Pakistan donors</span></td>
        <td bgcolor="#16A34A" style="background-color:#16A34A;color:#fff;text-align:center;padding:10px;">&#9733;&#9733;&#9733;&#9733;&#9733;<br><span style="font-size:11px;">4/4 &mdash; Islamabad, EdTech/education sector</span></td>
      </tr>
      <tr bgcolor="#F9FAFB" style="background-color:#F9FAFB;">
        <td style="font-weight:bold;padding:10px;">D4 Ownership &amp; Execution (15%)</td>
        <td bgcolor="#16A34A" style="background-color:#16A34A;color:#fff;text-align:center;padding:10px;">&#9733;&#9733;&#9733;&#9733;&#9733;<br><span style="font-size:11px;">4/4 &mdash; Built function, independently closed</span></td>
        <td bgcolor="#16A34A" style="background-color:#16A34A;color:#fff;text-align:center;padding:10px;">&#9733;&#9733;&#9733;&#9733;&#9733;<br><span style="font-size:11px;">4/4 &mdash; Led proposals, won independently</span></td>
        <td bgcolor="#22C55E" style="background-color:#22C55E;color:#fff;text-align:center;padding:10px;">&#9733;&#9733;&#9733;&#9733;&#9734;<br><span style="font-size:11px;">3/4 &mdash; Active management, scale unproven</span></td>
      </tr>
      <tr>
        <td style="font-weight:bold;padding:10px;">D5 Stakeholder Comm (10%)</td>
        <td bgcolor="#16A34A" style="background-color:#16A34A;color:#fff;text-align:center;padding:10px;">&#9733;&#9733;&#9733;&#9733;&#9733;<br><span style="font-size:11px;">4/4 &mdash; Named: FCDO, UNDP, ADB officers</span></td>
        <td bgcolor="#22C55E" style="background-color:#22C55E;color:#fff;text-align:center;padding:10px;">&#9733;&#9733;&#9733;&#9733;&#9734;<br><span style="font-size:11px;">3/4 &mdash; UNICEF, UNFPA, US Embassy, IRC</span></td>
        <td bgcolor="#22C55E" style="background-color:#22C55E;color:#fff;text-align:center;padding:10px;">&#9733;&#9733;&#9733;&#9733;&#9734;<br><span style="font-size:11px;">3/4 &mdash; 6+ international donors active</span></td>
      </tr>
      <tr bgcolor="#F9FAFB" style="background-color:#F9FAFB;">
        <td style="font-weight:bold;padding:10px;">D6 Hard Skills (10%)</td>
        <td bgcolor="#16A34A" style="background-color:#16A34A;color:#fff;text-align:center;padding:10px;">&#9733;&#9733;&#9733;&#9733;&#9733;<br><span style="font-size:11px;">4/4 &mdash; Proposal writing, grant systems</span></td>
        <td bgcolor="#16A34A" style="background-color:#16A34A;color:#fff;text-align:center;padding:10px;">&#9733;&#9733;&#9733;&#9733;&#9733;<br><span style="font-size:11px;">4/4 &mdash; Core career skill in proposals</span></td>
        <td bgcolor="#22C55E" style="background-color:#22C55E;color:#fff;text-align:center;padding:10px;">&#9733;&#9733;&#9733;&#9733;&#9734;<br><span style="font-size:11px;">3/4 &mdash; Proposal writing, concept notes</span></td>
      </tr>
      <tr>
        <td style="font-weight:bold;padding:10px;">D7 Growth &amp; Leadership (5%)</td>
        <td bgcolor="#16A34A" style="background-color:#16A34A;color:#fff;text-align:center;padding:10px;">&#9733;&#9733;&#9733;&#9733;&#9733;<br><span style="font-size:11px;">4/4 &mdash; Head-level, 20 years progression</span></td>
        <td bgcolor="#22C55E" style="background-color:#22C55E;color:#fff;text-align:center;padding:10px;">&#9733;&#9733;&#9733;&#9733;&#9734;<br><span style="font-size:11px;">3/4 &mdash; Deputy Mgr, 16 years growth</span></td>
        <td bgcolor="#22C55E" style="background-color:#22C55E;color:#fff;text-align:center;padding:10px;">&#9733;&#9733;&#9733;&#9733;&#9734;<br><span style="font-size:11px;">3/4 &mdash; Manager level, 8 years</span></td>
      </tr>
    </table>
    <p style="font-size:11px;color:#6B7280;margin-top:8px;">&#9733;&#9733;&#9733;&#9733;&#9733; Exceptional (4/4) &nbsp;|&nbsp; &#9733;&#9733;&#9733;&#9733;&#9734; Strong (3/4) &nbsp;|&nbsp; &#9733;&#9733;&#9733;&#9734;&#9734; Partial (2/4) &nbsp;|&nbsp; &#9733;&#9734;&#9734;&#9734;&#9734; Weak (1/4)</p>
  </td></tr>
</table>

<!-- D. Heatmap -->
<h3 style="color:#6B21A8;margin-top:30px;">D. Must-Have Coverage Heatmap &mdash; Top 5 Candidates</h3>
<table width="100%" border="1" cellpadding="9" cellspacing="0" style="border-collapse:collapse;border-color:#E5E7EB;font-size:12px;">
  <tr>
    <th bgcolor="#4C1D95" style="background-color:#4C1D95;color:#fff;text-align:left;padding:10px;">Must-have</th>
    <th bgcolor="#16A34A" style="background-color:#16A34A;color:#fff;text-align:center;">Danish<br><span style="font-size:10px;">97.5 A</span></th>
    <th bgcolor="#22C55E" style="background-color:#22C55E;color:#fff;text-align:center;">Zain &#128269;<br><span style="font-size:10px;">95.0 A</span></th>
    <th bgcolor="#1D4ED8" style="background-color:#1D4ED8;color:#fff;text-align:center;">Mizhgan<br><span style="font-size:10px;">78.8 B</span></th>
    <th bgcolor="#7C3AED" style="background-color:#7C3AED;color:#fff;text-align:center;">Arsalan<br><span style="font-size:10px;">72.2 B</span></th>
    <th bgcolor="#D97706" style="background-color:#D97706;color:#fff;text-align:center;">Sadia<br><span style="font-size:10px;">57.3 C</span></th>
  </tr>
  <tr>
    <td style="padding:9px 12px;">Fundraising / BD / institutional donor engagement</td>
    <td bgcolor="#DCFCE7" style="background-color:#DCFCE7;text-align:center;">&#9989;</td>
    <td bgcolor="#DCFCE7" style="background-color:#DCFCE7;text-align:center;">&#9989;</td>
    <td bgcolor="#DCFCE7" style="background-color:#DCFCE7;text-align:center;">&#9989;</td>
    <td bgcolor="#DCFCE7" style="background-color:#DCFCE7;text-align:center;">&#9989;</td>
    <td bgcolor="#DCFCE7" style="background-color:#DCFCE7;text-align:center;">&#9989;</td>
  </tr>
  <tr bgcolor="#F9FAFB" style="background-color:#F9FAFB;">
    <td style="padding:9px 12px;">Pakistan donor landscape (USAID/WB/FCDO/JICA/EU)</td>
    <td bgcolor="#DCFCE7" style="background-color:#DCFCE7;text-align:center;">&#9989;</td>
    <td bgcolor="#DCFCE7" style="background-color:#DCFCE7;text-align:center;">&#9989;</td>
    <td bgcolor="#DCFCE7" style="background-color:#DCFCE7;text-align:center;">&#9989;</td>
    <td bgcolor="#FEF9C3" style="background-color:#FEF9C3;text-align:center;">&#9888;</td>
    <td bgcolor="#FEE2E2" style="background-color:#FEE2E2;text-align:center;">&#10060;</td>
  </tr>
  <tr>
    <td style="padding:9px 12px;">Proposal / grant writing (submitted &amp; won)</td>
    <td bgcolor="#DCFCE7" style="background-color:#DCFCE7;text-align:center;">&#9989;</td>
    <td bgcolor="#DCFCE7" style="background-color:#DCFCE7;text-align:center;">&#9989;</td>
    <td bgcolor="#DCFCE7" style="background-color:#DCFCE7;text-align:center;">&#9989;</td>
    <td bgcolor="#DCFCE7" style="background-color:#DCFCE7;text-align:center;">&#9989;</td>
    <td bgcolor="#FEF9C3" style="background-color:#FEF9C3;text-align:center;">&#9888;</td>
  </tr>
  <tr bgcolor="#F9FAFB" style="background-color:#F9FAFB;">
    <td style="padding:9px 12px;">Pipeline management (30&ndash;50+ opportunities)</td>
    <td bgcolor="#DCFCE7" style="background-color:#DCFCE7;text-align:center;">&#9989;</td>
    <td bgcolor="#DCFCE7" style="background-color:#DCFCE7;text-align:center;">&#9989;</td>
    <td bgcolor="#FEF9C3" style="background-color:#FEF9C3;text-align:center;">&#9888;</td>
    <td bgcolor="#DCFCE7" style="background-color:#DCFCE7;text-align:center;">&#9989;</td>
    <td bgcolor="#FEE2E2" style="background-color:#FEE2E2;text-align:center;">&#10060;</td>
  </tr>
  <tr>
    <td style="padding:9px 12px;">Islamabad-based or willing to relocate</td>
    <td bgcolor="#FEF9C3" style="background-color:#FEF9C3;text-align:center;">&#9888;</td>
    <td bgcolor="#DCFCE7" style="background-color:#DCFCE7;text-align:center;">&#9989;</td>
    <td bgcolor="#DCFCE7" style="background-color:#DCFCE7;text-align:center;">&#9989;</td>
    <td bgcolor="#FEF9C3" style="background-color:#FEF9C3;text-align:center;">&#9888;</td>
    <td bgcolor="#DCFCE7" style="background-color:#DCFCE7;text-align:center;">&#9989;</td>
  </tr>
  <tr bgcolor="#F9FAFB" style="background-color:#F9FAFB;">
    <td style="padding:9px 12px;">Strong written &amp; presentation skills</td>
    <td bgcolor="#DCFCE7" style="background-color:#DCFCE7;text-align:center;">&#9989;</td>
    <td bgcolor="#DCFCE7" style="background-color:#DCFCE7;text-align:center;">&#9989;</td>
    <td bgcolor="#DCFCE7" style="background-color:#DCFCE7;text-align:center;">&#9989;</td>
    <td bgcolor="#DCFCE7" style="background-color:#DCFCE7;text-align:center;">&#9989;</td>
    <td bgcolor="#DCFCE7" style="background-color:#DCFCE7;text-align:center;">&#9989;</td>
  </tr>
</table>
<p style="font-size:12px;color:#6B7280;margin-top:6px;">&#9989; Present &nbsp;|&nbsp; &#9888; Partial / Adjacent &nbsp;|&nbsp; &#10060; Absent</p>

<!-- ══ 10. NEXT STEPS ══ -->
<h2 style="color:#6B21A8;border-bottom:3px solid #EC4899;padding-bottom:6px;margin-top:40px;font-size:18px;">10. Recommended Next Steps</h2>
<table cellpadding="0" cellspacing="0" border="0" width="100%">
  <tr><td bgcolor="#DCFCE7" style="background-color:#DCFCE7;border-left:5px solid #16A34A;border-radius:6px;padding:16px 20px;">
    <ol style="margin:0;padding-left:20px;line-height:2.2;">
      <li><b style="color:#16A34A;">Call Danish Hussain immediately</b> &mdash; 97.5, Tier A. Strongest fundraising track record in the pool (PKR 1B+, FCDO/WB/UNDP/ADB). Budget gap is large (PKR 280K over) but this is your most complete fundraiser. Consider performance-based package. Confirm relocation is firm.</li>
      <li><b style="color:#22C55E;">Call Zain Ul Abideen</b> &mdash; 95.0, Tier A. US $50M in won proposals. Islamabad-based. Smallest budget gap (PKR 80K over). Best combination of scale, location, and budget proximity. Almost missed entirely &mdash; CV was scanned.</li>
      <li><b style="color:#1D4ED8;">Interview Mizhgan Kirmani</b> &mdash; 78.8, Tier B. Best in-budget candidate. Zero relocation or salary risk. Probe: largest independently closed grant, pipeline scale, government relationships.</li>
      <li><b style="color:#7C3AED;">Interview Arsalan Ashraf</b> &mdash; 72.2, Tier B. Strong builder and closer. Gap: multilateral/bilateral experience. Confirm: is CSR-to-multilateral pivot credible? Confirm relocation.</li>
      <li><b style="color:#D97706;">Hold Sadia Sohail as Tier C backup</b> &mdash; 57.3. Proceed only if Tier A and B candidates do not work out. Probe multilateral exposure before advancing.</li>
      <li><b style="color:#DC2626;">Review LinkedIn Quick Apply settings</b> &mdash; 9 of 48 applications (19%) had no CVs. These applicants cannot be assessed. Consider requiring CV upload to proceed.</li>
    </ol>
  </td></tr>
</table>

<!-- FOOTER -->
<table cellpadding="0" cellspacing="0" border="0" width="100%" style="margin-top:48px;">
  <tr><td style="border-top:2px solid #DDD6FE;padding-top:16px;color:#6B7280;font-size:12px;">
    Taleemabad Talent Acquisition Agent &bull; 2026-03-03 &bull; Report v5 (7-Dimension Framework)<br>
    Job JOB-0032 &bull; Fundraising &amp; Partnerships Manager &bull; Budget: PKR 150,000&ndash;270,000/month<br>
    Dimensions: D1 Functional 25% &bull; D2 Outcomes 20% &bull; D3 Environment 15% &bull; D4 Ownership 15% &bull; D5 Stakeholder 10% &bull; D6 Hard Skills 10% &bull; D7 Growth 5%<br>
    Sent to: ayesha.khan@taleemabad.com only &bull; &#128269; = OCR-recovered candidate (Tesseract)
  </td></tr>
</table>

</body></html>"""

msg = MIMEMultipart("alternative")
msg["Subject"] = "Screening Report v5 — Fundraising & Partnerships Manager (7-Dimension Framework)"
msg["From"]    = SENDER
msg["To"]      = RECIPIENT
msg.attach(MIMEText(html, "html"))

with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.starttls()
    server.login(SENDER, PASSWORD)
    server.sendmail(SENDER, RECIPIENT, msg.as_string())

print(f"SUCCESS: v5 report sent to {RECIPIENT}")
