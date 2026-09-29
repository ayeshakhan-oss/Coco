"""Reading an offer letter thread: what was agreed, and where it says so.

Feeds the contract page so Ayesha does not retype a salary or a start date.
Every value comes back with the message it came from, and nothing is treated
as settled.

🔴 READ THE THREAD TO THE END. CLAUDE.md Rule 19, from a real case: Mariam and
   Hafiza both COUNTERED their offers, and the agreed figure was not the one
   in the first offer letter. So this orders messages oldest-first, reports
   the LATEST figure, and raises a conflict whenever an earlier message said
   something different. A function that returned "the salary" from the first
   match would have been wrong for two of the last handful of hires.

🔴 NOTHING HERE DECIDES. It proposes, with provenance, and the page keeps
   every box editable. An extracted figure that nobody looked at is worse than
   an empty box, because an empty box cannot be wrong quietly.

⚠️ OFFER EMAILS DO NOT SAY "OFFER". The real subject for one of them is
   "Congratulations Mariam on Your Selection as a Coach for the NIETE
   Project!". Searching by subject keyword misses them, so the search is by
   the candidate's address and the filtering is on content.
"""

from __future__ import annotations

import datetime as dt
import re
from typing import Optional

# --------------------------------------------------------------------------
# Money
# --------------------------------------------------------------------------

#: A currency amount as these letters actually write it: "PKR 150,000",
#: "Rs. 150,000/-", "150,000 PKR". The currency marker is required, because a
#: bare "150,000" in a sentence about beneficiaries reached is not a salary.
_AMOUNT = re.compile(
    r"(?:(?P<pre>PKR|Rs\.?|RS\.?|rupees)\s*(?P<a>\d[\d,]{2,})"
    r"|(?P<b>\d[\d,]{2,})\s*(?P<post>PKR|Rs\.?|rupees))",
    re.I,
)

#: What the amount is FOR, looked for in the words just before it.
_LABELS = (
    ("total", re.compile(r"total\s+earning|total\s+salary|total\s+compensation|gross\s+salary|gross\s+pay|total(?=\s*[:=])", re.I)),
    ("base", re.compile(r"\bbasic\b|\bbase\s+salary\b|\bbasic\s+salary\b", re.I)),
    ("medical", re.compile(r"medical", re.I)),
    ("other", re.compile(r"\bother(s)?\s+allowance|\bothers?\b\s*[:=]", re.I)),
    ("stipend", re.compile(r"stipend|honorarium", re.I)),
)

#: Words that mean this number is NOT pay.
_NOT_PAY = re.compile(
    r"budget|revenue|fund(ing|raising)|donation|grant|invoice|reimburse|"
    r"beneficiar|student|school|enrol|target",
    re.I,
)


def _clean_amount(raw: str) -> Optional[int]:
    digits = raw.replace(",", "").strip()
    if not digits.isdigit():
        return None
    value = int(digits)
    # A salary in PKR below a thousand is a typo or a page number, and above
    # ten million is not a salary in this organisation.
    return value if 1_000 <= value <= 10_000_000 else None


def find_amounts(text: str) -> list[dict]:
    """Every currency amount in a body, with what it seems to be for."""
    out: list[dict] = []
    for m in _AMOUNT.finditer(text or ""):
        raw = m.group("a") or m.group("b")
        value = _clean_amount(raw)
        if value is None:
            continue
        # 🔴 THE LABEL COMES FROM THIS LINE ONLY. A payslip breakdown puts
        # four amounts on four consecutive lines, and a lookback window that
        # crosses a newline reads "Base Salary" from the line above and labels
        # the Others figure as base. It did exactly that.
        line_start = text.rfind(chr(10), 0, m.start()) + 1
        line_window = text[line_start: m.start()]
        # "Not pay" is a property of the sentence, not the line, so it keeps
        # a wider view: "the project budget is" may sit before a line break.
        if _NOT_PAY.search(text[max(0, m.start() - 90): m.start()]):
            continue
        label = "unknown"
        best = -1
        for name, pattern in _LABELS:
            found = None
            for hit in pattern.finditer(line_window):
                found = hit
            # Closest label to the amount wins, not the first one declared.
            if found and found.end() > best:
                best, label = found.end(), name
        out.append({
            "label": label,
            "amount": value,
            "text": f"PKR {value:,}",
            "context": " ".join(
                text[max(0, m.start() - 70): m.end() + 30].split()
            ),
        })
    return out


# --------------------------------------------------------------------------
# Dates
# --------------------------------------------------------------------------

_MONTHS = {m.lower(): i for i, m in enumerate(
    ["January", "February", "March", "April", "May", "June", "July",
     "August", "September", "October", "November", "December"], start=1)}
for _full, _i in list(_MONTHS.items()):
    _MONTHS[_full[:3]] = _i

_DAY_MONTH_YEAR = re.compile(
    r"\b(\d{1,2})\s*(?:st|nd|rd|th)?\s+([A-Za-z]{3,9})\.?,?\s+(\d{4})\b")
_MONTH_DAY_YEAR = re.compile(
    r"\b([A-Za-z]{3,9})\.?\s+(\d{1,2})\s*(?:st|nd|rd|th)?,?\s+(\d{4})\b")
_ISO = re.compile(r"\b(\d{4})-(\d{2})-(\d{2})\b")

_START_WORDS = re.compile(
    r"start|commenc|join|effective|begin|from|onboard|first\s+day", re.I)
_END_WORDS = re.compile(r"\bend|until|till|through|expire|conclude|last\s+day", re.I)


def _as_date(day: int, month: int, year: int) -> Optional[dt.date]:
    try:
        d = dt.date(year, month, day)
    except ValueError:
        return None
    # A contract date far outside a plausible window is a misparse.
    return d if 2020 <= d.year <= 2035 else None


def find_dates(text: str) -> list[dict]:
    """Every date in a body, with whether it reads like a start or an end."""
    body = text or ""
    found: list[tuple[int, dt.date, str]] = []

    for m in _DAY_MONTH_YEAR.finditer(body):
        month = _MONTHS.get(m.group(2).lower())
        if month:
            d = _as_date(int(m.group(1)), month, int(m.group(3)))
            if d:
                found.append((m.start(), d, m.group(0)))
    for m in _MONTH_DAY_YEAR.finditer(body):
        month = _MONTHS.get(m.group(1).lower())
        if month:
            d = _as_date(int(m.group(2)), month, int(m.group(3)))
            if d:
                found.append((m.start(), d, m.group(0)))
    for m in _ISO.finditer(body):
        d = _as_date(int(m.group(3)), int(m.group(2)), int(m.group(1)))
        if d:
            found.append((m.start(), d, m.group(0)))

    out = []
    seen: set[tuple[int, dt.date]] = set()
    for at, d, raw in sorted(found):
        if (at, d) in seen:
            continue
        seen.add((at, d))
        window = body[max(0, at - 80): at]
        kind = "unknown"
        if _END_WORDS.search(window):
            kind = "end"
        elif _START_WORDS.search(window):
            kind = "start"
        out.append({
            "kind": kind,
            "date": d.isoformat(),
            "pretty": f"{d.day} {d.strftime('%B')} {d.year}",
            "raw": raw,
            "context": " ".join(body[max(0, at - 70): at + len(raw) + 30].split()),
        })
    return out


# --------------------------------------------------------------------------
# A whole thread
# --------------------------------------------------------------------------

#: A later message from the candidate that reads like a negotiation.
_COUNTER = re.compile(
    r"counter|negotiat|revise|revisit|reconsider|increase|higher|"
    r"expectation|would it be possible|hoping for|a bit more", re.I)


def read_thread(messages: list[dict]) -> dict:
    """What the thread settles on, and everything that disagrees with it.

    `messages` is oldest-first: {from_me, date, subject, body}. `from_me` is
    True when Taleemabad sent it.
    """
    ordered = sorted(messages or [], key=lambda m: m.get("date") or "")
    money: list[dict] = []
    dates: list[dict] = []
    counters: list[dict] = []

    for m in ordered:
        body = m.get("body") or ""
        source = {
            "subject": m.get("subject") or "",
            "date": m.get("date") or "",
            "from_us": bool(m.get("from_me")),
        }
        for a in find_amounts(body):
            money.append({**a, "source": source})
        for d in find_dates(body):
            dates.append({**d, "source": source})
        if not m.get("from_me") and _COUNTER.search(body):
            counters.append({
                "subject": source["subject"],
                "date": source["date"],
                "quote": " ".join(body.split())[:220],
            })

    def latest(items, pick):
        chosen = [i for i in items if pick(i)]
        return chosen[-1] if chosen else None

    proposed = {
        "total": latest(money, lambda i: i["label"] == "total"),
        "base": latest(money, lambda i: i["label"] == "base"),
        "medical": latest(money, lambda i: i["label"] == "medical"),
        "other": latest(money, lambda i: i["label"] == "other"),
        "stipend": latest(money, lambda i: i["label"] == "stipend"),
        "start_date": latest(dates, lambda i: i["kind"] == "start"),
        "end_date": latest(dates, lambda i: i["kind"] == "end"),
    }
    # An unlabelled amount is still worth offering when nothing else was found.
    if not proposed["total"] and not proposed["stipend"]:
        proposed["total"] = latest(money, lambda i: i["label"] == "unknown")

    warnings: list[str] = []
    for key in ("total", "base", "medical", "other", "stipend"):
        values = {i["amount"] for i in money if i["label"] == key}
        if len(values) > 1:
            warnings.append(
                f"The thread names more than one {key} figure "
                f"({', '.join('PKR {:,}'.format(v) for v in sorted(values))}). "
                "The latest is shown. Check which one was agreed."
            )

    # 🔴 A DIVERGENT UNLABELLED FIGURE COUNTS TOO. On Mariam's real thread the
    #    only figure carrying the word "total" was the FIRST offer, 116,000,
    #    while 118,000, 130,000 and 145,000 were discussed in later messages
    #    without that word. The same-label check above stayed silent and the
    #    page would have shown 116,000 as though it were settled. Any other
    #    pay figure in the thread that differs from the proposal is a reason
    #    to look.
    headline = proposed["total"] or proposed["stipend"]
    if headline:
        breakdown = {
            proposed[k]["amount"] for k in ("base", "medical", "other")
            if proposed[k]
        }
        others = sorted(
            {i["amount"] for i in money}
            - {headline["amount"]} - breakdown
        )
        if others:
            warnings.append(
                "Other figures appear in this thread that are not the one "
                f"shown: {', '.join('PKR {:,}'.format(v) for v in others)}. "
                "The one shown is the latest that was labelled, which is not "
                "the same as the one that was agreed."
            )

    # 🔴 A BREAKDOWN THAT CANNOT BE TRUE. Hafiza's real thread yields a base of
    #    135,000 against a total of 108,000. One of the two is mislabelled, and
    #    neither should be copied into a contract unchecked.
    if proposed["total"]:
        total = proposed["total"]["amount"]
        parts = {k: proposed[k]["amount"] for k in ("base", "medical", "other")
                 if proposed[k]}
        for name, amount in parts.items():
            if amount > total:
                warnings.append(
                    f"The {name} figure (PKR {amount:,}) is larger than the "
                    f"total (PKR {total:,}), so one of them has been read from "
                    "the wrong place. Do not use either without checking."
                )
                break
        else:
            if len(parts) >= 2 and abs(sum(parts.values()) - total) > 1:
                warnings.append(
                    f"The parts add up to PKR {sum(parts.values()):,} but the "
                    f"total says PKR {total:,}. Check the breakdown."
                )
    if counters:
        warnings.append(
            f"{len(counters)} message{'s' if len(counters) > 1 else ''} from "
            "the candidate read like a negotiation, so the first offer may not "
            "be the agreed figure. Mariam and Hafiza both countered."
        )
    if not money:
        warnings.append("No salary figure was found in this thread.")

    return {
        "proposed": proposed,
        "all_amounts": money,
        "all_dates": dates,
        "counters": counters,
        "warnings": warnings,
        "messages_read": len(ordered),
    }


# --------------------------------------------------------------------------
# Getting the thread out of the mailbox
# --------------------------------------------------------------------------


def _plain_text(payload) -> str:
    """The readable text of a Gmail message payload, preferring text/plain.

    Falls back to stripping the HTML part, because plenty of offer letters
    are sent as HTML only and the salary is in there either way.
    """
    import base64

    def decode(data: str) -> str:
        return base64.urlsafe_b64decode(data.encode()).decode("utf-8", "replace")

    plain, html_parts = [], []

    def walk(part):
        mime = part.get("mimeType", "")
        body = part.get("body") or {}
        if body.get("data"):
            if mime == "text/plain":
                plain.append(decode(body["data"]))
            elif mime == "text/html":
                html_parts.append(decode(body["data"]))
        for sub in part.get("parts") or []:
            walk(sub)

    walk(payload or {})
    if plain:
        return "\n".join(plain)
    if not html_parts:
        return ""
    import html as H

    text = "\n".join(html_parts)
    text = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", text, flags=re.S | re.I)
    # Keep the line structure: the salary breakdown is one figure per line and
    # the label is read from its own line.
    text = re.sub(r"<br\s*/?>|</p>|</tr>|</div>|</li>", "\n", text, flags=re.I)
    return H.unescape(re.sub(r"<[^>]+>", " ", text))


def read_for_candidate(email: str, limit: int = 25) -> dict:
    """Find and read this candidate's offer thread from the mailbox.

    Searched by ADDRESS, not by subject. A real offer email here is titled
    "Congratulations Mariam on Your Selection as a Coach for the NIETE
    Project!" and contains the word "offer" nowhere at all.
    """
    from .gmail_evidence import _build_service

    address = (email or "").strip()
    if not address:
        return read_thread([])

    svc = _build_service()
    query = f"(to:{address} OR from:{address} OR cc:{address})"
    listed = svc.users().messages().list(
        userId="me", q=query, maxResults=limit).execute()
    ids = [m["id"] for m in listed.get("messages", [])]

    messages = []
    for message_id in ids:
        full = svc.users().messages().get(
            userId="me", id=message_id, format="full").execute()
        headers = {
            h["name"].lower(): h["value"]
            for h in (full.get("payload", {}).get("headers") or [])
        }
        sent_at = ""
        if full.get("internalDate"):
            sent_at = dt.datetime.fromtimestamp(
                int(full["internalDate"]) / 1000, dt.timezone.utc).isoformat()
        messages.append({
            "from_me": "taleemabad.com" in (headers.get("from") or "").lower(),
            "date": sent_at,
            "subject": headers.get("subject", ""),
            "body": _plain_text(full.get("payload")),
        })
    return read_thread(messages)
