"""
audit_log.py — Coco Read-Layer Audit Logger
============================================
Logs every Gmail read and DB query — not just email sends.
Import and call from any script that reads external data.

Usage:
    from scripts.utils.audit_log import log_gmail_read, log_db_query
"""

import os
import logging

LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "read_audit.log")

_logger = logging.getLogger("coco_read_audit")
_logger.setLevel(logging.INFO)

if not _logger.handlers:
    _fh = logging.FileHandler(LOG_FILE, encoding="utf-8")
    _fh.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    ))
    _logger.addHandler(_fh)


def log_gmail_read(query: str, message_count: int, context: str = "unknown"):
    """Log a Gmail inbox read operation."""
    _logger.info(
        f"GMAIL_READ | context={context} | query={query!r} | messages_fetched={message_count}"
    )


def log_db_query(table: str, filters: str, rows_returned: int, context: str = "unknown"):
    """Log a Neon DB read query."""
    _logger.info(
        f"DB_READ | context={context} | table={table} | filters={filters!r} | rows={rows_returned}"
    )
