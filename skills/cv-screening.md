# Skill: CV Screening

## Purpose
Screen candidate CVs against a Job Description using structured, evidence-based analysis.
Produce a ranked shortlist with tier decisions, interview questions, and a hiring recommendation.

---

## Core Principles
- Do NOT assume anything not explicitly written in the CV.
- Do NOT infer missing experience — if it is not written, treat it as absent.
- Do NOT assume competence from job titles alone.
- Do NOT reward verbosity — quality of evidence beats quantity of text.
- Do NOT fabricate salary — if missing, state "Expected salary not mentioned."
- Every score must cite exact evidence from the CV.
- Must-have criteria are non-negotiable. Missing one triggers a -15% penalty.
- Process candidates one by one. Never batch or rush.
- If a PDF cannot be parsed, state: "Resume could not be parsed. Text extraction failed."

---

## Prerequisites
- Job Description text (from jobs.jd_text or jobs.description in DB)
- Budget range (from jobs.min_budget / jobs.max_budget — may be NULL)
- Candidate CVs (Base64-decoded PDFs from candidates.resume_data)
- Python with PyPDF2, python-docx, pymupdf (fitz), pytesseract installed
- Tesseract OCR at: C:\Program Files\Tesseract-OCR\tesseract.exe (for scanned PDFs)

---

## STEP 1 — Deconstruct the Job Description

Before reading any CV, extract from the JD:

**Role Mission**
- What core outcome must this person deliver?
- What problem is this role solving?

**6–10 Success Outcomes**
- What must be true in 6–12 months for this hire to be successful?

**3–5 Must-Have Criteria** (non-negotiable — missing one = -15% score penalty)

**3–5 Nice-to-Have Criteria**

**Failure Conditions**
- What would cause someone to fail in this role?

Save this as a structured checklist before reading any CV.

---

## STEP 2 — Parse Each CV

Standard PDF extraction:
```python
import PyPDF2, base64, io

def parse_cv(resume_data_b64):
    raw = base64.b64decode(resume_data_b64)
    reader = PyPDF2.PdfReader(io.BytesIO(raw))
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text
```

Scanned PDF detection: if extracted text < 50 characters → switch to OCR:
```python
import fitz, pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def ocr_pdf(raw_bytes):
    doc = fitz.open(stream=raw_bytes, filetype='pdf')
    text = ""
    for page in doc:
        mat = fitz.Matrix(2.0, 2.0)  # 2x zoom for quality
        pix = page.get_pixmap(matrix=mat)
        img = Image.frombytes('RGB', [pix.width, pix.height], pix.samples)
        text += pytesseract.image_to_string(img, lang='eng')
    return text
```

Flag unreadable CVs in CHAT before sending the report — do not bury in email only.

---

## STEP 3 — Full Experience Extraction (Per Candidate)

For each candidate, before scoring, extract and record:

- **Total years of experience**
- **Relevant years of experience** (matched to JD requirements)
- **Current role and organisation**
- **Past organisations** (full names — spell out abbreviations)
- **Education** (institution, degree, year)
- **Scholarships / distinctions** (explicit only)
- **Expected salary** (from marker field only — NEVER infer)

Compare all extracted experience directly against must-have and nice-to-have criteria.
Only count skills and experience that are **explicitly written** — do not assume from titles.

---

## STEP 4 — Organisation Signal Analysis

After extracting experience, flag any high-signal organisations. These are strategic signals —
they do NOT automatically raise the score, but they should be explicitly called out in the report.

### A. Competitor / EdTech / Startup Signal 🎓
- The Citizens Foundation (TCF)
- READ Foundation
- Teach For Pakistan
- Taleem / Tele-Taleem / EdTech startups
- Education-focused startups or high-growth startup environments

### B. Impact / Research / Data Signal 📊
- CERP (Centre for Economic Research in Pakistan)
- World Bank
- Research institutions / impact evaluation orgs
- Data-heavy organisations or policy think tanks

### C. International / Donor / Development Signal 🌐
- United Nations (UN) agencies — UNICEF, UNDP, UN Women, UNFPA, etc.
- FCDO (Foreign, Commonwealth & Development Office)
- USAID (United States Agency for International Development)
- GIZ (German Agency for International Cooperation)
- Other bilateral/multilateral donors

### D. Scholarship / Academic Excellence Signal 🏆
- Erasmus scholarship
- Chevening scholarship
- Fulbright scholarship
- Other major international merit-based scholarships

**Mark qualifying organisations as: "High Strategic Signal"**

---

## STEP 5 — CV Quality & Intent Signal

Evaluate the CV itself as a signal of the candidate's professionalism and effort:

| Rating | Criteria |
|---|---|
| **High effort** | Quantified achievements, role-specific tailoring, clear narrative arc, strong storytelling |
| **Moderate effort** | Some quantification, partially tailored, readable structure, impact not consistently articulated |
| **Low effort** | Generic language, no quantification, responsibilities listed without outcomes, poor structure |

Provide a 2–3 line justification for the rating. This does not affect the numerical score but
is included in the report to help the hiring manager calibrate confidence.

---

## STEP 6 — Score Each Candidate Across 7 Dimensions

Score each dimension **0–4**:

| Score | Meaning |
|---|---|
| 0 | Missing — no evidence |
| 1 | Weak / Adjacent — related but not the same |
| 2 | Partial Match — some evidence, gaps present |
| 3 | Strong Match — clear evidence, good fit |
| 4 | Exceptional — clear evidence with measurable impact |

**Evidence Rule (mandatory):**
- Cite exact text from the CV for every score.
- Label each piece of evidence as FACT (written in CV) or INFERENCE (logical deduction).
- If responsibilities are listed without outcomes → reduce score by one level.
- If a must-have is completely missing → apply automatic -15% penalty to final total.

### Dimension 1 — Functional Match (25%)
Does the candidate directly perform the core responsibilities of this role?
- Same scope, ownership, and complexity?
- Not just adjacent or supporting work — direct ownership.

### Dimension 2 — Demonstrated Outcomes (20%)
Quantified results only: revenue generated, grants won, budgets managed, growth numbers, systems built.
- If no measurable outcomes are cited anywhere in the CV → cap this dimension at score 2.

### Dimension 3 — Environment Fit (15%)
- Similar industry, geography, organisational constraints, and pace?
- For Taleemabad roles: Pakistani development sector, EdTech, NGO, or donor-funded orgs score highest.
- Location: Islamabad-based or explicitly willing to relocate = acceptable.
- Deal-breaker: Not Islamabad-based AND not willing to relocate.

### Dimension 4 — Ownership & Execution (15%)
Did the candidate actually build, lead, close, or drive outcomes — or just participate?
- Built a function from scratch → high score
- Led and closed deals/grants independently → high score
- Was part of a team that did those things, role unclear → lower score

### Dimension 5 — Stakeholder & Communication Strength (10%)
- Executive exposure (C-suite, ministry, donor principal)?
- Direct client/donor/government relationships?
- Cross-functional or cross-organisational leadership?

### Dimension 6 — Hard Skills / Technical Match (10%)
- Tools, certifications, required platforms?
- For fundraising roles: specific donor relationships, grant systems, proposal frameworks.
- For technical roles: exact software/language proficiency.

### Dimension 7 — Growth & Leadership Potential (5%)
- Increasing scope of responsibility over career?
- Team leadership or mentoring?
- Strategic involvement beyond execution?

### Score Calculation
```
raw_score = (D1 × 0.25) + (D2 × 0.20) + (D3 × 0.15) + (D4 × 0.15)
          + (D5 × 0.10) + (D6 × 0.10) + (D7 × 0.05)

# Each dimension is 0–4, max raw = 4.0
# Normalise to 0–100:
normalised = (raw_score / 4.0) × 100

# Apply must-have penalty (per missing must-have):
final_score = normalised × (0.85 ^ missing_musthaves)
```

---

## STEP 7 — Compensation Feasibility (Separate from Skill Ranking)

Assess independently — do NOT let this affect the skill score above.

- Salary desired (from marker field only — never infer) vs. role budget range
- Budget fit labels:
  - **In Budget**: salary ≤ max_budget
  - **Out of Budget**: salary > max_budget → flag for hiring manager, specify exact gap
  - **Missing**: salary not provided → note as "Expected salary not mentioned"
  - **Budget Not Set**: jobs.max_budget is NULL → screen on JD/experience/skills only, note "budget TBD"

Strong candidates who are over budget must be flagged separately. Never exclude silently.

---

## STEP 8 — Decision Tier

| Score | Tier | Action |
|---|---|---|
| 85–100 | **Tier A** | Strong Move Forward — interview immediately |
| 70–84 | **Tier B** | Interview with focused validation on gaps |
| 55–69 | **Tier C** | Risky / Backup — proceed only if pool is thin |
| < 55 | **No-Hire** | Do not shortlist |

---

## STEP 9 — Shortlist Size Rules

| Pool size | Shortlist |
|---|---|
| 20–40 applications | Top 7–10 |
| 50–100 applications | Top 15–20 |
| 100–200 applications | Top 25–30 |
| < 20 applications | All viable candidates |

Rank by final score → then by must-have strength → then by budget compatibility.

---

## STEP 10 — Output Per Shortlisted Candidate (Strict Structure)

For each shortlisted candidate provide:

1. **Candidate Name**
2. **Budget Status**: In Budget / Out of Budget (state expected salary vs budget ceiling; "Exceeds budget by PKR X")
3. **Total Experience** (years)
4. **Relevant Experience** (years, matched to JD)
5. **Current Role**
6. **Key Strengths** (bullet points — evidence-based, cite CV)
7. **Unique Value Proposition (USP)** — what makes this candidate distinctively valuable
8. **Strategic Signal** — note any High Strategic Signal organisations or scholarships
9. **Missing Areas / Grey Areas** — specific gaps against JD only; no assumptions
10. **CV Quality Rating** — High / Moderate / Low effort + 2-line justification
11. **5 Interview Questions** — targeted to validate gaps or unverified claims
12. **Confidence Level** — High / Medium / Low (based on CV completeness and specificity)

---

## STEP 11 — Report Structure (7 Sections)

### Section 1: Screening Summary
- Total Profiles Reviewed
- Role
- Budget Range
- Recommended Shortlist Size
- Overall Talent Quality Assessment (brief paragraph)

### Section 2: JD Scorecard
Present as a collapsible section. Include:

**Must-Have Criteria**
| Requirement | Candidate Match % | Evidence from CV |

**Nice-to-Have Criteria**
| Requirement | Candidate Match % | Evidence from CV |

Overall JD Match Score: XX% at bottom.

### Section 3: Ranked Shortlist
Full profiles per STEP 10 above, ranked by final score.

### Section 4: Deep Comparative Analysis — Top 3 Strongest
Side-by-side comparison table covering:
- Experience depth
- Organisation quality
- Strategic signal
- Budget comparison
- Long-term leadership potential
- Risk factors

If a top-3 candidate is out of budget, assess whether they fit a more senior role and recommend
appropriate level (e.g., Manager vs Senior Manager vs Head).

### Section 5: Strong Match but Out of Budget
For each over-budget strong match:
- Expected salary
- Budget difference
- Justification for whether the budget stretch is worth it

### Section 6: Visual Analytics
Generate exactly 3 charts — email-safe (HTML tables only, no SVG, no flexbox):
1. **Heatmap** — Candidate vs JD criteria match (table with coloured cells per dimension)
2. **Bar Chart** — Overall score comparison for shortlisted candidates (nested table bars)
3. **Spider / Radar equivalent** — Top 3 skill depth comparison (star-grid comparison table)

### Section 7: Why Others Did Not Make It
Group rejected candidates by reason:
- Insufficient relevant experience
- No direct JD match
- Junior profile vs required seniority
- No impact ownership
- No evidence of required technical skills

Be respectful and empathetic. Do not use dismissive language.

---

## STEP 12 — Send Report

See skills/email-notification.md. Send only to the hiring manager on record (users table,
via jobs.hiring_manager FK). Default recipient: ayesha.khan@taleemabad.com unless instructed otherwise.

---

## Common Mistakes to Avoid
- Never screen out over-budget strong matches — flag them separately
- Never assume salary from title or years of experience — state "not mentioned" if absent
- Never confuse activity with achievement (doing vs. delivering)
- Never inflate scores for high-signal organisation names without proof of individual impact
- Never use SVG or CSS flexbox in email HTML — use table-based charts only
- Always flag unreadable CVs in chat BEFORE sending the report
- Always read the JD fully before reading any CV
- Never infer skills from adjacent roles — if not written, treat as missing
- Never batch-process candidates — score one at a time
