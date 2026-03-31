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
<html>
<head>
<meta charset="UTF-8">
<style>
  body { font-family: Arial, sans-serif; font-size: 14px; color: #111827; max-width: 1100px; margin: 0 auto; padding: 24px; background: #fafafa; }
  h1 { background: linear-gradient(135deg, #4C1D95, #7C3AED); color: #fff; padding: 20px 24px; border-radius: 8px; font-size: 22px; margin-bottom: 8px; }
  h2 { color: #6B21A8; border-bottom: 3px solid #EC4899; padding-bottom: 6px; margin-top: 40px; font-size: 18px; }
  h3 { color: #1D4ED8; margin-top: 20px; font-size: 15px; }
  table { border-collapse: collapse; width: 100%; margin: 14px 0; font-size: 13px; }
  th { background: linear-gradient(90deg, #4C1D95, #1D4ED8); color: #fff; padding: 10px 12px; text-align: left; }
  td { padding: 9px 12px; border-bottom: 1px solid #E5E7EB; vertical-align: top; }
  tr:nth-child(even) td { background: #F5F3FF; }
  .in   { background:#DCFCE7; color:#166534; font-weight:bold; padding:3px 10px; border-radius:12px; white-space:nowrap; display:inline-block; }
  .out  { background:#FEE2E2; color:#991B1B; font-weight:bold; padding:3px 10px; border-radius:12px; white-space:nowrap; display:inline-block; }
  .unk  { background:#FEF9C3; color:#854D0E; font-weight:bold; padding:3px 10px; border-radius:12px; white-space:nowrap; display:inline-block; }
  .summary-box { background:linear-gradient(135deg,#EDE9FE,#FCE7F3); border-left:5px solid #7C3AED; padding:16px 20px; border-radius:6px; margin:16px 0; }
  .rec-box  { background:linear-gradient(135deg,#DCFCE7,#D1FAE5); border-left:5px solid #16A34A; padding:16px 20px; border-radius:6px; margin:16px 0; }
  .warn-box { background:linear-gradient(135deg,#FEF3C7,#FDE68A); border-left:5px solid #D97706; padding:16px 20px; border-radius:6px; margin:16px 0; }
  .profile  { background:#fff; border:1px solid #DDD6FE; border-left:5px solid #7C3AED; border-radius:6px; padding:16px; margin:16px 0; }
  .score-badge { display:inline-block; background:linear-gradient(135deg,#7C3AED,#EC4899); color:#fff; border-radius:20px; padding:4px 14px; font-weight:bold; font-size:14px; }
  .purple { color: #6B21A8; font-weight: bold; }
  .pink   { color: #DB2777; font-weight: bold; }
  .blue   { color: #1D4ED8; font-weight: bold; }
  .green  { color: #16A34A; font-weight: bold; }
  .red    { color: #DC2626; font-weight: bold; }
  ul { margin:6px 0; padding-left:20px; }
  li { margin:4px 0; }
  .footer { margin-top:48px; padding-top:16px; border-top:2px solid #DDD6FE; color:#6B7280; font-size:12px; }
  /* Bar chart */
  .bar-wrap { background:#fff; border-radius:8px; padding:16px; border:1px solid #DDD6FE; margin:12px 0; }
  .bar-row  { display:flex; align-items:center; margin:5px 0; font-size:12px; }
  .bar-label{ width:200px; text-align:right; padding-right:10px; color:#374151; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
  .bar-outer{ flex:1; background:#F3F4F6; border-radius:4px; height:18px; position:relative; }
  .bar-fill { height:18px; border-radius:4px; position:absolute; left:0; top:0; }
  .bar-val  { position:absolute; right:6px; top:0; line-height:18px; font-size:11px; font-weight:bold; color:#fff; }
</style>
</head>
<body>

<h1>&#128203; Candidate Screening Report &mdash; Fundraising &amp; Partnerships Manager</h1>
<p style="color:#6B21A8; font-weight:bold; margin-top:4px;">Updated Report &bull; Includes OCR-recovered candidate (Zain Ul Abideen)</p>

<!-- ══════════════════════════════════
     1. SCREENING SUMMARY
══════════════════════════════════ -->
<h2>1. Screening Summary</h2>
<div class="summary-box">
<table style="width:auto;margin:0;">
<tr><td><span class="purple">Job</span></td><td>Fundraising &amp; Partnerships Manager (Job ID 32)</td></tr>
<tr><td><span class="purple">Date</span></td><td>2026-03-02 (Updated)</td></tr>
<tr><td><span class="purple">Pool size</span></td><td>48 applications</td></tr>
<tr><td><span class="purple">Shortlist size</span></td><td>Top 20 (pool &ge;40 rule)</td></tr>
<tr><td><span class="purple">Budget</span></td><td>PKR 150,000 &ndash; 270,000 / month</td></tr>
<tr><td><span class="purple">Location</span></td><td>Islamabad &mdash; In-Person, Permanent</td></tr>
<tr><td><span class="purple">CVs readable</span></td><td>37 / 48 (36 PDF + 1 via OCR)</td></tr>
<tr><td><span class="purple">Scoring weights</span></td><td>Must-have 35% &bull; Experience 25% &bull; Domain 10% &bull; Responsibilities 10% &bull; Budget 15% &bull; Location 5%</td></tr>
</table>
</div>

<b>Data gaps:</b>
<ul>
  <li><span class="red">9 no-resume</span> (LinkedIn Quick Apply): apps 1332, 1336, 1348, 1350, 1366, 1372, 1386, 1407, 1515</li>
  <li><span class="blue">1 OCR-recovered</span>: Zain Ul Abideen (1333) &mdash; scanned PDF, extracted via Tesseract OCR. Strong candidate found.</li>
  <li><span class="red">1 test/junk entry</span>: AAMIR SOHAIL (1393) &mdash; salary entered as &ldquo;1&rdquo;, .doc unreadable</li>
  <li><span class="red">2 duplicates</span>: Danish Hussain (1347=1346), AAMIR SOHAIL (1418=1393)</li>
</ul>

<!-- ══════════════════════════════════
     2. JD SCORECARD
══════════════════════════════════ -->
<h2>2. JD Scorecard</h2>
<table>
<tr><th style="width:160px">Category</th><th>Detail</th></tr>
<tr><td><span class="purple"><b>Must-haves</b></span></td><td>
  1. Fundraising / partnerships / BD / institutional engagement experience<br>
  2. Knowledge of Pakistan donor landscape (USAID, World Bank, DFID/FCDO, JICA, EU, multilaterals, foundations)<br>
  3. Proposal / concept note / grant writing experience<br>
  4. Pipeline management (30&ndash;50+ opportunities simultaneously)<br>
  5. Islamabad-based <b>or willing to relocate</b><br>
  6. Strong written communication and presentation skills
</td></tr>
<tr><td><span class="blue"><b>Nice-to-haves</b></span></td><td>
  &bull; Existing donor relationships in Pakistan<br>
  &bull; Independently closed $500K+ funding deals<br>
  &bull; Education sector experience<br>
  &bull; Government/policy engagement in Islamabad
</td></tr>
<tr><td><span class="red"><b>Deal-breakers</b></span></td><td>
  &bull; Zero fundraising/BD/partnerships experience<br>
  &bull; <b>Not Islamabad-based AND not willing to relocate</b> (willing to relocate = acceptable)
</td></tr>
<tr><td><span class="pink"><b>Constraints</b></span></td><td>
  Budget: PKR 150,000&ndash;270,000/month &bull; Islamabad in-person &bull; Year 1 target: $500K&ndash;$1M+
</td></tr>
</table>

<!-- ══════════════════════════════════
     3. RANKED SHORTLIST — TOP 20
══════════════════════════════════ -->
<h2>3. Ranked Shortlist &mdash; Top 20</h2>
<p style="color:#6B21A8; font-style:italic;">Pool: 48 &bull; Shortlist rule: pool &ge;40 &rarr; top 20. Ranked by total score &rarr; must-have strength &rarr; budget fit.</p>

<table>
<tr>
  <th>#</th><th>Candidate</th><th>Score /10</th><th>Must-have match</th>
  <th>Salary (PKR/mo)</th><th>Budget</th><th>Key Strengths</th><th>Key Risks</th>
</tr>
<tr><td><b style="color:#6B21A8">1</b></td><td><b>Mizhgan Kirmani</b></td><td><b>8.0</b></td>
  <td>Donor relations &#10003; Proposals &#10003; FCDO/UNDP/USAID &#10003;</td>
  <td>250,000</td><td><span class="in">In Budget</span></td>
  <td>Manager Donor Relations TCF; PKR 72M closed FY; FCDO/UN Women/USAID/UNDP direct engagement; Islamabad</td>
  <td>No $500K+ deal independently closed yet</td></tr>
<tr><td><b style="color:#DB2777">2</b></td><td><b>Arsalan Ashraf</b></td><td><b>7.9</b></td>
  <td>Fundraising &#10003; Proposals &#10003; Pipeline &#10003;</td>
  <td>450,000</td><td><span class="out">Out of Budget</span></td>
  <td>Meta $100K, Chevron $250K, PKR 80M NAVTTC; built fundraising depts from scratch</td>
  <td>CSR/corporate focus; PKR 450K (67% over ceiling); Karachi-based (willing to relocate)</td></tr>
<tr><td><b style="color:#1D4ED8">3</b></td><td><b>Zain Ul Abideen</b> &#128269;</td><td><b>7.8</b></td>
  <td>Proposals &#10003; UNICEF/UNFPA/IRC/WaterAid &#10003; Pipeline &#10003;</td>
  <td>350,000</td><td><span class="out">Out of Budget</span></td>
  <td>US $50M in won proposals; PKR 2.36B at READ Foundation; PKR 1.23B at SPO; Islamabad-based</td>
  <td>PKR 350K over budget; M.Phil IR (not business/finance); freelance periods in CV</td></tr>
<tr><td>4</td><td><b>Sadia Sohail</b></td><td><b>7.5</b></td>
  <td>Donor relations &#10003; Proposals &#10003; Budget reporting &#10003;</td>
  <td>140,000</td><td><span class="in">In Budget</span></td>
  <td>8 yrs donor relations at READ Foundation; fundraising certifications; Islamabad-based</td>
  <td>Domestic NGO only &mdash; no multilateral (USAID/WB/FCDO) experience</td></tr>
<tr><td>5</td><td><b>Ahad Ahsan Khan</b></td><td><b>7.4</b></td>
  <td>Grants mgmt &#10003; USAID/WB &#10003; $134M portfolio &#10003;</td>
  <td>550,000</td><td><span class="out">Out of Budget</span></td>
  <td>Manager Grants AKU ($134M, 210 grants); World Bank HEDP lead; Islamabad hometown</td>
  <td>Grants compliance &ne; fundraising acquisition; PKR 550K far over budget</td></tr>
<tr><td>6</td><td><b>Danish Hussain</b></td><td><b>7.3</b></td>
  <td>Fundraising &#10003; FCDO/EU/WB &#10003; Grant writing &#10003;</td>
  <td>550,000</td><td><span class="out">Out of Budget</span></td>
  <td>20 yrs development; PKR 1B+ mobilized; Head Grants &amp; Partnerships; FCDO/WB/UNDP/ADB</td>
  <td>Hyderabad-based (willing to relocate); PKR 550K (2x ceiling); WASH focus not EdTech</td></tr>
<tr><td>7</td><td><b>Faheem Baig</b></td><td><b>6.7</b></td>
  <td>Donor networks &#10003; Dev sector &#10003; M.Phil PIDE &#10003;</td>
  <td>145,000</td><td><span class="in">In Budget</span></td>
  <td>DG-ECHO, GIZ, UN Women, USAID, AKDN networks; CEO/COO prog lead; Islamabad</td>
  <td>Programme implementation &mdash; no quantified proposal wins</td></tr>
<tr><td>8</td><td><b>Hamdan Ahmad</b></td><td><b>6.6</b></td>
  <td>WB partnership &#10003; Dev sector &#10003; Education &#10003;</td>
  <td>320,000</td><td><span class="out">Out of Budget</span></td>
  <td>World Bank ESFCD consultant ($100M project); Islamabad; education sector</td>
  <td>Programme mgmt not resource mobilisation; PKR 320K (PKR 50K over &mdash; closest gap)</td></tr>
<tr><td>9</td><td><b>Mushahid Hussain</b></td><td><b>6.6</b></td>
  <td>Donor reporting &#10003; Fundraising &#10003; Dev sector &#10003;</td>
  <td>170,000</td><td><span class="in">In Budget</span></td>
  <td>Donor Reporting Officer READ Foundation; fundraising, financial proposals; Islamabad</td>
  <td>4 yrs experience &mdash; junior for Manager; reporting not acquisition lead</td></tr>
<tr><td>10</td><td><b>Shakir Manzoor Khan</b></td><td><b>6.5</b></td>
  <td>Resource mobilisation &#10003; Grant proposals &#10003; PPP &#10003;</td>
  <td>350,000</td><td><span class="out">Out of Budget</span></td>
  <td>15 yrs resource mobilization; Commonwealth Foundation, WHO, AEIF proposals; Rawalpindi</td>
  <td>Health/pharma focus; grant contributions appear supporting not lead; PKR 350K over</td></tr>
<tr><td>11</td><td><b>Ahmed Al-Mayadeen</b></td><td><b>6.4</b></td>
  <td>UN fundraising &#10003; Multi-million campaigns &#10003;</td>
  <td>~PKR 980K ($3,500/mo)</td><td><span class="out">Out of Budget</span></td>
  <td>10+ yrs UN/NGO fundraising; UNESCO roster; Harvard Business diploma</td>
  <td>Yemen-based; PKR 980K (3.6x ceiling); Pakistan donor relationships unclear</td></tr>
<tr><td>12</td><td><b>Muhammad Usman</b></td><td><b>6.1</b></td>
  <td>Partnerships &#10003; Fundraising (competency) &#10003;</td>
  <td>350,000</td><td><span class="out">Out of Budget</span></td>
  <td>18 yrs stakeholder mgmt; international development alliances; Rawalpindi/Islamabad</td>
  <td>Fundraising listed but not quantified; PKR 350K over budget</td></tr>
<tr><td>13</td><td><b>Abdul Salam</b></td><td><b>5.9</b></td>
  <td>Donor projects &#10003; WB/USAID/DFID &#10003;</td>
  <td>400,000</td><td><span class="out">Out of Budget</span></td>
  <td>21 yrs development; managed WB/USAID/DFID/GIZ/UNICEF programmes; Islamabad</td>
  <td>WASH implementation not resource mobilisation; PKR 400K over budget</td></tr>
<tr><td>14</td><td><b>Zubair Hussain</b></td><td><b>5.6</b></td>
  <td>Dev sector &#10003; SEF education &#10003;</td>
  <td>30,000 &#9888;</td><td><span class="unk">Unknown*</span></td>
  <td>PPAF-ITC-EU project; education programme; gender/rights-based</td>
  <td>Salary anomaly (30K desired vs 250K current &mdash; likely typo); field specialist not BD</td></tr>
<tr><td>15</td><td><b>Arsim Tariq</b></td><td><b>5.4</b></td>
  <td>Proposals &#10003; FCDO/WB contracts &#10003; Education &#10003;</td>
  <td>280,000&ndash;300,000</td><td><span class="out">Out of Budget</span></td>
  <td>10+ dev sector proposals won; FCDO/WB contracts; Islamabad; NUST MS</td>
  <td>Programme mgmt/M&amp;E role; PKR 280K&ndash;300K marginally over 270K ceiling</td></tr>
<tr><td>16</td><td><b>Fahad Khan</b></td><td><b>5.0</b></td>
  <td>Fundraising role &#10003; Pipeline &#10003;</td>
  <td>350,000</td><td><span class="out">Out of Budget</span></td>
  <td>Associate Manager Fundraising Shaukat Khanum; BD experience; Islamabad</td>
  <td>Hospital charity &ne; institutional donors; PKR 350K over budget</td></tr>
<tr><td>17</td><td><b>Mahnoor Mellu</b></td><td><b>5.0</b></td>
  <td>Partnerships &#10003; B2B pipeline &#10003;</td>
  <td>350,000</td><td><span class="out">Out of Budget</span></td>
  <td>Partnerships Manager DigitalOcean-Cloudways; LUMS graduate</td>
  <td>Tech/SaaS &ne; dev sector fundraising; Lahore (willing to relocate); PKR 350K over</td></tr>
<tr><td>18</td><td><b>Imran Haider</b></td><td><b>4.9</b></td>
  <td>Education policy &#10003; WB/MoFEPT &#10003;</td>
  <td>350,000</td><td><span class="out">Out of Budget</span></td>
  <td>LUMS; education policy &amp; M&amp;E; WB PHCIP consultant; strong edu alignment</td>
  <td>Policy/implementation not resource mobilisation; PKR 350K over; Lahore (willing to relocate)</td></tr>
<tr><td>19</td><td><b>Sameen Amjad Ali</b></td><td><b>3.6</b></td>
  <td>Stakeholder engagement &#10003;</td>
  <td>650,000</td><td><span class="out">Out of Budget</span></td>
  <td>Senior marketing/comms; investor-facing materials; ministerial engagement</td>
  <td>No donor/dev sector fundraising; PKR 650K (2.4x budget)</td></tr>
<tr><td>20</td><td><b>Syeda Kainat</b></td><td><b>3.3</b></td>
  <td>Education &#10003; M&amp;E &#10003; Islamabad &#10003;</td>
  <td>110,000</td><td><span class="in">In Budget</span></td>
  <td>Education sector; WB TEACH certified; Islamabad; within budget</td>
  <td>M&amp;E/comms officer &mdash; missing all core fundraising must-haves for Manager</td></tr>
</table>
<p style="font-size:12px; color:#6B7280;">&#128269; = OCR-recovered candidate (scanned PDF, read via Tesseract)</p>

<!-- ══════════════════════════════════
     4. STRONGEST 3 — DEEP COMPARE
══════════════════════════════════ -->
<h2>4. Strongest 3 Candidates &mdash; Deep Comparison</h2>

<div class="profile">
<h3>&#127947; <span style="color:#6B21A8">Mizhgan Kirmani</span> &nbsp;<span class="score-badge">8.0 / 10</span> &nbsp;<span class="in">In Budget &bull; PKR 250,000</span></h3>
<b class="purple">Why she&rsquo;s top:</b>
<ul>
  <li>Currently <b>Manager Donor Relations at Citizens Foundation</b> &mdash; closed the FY at PKR 72M. Live, active institutional fundraising in Pakistan&rsquo;s education sector.</li>
  <li>Direct named relationships with <b>FCDO, UN Women, UNDP, USAID, Green Climate Fund</b> &mdash; the exact donor ecosystem in the JD.</li>
  <li>Islamabad-based, proposal writing active, within budget at PKR 250K &mdash; no location or budget risk.</li>
</ul>
<b class="red">Risks:</b>
<ul>
  <li>PKR 72M track record is strong but below the JD&rsquo;s Year 1 target of $500K&ndash;$1M+ (PKR 140M&ndash;280M).</li>
  <li>Probe in interview: has she independently won large competitive grants, or supported senior leads?</li>
</ul>
</div>

<div class="profile">
<h3>&#127948; <span style="color:#DB2777">Zain Ul Abideen</span> &nbsp;<span class="score-badge">7.8 / 10</span> &nbsp;<span class="out">Out of Budget &bull; PKR 350,000</span> &nbsp;&#128269;</h3>
<b class="blue">Why he&rsquo;s strong (flag for HM):</b>
<ul>
  <li><b>US $50M lifetime in won proposals</b>: PKR 2.36B (US $8.44M) at READ Foundation alone; PKR 1.23B (US $4.42M) at SPO. These are actual closed funding relationships with UNICEF, UNFPA, US Embassy, British Council, Oxfam, IRC, WaterAid, Save the Children.</li>
  <li><b>Islamabad-based with direct NGO fundraising leadership</b> &mdash; Deputy Manager at READ Foundation (exactly the kind of organisation Taleemabad competes with for the same donors).</li>
  <li>Strong proposal writer with 16+ years experience &mdash; including RFP/RFI/RFQ wins for US government contracts at En Pointe.</li>
</ul>
<b class="red">Risks:</b>
<ul>
  <li>PKR 350K &mdash; PKR 80K over budget ceiling. Gap is the smallest among the strong-but-over-budget group.</li>
  <li>CV was scanned and unreadable &mdash; originally missed. Process gap now fixed with OCR.</li>
</ul>
</div>

<div class="profile">
<h3>&#127949; <span style="color:#1D4ED8">Sadia Sohail</span> &nbsp;<span class="score-badge">7.5 / 10</span> &nbsp;<span class="in">In Budget &bull; PKR 140,000</span></h3>
<b class="green">Best in-budget safety option:</b>
<ul>
  <li><b>8 dedicated years in donor relations at READ Foundation</b> &mdash; proposal writing, donor database, budget reporting, funder communications. Most sustained in-budget donor relations experience.</li>
  <li>Fundraising-specific certifications: Major Donor Fundraising, NGO Boot Camp, Fundraising Essentials.</li>
  <li>Islamabad-based at PKR 140K &mdash; most affordable senior option with genuine donor relations background.</li>
</ul>
<b class="red">Risks:</b>
<ul>
  <li>READ Foundation is domestic NGO &mdash; no multilateral (USAID/WB/FCDO/EU) experience. Step-up to Taleemabad&rsquo;s international donor landscape is material.</li>
  <li>No evidence of 30&ndash;50 opportunity pipeline at scale.</li>
</ul>
</div>

<h3>Comparison Matrix &mdash; Top 3</h3>
<table>
<tr>
  <th>Criteria</th>
  <th style="background:#4C1D95;">Mizhgan Kirmani</th>
  <th style="background:#BE185D;">Zain Ul Abideen &#128269;</th>
  <th style="background:#1D4ED8;">Sadia Sohail</th>
</tr>
<tr><td><b>Score</b></td><td>8.0</td><td>7.8</td><td>7.5</td></tr>
<tr><td><b>Budget</b></td><td>&#10003; PKR 250K</td><td>&#10007; PKR 350K (+80K)</td><td>&#10003; PKR 140K</td></tr>
<tr><td><b>Location</b></td><td>&#10003; Islamabad</td><td>&#10003; Islamabad</td><td>&#10003; Rawalpindi/Isb</td></tr>
<tr><td><b>Fundraising track record</b></td><td>PKR 72M closed (FY)</td><td>US $50M+ in won proposals</td><td>Donor relations (no $ stated)</td></tr>
<tr><td><b>Multilateral donors</b></td><td>&#10003; FCDO/UN Women/USAID/UNDP</td><td>&#10003; UNICEF/UNFPA/US Embassy/IRC</td><td>&#10007; Domestic NGO only</td></tr>
<tr><td><b>Proposal writing</b></td><td>&#10003; Active</td><td>&#10003; Core career skill</td><td>&#10003; Active</td></tr>
<tr><td><b>$500K+ closed independently</b></td><td>&#10007; Not evidenced</td><td>&#10003; Multiple times ($4.42M, $8.44M)</td><td>&#10007; Not evidenced</td></tr>
<tr><td><b>Education sector</b></td><td>&#10003; TCF/EdTech</td><td>&#10003; READ Foundation</td><td>&#10003; READ Foundation</td></tr>
<tr><td><b>Seniority</b></td><td>Senior (8yr)</td><td>Senior (16yr)</td><td>Mid (10yr)</td></tr>
<tr><td><b>Recommended action</b></td><td style="color:#16A34A;font-weight:bold;">Interview first</td><td style="color:#D97706;font-weight:bold;">HM decision on budget</td><td style="color:#16A34A;font-weight:bold;">Interview (backup)</td></tr>
</table>

<!-- ══════════════════════════════════
     5. STRONG MATCH BUT OUT OF BUDGET
══════════════════════════════════ -->
<h2>5. Strong Match but Out of Budget</h2>
<div class="warn-box">These candidates scored &ge;6.5/10 but are above the PKR 270K ceiling. Do not exclude silently &mdash; flagged for hiring manager review.</div>

<table>
<tr><th>Candidate</th><th>Score</th><th>Salary Desired</th><th>Budget Gap</th><th>Why They&rsquo;re Strong</th><th>Notes</th></tr>
<tr>
  <td><b>Arsalan Ashraf</b></td><td>7.9</td><td>PKR 450,000</td><td><span class="red">+PKR 180,000</span></td>
  <td>Highest fundraising deal-closing in pool: Meta $100K, Chevron $250K, PKR 80M NAVTTC; built fundraising functions at 3 orgs</td>
  <td>Karachi-based, willing to relocate; has existing Islamabad office. Budget negotiation required.</td>
</tr>
<tr>
  <td><b>Zain Ul Abideen &#128269;</b></td><td>7.8</td><td>PKR 350,000</td><td><span class="red">+PKR 80,000</span></td>
  <td>US $50M in won proposals; UNICEF/UNFPA/IRC/WaterAid/US Embassy direct donor relationships; Islamabad-based; 16+ years</td>
  <td>Smallest budget gap in this group. Islamabad-based &mdash; no relocation risk. Strong candidate to negotiate with.</td>
</tr>
<tr>
  <td><b>Ahad Ahsan Khan</b></td><td>7.4</td><td>PKR 550,000</td><td><span class="red">+PKR 280,000</span></td>
  <td>$134M grants portfolio (AKU, 210 grants); World Bank HEDP; Islamabad hometown</td>
  <td>Grants compliance role &mdash; fundraising acquisition needs probing. Large salary gap.</td>
</tr>
<tr>
  <td><b>Danish Hussain</b></td><td>7.3</td><td>PKR 550,000</td><td><span class="red">+PKR 280,000</span></td>
  <td>20 yrs dev sector; PKR 1B+ mobilized; Head Grants &amp; Partnerships; FCDO/WB/UNDP/ADB; applied twice</td>
  <td>Hyderabad-based, willing to relocate. WASH focus not EdTech. Duplicate application (1346+1347).</td>
</tr>
<tr>
  <td><b>Hamdan Ahmad</b></td><td>6.6</td><td>PKR 320,000</td><td><span class="red">+PKR 50,000</span></td>
  <td>World Bank ESFCD consultant ($100M project); Islamabad-based; education/social sector</td>
  <td>Closest to budget in group &mdash; PKR 50K gap may be negotiable. Programme mgmt not BD.</td>
</tr>
<tr>
  <td><b>Shakir Manzoor Khan</b></td><td>6.5</td><td>PKR 350,000</td><td><span class="red">+PKR 80,000</span></td>
  <td>15 yrs resource mobilization; Commonwealth Foundation, WHO, AEIF grant contributions; PPP experience</td>
  <td>Rawalpindi-based; pharma/health focus; grant role appears supporting not lead.</td>
</tr>
</table>

<!-- ══════════════════════════════════
     6. WHY OTHERS DIDN'T MAKE THE CUT
══════════════════════════════════ -->
<h2>6. Why Others Didn&rsquo;t Make the Cut</h2>
<table>
<tr><th>Bucket</th><th>Count</th><th>Candidates</th></tr>
<tr>
  <td><span class="red"><b>Missing must-have skills</b><br>(no fundraising/BD/donor exp)</span></td><td>14</td>
  <td>Muhammad Taqi (IT SaaS BD), Aqsa Gul (customer service), Muhammad Akmal (admin), Asim Ur Rehman (rural volunteer), Hasan Shahid (marketing/PR), Sheraz Khan (Microsoft licensing), Anita Kanwal (UK charity digital), Muhammad Ali Zafar (research intern), Laveeza Shah (HR/admin), Moeen Hassan (AutoCAD/real estate), Zainab (early career HR), Muhammad Sumraiz Kundi (telecom sales), Sani Muhammad (IT/ops), Arooj Irfan (clinical psychologist)</td>
</tr>
<tr>
  <td><span class="red"><b>No resume submitted</b><br>(LinkedIn Quick Apply)</span></td><td>9</td>
  <td>umair (1332), anitakanwal (1336), mahnoor (1348), abeernoorbano (1350), tanveeralamm (1366), usmaanq (1372), imran (1386), saad (1407), hassansajjadkhan (1515)</td>
</tr>
<tr>
  <td><span class="red"><b>Budget too high + weak function match</b></span></td><td>3</td>
  <td>Sameen Amjad Ali (PKR 650K, marketing/comms), Samana Qaseem (PKR 430K, alumni admin), Bareera Rauf (USD 2K/mo, dev research)</td>
</tr>
<tr>
  <td><span class="red"><b>Test/junk data</b></span></td><td>1</td>
  <td>AAMIR SOHAIL (1393) &mdash; salary &ldquo;1&rdquo;, .doc format unreadable</td>
</tr>
<tr>
  <td><span class="red"><b>Duplicate application</b></span></td><td>2</td>
  <td>Danish Hussain (1347 = 1346), AAMIR SOHAIL (1418 = 1393)</td>
</tr>
</table>

<!-- ══════════════════════════════════
     7. CHARTS & VISUALS
══════════════════════════════════ -->
<h2>7. Charts &amp; Visuals</h2>

<!-- A. Horizontal Bar Chart -->
<h3 style="color:#6B21A8;">A. Score Distribution &mdash; Top 14 Candidates</h3>
<div class="bar-wrap">
<div class="bar-row"><div class="bar-label">Mizhgan Kirmani</div><div class="bar-outer"><div class="bar-fill" style="width:80%;background:linear-gradient(90deg,#7C3AED,#4C1D95);"><span class="bar-val">8.0 &#10003; In Budget</span></div></div></div>
<div class="bar-row"><div class="bar-label">Arsalan Ashraf</div><div class="bar-outer"><div class="bar-fill" style="width:79%;background:linear-gradient(90deg,#DC2626,#B91C1C);"><span class="bar-val">7.9 Out</span></div></div></div>
<div class="bar-row"><div class="bar-label">Zain Ul Abideen &#128269;</div><div class="bar-outer"><div class="bar-fill" style="width:78%;background:linear-gradient(90deg,#DB2777,#BE185D);"><span class="bar-val">7.8 Out</span></div></div></div>
<div class="bar-row"><div class="bar-label">Sadia Sohail</div><div class="bar-outer"><div class="bar-fill" style="width:75%;background:linear-gradient(90deg,#7C3AED,#4C1D95);"><span class="bar-val">7.5 &#10003; In Budget</span></div></div></div>
<div class="bar-row"><div class="bar-label">Ahad Ahsan Khan</div><div class="bar-outer"><div class="bar-fill" style="width:74%;background:linear-gradient(90deg,#DC2626,#B91C1C);"><span class="bar-val">7.4 Out</span></div></div></div>
<div class="bar-row"><div class="bar-label">Danish Hussain</div><div class="bar-outer"><div class="bar-fill" style="width:73%;background:linear-gradient(90deg,#DC2626,#B91C1C);"><span class="bar-val">7.3 Out</span></div></div></div>
<div class="bar-row"><div class="bar-label">Faheem Baig</div><div class="bar-outer"><div class="bar-fill" style="width:67%;background:linear-gradient(90deg,#059669,#047857);"><span class="bar-val">6.7 &#10003; In Budget</span></div></div></div>
<div class="bar-row"><div class="bar-label">Hamdan Ahmad</div><div class="bar-outer"><div class="bar-fill" style="width:66%;background:linear-gradient(90deg,#D97706,#B45309);"><span class="bar-val">6.6 Out (-50K)</span></div></div></div>
<div class="bar-row"><div class="bar-label">Mushahid Hussain</div><div class="bar-outer"><div class="bar-fill" style="width:66%;background:linear-gradient(90deg,#059669,#047857);"><span class="bar-val">6.6 &#10003; In Budget</span></div></div></div>
<div class="bar-row"><div class="bar-label">Shakir Manzoor Khan</div><div class="bar-outer"><div class="bar-fill" style="width:65%;background:linear-gradient(90deg,#DC2626,#B91C1C);"><span class="bar-val">6.5 Out</span></div></div></div>
<div class="bar-row"><div class="bar-label">Ahmed Al-Mayadeen</div><div class="bar-outer"><div class="bar-fill" style="width:64%;background:linear-gradient(90deg,#DC2626,#B91C1C);"><span class="bar-val">6.4 Out</span></div></div></div>
<div class="bar-row"><div class="bar-label">Muhammad Usman</div><div class="bar-outer"><div class="bar-fill" style="width:61%;background:linear-gradient(90deg,#DC2626,#B91C1C);"><span class="bar-val">6.1 Out</span></div></div></div>
<div class="bar-row"><div class="bar-label">Abdul Salam</div><div class="bar-outer"><div class="bar-fill" style="width:59%;background:linear-gradient(90deg,#DC2626,#B91C1C);"><span class="bar-val">5.9 Out</span></div></div></div>
<div class="bar-row"><div class="bar-label">Arsim Tariq</div><div class="bar-outer"><div class="bar-fill" style="width:54%;background:linear-gradient(90deg,#D97706,#B45309);"><span class="bar-val">5.4 Borderline</span></div></div></div>
<br><small style="color:#6B7280;">&#128996; Purple/Green = In Budget &nbsp;|&nbsp; &#128308; Red = Out of Budget &nbsp;|&nbsp; &#128993; Amber = Borderline/Unknown</small>
</div>

<!-- B. Pie Chart SVG -->
<h3 style="color:#6B21A8;">B. Budget Fit Overview &mdash; All 48 Applications</h3>
<div style="display:flex; align-items:center; gap:40px; background:#fff; border-radius:8px; padding:20px; border:1px solid #DDD6FE; flex-wrap:wrap;">
<svg width="200" height="200" viewBox="0 0 200 200">
  <!-- In budget ~25% -->
  <path d="M100,100 L100,10 A90,90 0 0,1 190,100 Z" fill="#16A34A"/>
  <!-- Out of budget ~52% -->
  <path d="M100,100 L190,100 A90,90 0 0,1 22,155 Z" fill="#DC2626"/>
  <!-- No data/excluded ~23% -->
  <path d="M100,100 L22,155 A90,90 0 0,1 100,10 Z" fill="#9333EA"/>
  <circle cx="100" cy="100" r="45" fill="white"/>
  <text x="100" y="95" text-anchor="middle" font-size="13" font-weight="bold" fill="#111">48</text>
  <text x="100" y="112" text-anchor="middle" font-size="10" fill="#6B7280">applications</text>
</svg>
<div style="font-size:14px; line-height:2.2;">
  <div><span style="display:inline-block;width:16px;height:16px;background:#16A34A;border-radius:3px;vertical-align:middle;margin-right:8px;"></span><b class="green">In Budget (&le;270K PKR)</b> &mdash; ~12 candidates</div>
  <div><span style="display:inline-block;width:16px;height:16px;background:#DC2626;border-radius:3px;vertical-align:middle;margin-right:8px;"></span><b class="red">Out of Budget (&gt;270K PKR)</b> &mdash; ~25 candidates</div>
  <div><span style="display:inline-block;width:16px;height:16px;background:#9333EA;border-radius:3px;vertical-align:middle;margin-right:8px;"></span><b class="purple">No data / Excluded</b> &mdash; ~11 candidates<br><small style="color:#6B7280;">(9 no-resume, 1 test data, 1 anomalous salary)</small></div>
</div>
</div>

<!-- C. Radar / Star Chart SVG -->
<h3 style="color:#6B21A8;">C. Candidate Radar &mdash; Top 3 Across 6 Dimensions</h3>
<div style="background:#fff; border-radius:8px; padding:20px; border:1px solid #DDD6FE; text-align:center;">
<svg width="420" height="340" viewBox="0 0 420 340">
  <!-- Grid lines -->
  <polygon points="210,40 340,125 295,270 125,270 80,125" fill="none" stroke="#E5E7EB" stroke-width="1"/>
  <polygon points="210,76 304,141 269,246 151,246 116,141" fill="none" stroke="#E5E7EB" stroke-width="1"/>
  <polygon points="210,112 268,157 243,222 177,222 152,157" fill="none" stroke="#E5E7EB" stroke-width="1"/>
  <polygon points="210,148 232,173 217,198 203,198 188,173" fill="none" stroke="#E5E7EB" stroke-width="1"/>
  <!-- Axis lines -->
  <line x1="210" y1="155" x2="210" y2="40" stroke="#D1D5DB" stroke-width="1"/>
  <line x1="210" y1="155" x2="340" y2="125" stroke="#D1D5DB" stroke-width="1"/>
  <line x1="210" y1="155" x2="295" y2="270" stroke="#D1D5DB" stroke-width="1"/>
  <line x1="210" y1="155" x2="125" y2="270" stroke="#D1D5DB" stroke-width="1"/>
  <line x1="210" y1="155" x2="80" y2="125" stroke="#D1D5DB" stroke-width="1"/>
  <!-- Axis labels -->
  <text x="210" y="32" text-anchor="middle" font-size="11" fill="#6B21A8" font-weight="bold">Must-have</text>
  <text x="355" y="120" text-anchor="start" font-size="11" fill="#6B21A8" font-weight="bold">Experience</text>
  <text x="302" y="290" text-anchor="middle" font-size="11" fill="#6B21A8" font-weight="bold">Domain</text>
  <text x="118" y="290" text-anchor="middle" font-size="11" fill="#6B21A8" font-weight="bold">Budget Fit</text>
  <text x="48" y="120" text-anchor="end" font-size="11" fill="#6B21A8" font-weight="bold">Location</text>
  <!-- Mizhgan: must=3.2/3.5=91%, exp=2.0/2.5=80%, domain=0.8, budget=1.4/1.5=93%, loc=0.5 -->
  <!-- Scale: 100% = outer pentagon -->
  <!-- Mizhgan Kirmani (purple) -->
  <polygon points="210,47 333,127 287,261 144,259 83,128"
    fill="#7C3AED" fill-opacity="0.15" stroke="#7C3AED" stroke-width="2.5"/>
  <!-- Zain Ul Abideen (pink) -->
  <polygon points="210,49 330,128 282,263 148,257 86,129"
    fill="#EC4899" fill-opacity="0.15" stroke="#EC4899" stroke-width="2.5" stroke-dasharray="5,3"/>
  <!-- Sadia Sohail (blue) -->
  <polygon points="210,62 308,138 275,255 158,255 103,135"
    fill="#1D4ED8" fill-opacity="0.15" stroke="#1D4ED8" stroke-width="2" stroke-dasharray="8,4"/>
  <!-- Legend -->
  <rect x="50" y="305" width="14" height="14" fill="#7C3AED" rx="2"/>
  <text x="70" y="316" font-size="11" fill="#7C3AED" font-weight="bold">Mizhgan Kirmani (8.0)</text>
  <rect x="185" y="305" width="14" height="14" fill="#EC4899" rx="2"/>
  <text x="205" y="316" font-size="11" fill="#EC4899" font-weight="bold">Zain Ul Abideen (7.8)</text>
  <rect x="320" y="305" width="14" height="14" fill="#1D4ED8" rx="2"/>
  <text x="340" y="316" font-size="11" fill="#1D4ED8" font-weight="bold">Sadia Sohail (7.5)</text>
</svg>
<p style="font-size:12px; color:#6B7280; margin-top:4px;">Axes: Must-have match &bull; Relevant Experience &bull; Domain/Industry &bull; Budget Fit &bull; Location</p>
</div>

<!-- D. Must-have Heatmap -->
<h3 style="color:#6B21A8;">D. Must-have Coverage Heatmap &mdash; Top 8 Candidates</h3>
<table>
<tr>
  <th>Must-have skill</th>
  <th style="background:#4C1D95;">Mizhgan</th>
  <th style="background:#BE185D;">Zain &#128269;</th>
  <th style="background:#B45309;">Arsalan</th>
  <th style="background:#155E75;">Sadia</th>
  <th style="background:#065F46;">Faheem</th>
  <th style="background:#1D4ED8;">Mushahid</th>
  <th style="background:#92400E;">Danish</th>
  <th style="background:#6B21A8;">Hamdan</th>
</tr>
<tr><td>Fundraising / BD / partnerships</td>
  <td style="background:#DCFCE7;text-align:center;">&#9989;</td><td style="background:#DCFCE7;text-align:center;">&#9989;</td><td style="background:#DCFCE7;text-align:center;">&#9989;</td>
  <td style="background:#DCFCE7;text-align:center;">&#9989;</td><td style="background:#FEF9C3;text-align:center;">&#9888;</td><td style="background:#FEF9C3;text-align:center;">&#9888;</td>
  <td style="background:#DCFCE7;text-align:center;">&#9989;</td><td style="background:#FEF9C3;text-align:center;">&#9888;</td></tr>
<tr><td>Pakistan donor landscape knowledge</td>
  <td style="background:#DCFCE7;text-align:center;">&#9989;</td><td style="background:#DCFCE7;text-align:center;">&#9989;</td><td style="background:#FEF9C3;text-align:center;">&#9888;</td>
  <td style="background:#FEF9C3;text-align:center;">&#9888;</td><td style="background:#DCFCE7;text-align:center;">&#9989;</td><td style="background:#FEF9C3;text-align:center;">&#9888;</td>
  <td style="background:#DCFCE7;text-align:center;">&#9989;</td><td style="background:#DCFCE7;text-align:center;">&#9989;</td></tr>
<tr><td>Proposal / grant writing</td>
  <td style="background:#DCFCE7;text-align:center;">&#9989;</td><td style="background:#DCFCE7;text-align:center;">&#9989;</td><td style="background:#DCFCE7;text-align:center;">&#9989;</td>
  <td style="background:#DCFCE7;text-align:center;">&#9989;</td><td style="background:#FEF9C3;text-align:center;">&#9888;</td><td style="background:#FEF9C3;text-align:center;">&#9888;</td>
  <td style="background:#DCFCE7;text-align:center;">&#9989;</td><td style="background:#FEF9C3;text-align:center;">&#9888;</td></tr>
<tr><td>Pipeline management (30-50+ opps)</td>
  <td style="background:#FEF9C3;text-align:center;">&#9888;</td><td style="background:#DCFCE7;text-align:center;">&#9989;</td><td style="background:#DCFCE7;text-align:center;">&#9989;</td>
  <td style="background:#FEF9C3;text-align:center;">&#9888;</td><td style="background:#FEE2E2;text-align:center;">&#10060;</td><td style="background:#FEE2E2;text-align:center;">&#10060;</td>
  <td style="background:#DCFCE7;text-align:center;">&#9989;</td><td style="background:#FEE2E2;text-align:center;">&#10060;</td></tr>
<tr><td>Islamabad / willing to relocate</td>
  <td style="background:#DCFCE7;text-align:center;">&#9989;</td><td style="background:#DCFCE7;text-align:center;">&#9989;</td><td style="background:#FEF9C3;text-align:center;">&#9888;</td>
  <td style="background:#DCFCE7;text-align:center;">&#9989;</td><td style="background:#DCFCE7;text-align:center;">&#9989;</td><td style="background:#DCFCE7;text-align:center;">&#9989;</td>
  <td style="background:#FEF9C3;text-align:center;">&#9888;</td><td style="background:#DCFCE7;text-align:center;">&#9989;</td></tr>
<tr><td>Strong written / presentation skills</td>
  <td style="background:#DCFCE7;text-align:center;">&#9989;</td><td style="background:#DCFCE7;text-align:center;">&#9989;</td><td style="background:#DCFCE7;text-align:center;">&#9989;</td>
  <td style="background:#DCFCE7;text-align:center;">&#9989;</td><td style="background:#DCFCE7;text-align:center;">&#9989;</td><td style="background:#FEF9C3;text-align:center;">&#9888;</td>
  <td style="background:#DCFCE7;text-align:center;">&#9989;</td><td style="background:#DCFCE7;text-align:center;">&#9989;</td></tr>
<tr><td>$500K+ deal closed independently</td>
  <td style="background:#FEE2E2;text-align:center;">&#10060;</td><td style="background:#DCFCE7;text-align:center;">&#9989;</td><td style="background:#DCFCE7;text-align:center;">&#9989;</td>
  <td style="background:#FEE2E2;text-align:center;">&#10060;</td><td style="background:#FEE2E2;text-align:center;">&#10060;</td><td style="background:#FEE2E2;text-align:center;">&#10060;</td>
  <td style="background:#DCFCE7;text-align:center;">&#9989;</td><td style="background:#FEE2E2;text-align:center;">&#10060;</td></tr>
</table>
<p style="font-size:12px;color:#6B7280;">&#9989; Present &nbsp;|&nbsp; &#9888; Partial/Adjacent &nbsp;|&nbsp; &#10060; Absent</p>

<!-- ══════════════════════════════════
     NEXT STEPS
══════════════════════════════════ -->
<h2>Recommended Next Steps</h2>
<div class="rec-box">
<ol>
  <li><b class="purple">Interview Mizhgan Kirmani first</b> &mdash; strongest in-budget candidate. Probe: what did you personally win vs. support? Largest grant independently closed?</li>
  <li><b class="pink">HM decision on Zain Ul Abideen</b> &mdash; PKR 350K (PKR 80K over ceiling). US $50M in won proposals. Smallest budget gap among all strong-but-out-of-budget candidates. Worth a call to discuss.</li>
  <li><b class="blue">Interview Sadia Sohail</b> &mdash; 8 yrs donor relations, in budget. Probe: has she engaged multilateral/bilateral donors directly or only domestic NGOs?</li>
  <li><b class="green">Interview Faheem Baig and Mushahid Hussain</b> &mdash; both Islamabad-based, within budget. Probe grant writing experience specifically.</li>
  <li><b class="red">HM decision on Arsalan Ashraf</b> &mdash; strongest fundraising closer in pool but PKR 450K. Budget negotiation required.</li>
  <li><b style="color:#D97706;">Consider Hamdan Ahmad</b> &mdash; PKR 320K, only PKR 50K over ceiling. World Bank background. Closest to negotiability.</li>
  <li><b style="color:#666;">Disable LinkedIn Quick Apply</b> &mdash; 9/48 applications (19%) were empty submissions with temp emails and no CVs.</li>
</ol>
</div>

<div class="footer">
  Report generated by Taleemabad Talent Acquisition Agent &bull; 2026-03-02 (v2 &mdash; OCR update)<br>
  Job ID 32 &bull; Fundraising &amp; Partnerships Manager &bull; Budget: PKR 150,000&ndash;270,000/month<br>
  Scoring: Must-have 35% &bull; Experience 25% &bull; Domain 10% &bull; Responsibilities 10% &bull; Budget 15% &bull; Location 5%<br>
  Sent to: ayesha.khan@taleemabad.com only &bull; &#128269; = OCR-recovered via Tesseract
</div>

</body>
</html>"""

msg = MIMEMultipart("alternative")
msg["Subject"] = "UPDATED: Screening Report — Fundraising & Partnerships Manager (v2 · OCR + Charts)"
msg["From"]    = SENDER
msg["To"]      = RECIPIENT
msg.attach(MIMEText(html, "html"))

with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.starttls()
    server.login(SENDER, PASSWORD)
    allow_candidate_addresses(RECIPIENT if isinstance(RECIPIENT, list) else [RECIPIENT])
        safe_sendmail(server, SENDER, RECIPIENT, msg.as_string(), context='send_job32_report_v3')

print(f"SUCCESS: Updated report sent to {RECIPIENT}")
