"""
safe_send.py — Coco Email Security Bouncer
==========================================
ALL email sending in Coco must go through safe_sendmail().
Raw smtplib.sendmail() must never be called directly.

The bouncer:
  1. Checks every recipient against the ALLOWED_DOMAINS + ALLOWED_ADDRESSES allowlist
  2. Hard-blocks (raises exception) if any unapproved address is found
  3. Logs every send attempt to logs/email_audit.log — approved or blocked

Rule 2 fix — set by user 2026-03-30.
"""

import os
import smtplib
import logging
from datetime import datetime

# ── ALLOWLIST ─────────────────────────────────────────────────────────────────
# Approved domains — any address @these domains is allowed
ALLOWED_DOMAINS = {
    "taleemabad.com",
    "niete.edu.pk",
}

# Approved external addresses — specific non-Taleemabad addresses allowed
# (candidates, hiring managers at partner orgs, etc.)
# This list is extended at runtime when sending to candidates — see note below.
ALLOWED_EXTERNAL = set()

# ── LOGGING SETUP ─────────────────────────────────────────────────────────────
LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "email_audit.log")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def _extract_email(addr: str) -> str:
    """Extract plain email from 'Name <email>' format."""
    addr = addr.strip()
    if "<" in addr and ">" in addr:
        return addr.split("<")[1].split(">")[0].strip().lower()
    return addr.lower()


def _is_allowed(addr: str) -> bool:
    """Return True if address is in allowed domains or explicit allowlist."""
    email = _extract_email(addr)
    domain = email.split("@")[-1] if "@" in email else ""
    return domain in ALLOWED_DOMAINS or email in ALLOWED_EXTERNAL


def allow_candidate_addresses(addresses: list):
    """
    Temporarily allow candidate email addresses for the current send operation.
    Call this before safe_sendmail() when sending to candidates.
    """
    for addr in addresses:
        ALLOWED_EXTERNAL.add(_extract_email(addr))


def safe_sendmail(
    smtp_server: smtplib.SMTP,
    sender: str,
    recipients: list,
    message: str,
    context: str = "unknown",
):
    """
    Drop-in replacement for smtp.sendmail().
    Raises SecurityError if any recipient is not on the allowlist.
    Logs all attempts.

    Args:
        smtp_server: authenticated smtplib.SMTP instance
        sender:      from address string
        recipients:  list of to/cc/bcc addresses
        message:     raw email message string
        context:     human-readable label for the log (e.g. 'job36_rejection')
    """
    blocked = [r for r in recipients if not _is_allowed(r)]

    if blocked:
        log_msg = (
            f"BLOCKED | context={context} | sender={sender} | "
            f"blocked_recipients={blocked} | all_recipients={recipients}"
        )
        logging.warning(log_msg)
        raise SecurityError(
            f"\n\nSEND BLOCKED -- unapproved recipient(s) detected:\n"
            f"   {blocked}\n\n"
            f"   Only @taleemabad.com, @niete.edu.pk, and explicitly approved\n"
            f"   candidate addresses are allowed.\n"
            f"   To send to an external address, call allow_candidate_addresses([...]) first."
        )

    # All clear — send
    smtp_server.sendmail(sender, recipients, message)

    log_msg = (
        f"SENT | context={context} | sender={sender} | "
        f"recipients={recipients}"
    )
    logging.info(log_msg)
    print(f"[safe_send] SENT | {context} -> {recipients}")


class SecurityError(Exception):
    """Raised when a send is blocked due to unapproved recipient."""
    pass
