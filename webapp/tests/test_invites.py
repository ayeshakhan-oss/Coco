"""The invite gates, proven against deliberately broken invites.

Rule 25's lesson: "prove every check fires against a deliberately broken draft
-- a gate that has only ever passed proves nothing." So every test below that
asserts a rule also builds the invite that breaks it.

The four things that must never happen:
  1. A pilot reaching anybody but Ayesha, or carrying a CC.
  2. "[PILOT" surviving into a live subject line.
  3. A live send on a booking link nobody has fetched (the Lahore/Karachi trap).
  4. A booking button on a type that confirms by reply, or none at all.

Run: python -m pytest webapp/tests/test_invites.py -v
"""

from __future__ import annotations

import pytest

from webapp.services import invite_render as rnd
from webapp.services import invites as inv

GOOD = {
    "values_interview": dict(
        first_name="Ushna", full_name="Ushna Tariq",
        position="Growth Manager - Lahore",
        jd_url="https://drive.google.com/file/d/lahore-jd/view",
        prep_url="https://docs.google.com/document/d/prep",
        booking_url="https://calendar.google.com/…/lahore",
    ),
    "case_study_debrief": dict(
        first_name="Ali", full_name="Ali Raza", position="Senior Manager Growth",
        booking_url="https://calendar.google.com/…/debrief",
    ),
    "exploratory_call": dict(
        first_name="Sara", full_name="Sara Ahmed", position="Fundraising",
        booking_url="https://calendar.google.com/…/explore",
        context="We came across your work on multilateral partnerships.",
    ),
    "warm_bench_opportunity": dict(
        first_name="Hajra", full_name="Hajra Noor", position="CPD Coach",
        booking_url="https://calendar.google.com/…/warm",
        previous_role="Programme Fellow",
    ),
    "keep_in_touch": dict(
        first_name="Omar", full_name="Omar Shah", position="Growth Manager",
    ),
    "interview_reminder": dict(
        first_name="Zoya", full_name="Zoya Khan", position="Senior Manager Growth",
        interview_date="Friday, September 26, 2026",
        interview_time="11:00 AM to 12:00 PM, Pakistan Standard Time",
    ),
    "assessment_center": dict(
        first_name="Bilal", full_name="Bilal Ahmed", position="CPD Coach",
        activity_date="Thursday, August 6, 2026",
        start_time="10:30 AM", end_time="5:00 PM",
        venue="Service Rd W, Sector H-9/1, Islamabad, 44000, Pakistan",
        maps_url="https://maps.app.goo.gl/wmSUN8BKUBkhaeYA8",
        confirm_by_date="Monday, August 3, 2026",
    ),
}


# --------------------------------------------------------------------------
# The registries agree with each other
# --------------------------------------------------------------------------


def test_every_type_appears_in_every_registry():
    """A type present in one map and absent from another is how a picker
    offers an invite the gate has no rules for."""
    assert set(inv.INVITE_TYPES) == set(rnd.CHROME) == set(rnd.REQUIRED)
    assert len(inv.INVITE_TYPES) == 7


def test_every_type_has_a_worked_example_here():
    """Otherwise a new type ships with no test at all."""
    assert set(GOOD) == set(inv.INVITE_TYPES)


# --------------------------------------------------------------------------
# 1. Pilots go to Ayesha, alone
# --------------------------------------------------------------------------


def test_a_pilot_goes_to_ayesha_and_nobody_else():
    r = inv.recipients_for(
        live=False, candidate_email="candidate@example.com",
        cc=["hiring@taleemabad.com", "waqas.tanveer@taleemabad.com"],
    )
    assert r["to"] == [inv.PILOT_RECIPIENT]
    assert r["cc"] == []
    # The candidate's address must not appear anywhere in a pilot.
    assert "candidate@example.com" not in r["to"] + r["cc"]


def test_a_pilot_with_a_cc_is_refused_outright():
    problems = inv.check_before_send(
        invite_type="values_interview", live=False, subject="Values Interview",
        candidate_email="c@example.com", booking_url="https://b",
        cc=["hiring@taleemabad.com"],
    )
    assert any("pilot has no CC" in p for p in problems)


def test_a_live_send_keeps_its_cc_list():
    r = inv.recipients_for(
        live=True, candidate_email="candidate@example.com",
        cc=["hiring@taleemabad.com"],
    )
    assert r["to"] == ["candidate@example.com"]
    assert r["cc"] == ["hiring@taleemabad.com"]


def test_a_live_send_without_an_address_raises_rather_than_guessing():
    with pytest.raises(inv.InviteError):
        inv.recipients_for(live=True, candidate_email=None)


# --------------------------------------------------------------------------
# 2. "[PILOT" never survives into a live subject
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "subject",
    [
        "[PILOT - ] Values Interview for CPD Coach",
        "[PILOT] Values Interview",
        "[pilot - Ushna] Values Interview",
        "[ PILOT - ] Values Interview",
    ],
)
def test_a_live_subject_carrying_a_pilot_marker_is_refused(subject):
    problems = inv.check_before_send(
        invite_type="values_interview", live=True, subject=subject,
        candidate_email="c@example.com", booking_url="https://b",
        booking_verified_title="Zero in Call for Growth Manager Lahore",
    )
    assert any("[PILOT" in p for p in problems), problems


def test_a_clean_live_subject_passes():
    assert inv.check_before_send(
        invite_type="values_interview", live=True,
        subject="Values Interview for Growth Manager - Lahore - Ushna Tariq",
        candidate_email="c@example.com", booking_url="https://b",
        booking_verified_title="Zero in Call for Growth Manager Lahore",
    ) == []


def test_a_pilot_without_the_marker_is_allowed():
    """A threaded pilot must NOT carry the prefix, because it breaks
    threading. Its absence is therefore not an error."""
    assert inv.check_before_send(
        invite_type="values_interview", live=False,
        subject="Values Interview for Growth Manager",
        candidate_email=None, booking_url="https://b",
    ) == []


# --------------------------------------------------------------------------
# 3. An unverified booking link blocks a LIVE send (the Lahore/Karachi trap)
# --------------------------------------------------------------------------


def test_a_live_send_on_an_unverified_booking_link_is_refused():
    problems = inv.check_before_send(
        invite_type="values_interview", live=True, subject="Values Interview",
        candidate_email="c@example.com",
        booking_url="https://calendar.google.com/…/AcZssZ0hJDcEaQ96",
        booking_verified_title=None,
    )
    assert any("not been verified" in p for p in problems), problems


def test_a_pilot_does_not_need_a_verified_link():
    """Verifying before a pilot would stop Ayesha seeing the draft at all,
    and the pilot is exactly where she checks the link herself."""
    assert inv.check_before_send(
        invite_type="values_interview", live=False, subject="Values Interview",
        candidate_email=None, booking_url="https://b", booking_verified_title=None,
    ) == []


def test_a_booking_type_with_no_link_at_all_is_refused():
    problems = inv.check_before_send(
        invite_type="values_interview", live=False, subject="Values Interview",
        candidate_email=None, booking_url=None,
    )
    assert any("needs a booking link" in p for p in problems)


def test_the_karachi_title_does_not_pass_for_a_lahore_role():
    """The actual failure Rule 24 was written for: a Job 41 Karachi booking
    link sitting in the job39 folder."""
    karachi = "Zero in Call for Growth Manager Karachi"
    assert inv.title_mentions(karachi, "Zero in Call for Growth Manager Karachi")
    assert not inv.title_mentions(karachi, "Zero in Call for Growth Manager Lahore")


def test_title_matching_survives_punctuation_and_double_spaces():
    """Markaz subjects carry double spaces ("Growth  Manager") and Google
    titles differ in dashes, so a strict compare reports a false mismatch."""
    assert inv.title_mentions("Zero in Call for Growth  Manager - Lahore",
                              "Zero in Call for Growth Manager Lahore")


def test_an_empty_title_never_counts_as_a_match():
    assert not inv.title_mentions(None, "Growth Manager Lahore")
    assert not inv.title_mentions("", "Growth Manager Lahore")
    assert not inv.title_mentions("Growth Manager Lahore", "")


def test_title_is_read_out_of_real_html():
    html = "<html><head><title>Zero in Call for\n  Growth Manager Lahore</title></head></html>"
    assert inv.title_of(html) == "Zero in Call for Growth Manager Lahore"
    assert inv.title_of("<html><head></head></html>") is None


# --------------------------------------------------------------------------
# 4. Booking buttons only where the type has one
# --------------------------------------------------------------------------


@pytest.mark.parametrize("invite_type", ["keep_in_touch", "assessment_center",
                                         "interview_reminder"])
def test_a_booking_link_on_a_no_button_type_is_refused(invite_type):
    problems = inv.check_before_send(
        invite_type=invite_type, live=False, subject="A note",
        candidate_email=None, booking_url="https://calendar.google.com/book",
    )
    assert any("must not carry a booking link" in p for p in problems), problems


def test_the_renderer_also_refuses_a_booking_link_on_those_types():
    ctx = dict(GOOD["keep_in_touch"], booking_url="https://calendar.google.com/book")
    with pytest.raises(inv.InviteError, match="no booking button"):
        rnd.render("keep_in_touch", ctx)


def test_keep_in_touch_carries_no_link_and_no_promise():
    """🔒 Two hard rules for this type: no booking button, no links at all, and
    nothing the candidate can count on."""
    html = rnd.render("keep_in_touch", GOOD["keep_in_touch"])
    assert "background:#5b3fc4" not in html          # no purple button
    assert "impact-microsite" not in html            # no links in the body
    for promise in ("we will reach out", "we will be in touch",
                    "we will contact you", "keep your name on file"):
        assert promise not in html.lower(), promise


def test_the_assessment_centre_confirms_by_reply_and_carries_ayeshas_block():
    html = rnd.render("assessment_center", GOOD["assessment_center"])
    assert "background:#5b3fc4" not in html
    assert "kindly reply to this email" in html
    assert "Ayesha Raza Khan" in html
    # Onsite, so no recording-consent line and no Meet link.
    assert "will be recorded" not in html


# --------------------------------------------------------------------------
# The reminder never invents a Meet link
# --------------------------------------------------------------------------


def test_a_reminder_without_a_verified_meet_link_gets_the_fallback_line():
    html = rnd.render("interview_reminder", GOOD["interview_reminder"])
    assert "background:#5b3fc4" not in html
    assert "Google Meet link in your calendar invitation" in html


def test_a_reminder_with_a_verified_meet_link_gets_the_button():
    ctx = dict(GOOD["interview_reminder"], meet_url="https://meet.google.com/abc-defg-hij")
    html = rnd.render("interview_reminder", ctx)
    assert "https://meet.google.com/abc-defg-hij" in html
    assert "Join your Interview" in html
    assert "Google Meet link in your calendar invitation" not in html


def test_a_reminder_always_states_the_date_and_time():
    html = rnd.render("interview_reminder", GOOD["interview_reminder"])
    assert "Friday, September 26, 2026" in html
    assert "11:00 AM to 12:00 PM" in html


# --------------------------------------------------------------------------
# Missing fields refuse, they do not render a placeholder
# --------------------------------------------------------------------------


@pytest.mark.parametrize("invite_type", sorted(GOOD))
def test_every_type_renders_from_its_worked_example(invite_type):
    html = rnd.render(invite_type, GOOD[invite_type])
    assert html.startswith("<html>")
    assert "cid:taleemabad_logo" in html
    assert "People and Culture Team" in html
    # No unsubstituted format slot survived into the output.
    assert "{" not in html.split("<style>")[1].split("</style>")[1]


@pytest.mark.parametrize("invite_type", sorted(GOOD))
def test_dropping_any_required_field_refuses_the_render(invite_type):
    for field in rnd.REQUIRED[invite_type]:
        ctx = dict(GOOD[invite_type])
        ctx.pop(field, None)
        with pytest.raises(inv.InviteError) as exc:
            rnd.render(invite_type, ctx)
        assert field in str(exc.value)


def test_a_blank_string_counts_as_missing():
    """An empty position would otherwise render an empty subtitle and an
    invite addressed to nothing in particular."""
    ctx = dict(GOOD["case_study_debrief"], position="   ")
    with pytest.raises(inv.InviteError, match="position"):
        rnd.render("case_study_debrief", ctx)


# --------------------------------------------------------------------------
# A candidate's own name cannot break the markup
# --------------------------------------------------------------------------


def test_a_name_with_an_apostrophe_or_ampersand_is_escaped():
    ctx = dict(GOOD["case_study_debrief"], first_name="O'Brien",
               position="Research & Learning")
    html = rnd.render("case_study_debrief", ctx)
    assert "O&#x27;Brien" in html
    assert "Research &amp; Learning" in html
    assert "<script" not in html


def test_html_in_a_field_is_neutralised():
    ctx = dict(GOOD["case_study_debrief"],
               first_name="<script>alert(1)</script>")
    html = rnd.render("case_study_debrief", ctx)
    assert "<script>" not in html
    assert "&lt;script&gt;" in html


# --------------------------------------------------------------------------
# The locked design is not quietly redesigned
# --------------------------------------------------------------------------


LOCKED = [
    ("#f5f5f5", "page background"),
    ("#e5e7e2", "wrapper"),
    ("#3157b7", "header colour"),
    ("#3d63c8", "link colour"),
    ("#4b67d1", "2px divider"),
    ('width="775"', "card width"),
    ("Georgia,Cambria,'Times New Roman',serif", "typeface"),
    ('width="34" height="34"', "34px logo"),
]


@pytest.mark.parametrize("token,what", LOCKED, ids=[w for _, w in LOCKED])
def test_the_locked_design_tokens_are_all_present(token, what):
    """memory/locked_email_template_interview_invites_FINAL_2026_05_13.md.
    Design is 100% locked; only content changes."""
    html = rnd.render("values_interview", GOOD["values_interview"])
    assert token in html, what


def test_no_em_dashes_anywhere_in_any_rendered_invite():
    """An em dash is a standing hard block on everything we send."""
    for invite_type, ctx in GOOD.items():
        html = rnd.render(invite_type, ctx)
        assert "—" not in html.replace("&mdash;", ""), invite_type


def test_subjects_are_clean_of_the_pilot_marker_by_construction():
    for invite_type, ctx in GOOD.items():
        subject = rnd.subject_for(invite_type, ctx)
        assert not inv.subject_has_pilot_marker(subject), invite_type
        assert subject.strip() == subject
        assert "{" not in subject
