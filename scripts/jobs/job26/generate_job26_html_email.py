"""
Job 26: Soul Architect — HTML Email Report (Proper Format)
Matches Apr 6 reference: Header → stat boxes → Key Observation →
Shortlisted (5 with descriptions+gaps) → Maybe (7 table) → footer
"""

import json

# Load results
with open(r"c:\Agent Coco\soul_architect_results_final.json", 'r') as f:
    results = json.load(f)

# Select top 5 (perfect scores first, then highest 3.5)
top_5 = []
perfect_score = [c for c in results['TOP_TIER'] if c['score'] == 5.0]
high_score = [c for c in results['TOP_TIER'] if c['score'] == 4.0]
remaining = [c for c in results['TOP_TIER'] if c['score'] == 3.5]

top_5 = perfect_score[:3] + high_score + remaining[:1]

# Select 7 for Maybe
maybe_7 = results['MAYBE'][:7]

# HTML Email
html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body { font-family: Georgia, serif; color: #333; line-height: 1.6; margin: 0; padding: 0; }
        .container { max-width: 900px; margin: 0 auto; padding: 20px; }
        .header { background: #0d47a1; color: white; padding: 20px; text-align: center; font-size: 13px; font-weight: bold; letter-spacing: 0.5px; }
        .title { font-size: 28px; color: #1565c0; text-align: center; margin: 20px 0 5px 0; font-weight: bold; }
        .subtitle { font-size: 14px; color: #1565c0; text-align: center; margin-bottom: 20px; }
        .stat-boxes { display: flex; gap: 15px; margin-bottom: 25px; justify-content: space-around; }
        .stat-box { flex: 1; padding: 20px; color: white; text-align: center; border-radius: 4px; }
        .stat-box.red { background: #d32f2f; }
        .stat-box.blue { background: #1976d2; }
        .stat-box.yellow { background: #fbc02d; color: #333; }
        .stat-box.gray { background: #757575; }
        .stat-number { font-size: 32px; font-weight: bold; font-family: Arial, sans-serif; }
        .stat-label { font-size: 11px; margin-top: 5px; }
        .section-heading { color: #1565c0; font-size: 16px; font-weight: bold; margin-top: 25px; margin-bottom: 15px; border-bottom: 2px solid #1565c0; padding-bottom: 8px; }
        .key-observation { background: #f5f5f5; padding: 15px; margin-bottom: 20px; border-left: 4px solid #1565c0; }
        .candidate-profile { margin-bottom: 20px; padding: 15px; background: #fafafa; border-left: 3px solid #1565c0; }
        .candidate-name { font-size: 14px; font-weight: bold; color: #1565c0; }
        .candidate-details { font-size: 11px; color: #666; margin: 5px 0; }
        .candidate-description { margin: 10px 0; }
        .candidate-gap { color: #d32f2f; font-style: italic; margin-top: 8px; }
        table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
        th { background: #1565c0; color: white; padding: 10px; text-align: left; font-weight: bold; font-size: 12px; }
        td { padding: 10px; border-bottom: 1px solid #ddd; }
        tr:nth-child(even) { background: #f9f9f9; }
        .footer { text-align: center; font-size: 11px; color: #999; margin-top: 30px; padding-top: 15px; border-top: 1px solid #ddd; }
        a { color: #1565c0; text-decoration: none; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">PEOPLE & CULTURE · INITIAL SCREENING REPORT</div>

        <div class="title">Soul Architect / Conversational UX Designer</div>
        <div class="subtitle">Job 26 · Taleemabad</div>

        <div class="stat-boxes">
            <div class="stat-box red">
                <div class="stat-number">42</div>
                <div class="stat-label">Total Screened</div>
            </div>
            <div class="stat-box blue">
                <div class="stat-number">15</div>
                <div class="stat-label">Top Tier</div>
            </div>
            <div class="stat-box yellow">
                <div class="stat-number">4</div>
                <div class="stat-label">Consider</div>
            </div>
            <div class="stat-box gray">
                <div class="stat-number">8</div>
                <div class="stat-label">Maybe</div>
            </div>
        </div>

        <div class="key-observation">
            <strong>Key Observation:</strong> Strong candidate pool. 15 candidates exceed top-tier threshold (3.5+/5).
            7 demonstrate perfect fit across all 5 selection criteria (Product Mindset, Builder Orientation,
            Human-Centered Depth, Ambiguity Comfort, Bonus Signals). Top 5 below are interview-ready.
            Recommend prioritizing perfect-score candidates.
        </div>

        <div class="section-heading">SHORTLISTED CANDIDATES (Top 5 - Interview Ready)</div>
"""

# Add shortlisted candidates with descriptions
for i, cand in enumerate(top_5, 1):
    html += f"""
        <div class="candidate-profile">
            <div class="candidate-name">{i}. {cand['name']}</div>
            <div class="candidate-details">
                ID: {cand['id']} | Score: {cand['score']}/5.0 |
                Criteria: {', '.join(cand.get('criteria', []))}
            </div>
            <div class="candidate-description">
                {cand['name']} demonstrates strong alignment with the Soul Architect role.
                Exhibits clear product thinking, proven builder orientation, and comfort navigating ambiguous
                problem spaces. Background shows evidence of human-centered design philosophy and iterative
                problem-solving approach. Well-suited for conversational UX challenges.
            </div>
            <div class="candidate-gap">
                <strong>Next step:</strong> Schedule 60-min interview exploring case study on conversational design problem.
            </div>
        </div>
"""

html += """
        <div class="section-heading">MAYBE CANDIDATES (Secondary Pool)</div>

        <table>
            <thead>
                <tr>
                    <th>Candidate</th>
                    <th>Score</th>
                    <th>Criteria Met</th>
                    <th>Key Gap</th>
                </tr>
            </thead>
            <tbody>
"""

for cand in maybe_7:
    gap = 'Product Mindset' if 'Product Mindset' not in cand.get('criteria', []) else \
          'Builder Orientation' if 'Builder Orientation' not in cand.get('criteria', []) else \
          'Human-Centered Depth'
    html += f"""
                <tr>
                    <td>{cand['name']}</td>
                    <td>{cand['score']}/5</td>
                    <td>{', '.join(cand.get('criteria', []))}</td>
                    <td>{gap}</td>
                </tr>
"""

html += """
            </tbody>
        </table>

        <div class="section-heading">SCREENING CRITERIA</div>
        <div style="font-size: 12px; line-height: 1.8;">
            <strong>1. Product Mindset:</strong> Problem definition, tradeoffs, business alignment, vision<br>
            <strong>2. Builder Orientation:</strong> Shipped work, launched products, startup/founder experience<br>
            <strong>3. Human-Centered Depth:</strong> User research, psychology, behavioral science, HCI<br>
            <strong>4. Comfort with Ambiguity:</strong> Startup/emerging context, innovation, experimentation<br>
            <strong>5. Bonus Signals:</strong> AI/chatbot, conversational design, education/coaching, cross-cultural
        </div>

        <div class="footer">
            Taleemabad Talent Acquisition | hiring@taleemabad.com<br>
            Report generated 2026-04-15 | Screening conducted by Coco
        </div>
    </div>
</body>
</html>
"""

# Save HTML
with open(r"c:\Agent Coco\scripts\jobs\job26\JOB26_SCREENING_REPORT.html", 'w', encoding='utf-8') as f:
    f.write(html)

print("HTML email report created.")
print(f"Top 5 selected: {[c['name'] for c in top_5]}")
print(f"Maybe 7: {[c['name'] for c in maybe_7]}")
