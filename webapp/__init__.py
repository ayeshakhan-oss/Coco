"""Coco — Candidate Communication web app (FastAPI backend).

This package wraps and reuses the existing, locked Python logic under scripts/
(v8 email layout, the candidate-communication validation harness, and the
safe_send bouncer). It never reimplements them. See webapp/reuse.py.
"""

__version__ = "0.1.0"
