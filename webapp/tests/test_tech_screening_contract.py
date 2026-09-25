"""The scoring contract: the rubric's output_schema must reach the model.

THE BUG THESE EXIST FOR (2026-09-25, job 38 "AI Engineer Lead", run aef6ed75).
Ayesha ran 20 candidates. Every one failed and the page told her all 20 CVs
"could not be read". None of that was true.

`_call_model` called `drafting.draft()` -- the candidate-LETTER path -- passing
the rubric's system prompt and nothing else. The rubric's `output_schema` was
loaded, hashed, written to the run row, and never transmitted. A hash of a
contract nobody sent looks exactly like enforcement.

Reproduced against the live model before any of this was written:

    stop_reason  : end_turn        <- finished cleanly, NOT truncation
    output_tokens: 2912            <- nowhere near the 4096 ceiling
    returned     : must_have_skills, responsibility_alignment, stack_match,
                   technical_breadth, experience_depth, strengths, gaps,
                   hard_filters, confidence, overall_score, recommendation
    code read    : parsed["dimensions"]  ->  {}

All five dimensions were there. They were top-level instead of nested, so
`score_dimensions` raised on the first one, every candidate "failed", and the
run loop filed those failures under "could not be read".

Run: python -m pytest webapp/tests/test_tech_screening_contract.py -v
"""

from __future__ import annotations

import pytest

from webapp.services import drafting, screening_runs, tech_tiering

# The rubric's real dimension order, which matters: `must_have_skills` is
# FIRST, so the error named the first dimension and looked like the model had
# stopped early. It had not.
RUBRIC = {
    "dimensions": [
        {"key": "must_have_skills", "weight": 3, "label": "Must-have skills"},
        {"key": "responsibility_alignment", "weight": 2},
        {"key": "stack_match", "weight": 2},
        {"key": "technical_breadth", "weight": 1},
        {"key": "experience_depth", "weight": 2},
    ],
    "max_score": 100,
}

# What the model actually returned, shape-for-shape.
FLAT_RESPONSE = {
    "candidate_name": "A Candidate",
    "must_have_skills": {"raw": 4, "evidence": ["built RAG pipelines"]},
    "responsibility_alignment": {"raw": 3, "evidence": []},
    "stack_match": {"raw": 4, "evidence": []},
    "technical_breadth": {"raw": 3, "evidence": []},
    "experience_depth": {"raw": 2, "evidence": []},
    "strengths": ["ships production systems"],
    "gaps": ["no team leadership"],
    "hard_filters": {},
    "confidence": "medium",
    "overall_score": 68,
    "recommendation": "interview",
}


# --------------------------------------------------------------------------
# The shape the code reads
# --------------------------------------------------------------------------


def test_the_real_failing_response_is_understood_not_rejected():
    """The exact payload that failed 20 candidates now yields all 5 scores."""
    dims = screening_runs.normalise_dimensions(FLAT_RESPONSE, RUBRIC)
    assert sorted(dims) == sorted(d["key"] for d in RUBRIC["dimensions"])
    scores, total, _ = tech_tiering.score_dimensions(RUBRIC, dims)
    assert total > 0
    assert scores["must_have_skills"]["raw"] == 4


def test_the_old_reader_really_did_fail_on_this(caplog):
    """Proof the test above is load-bearing: reading `dimensions` directly --
    what the code used to do -- still raises on this very payload."""
    with pytest.raises(tech_tiering.TieringError) as exc:
        tech_tiering.score_dimensions(RUBRIC, FLAT_RESPONSE.get("dimensions") or {})
    assert "must_have_skills" in str(exc.value)


def test_a_correctly_nested_response_is_left_alone():
    nested = {"dimensions": {d["key"]: {"raw": 5} for d in RUBRIC["dimensions"]}}
    assert screening_runs.normalise_dimensions(nested, RUBRIC) == nested["dimensions"]


def test_nothing_is_invented_for_a_dimension_the_model_omitted():
    """Lifting is not guessing. A dimension absent from BOTH places stays
    absent, so the run still refuses rather than scoring a blank."""
    partial = {k: v for k, v in FLAT_RESPONSE.items() if k != "stack_match"}
    dims = screening_runs.normalise_dimensions(partial, RUBRIC)
    assert "stack_match" not in dims
    with pytest.raises(tech_tiering.TieringError):
        tech_tiering.score_dimensions(RUBRIC, dims)


def test_a_nested_value_wins_over_a_top_level_one_of_the_same_name():
    both = {"dimensions": {"must_have_skills": {"raw": 1}}, "must_have_skills": {"raw": 5}}
    assert screening_runs.normalise_dimensions(both, RUBRIC)["must_have_skills"]["raw"] == 1


def test_lifting_is_logged_rather_than_silent(caplog):
    """A shape drifting back is worth knowing about. Silence would let the
    same defect return with the symptom papered over."""
    with caplog.at_level("WARNING"):
        screening_runs.normalise_dimensions(FLAT_RESPONSE, RUBRIC)
    # getMessage() renders the %-args, which is what a reader would actually see.
    assert any("top level" in r.getMessage() for r in caplog.records)
    assert any("must_have_skills" in r.getMessage() for r in caplog.records)


# --------------------------------------------------------------------------
# The schema actually leaves the building
# --------------------------------------------------------------------------


class _SpyDrafter:
    """Records which path was taken and what was handed over."""

    calls: list = []
    model = "test-model"

    def __init__(self):
        self.structured_with = None
        self.drafted = False

    def structured(self, *, system, user, schema, tool_name="submit", max_tokens=8192):
        self.structured_with = {"schema": schema, "tool_name": tool_name,
                                "max_tokens": max_tokens}
        return {"dimensions": {}}

    def draft(self, **kw):
        self.drafted = True
        return {}


def test_the_rubric_schema_is_sent_to_the_model(monkeypatch):
    """🔴 THE REGRESSION. The schema used to be stored and never transmitted."""
    spy = _SpyDrafter()
    monkeypatch.setattr(drafting, "get_drafter", lambda: spy)
    schema = {"type": "object", "required": ["dimensions"]}

    screening_runs._call_model(
        system_prompt="rules", user_prompt="a cv", output_schema=schema,
    )

    assert spy.structured_with is not None, "the schema never reached the model"
    assert spy.structured_with["schema"] == schema
    assert spy.drafted is False, "scoring must not go through the letter path"


def test_without_a_schema_it_does_not_pretend_to_have_one(monkeypatch):
    spy = _SpyDrafter()
    monkeypatch.setattr(drafting, "get_drafter", lambda: spy)
    screening_runs._call_model(system_prompt="rules", user_prompt="a cv")
    assert spy.structured_with is None
    assert spy.drafted is True


def test_the_offline_stub_refuses_to_produce_a_score():
    """It may fake a letter. It must never fake a judgement about a person."""
    with pytest.raises(drafting.DraftingUnavailable):
        drafting.StubDrafter().structured(
            system="s", user="u", schema={"type": "object"},
        )


# --------------------------------------------------------------------------
# NUL bytes: one of the 20 died on this alone
# --------------------------------------------------------------------------


def test_nul_bytes_are_stripped_from_extracted_cv_text():
    """PostgreSQL text cannot hold 0x00, so one stray NUL from a PDF parser
    made the resume-cache INSERT raise DataError and took that candidate with
    it -- reported, of course, as a CV that could not be read."""
    assert "\x00" not in screening_runs._strip_nul("Ali\x00Khan\x00")


def test_stripping_removes_rather_than_replaces():
    """Replacing would shift every character offset after it, and evidence is
    quoted verbatim from this text."""
    assert screening_runs._strip_nul("ab\x00cd") == "abcd"


def test_no_cv_text_stays_none():
    assert screening_runs._strip_nul(None) is None


# --------------------------------------------------------------------------
# The model answers in SEVERAL tool_use blocks, not one
# --------------------------------------------------------------------------


class _Block:
    def __init__(self, type_, **kw):
        self.type = type_
        for k, v in kw.items():
            setattr(self, k, v)


class _Msg:
    def __init__(self, content, stop_reason="tool_use"):
        self.content = content
        self.stop_reason = stop_reason
        self.usage = type("U", (), {"input_tokens": 1, "output_tokens": 1,
                                    "cache_read_input_tokens": 0,
                                    "cache_creation_input_tokens": 0})()


class _FakeClient:
    def __init__(self, msg):
        self._msg = msg
        self.kwargs = None
        self.messages = self

    def create(self, **kw):
        self.kwargs = kw
        return self._msg


def _drafter_with(msg):
    d = drafting.AnthropicDrafter.__new__(drafting.AnthropicDrafter)
    d.model = "claude-haiku-4-5-20251001"
    d.degraded_from = None
    # `calls` is a lazy read-only property on the real class, so it is left
    # alone here rather than assigned -- the same way the other drafting tests
    # build this object with __new__.
    d.client = _FakeClient(msg)
    return d


def test_every_tool_use_block_is_merged_not_just_the_first():
    """🔴 MEASURED ON THE LIVE MODEL. Haiku 4.5 answered a real screening
    schema with SEVEN tool_use blocks, one per top-level property. Reading
    `content[0].input` gave {"extracted": ...} alone -- which reads downstream
    exactly like a model that refused to score, and produced the very same
    "did not score the dimension 'must_have_skills'" this file exists for."""
    msg = _Msg([
        _Block("tool_use", input={"extracted": {"years_total_experience": 4}}),
        _Block("tool_use", input={"dimensions": {"must_have_skills": {"score": 4}}}),
        _Block("tool_use", input={"strengths": ["ships"]}),
        _Block("tool_use", input={"gaps": ["no leadership"]}),
        _Block("tool_use", input={"confidence": "medium"}),
    ])
    out = _drafter_with(msg).structured(
        system="s", user="u", schema={"type": "object"}, tool_name="submit_screening",
    )
    assert sorted(out) == ["confidence", "dimensions", "extracted", "gaps", "strengths"]
    assert out["dimensions"]["must_have_skills"]["score"] == 4


def test_the_schema_is_forced_rather_than_merely_offered():
    """tool_choice "auto" would let the model answer in prose instead, which is
    how the whole contract went unenforced in the first place."""
    msg = _Msg([_Block("tool_use", input={"dimensions": {}})])
    d = _drafter_with(msg)
    schema = {"type": "object", "required": ["dimensions"]}
    d.structured(system="s", user="u", schema=schema, tool_name="submit_screening")

    sent = d.client.kwargs
    assert sent["tool_choice"] == {"type": "tool", "name": "submit_screening"}
    assert sent["tools"][0]["name"] == "submit_screening"
    # The rubric's own schema, plus the `additionalProperties: false` the API
    # demands on every object. Equality with the STORED schema is not the
    # contract: repairing it at send time is what keeps rubrics published
    # before that fix screenable without a migration.
    assert sent["tools"][0]["input_schema"] == {**schema, "additionalProperties": False}


def test_a_reply_cut_off_at_the_ceiling_is_refused_not_scored():
    """A truncated answer used to reach a regex that salvaged the outermost
    braces and produced a plausible, wrong object. Nothing checked stop_reason
    anywhere in the codebase."""
    msg = _Msg([_Block("tool_use", input={"dimensions": {}})], stop_reason="max_tokens")
    with pytest.raises(drafting.DraftingUnavailable) as exc:
        _drafter_with(msg).structured(system="s", user="u", schema={"type": "object"})
    assert "incomplete" in str(exc.value)


def test_a_model_that_answers_in_prose_is_an_error_not_an_empty_score():
    msg = _Msg([_Block("text", text="Here is my assessment...")], stop_reason="end_turn")
    with pytest.raises(ValueError):
        _drafter_with(msg).structured(system="s", user="u", schema={"type": "object"})


# --------------------------------------------------------------------------
# The CALLER must actually supply the schema
#
# 🔴 THE SECOND-ORDER BUG, and the sharper lesson of the two. The forced-tool
# fix was verified by calling `_call_model` with a schema and watching it work.
# Nobody checked that `work()` SUPPLIES one. Its rubric SELECT did not include
# `output_schema`, so `rubric.get("output_schema")` was None on every real run
# and scoring fell straight back to the prose path -- for every job, while the
# column sat populated in the database the whole time.
#
# Run 1b44a642 scored 67 candidates that way and looked fine, because
# `normalise_dimensions` lifted the flattened dimensions. Only the one
# candidate whose prose happened to be malformed JSON failed, which is the
# single thread that surfaced it.
#
# A function that works when called correctly proves nothing about the code
# that calls it.
# --------------------------------------------------------------------------


def test_the_run_selects_every_column_scoring_reads():
    """The contract between the rubric query and `score_one`, asserted as a
    column set rather than a string match, so it survives reformatting."""
    sql = screening_runs._RUBRIC_FOR_RUN_SQL.lower()
    selected = sql.split("select", 1)[1].split("from", 1)[0]
    columns = {c.strip() for c in selected.split(",")}
    for needed in screening_runs.RUBRIC_COLUMNS_SCORING_NEEDS:
        assert needed in columns, (
            f"the run's rubric SELECT is missing {needed!r}; scoring reads it"
        )


def test_output_schema_is_among_them():
    """Named on its own, because this is the one that went missing and the
    column set above would pass if somebody removed it from BOTH places."""
    assert "output_schema" in screening_runs.RUBRIC_COLUMNS_SCORING_NEEDS
    assert "output_schema" in screening_runs._RUBRIC_FOR_RUN_SQL


def test_a_rubric_without_its_schema_refuses_rather_than_scoring_in_prose(monkeypatch):
    """Refuse, do not degrade. The prose fallback produces plausible
    evaluations that get written to the database, so a silent switch changes
    how every candidate is judged with nothing in the output saying so."""
    called = []
    monkeypatch.setattr(screening_runs, "_call_model",
                        lambda **kw: called.append(kw) or ({}, "m", {}, 1))
    monkeypatch.setattr(screening_runs, "_one", lambda db, sql, **kw: {
        "candidate_id": 1, "first_name": "A", "last_name": "B", "email": "a@b.c",
        "applied_at": None, "cover_letter": None, "custom_answers": None,
        "canned_answers": None, "resume_data": None,
    })
    monkeypatch.setattr(screening_runs, "_resume_for",
                        lambda db, row: ("a cv " * 200, {
                            "chars": 1000, "health": 100, "issues": [],
                            "type": "pdf", "truncated": False,
                            "parse_success": True, "parse_error": None}))
    monkeypatch.setattr(screening_runs.tech_tiering, "route_unscorable",
                        lambda **kw: None)

    rubric = {"id": "r1", "version": 1, "system_prompt": "rules",
              "dimensions": [{"key": "a", "weight": 1}], "max_score": 100}
    run = {"id": "run1", "job_id": 24, "model": "m", "effort": "medium"}

    with pytest.raises(screening_runs.RunError) as exc:
        screening_runs.score_one(None, run=run, rubric=rubric, application_id=1)

    assert "output_schema" in str(exc.value)
    assert called == [], "it fell back to the unconstrained path instead of refusing"


# --------------------------------------------------------------------------
# additionalProperties: the API refuses a schema without it
#
# 🔴 Run 4b3a144f, 66 of 76 candidates lost to a 400 on every single one:
# "output_config.format.schema: For 'object' type, 'additionalProperties' must
# be explicitly set to false".
#
# The forced-schema fix had been verified against job 38's rubric, which is
# hand-edited and already carried the flag. Job 24's was the first rubric a
# MODEL had written, and it was missing the flag on nine nodes including the
# root. Verifying against one sample of a population is not verifying.
# --------------------------------------------------------------------------


def _missing_additional_properties(node, path="$"):
    bad = []
    if isinstance(node, dict):
        if node.get("type") == "object" and "additionalProperties" not in node:
            bad.append(path)
        for k, v in node.items():
            bad += _missing_additional_properties(v, f"{path}.{k}")
    elif isinstance(node, list):
        for i, v in enumerate(node):
            bad += _missing_additional_properties(v, f"{path}[{i}]")
    return bad


# The shape job 24's rubric actually had: no flag at the root, on `extracted`,
# on `dimensions`, or on any dimension inside it.
LOOSE_SCHEMA = {
    "type": "object",
    "required": ["dimensions", "extracted"],
    "properties": {
        "dimensions": {
            "type": "object",
            "required": ["frontend_craft"],
            "properties": {
                "frontend_craft": {
                    "type": "object",
                    "required": ["raw"],
                    "properties": {
                        "raw": {"type": "integer", "minimum": 0, "maximum": 5},
                        "evidence": {"type": "array", "items": {"type": "string"}},
                    },
                },
            },
        },
        "extracted": {"type": "object"},
        "confidence": {"enum": ["high", "medium", "low"]},
    },
}


def test_the_real_rejected_schema_is_repaired():
    assert _missing_additional_properties(LOOSE_SCHEMA), "fixture is not loose"
    strict = drafting.AnthropicDrafter._strict_schema(LOOSE_SCHEMA)
    assert _missing_additional_properties(strict) == []
    assert strict["additionalProperties"] is False
    assert strict["properties"]["dimensions"]["additionalProperties"] is False
    assert (strict["properties"]["dimensions"]["properties"]
            ["frontend_craft"]["additionalProperties"] is False)


def test_the_properties_map_itself_is_never_given_the_flag():
    """`properties` is a MAP of names to schemas, not a schema. Setting the
    flag on it would invent a property called additionalProperties."""
    strict = drafting.AnthropicDrafter._strict_schema(LOOSE_SCHEMA)
    assert "additionalProperties" not in strict["properties"]
    assert "additionalProperties" not in strict["properties"]["dimensions"]["properties"]


def test_a_property_literally_named_type_does_not_confuse_it():
    loose = {"type": "object", "properties": {"type": {"type": "string"}}}
    strict = drafting.AnthropicDrafter._strict_schema(loose)
    assert strict["additionalProperties"] is False
    assert "additionalProperties" not in strict["properties"]["type"]


def test_an_already_strict_schema_is_unchanged():
    """Three of the four live rubrics are hand-edited and already correct;
    repairing them must be a no-op, not a rewrite."""
    strict_once = drafting.AnthropicDrafter._strict_schema(LOOSE_SCHEMA)
    assert drafting.AnthropicDrafter._strict_schema(strict_once) == strict_once


def test_an_explicit_true_is_respected_not_overwritten():
    loose = {"type": "object", "additionalProperties": True, "properties": {}}
    assert drafting.AnthropicDrafter._strict_schema(loose)["additionalProperties"] is True


def test_the_schema_sent_to_the_api_is_the_repaired_one():
    """The whole point: repair happens at SEND time, so a rubric published
    before this fix is screenable without a migration."""
    msg = _Msg([_Block("tool_use", input={"dimensions": {}})])
    d = _drafter_with(msg)
    d.structured(system="s", user="u", schema=LOOSE_SCHEMA, tool_name="submit_screening")
    sent = d.client.kwargs["tools"][0]["input_schema"]
    assert _missing_additional_properties(sent) == []


def test_a_newly_drafted_rubric_is_born_strict():
    """The other half. Repairing at send time keeps old rubrics working;
    this stops new ones being written wrong in the first place."""
    from webapp.services import rubric_drafting

    schema = rubric_drafting.output_schema(
        {"dimensions": [{"key": "alpha"}, {"key": "beta"}]}
    )
    assert _missing_additional_properties(schema) == []
    assert schema["additionalProperties"] is False
