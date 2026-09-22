"""The locked case-study scoring rules, tested without a model or a database.

The zero is the point: anchoring at 1 floors every dimension at 20% of its weight,
which is the defect that put all 25 RM case studies above the bar (CLAUDE.md Rule 27).
"""

from __future__ import annotations

import pytest

from webapp.services.case_study_scoring import (
    DIMENSIONS,
    SCORES,
    CaseStudyScoringError,
    band,
    validate_scores,
    weighted_total,
)


def _all(n):
    return {d["key"]: n for d in DIMENSIONS}


def test_weights_are_the_locked_six_and_sum_to_100():
    assert [d["weight"] for d in DIMENSIONS] == [20, 25, 20, 15, 10, 10]
    assert sum(d["weight"] for d in DIMENSIONS) == 100
    assert len(DIMENSIONS) == 6


def test_the_scale_has_a_real_zero():
    assert SCORES == (0, 1, 2, 3, 4, 5)
    # THE defect this rubric change exists to remove: all-minimum must be 0, not 20.
    assert weighted_total(_all(0)) == 0.0


def test_conversion_is_linear_on_the_full_scale():
    assert weighted_total(_all(5)) == 100.0
    assert weighted_total(_all(4)) == 80.0
    assert weighted_total(_all(3)) == 60.0
    assert weighted_total(_all(2)) == 40.0
    assert weighted_total(_all(1)) == 20.0


def test_weighting_is_per_dimension_not_flat():
    # Only Execution specificity (weight 25) at full marks.
    scores = _all(0)
    scores["execution_specificity"] = 5
    assert weighted_total(scores) == 25.0


def test_bands_match_the_locked_thresholds():
    assert band(80.0, []) == "strong_yes"
    assert band(95.0, []) == "strong_yes"
    assert band(79.9, []) == "yes"
    assert band(65.0, []) == "yes"
    assert band(64.9, []) == "borderline"
    assert band(50.0, []) == "borderline"
    assert band(49.9, []) == "no"
    assert band(0.0, []) == "no"


def test_fabricated_data_disqualifies_regardless_of_total():
    assert band(100.0, ["fabricated_data"]) == "disqualified"
    assert band(92.0, ["fabricated_data", "undisclosed_ai"]) == "disqualified"
    # A serious-but-not-disqualifying flag does NOT override the band.
    assert band(92.0, ["undisclosed_ai"]) == "strong_yes"


def test_benchmark_table_is_in_the_coco_schema():
    from webapp.models import EvalBenchmark

    assert EvalBenchmark.__table__.schema == "coco"


def test_benchmark_carries_a_qa_gate():
    from webapp.models import EvalBenchmark

    cols = {c.name for c in EvalBenchmark.__table__.columns}
    # Rule 0 is enforced by requiring these before a run may start.
    assert {"qa_approved_at", "qa_approved_by", "status"} <= cols


def test_validate_rejects_a_bad_score_set():
    with pytest.raises(CaseStudyScoringError):
        validate_scores({d["key"]: 3 for d in DIMENSIONS[:5]})     # missing one
    with pytest.raises(CaseStudyScoringError):
        bad = _all(3); bad["data_judgment"] = 6
        validate_scores(bad)                                        # out of range
    with pytest.raises(CaseStudyScoringError):
        bad = _all(3); bad["not_a_dimension"] = 3
        validate_scores(bad)                                        # unknown key
    with pytest.raises(CaseStudyScoringError):
        bad = _all(3); bad["data_judgment"] = 2.5
        validate_scores(bad)                                        # not an integer
    validate_scores(_all(0))                                        # zero is VALID


# ── Submission retrieval (webapp/services/submissions.py) ──────────────────
#
# The core rule: an unreadable submission is REFUSED, never scored as a weak
# one (mirrors cv_text.CVUnreadable). Every fetcher here is exercised through
# an injected fake -- no test in this module opens a socket, a mailbox, or
# Drive. A test that reaches the network is not a unit test.

from webapp.services.submissions import (  # noqa: E402
    RawAttachment,
    SubmissionContext,
    SubmissionUnreadable,
    _drive_file_id,
    _extract_links,
    corpus_for,
    markaz_case_study_api,
    markaz_linked_documents,
)


def _ctx(**overrides):
    base = dict(application_id=4242, candidate_name="Zara Khan",
                candidate_email="zara@example.com", job_title="Growth Manager")
    base.update(overrides)
    return SubmissionContext(**base)


def test_corpus_for_refuses_when_no_fetcher_finds_anything():
    """No attachments at all from any channel -> refuse, not an empty corpus."""
    empty_fetcher = lambda ctx: []  # noqa: E731
    with pytest.raises(SubmissionUnreadable):
        corpus_for(4242, context=_ctx(), fetchers=[empty_fetcher, empty_fetcher])


def test_corpus_for_refuses_below_the_usable_floor():
    """A source that DOES yield content, but under MIN_USABLE_CHARS, still
    refuses -- a thin scrap is treated the same as nothing, never scored."""
    thin = RawAttachment(origin="Gmail attachment: note.txt", filename="note.txt",
                          content=b"Not much here.")

    def fetcher(ctx):
        return [thin]

    with pytest.raises(SubmissionUnreadable) as exc_info:
        corpus_for(4242, context=_ctx(), fetchers=[fetcher])
    assert "4242" in str(exc_info.value)


def test_corpus_for_never_returns_usable_false():
    """The dict shape carries `usable: bool`, but the contract is refuse-or-
    succeed: corpus_for never hands back a dict with usable=False, mirroring
    cv_text.extract's raise-don't-degrade pattern."""
    thin = RawAttachment(origin="x", filename="x.txt", content=b"short")
    with pytest.raises(SubmissionUnreadable):
        corpus_for(4242, context=_ctx(), fetchers=[lambda ctx: [thin]])


def test_corpus_for_succeeds_and_records_every_source_actually_read():
    long_text = ("The candidate proposed a three-phase rollout for the growth "
                 "flywheel, sequencing partner recruitment before budget commitments. ") * 5
    assert len(long_text) >= 400
    att_a = RawAttachment(origin="Gmail attachment: case-study-4242-word-1.docx",
                           filename="submission.txt", content=long_text.encode("utf-8"))

    def mailbox_fetcher(ctx):
        return [att_a]

    def empty_fetcher(ctx):
        return []

    result = corpus_for(4242, context=_ctx(), fetchers=[mailbox_fetcher, empty_fetcher])

    assert result["usable"] is True
    assert result["chars"] == len(result["text"])
    assert result["chars"] >= 400
    assert result["sources"] == ["Gmail attachment: case-study-4242-word-1.docx"]
    assert "three-phase rollout" in result["text"]


def test_corpus_for_combines_multiple_sources_and_lists_each():
    part1 = "A" * 250
    part2 = "B" * 250
    att1 = RawAttachment(origin="Gmail attachment: part1.txt", filename="p1.txt",
                          content=part1.encode())
    att2 = RawAttachment(origin="Drive: https://drive.google.com/file/d/abc/view",
                          filename="p2.txt", content=part2.encode())

    result = corpus_for(
        4242, context=_ctx(),
        fetchers=[lambda ctx: [att1], lambda ctx: [att2]],
    )
    assert result["sources"] == [
        "Gmail attachment: part1.txt",
        "Drive: https://drive.google.com/file/d/abc/view",
    ]
    assert part1 in result["text"] and part2 in result["text"]


def test_corpus_for_skips_a_source_that_yields_nothing_but_keeps_trying():
    """A fetcher that raises (network error on one channel) must not abort the
    others -- it tries the next source, exactly like cv_text tries the next
    parser."""
    good = RawAttachment(origin="Gmail attachment: real.txt", filename="real.txt",
                          content=(b"C" * 500))

    def broken_fetcher(ctx):
        raise ConnectionError("mailbox unreachable")

    result = corpus_for(4242, context=_ctx(), fetchers=[broken_fetcher, lambda ctx: [good]])
    assert result["usable"] is True
    assert result["sources"] == ["Gmail attachment: real.txt"]


def test_corpus_for_needs_context_or_db():
    with pytest.raises(ValueError):
        corpus_for(4242)


def test_corpus_for_delegates_docx_extraction_to_fetch_submission_corpora():
    """Proves real delegation, not a reimplementation: a genuine .docx built
    with python-docx (same library cv_text.py uses) must come back as text via
    the shared fetch_submission_corpora.extract dispatch."""
    import io as _io

    import docx

    document = docx.Document()
    document.add_paragraph(
        "Our recommendation is to sequence the Lahore pilot before Karachi, "
        "because the partner data only supports one cohort at a time and the "
        "growth team cannot staff two onboarding tracks simultaneously this term."
    )
    document.add_paragraph(
        "Risks: the Karachi partner has a harder deadline, so a delay there "
        "carries more downside than a delay in Lahore, and we have built in a "
        "two-week buffer before the Karachi kickoff to absorb any slippage "
        "from the Lahore rollout finishing late."
    )
    buf = _io.BytesIO()
    document.save(buf)
    content = buf.getvalue()
    assert len(content) > 0

    att = RawAttachment(origin="Gmail attachment: plan.docx", filename="plan.docx", content=content)
    result = corpus_for(4242, context=_ctx(), fetchers=[lambda ctx: [att]])
    assert "Lahore pilot before Karachi" in result["text"]


def test_extract_links_finds_drive_and_markaz_upload_urls_only():
    blob = (
        "Please see my case study here: https://drive.google.com/file/d/1AbC-XyZ/view?usp=sharing "
        "and the workbook at https://markaz.taleemabad.com/uploads/case-study-99.xlsx. "
        "Also see my portfolio at https://myportfolio.example.com/work (not a submission link)."
    )
    links = _extract_links(blob)
    assert "https://drive.google.com/file/d/1AbC-XyZ/view?usp=sharing" in links
    assert "https://markaz.taleemabad.com/uploads/case-study-99.xlsx" in links
    assert not any("myportfolio" in link for link in links)


def test_extract_links_on_empty_or_none_is_empty():
    assert _extract_links("") == []
    assert _extract_links(None) == []


def test_drive_file_id_parses_the_common_share_url_shapes():
    real_length_id = "1AbC-XyZ9876543210abcdef"  # realistic Drive file ID length
    assert _drive_file_id(f"https://drive.google.com/file/d/{real_length_id}/view") == real_length_id
    assert _drive_file_id(f"https://drive.google.com/open?id={real_length_id}") == real_length_id
    assert _drive_file_id("https://example.com/not-a-drive-link") is None


def test_markaz_linked_documents_skips_the_spa_shell_trap():
    """markaz.taleemabad.com/uploads/... answers HTTP 200 with the SPA's own
    index.html for a missing file -- content-type must be checked, not status."""

    class FakeResponse:
        status_code = 200
        headers = {"content-type": "text/html; charset=utf-8"}
        content = b"<!doctype html><html>...</html>"

    def fake_get(url, timeout=15):
        return FakeResponse()

    ctx = _ctx(links=("https://markaz.taleemabad.com/uploads/case-study-99.docx",))
    result = markaz_linked_documents(ctx, http_get=fake_get)
    assert result == []


def test_markaz_linked_documents_accepts_a_real_content_type():
    class FakeResponse:
        status_code = 200
        headers = {
            "content-type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        }
        content = b"real bytes"

    def fake_get(url, timeout=15):
        return FakeResponse()

    ctx = _ctx(links=("https://markaz.taleemabad.com/uploads/case-study-99.docx",))
    result = markaz_linked_documents(ctx, http_get=fake_get)
    assert len(result) == 1
    assert result[0].content == b"real bytes"


def test_markaz_linked_documents_uses_drive_download_for_drive_urls():
    calls = []
    real_length_id = "1AbC-XyZ9876543210abcdef"

    def fake_drive_download(file_id):
        calls.append(file_id)
        return "Case Study - Zara Khan.docx", b"drive bytes"

    ctx = _ctx(links=(f"https://drive.google.com/file/d/{real_length_id}/view",))
    result = markaz_linked_documents(ctx, drive_download=fake_drive_download)
    assert calls == [real_length_id]
    assert result[0].content == b"drive bytes"
    assert result[0].filename == "Case Study - Zara Khan.docx"


def test_markaz_case_study_api_treats_401_as_a_documented_wall_not_an_error():
    """The endpoint returning 401 to automation must never surface as an
    exception or be mistaken for 'the submission doesn't exist'."""

    class FakeResponse:
        status_code = 401
        headers = {}
        content = b""

    def fake_get(url, timeout=10):
        return FakeResponse()

    ctx = _ctx()
    result = markaz_case_study_api(ctx, http_get=fake_get)  # must not raise
    assert result == []


def test_markaz_case_study_api_tries_both_word_and_excel():
    seen_urls = []

    class FakeResponse:
        status_code = 200
        headers = {"content-type": "application/octet-stream"}
        content = b"file bytes"

    def fake_get(url, timeout=10):
        seen_urls.append(url)
        return FakeResponse()

    ctx = _ctx()
    result = markaz_case_study_api(ctx, http_get=fake_get)
    assert len(result) == 2
    assert any(url.endswith("/4242/word") for url in seen_urls)
    assert any(url.endswith("/4242/excel") for url in seen_urls)


def test_mailbox_attachments_is_injectable_and_filters_by_application_id_in_filename():
    """Filtering must be by APPLICATION ID inside the filename (Rule 18), not
    by subject text or MIME type -- both files ride the same notification."""

    class FakeMessagePart:
        def __init__(self, filename, payload):
            self._filename = filename
            self._payload = payload

        def get_filename(self):
            return self._filename

        def get_payload(self, decode=False):
            return self._payload

    class FakeEmailMessage:
        def __init__(self, parts):
            self._parts = parts

        def walk(self):
            return iter(self._parts)

    import email as email_lib

    from webapp.services import submissions as submissions_module

    wanted = FakeEmailMessage([
        FakeMessagePart("case-study-4242-word-171.docx", b"wanted bytes"),
        FakeMessagePart("case-study-4242-excel-171.xlsx", b"wanted bytes 2"),
    ])
    other_app = FakeEmailMessage([
        FakeMessagePart("case-study-9999-word-171.docx", b"other candidate bytes"),
    ])

    class FakeIMAP:
        def __init__(self):
            self.logged_out = False

        def select(self, mailbox, readonly=True):
            return "OK", [b"1"]

        def search(self, charset, criteria):
            return "OK", [b"1 2"]

        def fetch(self, msg_id, parts):
            return "OK", [(b"1", b"placeholder")]

        def logout(self):
            self.logged_out = True

    fake_client = FakeIMAP()
    orig_from_bytes = email_lib.message_from_bytes
    call_order = {"n": 0}

    def fake_from_bytes(raw):
        call_order["n"] += 1
        return wanted if call_order["n"] == 1 else other_app

    email_lib.message_from_bytes = fake_from_bytes
    try:
        result = submissions_module.mailbox_attachments(_ctx(), imap_factory=lambda: fake_client)
    finally:
        email_lib.message_from_bytes = orig_from_bytes

    assert fake_client.logged_out is True
    origins = [r.origin for r in result]
    assert any("case-study-4242-word-171.docx" in o for o in origins)
    assert any("case-study-4242-excel-171.xlsx" in o for o in origins)
    assert not any("9999" in o for o in origins)


def test_mailbox_attachments_never_constructs_a_real_imap_client(monkeypatch):
    """Structural guarantee: without an injected imap_factory, this fetcher
    must go through _default_imap_client (lazy-imported), never silently
    reach the network some other way inside a test."""
    import imaplib

    def boom(*a, **kw):
        raise AssertionError("a unit test must never construct a real IMAP4_SSL")

    monkeypatch.setattr(imaplib, "IMAP4_SSL", boom)

    class FakeIMAP:
        def select(self, *a, **kw):
            return "OK", [b""]

        def search(self, *a, **kw):
            return "OK", [b""]

        def logout(self):
            pass

    from webapp.services import submissions as submissions_module

    result = submissions_module.mailbox_attachments(_ctx(), imap_factory=lambda: FakeIMAP())
    assert result == []
