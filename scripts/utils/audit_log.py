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


# Sourcing audit logger (separate log file for talent sourcing operations)
_sourcing_logger = logging.getLogger("coco_sourcing_audit")
_sourcing_logger.setLevel(logging.INFO)
_sourcing_log_file = os.path.join(LOG_DIR, "sourcing_audit.log")

if not _sourcing_logger.handlers:
    _sourcing_fh = logging.FileHandler(_sourcing_log_file, encoding="utf-8")
    _sourcing_fh.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    ))
    _sourcing_logger.addHandler(_sourcing_fh)


def log_sourcing_action(platform: str, query: str, results_found: int, context: str = "unknown"):
    """
    Log a talent sourcing search action.

    Args:
        platform: str - Search platform ("GitHub", "Google", "LinkedIn (Google)", "[Org Name]", etc.)
        query: str - The actual search query or URL used
        results_found: int - Number of candidate results reviewed
        context: str - Search layer context ("org_team_page", "targeted_google", "linkedin_google")

    Logs to: logs/sourcing_audit.log
    """
    _sourcing_logger.info(
        f"SOURCING | platform={platform!r} | query={query!r} | results_found={results_found} | context={context}"
    )
