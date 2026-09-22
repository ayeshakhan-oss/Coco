"""Case-study tracking: status reconciliation, completeness, AI flags, mirrors.

The load-bearing test in this file is
`test_no_submission_is_never_reported_as_not_sent`. Markaz records no case-study
send at all (measured 2026-09-22: no `case_study_sent_at` column, and
`candidate_communications` holds 16 typed rows in the whole table while
reporting 0 sends against 4-17 submissions per job), so a status vocabulary that
let a reader say "43 were never sent one" would be inventing that number.

Run: python -m pytest webapp/tests/test_case_study_tracking.py -v
"""

from __future__ import annotations

import pytest

from webapp.services import case_study_tracking as t


def _row(**over) -> dict:
    row = {
        "case_study_submission": None,
        "case_study_word_file": None,
        "case_study_excel_file": None,
        "case_study_video_file": None,
    }
    row.update(over)
    return row


# --------------------------------------------------------------------------
# Status reconciliation
# --------------------------------------------------------------------------


def test_no_submission_is_never_reported_as_not_sent():
    """The whole point of the module. We cannot see the send, so the absence of
    a record is a statement about OUR RECORDS, not about the candidate."""
    status = t.submission_status(_row(), send_found=None)
    assert status == t.NO_RECORD_OF_A_SEND
    assert status in t.UNPROVEN_ABSENCE
    assert "not_sent" not in t.STATUSES, (
        "a 'not_sent' status would let a report claim something we cannot see"
    )


def test_an_unprobed_candidate_is_not_treated_as_unsent():
    """send_found=None (never probed) and send_found=False (probed, nothing
    found) must land in the same place: both mean no record."""
    assert t.submission_status(_row(), send_found=None) == t.NO_RECORD_OF_A_SEND
    assert t.submission_status(_row(), send_found=False) == t.NO_RECORD_OF_A_SEND


def test_a_found_send_with_no_submission_is_awaiting():
    assert t.submission_status(_row(), send_found=True) == t.AWAITING


def test_any_channel_counts_as_a_submission():
    for channel in (
        "case_study_submission", "case_study_word_file",
        "case_study_excel_file", "case_study_video_file",
    ):
        row = _row(**{channel: "something"})
        assert t.submission_status(row, send_found=True) == t.SUBMITTED, channel


def test_a_submission_with_no_send_record_is_surfaced_not_hidden():
    row = _row(case_study_word_file="/uploads/x.docx")
    assert t.submission_status(row, send_found=False) == t.SUBMITTED_WITHOUT_SEND_RECORD


def test_a_blank_channel_is_not_a_submission():
    assert t.channels_present(_row(case_study_submission="   ")) == []
    assert t.channels_present(_row(case_study_submission="")) == []


def test_every_channel_is_checked_not_just_the_first():
    """The SOP: a candidate may use one, both or neither, so check them all."""
    row = _row(case_study_submission="link", case_study_excel_file="/x.xlsx")
    assert t.channels_present(row) == ["submission_text", "excel_file"]


def test_the_summary_carries_the_caveat_as_a_number():
    counts = t.summarise([
        t.SUBMITTED, t.SUBMITTED, t.AWAITING,
        t.NO_RECORD_OF_A_SEND, t.NO_RECORD_OF_A_SEND, t.NO_RECORD_OF_A_SEND,
    ])
    assert counts["total"] == 6
    assert counts[t.SUBMITTED] == 2
    assert counts["unproven_absence"] == 3


def test_the_summary_refuses_an_unknown_status():
    with pytest.raises(ValueError, match="unknown submission status"):
        t.summarise([t.SUBMITTED, "not_sent"])


# --------------------------------------------------------------------------
# Completeness
# --------------------------------------------------------------------------


def test_completeness_refuses_to_guess_when_nothing_is_configured():
    """Deriving the required sections from the submission's own headings would
    mark every submission complete by construction."""
    out = t.completeness("any text at all", None)
    assert out["known"] is False
    assert out["missing"] == []
    assert "cannot be assessed" in out["note"]


def test_completeness_finds_present_and_missing_parts():
    text = "Part 1: Market sizing ... our Go to market plan ... appendix"
    out = t.completeness(text, ["Market sizing", "Go to market", "Financial model"])
    assert out["known"] is True
    assert out["present"] == ["Market sizing", "Go to market"]
    assert out["missing"] == ["Financial model"]


def test_completeness_ignores_case_and_wrapped_whitespace():
    out = t.completeness("the\n  GO   TO\n market  plan", ["go to market"])
    assert out["missing"] == []


# --------------------------------------------------------------------------
# Content-dump flags
# --------------------------------------------------------------------------


def test_a_clean_submission_raises_nothing():
    text = (
        "We sized the opportunity from the enrolment data in Sheet 2. At 1,200 "
        "schools and a 9 percent conversion rate the pipeline supports 108 "
        "partners in year one, which is below the target of 150."
    )
    assert t.content_dump_flags(text) == []


def test_assistant_voice_is_flagged_with_its_evidence():
    flags = t.content_dump_flags(
        "Certainly! Here is a comprehensive analysis of the opportunity."
    )
    names = {f["flag"] for f in flags}
    assert "assistant_voice" in names
    voice = next(f for f in flags if f["flag"] == "assistant_voice")
    assert voice["evidence"], "a flag a human cannot check is an accusation"
    assert voice["meaning"]


def test_emoji_and_markdown_artefacts_are_flagged():
    flags = t.content_dump_flags("## Findings\n\n**Key point** rocket \U0001F680 growth")
    names = {f["flag"] for f in flags}
    assert "emoji" in names and "markdown_artefacts" in names


def test_one_stock_phrase_is_not_filler_but_several_are():
    assert t.content_dump_flags("We followed best practices throughout.") == []
    flags = t.content_dump_flags(
        "Best practices and a holistic approach to leverage synergies with key stakeholders."
    )
    assert "generic_language" in {f["flag"] for f in flags}


def test_every_flag_carries_a_meaning_a_reader_can_act_on():
    flags = t.content_dump_flags("Certainly! \U0001F680 ## Heading **bold**")
    assert flags
    for f in flags:
        assert f["meaning"] in t.FLAG_MEANINGS.values()


# --------------------------------------------------------------------------
# The mirror problem
# --------------------------------------------------------------------------

_SHARED = (
    "the pipeline supports one hundred and eight partners in year one which is "
    "below the target of one hundred and fifty schools across the region "
    "requiring an additional forty two partnerships to close the gap entirely"
)


def test_two_independent_submissions_do_not_mirror():
    pairs = t.mirror_pairs({
        1: "We sized the opportunity from the enrolment data in sheet two carefully.",
        2: "Our approach began with the cost per school and worked backwards from margin.",
    })
    assert pairs == []


def test_a_long_shared_run_across_two_submissions_is_surfaced():
    pairs = t.mirror_pairs({
        1: "Opening line from candidate one. " + _SHARED,
        2: "A completely different opening. " + _SHARED,
    })
    assert len(pairs) == 1
    assert pairs[0]["application_ids"] == [1, 2]
    assert pairs[0]["shared_runs"] >= t.MIRROR_MIN_SHARED
    assert pairs[0]["examples"], "the shared text itself must be shown"


def test_mirroring_is_reported_without_naming_a_cause():
    """Two candidates quoting the same paragraph of the assignment look
    identical to two sharing an assistant. The result carries the evidence and
    no verdict."""
    pair = t.mirror_pairs({1: _SHARED, 2: _SHARED})[0]
    assert set(pair) == {"application_ids", "shared_runs", "examples"}


def test_a_short_submission_cannot_mirror():
    assert t.mirror_pairs({1: "too short", 2: "too short"}) == []


def test_pairs_are_ordered_by_how_much_they_share():
    more = _SHARED + " " + _SHARED[::-1]
    pairs = t.mirror_pairs({1: more, 2: more, 3: "x " + _SHARED})
    assert pairs[0]["shared_runs"] >= pairs[-1]["shared_runs"]
