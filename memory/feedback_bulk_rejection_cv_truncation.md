---
name: Bulk Rejection Email — CV Truncation Rules
description: Sehrish Irfan pushed back after her rejection email missed 6 years of experience due to CV being truncated at 4,500 chars. Rules for all future bulk generation.
type: feedback
---

Never use `cv_text[:4500]` in bulk rejection generation prompts. Minimum 10,000 chars.

**Why:** Sehrish Irfan (Job 35, app 1514) replied correcting factual errors in her rejection email — it missed her SPSS usage, Python/SQL/Power BI training, econometrics coursework, and 6 years of experience because her 14,147-char CV was truncated at 4,500. The model only saw her 3 most recent projects.

**How to apply:**
1. CV truncation: always use `cv_text[:10000]` minimum in generation prompts
2. Flag CVs >8,000 chars with a logged warning before generation
3. Add to system prompt: "Before suggesting the candidate develop any skill or take any course, verify it is not already present in the CV text provided."
4. Post-generation: if CV >8k chars but generated email <900 words, flag for manual review before including in pilot PDF
5. Candidate reply protocol: if a candidate pushes back with factual corrections, Ayesha replies personally — Coco drafts, Ayesha sends from her own voice
