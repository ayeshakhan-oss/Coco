import smtplib, os, json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()
import sys as _sys
_sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from scripts.utils.safe_send import safe_sendmail, allow_candidate_addresses


# ── CONFIG ──────────────────────────────────────────────────────────────────
RECIPIENT = "ayesha.khan@taleemabad.com"
SENDER    = os.getenv("EMAIL_USER")
PASSWORD  = os.getenv("EMAIL_PASSWORD")

# ── HTML REPORT ─────────────────────────────────────────────────────────────
html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
  body { font-family: Arial, sans-serif; font-size: 14px; color: #1a1a1a; max-width: 1100px; margin: 0 auto; padding: 24px; }
  h1 { background: #1a3c5e; color: #fff; padding: 16px 20px; border-radius: 6px; font-size: 22px; }
  h2 { color: #1a3c5e; border-bottom: 2px solid #1a3c5e; padding-bottom: 6px; margin-top: 36px; }
  h3 { color: #2e5d8e; margin-top: 24px; }
  table { border-collapse: collapse; width: 100%; margin: 16px 0; font-size: 13px; }
  th { background: #1a3c5e; color: #fff; padding: 10px 12px; text-align: left; }
  td { padding: 9px 12px; border-bottom: 1px solid #dde3ea; vertical-align: top; }
  tr:nth-child(even) td { background: #f4f7fb; }
  .in  { color: #1a7a3c; font-weight: bold; }
  .out { color: #c0392b; font-weight: bold; }
  .unk { color: #b07d00; font-weight: bold; }
  .tag-in  { background:#d4edda; color:#155724; padding:2px 8px; border-radius:12px; font-size:12px; white-space:nowrap; }
  .tag-out { background:#f8d7da; color:#721c24; padding:2px 8px; border-radius:12px; font-size:12px; white-space:nowrap; }
  .tag-unk { background:#fff3cd; color:#856404; padding:2px 8px; border-radius:12px; font-size:12px; white-space:nowrap; }
  .summary-box { background:#eef4fb; border-left:4px solid #1a3c5e; padding:14px 18px; border-radius:4px; margin:16px 0; }
  .rec-box { background:#eaf7ed; border-left:4px solid #1a7a3c; padding:14px 18px; border-radius:4px; margin:16px 0; }
  .warn-box { background:#fff8e1; border-left:4px solid #f0a500; padding:14px 18px; border-radius:4px; margin:16px 0; }
  .bar { font-family: monospace; font-size: 13px; line-height: 1.8; }
  .profile { background:#fafbfd; border:1px solid #dde3ea; border-radius:6px; padding:16px; margin:16px 0; }
  .score-badge { display:inline-block; background:#1a3c5e; color:#fff; border-radius:20px; padding:3px 12px; font-weight:bold; font-size:14px; }
  ul { margin: 6px 0; padding-left: 20px; }
  li { margin: 4px 0; }
  .footer { margin-top: 48px; padding-top: 16px; border-top: 1px solid #dde3ea; color: #888; font-size: 12px; }
</style>
</head>
<body>

<h1>Candidate Screening Report — Fundraising &amp; Partnerships Manager</h1>

<!-- ═══════════════════════════════════════════════════════════════
     1. SCREENING SUMMARY
════════════════════════════════════════════════════════════════ -->
<h2>1. Screening Summary</h2>
<div class="summary-box">
<table style="width:auto; margin:0;">
<tr><td><b>Job</b></td><td>Fundraising &amp; Partnerships Manager (Job ID 32)</td></tr>
<tr><td><b>Date</b></td><td>2026-03-02</td></tr>
<tr><td><b>Pool size</b></td><td>48 applications</td></tr>
<tr><td><b>Shortlist size</b></td><td>Top 20 (pool ≥ 40 rule)</td></tr>
<tr><td><b>Budget</b></td><td>PKR 150,000 – 270,000 / month</td></tr>
<tr><td><b>Location</b></td><td>Islamabad — In-Person, Permanent</td></tr>
<tr><td><b>Data coverage</b></td><td>36 / 48 CVs readable</td></tr>
<tr><td><b>Scoring weights</b></td><td>Must-have 35% · Experience 25% · Domain 10% · Responsibilities 10% · Budget 15% · Location 5%</td></tr>
</table>
</div>

<b>Data gaps:</b>
<ul>
  <li><b>9 no-resume</b> (LinkedIn Quick Apply): apps 1332, 1336, 1348, 1350, 1366, 1372, 1386, 1407, 1515 — auto-excluded</li>
  <li><b>1 unreadable CV</b>: Zain Ul Abideen (1333) — scanned PDF, text not extractable. Salary stated: PKR 350,000 (over budget)</li>
  <li><b>1 test/junk entry</b>: AAMIR SOHAIL (1393) — salary entered as "1", .doc file unreadable</li>
  <li><b>2 duplicates</b>: Danish Hussain (1347 = 1346), AAMIR SOHAIL (1418 = 1393) — merged to single entry</li>
</ul>


<!-- ═══════════════════════════════════════════════════════════════
     2. JD SCORECARD
════════════════════════════════════════════════════════════════ -->
<h2>2. JD Scorecard</h2>
<table>
<tr><th style="width:180px">Category</th><th>Detail</th></tr>
<tr><td><b>Must-haves</b></td><td>
  1. Fundraising / partnerships / BD / institutional engagement experience<br>
  2. Knowledge of Pakistan donor landscape (USAID, World Bank, DFID/FCDO, JICA, EU, foundations)<br>
  3. Proposal / concept note / grant writing experience<br>
  4. Pipeline management (track 30–50+ opportunities simultaneously)<br>
  5. Islamabad-based or willing to relocate (in-person, daily)<br>
  6. Strong written communication and presentation skills
</td></tr>
<tr><td><b>Nice-to-haves</b></td><td>
  • Existing relationships within Pakistan's donor community<br>
  • Experience closing $500K+ funding deals independently<br>
  • Education sector experience in Pakistan<br>
  • Government/policy engagement in Islamabad's ecosystem
</td></tr>
<tr><td><b>Deal-breakers</b></td><td>
  • Zero fundraising/BD/partnerships experience<br>
  • Not Islamabad-based AND not willing to relocate
</td></tr>
<tr><td><b>Constraints</b></td><td>
  • Budget: PKR 150,000 – 270,000/month<br>
  • Location: Islamabad, full-time in-person<br>
  • Year 1 target: $500K – $1M+ in new funding closed<br>
  • Must build pipeline of 6–12 months visibility
</td></tr>
</table>


<!-- ═══════════════════════════════════════════════════════════════
     3. RANKED SHORTLIST — TOP 20
════════════════════════════════════════════════════════════════ -->
<h2>3. Ranked Shortlist — Top 20</h2>
<p><i>Pool: 48 · Shortlist rule: pool ≥ 40 → top 20. Ranked by total score, then must-have strength, then budget fit.</i></p>

<table>
<tr>
  <th>#</th><th>Candidate</th><th>Score</th><th>Must-have match</th>
  <th>Salary (PKR/mo)</th><th>Budget</th><th>Key Strengths</th><th>Key Risks</th>
</tr>
<tr>
  <td>1</td><td><b>Mizhgan Kirmani</b></td><td><b>8.0</b></td>
  <td>Donor relations ✅ Proposal writing ✅ FCDO/UNDP/USAID ✅</td>
  <td>250,000</td><td><span class="tag-in">In Budget</span></td>
  <td>Manager Donor Relations at TCF; closed FY at PKR 72M; FCDO, UN Women, USAID, UNDP direct engagement; Islamabad-based</td>
  <td>Proposal-drafting vs. large-scale grant-winning not yet evidenced; no $500K+ deal independently closed</td>
</tr>
<tr>
  <td>2</td><td><b>Arsalan Ashraf</b></td><td><b>7.9</b></td>
  <td>Fundraising ✅ Proposal writing ✅ Pipeline mgmt ✅</td>
  <td>450,000</td><td><span class="tag-out">Out of Budget</span></td>
  <td>Strongest fundraising track record in pool: Meta $100K, Chevron $250K, PKR 80M NAVTTC, PKR 30M Sindh govt; multi-sector pipeline management</td>
  <td>Primarily CSR/corporate donors — less USAID/WB/FCDO multilateral experience; Karachi-based (willing to relocate)</td>
</tr>
<tr>
  <td>3</td><td><b>Sadia Sohail</b></td><td><b>7.5</b></td>
  <td>Donor relations ✅ Proposal writing ✅ Budget reporting ✅</td>
  <td>140,000</td><td><span class="tag-in">In Budget</span></td>
  <td>8 years Donor Relations at READ Foundation; proposal writing, donor database, fundraising certifications (Major Donor, NGO Boot Camp); Islamabad-based</td>
  <td>Domestic NGO focus — no multilateral (USAID/WB/FCDO/EU) experience; no evidence of 30–50 opportunity pipeline at scale</td>
</tr>
<tr>
  <td>4</td><td><b>Ahad Ahsan Khan</b></td><td><b>7.4</b></td>
  <td>Grants management ✅ USAID/WB compliance ✅ Portfolio scale ✅</td>
  <td>550,000</td><td><span class="tag-out">Out of Budget</span></td>
  <td>Manager Grants at AKU ($134M portfolio, 210 grants); World Bank HEDP lead; Islamabad hometown; team of 8</td>
  <td>Grants compliance/reporting ≠ fundraising acquisition; PKR 550K far over budget</td>
</tr>
<tr>
  <td>5</td><td><b>Danish Hussain</b></td><td><b>7.3</b></td>
  <td>Fundraising ✅ FCDO/EU/WB ✅ Grant writing ✅</td>
  <td>550,000</td><td><span class="tag-out">Out of Budget</span></td>
  <td>20 years development sector; PKR 1B+ in mobilized donor funding; Head of Grants &amp; Partnerships; FCDO/EU/WB/UNDP/ADB engagement</td>
  <td>Hyderabad-based (no relocation mentioned); humanitarian/social sector not EdTech; PKR 550K (2x budget ceiling)</td>
</tr>
<tr>
  <td>6</td><td><b>Faheem Baig</b></td><td><b>6.7</b></td>
  <td>Donor networks ✅ Development sector ✅ M.Phil PIDE ✅</td>
  <td>145,000</td><td><span class="tag-in">In Budget</span></td>
  <td>DG-ECHO, GIZ, UN Women, USAID, AKDN networks; CEO/COO programme lead; M.Phil Development Studies (PIDE); Islamabad-based; within budget</td>
  <td>Programme implementation focus — no dedicated grant writing or quantified proposal wins; limited EdTech experience</td>
</tr>
<tr>
  <td>7</td><td><b>Hamdan Ahmad</b></td><td><b>6.6</b></td>
  <td>WB partnership ✅ Development sector ✅ Education ✅</td>
  <td>320,000</td><td><span class="tag-out">Out of Budget</span></td>
  <td>World Bank consultant (ESFCD, $100M project); Islamabad G-13; education/social sector; stakeholder engagement with govt and donors</td>
  <td>Programme management not resource mobilisation; PKR 320K (PKR 50K over ceiling) — closest to budget in out-of-budget group</td>
</tr>
<tr>
  <td>8</td><td><b>Mushahid Hussain</b></td><td><b>6.6</b></td>
  <td>Donor reporting ✅ Fundraising ✅ Development ✅</td>
  <td>170,000</td><td><span class="tag-in">In Budget</span></td>
  <td>Donor Reporting Officer at READ Foundation; fundraising, financial proposals, RBM; Islamabad-based; well within budget</td>
  <td>4 years experience — junior for Manager; donor reporting role not acquisition/BD lead; pipeline management not evidenced</td>
</tr>
<tr>
  <td>9</td><td><b>Shakir Manzoor Khan</b></td><td><b>6.5</b></td>
  <td>Grant proposals ✅ Resource mobilization ✅ PPP ✅</td>
  <td>350,000</td><td><span class="tag-out">Out of Budget</span></td>
  <td>15 years resource mobilization; Commonwealth Foundation, WHO, AEIF grant proposals; public-private partnerships; Rawalpindi (near Islamabad)</td>
  <td>Pharma/public health focus not EdTech; grant contributions appear supporting not lead; PKR 350K over budget</td>
</tr>
<tr>
  <td>10</td><td><b>Ahmed Al-Mayadeen</b></td><td><b>6.4</b></td>
  <td>UN fundraising ✅ Multi-million campaigns ✅ MENA donors ✅</td>
  <td>~PKR 980,000 ($3,500/mo)</td><td><span class="tag-out">Out of Budget</span></td>
  <td>10+ years UN/NGO fundraising; UNESCO evaluation roster; multi-million campaigns; Harvard Business diploma</td>
  <td>Yemen-based (not Pakistan); PKR 980K (3.6x budget); Pakistan donor relationships not established</td>
</tr>
<tr>
  <td>11</td><td><b>Muhammad Usman</b></td><td><b>6.1</b></td>
  <td>Partnerships ✅ Fundraising (competency) ✅ Int'l dev ✅</td>
  <td>350,000</td><td><span class="tag-out">Out of Budget</span></td>
  <td>18 years stakeholder management; international development alliances; UNODC/British Council trained; Rawalpindi/Islamabad area</td>
  <td>Fundraising listed as competency but no quantified wins; PKR 350K over budget</td>
</tr>
<tr>
  <td>12</td><td><b>Abdul Salam</b></td><td><b>5.9</b></td>
  <td>Donor projects ✅ WB/USAID/DFID ✅ Islamabad ✅</td>
  <td>400,000</td><td><span class="tag-out">Out of Budget</span></td>
  <td>21 years development; managed WB/USAID/DFID/GIZ/UNICEF funded programmes; Islamabad-based</td>
  <td>WASH/humanitarian implementation — not resource mobilisation; PKR 400K (1.5x ceiling)</td>
</tr>
<tr>
  <td>13</td><td><b>Zubair Hussain</b></td><td><b>5.6</b></td>
  <td>Development sector ✅ Education (SEF) ✅ Fundraising (listed) ✅</td>
  <td>30,000 (⚠️ likely data error)</td><td><span class="tag-unk">Unknown*</span></td>
  <td>Development sector; PPAF-ITC-EU project; SEF education programme; gender/rights-based approaches</td>
  <td>Salary entry anomalous (30K desired vs 250K current — likely typo); field/gender specialist not BD lead</td>
</tr>
<tr>
  <td>14</td><td><b>Arsim Tariq</b></td><td><b>5.4</b></td>
  <td>Proposals ✅ FCDO/WB contracts ✅ Education sector ✅</td>
  <td>280,000–300,000</td><td><span class="tag-out">Out of Budget</span></td>
  <td>Secured 10+ development sector projects via proposals; FCDO/WB contracts; Islamabad-based; NUST MS</td>
  <td>Programme management/M&amp;E role — not dedicated fundraising BD; slightly over budget (280–300K vs 270K ceiling)</td>
</tr>
<tr>
  <td>15</td><td><b>Fahad Khan</b></td><td><b>5.0</b></td>
  <td>Fundraising role ✅ Pipeline mgmt ✅</td>
  <td>350,000</td><td><span class="tag-out">Out of Budget</span></td>
  <td>Associate Manager Fundraising at Shaukat Khanum; BD experience; Islamabad-based</td>
  <td>Hospital charity fundraising ≠ institutional donors (USAID/WB/FCDO); PKR 350K over budget</td>
</tr>
<tr>
  <td>16</td><td><b>Mahnoor Mellu</b></td><td><b>5.0</b></td>
  <td>Partnerships ✅ Pipeline mgmt ✅ LUMS ✅</td>
  <td>350,000</td><td><span class="tag-out">Out of Budget</span></td>
  <td>Partnerships Manager at DigitalOcean-Cloudways; B2B pipeline; LUMS graduate</td>
  <td>Tech/SaaS partnerships ≠ development sector fundraising; Lahore-based; PKR 350K over budget</td>
</tr>
<tr>
  <td>17</td><td><b>Imran Haider</b></td><td><b>4.9</b></td>
  <td>Education policy ✅ MoFEPT/WB ✅ M&amp;E ✅</td>
  <td>350,000</td><td><span class="tag-out">Out of Budget</span></td>
  <td>LUMS-educated; education policy &amp; M&amp;E; WB PHCIP GRM consultant; strong education alignment</td>
  <td>Policy/implementation not resource mobilisation; no proposal writing lead; PKR 350K over budget; Lahore-based</td>
</tr>
<tr>
  <td>18</td><td><b>Sameen Amjad Ali</b></td><td><b>3.6</b></td>
  <td>Stakeholder engagement ✅ Investor materials ✅</td>
  <td>650,000</td><td><span class="tag-out">Out of Budget</span></td>
  <td>Senior marketing/comms; investor-facing materials; ministerial-level stakeholder engagement</td>
  <td>No donor/development sector fundraising; PKR 650K (2.4x budget)</td>
</tr>
<tr>
  <td>19</td><td><b>Samana Qaseem</b></td><td><b>3.5</b></td>
  <td>Grants programme ✅ Education ✅</td>
  <td>430,000</td><td><span class="tag-out">Out of Budget</span></td>
  <td>Pakistan-US Alumni Network grants lead; education programme coordination; IFC certified</td>
  <td>Alumni affairs/admin not donor-facing BD; PKR 430K over budget</td>
</tr>
<tr>
  <td>20</td><td><b>Syeda Kainat</b></td><td><b>3.3</b></td>
  <td>Education ✅ M&amp;E ✅ Islamabad ✅</td>
  <td>110,000</td><td><span class="tag-in">In Budget</span></td>
  <td>Education sector; WB TEACH certified; Islamabad-based; within budget</td>
  <td>M&amp;E/comms officer — missing all core fundraising must-haves for Manager level</td>
</tr>
</table>


<!-- ═══════════════════════════════════════════════════════════════
     4. STRONGEST 2–3 CANDIDATES — DEEP COMPARE
════════════════════════════════════════════════════════════════ -->
<h2>4. Strongest 2–3 Candidates — Deep Comparison</h2>

<div class="profile">
<h3>🥇 Mizhgan Kirmani — <span class="score-badge">8.0 / 10</span> &nbsp; <span class="tag-in">In Budget · PKR 250,000</span></h3>
<b>Why she's top:</b>
<ul>
  <li>Currently <b>Manager Donor Relations at Citizens Foundation</b> — closed the financial year at PKR 72M in donor contributions. This is live, active institutional fundraising in Pakistan's education sector, directly parallel to what Taleemabad needs.</li>
  <li>Direct, named relationships with <b>FCDO, UN Women, UNDP, USAID, and Green Climate Fund</b> — the exact donor ecosystem the JD references. Not adjacent exposure — she is in these offices regularly as part of her current role.</li>
  <li>Islamabad-based, certified NDI political trainer, proposal writing experience, within budget at PKR 250K — no location risk, no budget negotiation required.</li>
</ul>
<b>Risks / concerns:</b>
<ul>
  <li>Her current PKR 72M track record is strong but below the JD's Year 1 target of $500K–$1M+ (PKR 140M–280M). The scale-up is significant.</li>
  <li>Proposal-drafting vs. independently winning large competitive grants is a distinction worth probing in interview.</li>
</ul>
</div>

<div class="profile">
<h3>🥈 Arsalan Ashraf — <span class="score-badge">7.9 / 10</span> &nbsp; <span class="tag-out">Out of Budget · PKR 450,000</span></h3>
<b>Why he's strong (flagged for HM review):</b>
<ul>
  <li><b>Strongest proven fundraising track record in the entire pool</b>: Meta ($100K), Chevron ($250K), PKR 80M from NAVTTC, PKR 30M from Government of Sindh, USD 40K recurring international donors for HANDS. These are closed deals, not pipeline.</li>
  <li>Built fundraising departments from scratch at multiple organisations (HANDS, CHAL Foundation, IBA AMAN) — the infrastructure-building capability the JD explicitly requires.</li>
  <li>Has established an Islamabad office (CHAL Foundation) — on-ground presence already exists despite Karachi base.</li>
</ul>
<b>Risks / concerns:</b>
<ul>
  <li>PKR 450K is 67% above the budget ceiling — significant gap. Negotiation required.</li>
  <li>Fundraising mix is CSR and government grants — less multilateral bilateral (USAID/FCDO/WB) experience than Mizhgan.</li>
</ul>
</div>

<div class="profile">
<h3>🥉 Sadia Sohail — <span class="score-badge">7.5 / 10</span> &nbsp; <span class="tag-in">In Budget · PKR 140,000</span></h3>
<b>Why she's the best in-budget safety option:</b>
<ul>
  <li><b>8 dedicated years in donor relations at READ Foundation</b> — proposal writing, donor database management, budget reporting, funder communications. More sustained donor relations experience than anyone else in-budget.</li>
  <li>Holds fundraising-specific certifications: Major Donor Fundraising, NGO Boot Camp, Fundraising Essentials — evidence of deliberate professional development in this exact function.</li>
  <li>Islamabad-based (Rawalpindi) at PKR 140K — the most affordable senior-level option in the pool with genuine donor relations background.</li>
</ul>
<b>Risks / concerns:</b>
<ul>
  <li>READ Foundation is a domestic NGO — no multilateral (USAID/World Bank/FCDO/EU) experience. The step up to Taleemabad's international donor landscape is material.</li>
  <li>No evidence of pipeline management at 30–50 opportunity scale. Interview should probe this explicitly.</li>
</ul>
</div>

<h3>Comparison Matrix — Top 3</h3>
<table>
<tr>
  <th>Criteria</th>
  <th>Mizhgan Kirmani</th>
  <th>Arsalan Ashraf</th>
  <th>Sadia Sohail</th>
</tr>
<tr><td><b>Score</b></td><td>8.0</td><td>7.9</td><td>7.5</td></tr>
<tr><td><b>Budget fit</b></td><td>✅ PKR 250K</td><td>❌ PKR 450K</td><td>✅ PKR 140K</td></tr>
<tr><td><b>Location</b></td><td>✅ Islamabad</td><td>⚠️ Karachi (relocate)</td><td>✅ Rawalpindi/Isb</td></tr>
<tr><td><b>Fundraising track record</b></td><td>PKR 72M closed (FY)</td><td>$350K+ closed deals</td><td>Donor relations (no $ closed stated)</td></tr>
<tr><td><b>Multilateral donors (USAID/WB/FCDO)</b></td><td>✅ Direct engagement</td><td>⚠️ Limited</td><td>❌ Domestic NGO only</td></tr>
<tr><td><b>Proposal writing</b></td><td>✅ Active</td><td>✅ Active</td><td>✅ Active</td></tr>
<tr><td><b>Pipeline management</b></td><td>⚠️ Not quantified</td><td>✅ Multi-org evidence</td><td>⚠️ Not at scale</td></tr>
<tr><td><b>Education sector alignment</b></td><td>✅ TCF / EdTech</td><td>⚠️ Multi-sector</td><td>✅ READ Foundation</td></tr>
<tr><td><b>Seniority</b></td><td>Senior (8yr)</td><td>Senior (12yr)</td><td>Mid (10yr)</td></tr>
<tr><td><b>$500K+ deal closed independently</b></td><td>⚠️ Not evidenced</td><td>✅ Chevron $250K + others</td><td>❌ Not evidenced</td></tr>
<tr><td><b>Recommended action</b></td><td>Interview first</td><td>HM decision on budget</td><td>Interview (backup)</td></tr>
</table>


<!-- ═══════════════════════════════════════════════════════════════
     5. STRONG MATCH BUT OUT OF BUDGET
════════════════════════════════════════════════════════════════ -->
<h2>5. Strong Match but Out of Budget</h2>
<div class="warn-box">These candidates scored ≥ 6.5/10 but are above the PKR 270K ceiling. Flagged for hiring manager review — do not silently exclude.</div>

<table>
<tr>
  <th>Candidate</th><th>Score</th><th>Salary Desired</th><th>Budget Gap</th>
  <th>Why They're Strong</th><th>Notes</th>
</tr>
<tr>
  <td><b>Arsalan Ashraf</b></td><td>7.9</td><td>PKR 450,000</td><td>+PKR 180,000</td>
  <td>Highest fundraising impact in pool; $350K+ in closed deals; built fundraising functions from scratch at 3 orgs</td>
  <td>Karachi-based but willing to relocate; has Islamabad office presence via CHAL. Budget negotiation required.</td>
</tr>
<tr>
  <td><b>Ahad Ahsan Khan</b></td><td>7.4</td><td>PKR 550,000</td><td>+PKR 280,000</td>
  <td>$134M grants portfolio (AKU); World Bank HEDP; institutional donor compliance; Islamabad hometown</td>
  <td>Grants management role — fundraising acquisition needs to be probed. Large salary gap.</td>
</tr>
<tr>
  <td><b>Danish Hussain</b></td><td>7.3</td><td>PKR 550,000</td><td>+PKR 280,000</td>
  <td>20 years development; PKR 1B+ in mobilized funding; Head of Grants &amp; Partnerships; FCDO/WB/UNDP; also applied twice</td>
  <td>Hyderabad-based — relocation to Islamabad not confirmed. Duplicate application (1346 + 1347).</td>
</tr>
<tr>
  <td><b>Hamdan Ahmad</b></td><td>6.6</td><td>PKR 320,000</td><td>+PKR 50,000</td>
  <td>World Bank consultant (ESFCD, $100M project); Islamabad-based; education sector; stakeholder engagement</td>
  <td>Closest to budget in this group — PKR 50K gap may be negotiable. Primary strength is programme management not BD.</td>
</tr>
<tr>
  <td><b>Shakir Manzoor Khan</b></td><td>6.5</td><td>PKR 350,000</td><td>+PKR 80,000</td>
  <td>15 years resource mobilization; Commonwealth Foundation, WHO, AEIF grant contributions; PPP experience</td>
  <td>Rawalpindi-based; pharmaceutical/health sector focus; grant role appears supporting not leading.</td>
</tr>
</table>


<!-- ═══════════════════════════════════════════════════════════════
     6. WHY OTHERS DIDN'T MAKE THE CUT
════════════════════════════════════════════════════════════════ -->
<h2>6. Why Others Didn't Make the Cut</h2>

<table>
<tr><th>Rejection Bucket</th><th>Count</th><th>Candidates</th></tr>
<tr>
  <td><b>Missing must-have skills<br>(no fundraising/BD/donor experience)</b></td>
  <td>14</td>
  <td>Muhammad Taqi (IT/SaaS BD), Aqsa Gul (customer service/teaching), Muhammad Akmal (admin), Asim Ur Rehman (rural volunteer), Hasan Shahid (marketing/PR), Sheraz Khan (Microsoft licensing), Anita Kanwal (UK charity digital), Muhammad Ali Zafar (research intern), Laveeza Shah (HR/admin), Moeen Hassan (AutoCAD/real estate), Zainab (early career HR), Muhammad Sumraiz Kundi (telecom sales), Sani Muhammad (IT/operations), Arooj Irfan (clinical psychologist)</td>
</tr>
<tr>
  <td><b>No resume submitted<br>(LinkedIn Quick Apply)</b></td>
  <td>9</td>
  <td>umair Applicant (1332), anitakanwal Applicant (1336), mahnoor Applicant (1348), abeernoorbano Applicant (1350), tanveeralamm Applicant (1366), usmaanq Applicant (1372), imran Applicant (1386), saad Applicant (1407), hassansajjadkhan Applicant (1515)</td>
</tr>
<tr>
  <td><b>Budget too high + weak function match</b></td>
  <td>3</td>
  <td>Sameen Amjad Ali (PKR 650K, marketing/comms background), Samana Qaseem (PKR 430K, alumni admin), Bareera Rauf (USD 2,000/mo ≈ PKR 560K, development research background)</td>
</tr>
<tr>
  <td><b>CV unreadable</b></td>
  <td>1</td>
  <td>Zain Ul Abideen (1333) — scanned PDF, text not extractable. Salary stated PKR 350,000 (over budget). Recommend: request DOCX or typed PDF to assess.</td>
</tr>
<tr>
  <td><b>Test data / junk entry</b></td>
  <td>1</td>
  <td>AAMIR SOHAIL (1393) — salary entered as "1", .doc format unreadable. Treat as invalid entry.</td>
</tr>
<tr>
  <td><b>Duplicate application</b></td>
  <td>2</td>
  <td>Danish Hussain (1347 = duplicate of 1346), AAMIR SOHAIL (1418 = duplicate of 1393)</td>
</tr>
</table>


<!-- ═══════════════════════════════════════════════════════════════
     7. CHARTS & VISUALS
════════════════════════════════════════════════════════════════ -->
<h2>7. Charts &amp; Visuals</h2>

<h3>A. Score Distribution — Top 14 Candidates</h3>
<div class="bar" style="background:#f4f7fb; padding:16px; border-radius:6px;">
<pre style="margin:0; font-size:13px; line-height:1.9;">
Mizhgan Kirmani       ████████░░  8.0  ✅ In Budget
Arsalan Ashraf        ███████░░░  7.9  ❌ Out of Budget
Sadia Sohail          ███████░░░  7.5  ✅ In Budget
Ahad Ahsan Khan       ███████░░░  7.4  ❌ Out of Budget
Danish Hussain        ███████░░░  7.3  ❌ Out of Budget
Faheem Baig           ██████░░░░  6.7  ✅ In Budget
Hamdan Ahmad          ██████░░░░  6.6  ❌ Out of Budget (PKR 50K gap)
Mushahid Hussain      ██████░░░░  6.6  ✅ In Budget
Shakir Manzoor Khan   ██████░░░░  6.5  ❌ Out of Budget
Ahmed Al-Mayadeen     ██████░░░░  6.4  ❌ Out of Budget (Yemen-based)
Muhammad Usman        ██████░░░░  6.1  ❌ Out of Budget
Abdul Salam           █████░░░░░  5.9  ❌ Out of Budget
Zubair Hussain        █████░░░░░  5.6  ⚠️ Salary anomaly
Arsim Tariq           █████░░░░░  5.4  ❌ Out of Budget (marginally)
</pre>
</div>

<h3>B. Budget Fit Overview — All 48 Applications</h3>
<table style="width:auto;">
<tr><th>Status</th><th>Count</th><th>Notes</th></tr>
<tr><td><span class="tag-in">In Budget (≤ PKR 270K)</span></td><td><b>10</b></td><td>Mizhgan Kirmani, Sadia Sohail, Faheem Baig, Mushahid Hussain, Anita Kanwal, Syeda Kainat, Zainab, Laveeza Shah, Muhammad Ali Zafar, Aqsa Gul + others with low salary</td></tr>
<tr><td><span class="tag-out">Out of Budget (&gt; PKR 270K)</span></td><td><b>25</b></td><td>Includes 5 "strong but out of budget" candidates flagged above</td></tr>
<tr><td><span class="tag-unk">Unknown / Anomalous</span></td><td><b>10</b></td><td>9 no-resume (LinkedIn), 1 anomalous entry (Zubair Hussain 30K vs 250K current)</td></tr>
<tr><td><b>Duplicate / Test / Unreadable</b></td><td><b>3</b></td><td>Excluded from analysis</td></tr>
</table>

<h3>C. Must-Have Coverage Heatmap — Top 8 Candidates</h3>
<table>
<tr>
  <th>Must-have skill</th>
  <th>Mizhgan<br>Kirmani</th>
  <th>Arsalan<br>Ashraf</th>
  <th>Sadia<br>Sohail</th>
  <th>Ahad Ahsan<br>Khan</th>
  <th>Danish<br>Hussain</th>
  <th>Faheem<br>Baig</th>
  <th>Mushahid<br>Hussain</th>
  <th>Hamdan<br>Ahmad</th>
</tr>
<tr>
  <td>Fundraising / BD / partnerships experience</td>
  <td>✅</td><td>✅</td><td>✅</td><td>⚠️</td><td>✅</td><td>⚠️</td><td>⚠️</td><td>⚠️</td>
</tr>
<tr>
  <td>Pakistan donor landscape knowledge</td>
  <td>✅</td><td>⚠️</td><td>⚠️</td><td>✅</td><td>✅</td><td>✅</td><td>⚠️</td><td>✅</td>
</tr>
<tr>
  <td>Proposal / grant writing</td>
  <td>✅</td><td>✅</td><td>✅</td><td>✅</td><td>✅</td><td>⚠️</td><td>⚠️</td><td>⚠️</td>
</tr>
<tr>
  <td>Pipeline management (30–50+ opps)</td>
  <td>⚠️</td><td>✅</td><td>⚠️</td><td>⚠️</td><td>✅</td><td>❌</td><td>❌</td><td>❌</td>
</tr>
<tr>
  <td>Islamabad-based / reliable in-person</td>
  <td>✅</td><td>⚠️</td><td>✅</td><td>⚠️</td><td>❌</td><td>✅</td><td>✅</td><td>✅</td>
</tr>
<tr>
  <td>Strong written / presentation skills</td>
  <td>✅</td><td>✅</td><td>✅</td><td>✅</td><td>✅</td><td>✅</td><td>⚠️</td><td>✅</td>
</tr>
<tr>
  <td>$500K+ deal closed independently</td>
  <td>❌</td><td>✅</td><td>❌</td><td>⚠️</td><td>✅</td><td>❌</td><td>❌</td><td>❌</td>
</tr>
</table>
<p style="font-size:12px; color:#666;">✅ Present &nbsp;|&nbsp; ⚠️ Partial / Adjacent &nbsp;|&nbsp; ❌ Absent</p>


<!-- ═══════════════════════════════════════════════════════════════
     RECOMMENDED NEXT STEPS
════════════════════════════════════════════════════════════════ -->
<h2>Recommended Next Steps</h2>
<div class="rec-box">
<ol>
  <li><b>Interview Mizhgan Kirmani first</b> — strongest in-budget candidate, direct donor relations at TCF, FCDO/UNDP/USAID ecosystem. Probe: what did you personally write and win vs. support? What is the largest grant you independently closed?</li>
  <li><b>Interview Sadia Sohail</b> — 8 years donor relations within budget. Probe: has she engaged multilateral/bilateral donors or only domestic NGO donors? Can she name a funder at USAID/WB/FCDO?</li>
  <li><b>Interview Faheem Baig and Mushahid Hussain</b> — both Islamabad-based, within budget, development sector. Good backup options. Probe grant writing experience specifically.</li>
  <li><b>HM decision on Arsalan Ashraf</b> — strongest fundraising track record in pool but PKR 450K. If budget can flex, he is the most proven closer.</li>
  <li><b>HM decision on Hamdan Ahmad</b> — Islamabad-based, World Bank background, PKR 320K (PKR 50K over ceiling). If budget cannot flex to 320K, he falls out. Closest out-of-budget candidate to negotiability.</li>
  <li><b>Request readable CV from Zain Ul Abideen (1333)</b> — scanned PDF unreadable. Salary stated PKR 350K (over budget) but M.Phil IR profile may be worth reviewing.</li>
  <li><b>Disable LinkedIn Quick Apply</b> — 9 out of 48 applications (19%) were empty submissions with temp emails and no CVs. Same pattern as previous posting.</li>
</ol>
</div>

<div class="footer">
  Report generated by Taleemabad Talent Acquisition Agent · 2026-03-02<br>
  Job ID 32 · Fundraising &amp; Partnerships Manager · Budget: PKR 150,000 – 270,000/month<br>
  Scoring: Must-have 35% · Experience 25% · Domain 10% · Responsibilities 10% · Budget 15% · Location 5%<br>
  Sent to: ayesha.khan@taleemabad.com only
</div>

</body>
</html>
"""

# ── SEND ────────────────────────────────────────────────────────────────────
msg = MIMEMultipart("alternative")
msg["Subject"] = "Screening Report — Fundraising & Partnerships Manager (48 Applications · Top 20 Ranked)"
msg["From"]    = SENDER
msg["To"]      = RECIPIENT

msg.attach(MIMEText(html, "html"))

with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.starttls()
    server.login(SENDER, PASSWORD)
    allow_candidate_addresses(RECIPIENT if isinstance(RECIPIENT, list) else [RECIPIENT])
        safe_sendmail(server, SENDER, RECIPIENT, msg.as_string(), context='send_job32_report_v2')

print(f"SUCCESS: Report sent to {RECIPIENT}")
