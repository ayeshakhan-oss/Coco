"""Database engine / session setup for the web service.

The web service connects DIRECTLY to Neon via DATABASE_URL (the MCP server is
only for the Claude Code agent, not this app). Use the POOLED Neon endpoint
(`-pooler` host, PgBouncer transaction mode): we therefore disable server-side
prepared statements, which PgBouncer transaction pooling does not support.

The engine is created lazily so the app can boot and serve /healthz even before
DATABASE_URL is configured.
"""

from __future__ import annotations

from typing import Iterator, Optional

from sqlalchemy import create_engine, event, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from .config import get_settings

Base = declarative_base()

_engine: Optional[Engine] = None
_SessionLocal: Optional[sessionmaker] = None


def _normalize_url(url: str) -> str:
    """Force the SQLAlchemy psycopg (v3) driver, which has Python 3.14 wheels."""
    if url.startswith("postgresql+"):
        return url
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+psycopg://", 1)
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql+psycopg://", 1)
    return url


def get_engine() -> Engine:
    global _engine, _SessionLocal
    if _engine is None:
        settings = get_settings()
        if not settings.database_url:
            raise RuntimeError(
                "DATABASE_URL is not set. Configure the pooled Neon connection string."
            )
        _engine = create_engine(
            _normalize_url(settings.database_url),
            pool_pre_ping=True,
            pool_recycle=300,
            pool_size=5,
            max_overflow=5,
            future=True,
        )

        @event.listens_for(_engine, "connect")
        def _disable_prepared_statements(dbapi_conn, conn_record):  # noqa: ANN001
            # PgBouncer transaction mode (Neon pooled endpoint) cannot reuse
            # server-side prepared statements across pooled connections.
            try:
                dbapi_conn.prepare_threshold = None
            except Exception:
                pass

        _SessionLocal = sessionmaker(
            bind=_engine, autoflush=False, autocommit=False, future=True
        )
    return _engine


def get_sessionmaker() -> sessionmaker:
    if _SessionLocal is None:
        get_engine()
    assert _SessionLocal is not None
    return _SessionLocal


def get_db() -> Iterator[Session]:
    """FastAPI dependency: yields a per-request session and always closes it."""
    SessionLocal = get_sessionmaker()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_db() -> bool:
    """Lightweight readiness probe — returns True if SELECT 1 succeeds."""
    try:
        engine = get_engine()
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception:
        return False
