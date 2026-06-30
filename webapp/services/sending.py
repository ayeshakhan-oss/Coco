"""Send pipeline + pluggable transport.

Safety properties:
- AUTHORITATIVE gate: the email is re-rendered from stored content and re-run
  through evaluate_email() at send time; a HARD-BLOCK aborts the send (the
  client's pass/fail is never trusted).
- PILOT = ayesha.khan@taleemabad.com ONLY, no CC. LIVE = candidate (To) +
  hiring@ + ayesha (Cc). The [PILOT - name] subject prefix is applied only for
  pilot sends and never persisted.
- Sends are serialized behind a lock because safe_send.ALLOWED_EXTERNAL is a
  process-global set (avoids a candidate address leaking across requests).

Transports: SmtpTransport (real, via the safe_send bouncer) and CaptureTransport
(records, does not send) for tests. get_transport() refuses if EMAIL_PASSWORD is
unset, so a misconfigured deploy cannot silently no-op.
"""

from __future__ import annotations

import logging
import smtplib
import threading
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import make_msgid
from typing import Optional, Protocol

from ..config import get_settings
from ..reuse import allow_candidate_addresses, attach_logo, evaluate_email, safe_sendmail
from . import rendering

log = logging.getLogger("webapp.sending")

_send_lock = threading.Lock()

PILOT_RECIPIENT = "ayesha.khan@taleemabad.com"
LIVE_CC = ["hiring@taleemabad.com", "ayesha.khan@taleemabad.com"]

# Test hook: set to a Transport instance to bypass real SMTP.
_transport_override: Optional["Transport"] = None


class SendBlocked(Exception):
    def __init__(self, violations: list[dict]):
        self.violations = violations
        super().__init__("Send blocked by HARD-BLOCK validation")


class SendNotConfigured(Exception):
    pass


class Transport(Protocol):
    def send(self, *, sender: str, recipients: list[str], message: str, context: str) -> None: ...


class SmtpTransport:
    def __init__(self, host: str, port: int, sender: str, password: str):
        self.host, self.port, self.sender, self.password = host, port, sender, password

    def _connect(self) -> smtplib.SMTP:
        """Connect over IPv4 explicitly. Railway containers frequently have no
        IPv6 route, so resolving smtp.gmail.com to its AAAA (IPv6) record yields
        "[Errno 101] Network is unreachable". We pin the A (IPv4) record, then
        validate STARTTLS against the real hostname (not the IP literal). Falls
        back to the default resolver if the IPv4 lookup itself fails."""
        import socket

        try:
            ipv4 = socket.getaddrinfo(
                self.host, self.port, socket.AF_INET, socket.SOCK_STREAM
            )[0][4][0]
        except OSError:
            return smtplib.SMTP(self.host, self.port, timeout=30)
        server = smtplib.SMTP(timeout=30)
        server.connect(ipv4, self.port)
        server._host = self.host  # STARTTLS uses this for SNI + cert hostname check
        return server

    def send(self, *, sender, recipients, message, context):
        import ssl

        server = self._connect()
        try:
            server.ehlo()
            server.starttls(context=ssl.create_default_context())
            server.ehlo()
            server.login(self.sender, self.password)
            safe_sendmail(server, sender, recipients, message, context=context)
        finally:
            try:
                server.quit()
            except Exception:
                pass


class CaptureTransport:
    """Records sends without delivering — for tests/dry runs."""

    def __init__(self):
        self.sent: list[dict] = []

    def send(self, *, sender, recipients, message, context):
        self.sent.append(
            {"sender": sender, "recipients": list(recipients), "context": context, "bytes": len(message)}
        )


def get_transport() -> Transport:
    if _transport_override is not None:
        return _transport_override
    s = get_settings()
    if not s.email_password:
        raise SendNotConfigured("EMAIL_PASSWORD not configured — sending is disabled")
    return SmtpTransport(s.smtp_host, s.smtp_port, s.email_sender, s.email_password)


def resolve_recipients(mode: str, candidate_email: Optional[str]) -> tuple[list[str], list[str], list[str]]:
    """Returns (to, all_recipients, cc)."""
    if mode == "pilot":
        return [PILOT_RECIPIENT], [PILOT_RECIPIENT], []
    if not candidate_email:
        raise ValueError("Live send requires a candidate email")
    to = [candidate_email]
    cc = list(LIVE_CC)
    return to, to + cc, cc


def build_subject(mode: str, title_line: str, first_name: str) -> str:
    if mode == "pilot":
        return f"[PILOT - {first_name}] {title_line}"
    return title_line


def _build_message(*, full_html: str, subject: str, sender: str, to: list[str], cc: list[str]):
    msg = MIMEMultipart("related")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = ", ".join(to)
    if cc:
        msg["Cc"] = ", ".join(cc)
    message_id = make_msgid(domain="taleemabad.com")
    msg["Message-ID"] = message_id
    alt = MIMEMultipart("alternative")
    alt.attach(MIMEText(full_html, "html"))
    msg.attach(alt)
    attach_logo(msg)
    return msg, message_id


def send_communication(
    comm,
    *,
    mode: str,
    first_name: str,
    candidate_email: Optional[str],
    transport: Optional[Transport] = None,
) -> dict:
    """Gate + build + send. Returns the resolved recipients / subject / message_id
    / eval result. Does NOT touch the DB — the caller persists the transition."""
    settings = get_settings()
    role = comm.role_title or "the role"

    full_html = rendering.wrap_full(
        comm.body_html or "", title_line=comm.title_line or "", role=role, email_type=comm.email_type
    )
    subject = build_subject(mode, comm.title_line or "", first_name)
    pilot = mode == "pilot"

    # Authoritative gate.
    result = evaluate_email(full_html, subject, comm.email_type, pilot_mode=pilot)
    if any(v["severity"] == "HARD_BLOCK" for v in result["violations"]):
        raise SendBlocked(result["violations"])

    to, all_recipients, cc = resolve_recipients(mode, candidate_email)
    msg, message_id = _build_message(
        full_html=full_html, subject=subject, sender=settings.email_sender, to=to, cc=cc
    )

    tx = transport or get_transport()
    with _send_lock:
        if mode == "live":
            allow_candidate_addresses([candidate_email])
        tx.send(
            sender=settings.email_sender,
            recipients=all_recipients,
            message=msg.as_string(),
            context=f"{comm.email_type}_{comm.candidate_id}_{mode}",
        )

    return {
        "mode": mode,
        "subject": subject,
        "recipients": all_recipients,
        "message_id": message_id,
        "full_html": full_html,
        "eval": result,
    }
