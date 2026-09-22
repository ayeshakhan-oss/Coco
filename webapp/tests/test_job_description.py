"""Turning Markaz's stored job description into text a model can screen against.

Verified against all 32 live jobs on 2026-09-22: 31 produced usable JD text
(2,072 to 17,693 characters) and the one refusal was job 30 "Hackathon 2026",
whose description is 14 characters. Job 43 went from 3,300,555 characters of
Google-Docs markup to 6,006 characters of job description.

Run: python -m pytest webapp/tests/test_job_description.py -v
"""

from __future__ import annotations

import pytest

from webapp.services.job_description import (
    MAX_CHARS,
    MIN_USABLE_CHARS,
    JobDescriptionUnreadable,
    to_text,
)

REAL_SHAPE = (
    '<!--StartFragment--><meta charset="utf-8" dir="ltr">'
    '<h2 style="line-height:1.38;margin-top:18pt;" dir="ltr">'
    '<b data-path-to-node="0" dir="ltr">Job Title: Growth Manager</b></h2>'
    "<hr><p>You will own partnerships with government and low-cost private "
    "schools across the region.</p>"
    "<ul><li>Build a pipeline of school partners</li>"
    "<li>Own the commercial conversation end to end</li></ul>"
    "<p>Requirements: 4&ndash;7 years in partnerships, and a track record you "
    "can evidence.</p>"
)


def test_a_real_markaz_job_description_becomes_readable_text():
    out = to_text(REAL_SHAPE, job_id=39)
    assert "Job Title: Growth Manager" in out
    assert "low-cost private schools" in out
    assert "4-7 years" in out or "4–7 years" in out, "entities are unescaped"
    assert "<" not in out and ">" not in out, "markup survived"
    assert "style=" not in out and "data-path-to-node" not in out


def test_list_items_keep_their_shape():
    """A JD is a list of responsibilities. Running them into one paragraph
    loses the structure a screen has to read against."""
    out = to_text(REAL_SHAPE, job_id=39)
    assert "- Build a pipeline of school partners" in out
    assert "- Own the commercial conversation end to end" in out


def test_an_embedded_base64_image_is_removed_before_tags_are_stripped():
    """Job 43's description is 3,300,555 characters, nearly all of it payload
    like this. Stripping tags first would leave the base64 behind as text."""
    payload = "A" * 500_000
    html = f'<p>Real JD text about the role. {"Responsibilities. " * 20}</p><img src="data:image/png;base64,{payload}">'
    out = to_text(html, job_id=43)
    assert "Real JD text about the role." in out
    assert payload[:200] not in out
    assert len(out) < 2_000, f"the payload survived: {len(out)} chars"


def test_script_and_style_blocks_are_dropped_with_their_contents():
    html = (
        "<style>.x{color:red;font-family:Lexend}</style>"
        "<p>" + "The actual job description text. " * 10 + "</p>"
        "<script>window.x = 1</script>"
    )
    out = to_text(html, job_id=1)
    assert "color:red" not in out and "window.x" not in out
    assert "The actual job description text." in out


def test_an_empty_or_missing_description_is_refused():
    """cv_text refuses rather than returning a thin string, and so does this:
    a CV screened against an empty JD is not a screen."""
    for value in (None, "", "   "):
        with pytest.raises(JobDescriptionUnreadable, match="no description"):
            to_text(value, job_id=7)


def test_a_description_that_is_all_markup_is_refused():
    """Job 30 "Hackathon 2026" is the live example: 14 characters."""
    with pytest.raises(JobDescriptionUnreadable, match="readable text"):
        to_text('<p style="margin:0"></p><div></div>', job_id=30)


def test_the_refusal_names_the_job_so_it_is_actionable():
    with pytest.raises(JobDescriptionUnreadable, match="job 30"):
        to_text("<p></p>", job_id=30)
    with pytest.raises(JobDescriptionUnreadable, match="this job"):
        to_text("<p></p>")


def test_output_is_capped_so_a_huge_jd_cannot_crowd_out_the_cv():
    out = to_text("<p>" + ("Responsibility statement. " * 5_000) + "</p>", job_id=1)
    assert len(out) == MAX_CHARS


def test_the_floor_sits_below_the_cap():
    assert MIN_USABLE_CHARS < MAX_CHARS


def test_whitespace_is_collapsed_without_losing_paragraphs():
    out = to_text(
        "<p>" + "First paragraph. " * 10 + "</p>\n\n\n\n<p>" + "Second one. " * 10 + "</p>",
        job_id=1,
    )
    assert "\n\n\n" not in out
    assert "First paragraph." in out and "Second one." in out
