"""Turn a Markaz job's stored description into readable job-description text.

Markaz keeps the JD in `jobs.description` as HTML pasted out of Google Docs:
inline `style=` on nearly every tag, `data-path-to-node` attributes, a
`<!--StartFragment-->` wrapper, and sometimes base64 `data:` image URIs. Job 43
is 3,300,555 characters of it. Handed to a model raw, that is mostly markup, and
the few hundred words of actual JD are buried in it.

`jobs.jd_text` looks like the obvious column and is a trap: measured across all
32 live jobs on 2026-09-22, `description` is populated on 31 of them while
`jd_text` is populated on ONE and averages 211 characters. Screening against
`jd_text` would silently screen against nothing.

This module is the only place the webapp turns that column into text. Like
`cv_text`, it RAISES rather than returning a thin string: a CV screened against
an empty job description is not a screen.
"""

from __future__ import annotations

import html
import re

# A JD longer than this is not a JD, it is a document. Cutting here keeps a
# pathological row from crowding the CV out of the prompt.
MAX_CHARS = 20_000

# Below this there is no JD to screen against, whatever the column contained.
MIN_USABLE_CHARS = 200

_BLOCK_END = re.compile(
    r"</\s*(?:p|div|h[1-6]|li|tr|table|section|article|blockquote|br)\s*/?>",
    re.I,
)
_SELF_CLOSING_BREAK = re.compile(r"<\s*(?:br|hr)\s*/?>", re.I)
_LIST_ITEM = re.compile(r"<\s*li[^>]*>", re.I)
# Must run BEFORE tags are stripped: a base64 image lives inside an attribute,
# so removing the tag text alone would leave megabytes of payload behind.
_DATA_URI = re.compile(r"""\bdata:[^\s"'>]{200,}""", re.I)
_SCRIPT_STYLE = re.compile(r"<\s*(script|style)[^>]*>.*?<\s*/\s*\1\s*>", re.I | re.S)
_COMMENT = re.compile(r"<!--.*?-->", re.S)
_TAG = re.compile(r"<[^>]+>")
_SPACES = re.compile(r"[ \t ]+")
_BLANK_LINES = re.compile(r"\n{3,}")


class JobDescriptionUnreadable(Exception):
    """The job has no usable description text to screen against."""


def to_text(description: str | None, *, job_id: int | None = None) -> str:
    """Return readable JD text, or raise JobDescriptionUnreadable.

    Kept deliberately simple: no HTML parser dependency, because the input is
    machine-generated Google Docs markup rather than arbitrary web pages, and a
    regex pass over it is both sufficient and far cheaper than parsing three
    megabytes of styled spans.
    """
    where = f"job {job_id}" if job_id is not None else "this job"

    if not description or not description.strip():
        raise JobDescriptionUnreadable(
            f"{where} has no description on file. Refusing to screen a CV "
            "against an empty job description."
        )

    text = description
    text = _SCRIPT_STYLE.sub(" ", text)
    text = _COMMENT.sub(" ", text)
    # Before tag-stripping, or the payload survives the tag it lived in.
    text = _DATA_URI.sub(" ", text)
    # Keep the document's shape: a JD is a list of responsibilities and
    # requirements, and running them into one paragraph loses that.
    text = _LIST_ITEM.sub("\n- ", text)
    text = _SELF_CLOSING_BREAK.sub("\n", text)
    text = _BLOCK_END.sub("\n", text)
    text = _TAG.sub(" ", text)
    text = html.unescape(text)

    text = text.replace("\r\n", "\n").replace("\xa0", " ")
    text = _SPACES.sub(" ", text)
    text = "\n".join(line.strip() for line in text.split("\n"))
    text = _BLANK_LINES.sub("\n\n", text).strip()

    if len(text) < MIN_USABLE_CHARS:
        raise JobDescriptionUnreadable(
            f"{where}: only {len(text)} characters of readable text could be "
            f"recovered from its description (need {MIN_USABLE_CHARS}+). The "
            "stored value may be markup or an image with no text in it."
        )

    return text[:MAX_CHARS]
