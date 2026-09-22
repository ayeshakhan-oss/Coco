# syntax=docker/dockerfile:1
# Coco — single-service image: FastAPI backend that also serves the built React SPA.

# ---- Stage 1: build the React frontend ----
FROM node:22-slim AS frontend
WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm ci || npm install
COPY frontend/ ./
RUN npm run build

# ---- Stage 2: Python runtime ----
FROM python:3.13-slim
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app
WORKDIR /app

# Backend dependencies. NOTE: the reused scripts/utils/* send + layout helpers
# are stdlib-only, but scripts/evals/fetch_submission_corpora.py (case-study
# extraction, reused below) needs python-docx, python-pptx, openpyxl and
# PyMuPDF -- see webapp/requirements.txt.
COPY webapp/requirements.txt webapp/requirements.txt
RUN pip install --no-cache-dir -r webapp/requirements.txt

# App code.
COPY webapp/ webapp/
COPY alembic/ alembic/
COPY alembic.ini alembic.ini
COPY assets/ assets/

# ONLY the clean, reused scripts modules (NOT the 84 files with the old DB
# password — those never enter the image).
COPY scripts/__init__.py scripts/__init__.py
COPY scripts/utils/__init__.py scripts/utils/__init__.py
COPY scripts/utils/v8_template.py scripts/utils/v8_template.py
COPY scripts/utils/safe_send.py scripts/utils/safe_send.py
COPY scripts/utils/feedback_widget.py scripts/utils/feedback_widget.py
COPY scripts/evals/__init__.py scripts/evals/__init__.py
COPY scripts/evals/candidate_communication_eval.py scripts/evals/candidate_communication_eval.py
COPY scripts/evals/fetch_submission_corpora.py scripts/evals/fetch_submission_corpora.py

# Tone master file used as the drafting system prompt.
COPY memory/CANDIDATE_COMMUNICATION_TONE_PHILOSOPHY_LOCKED.md memory/CANDIDATE_COMMUNICATION_TONE_PHILOSOPHY_LOCKED.md

# The per-type SOPs. Until 2026-09-14 the image shipped ONLY the tone master
# above, so the live drafter had 2,774 words of guidance and had never read the
# other 17,366 that define how each letter is actually written: the specific
# interview moment, company vulnerability, timestamps, the P.S., the subject
# line. Editing a skill file changed nothing in production. Now it does.
COPY .claude/skills/01_candidate-communication/ .claude/skills/01_candidate-communication/
COPY .claude/skills/02_candidate-evaluation/ .claude/skills/02_candidate-evaluation/
COPY memory/warm_bench_final_locked_approach.md memory/warm_bench_final_locked_approach.md
COPY memory/gwc_rejection_locked_approach_2026_06_08.md memory/gwc_rejection_locked_approach_2026_06_08.md
COPY memory/v8_candidate_comms_layout_LOCKED.md memory/v8_candidate_comms_layout_LOCKED.md
COPY memory/feedback_email_rules.md memory/feedback_email_rules.md

# Built SPA from stage 1.
COPY --from=frontend /app/frontend/dist frontend/dist

RUN mkdir -p logs

EXPOSE 8000
# Just run the server. DB migrations are a SEPARATE, deliberate step (run
# `alembic upgrade head` manually / via a one-off command), not on every boot —
# running them on startup couples boot to DB locks and caused healthcheck hangs.
# Single worker: the send pipeline serializes on an in-process lock
# (safe_send.ALLOWED_EXTERNAL is a process-global set).
CMD ["sh", "-c", "uvicorn webapp.main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 1"]
