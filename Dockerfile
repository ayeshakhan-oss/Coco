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

# Backend dependencies (the reused scripts/* modules are stdlib-only).
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

# Tone master file used as the drafting system prompt.
COPY memory/CANDIDATE_COMMUNICATION_TONE_PHILOSOPHY_LOCKED.md memory/CANDIDATE_COMMUNICATION_TONE_PHILOSOPHY_LOCKED.md

# Built SPA from stage 1.
COPY --from=frontend /app/frontend/dist frontend/dist

RUN mkdir -p logs

EXPOSE 8000
# Run the migration in the start command (where Railway injects runtime env vars,
# unlike the pre-deploy hook) then start the server. Single worker: the send
# pipeline serializes on an in-process lock (safe_send.ALLOWED_EXTERNAL global).
CMD ["sh", "-c", "alembic upgrade head && uvicorn webapp.main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 1"]
