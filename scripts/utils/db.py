"""One way for a script to reach the Neon database: DATABASE_URL from .env.

Seventy-odd scripts used to carry the owner password inline, which put the
production credential in every clone of the repo. Never write a host, user or
password into a script again; call connect() instead.
"""

from __future__ import annotations

import os
from pathlib import Path


def database_url() -> str:
    try:
        from dotenv import load_dotenv

        load_dotenv(Path(__file__).resolve().parents[2] / ".env")
    except ImportError:
        pass
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise RuntimeError(
            "DATABASE_URL is not set. Copy .env.example to .env and fill in your "
            "own Neon connection string."
        )
    return url


def connect():
    import psycopg2

    return psycopg2.connect(database_url())
