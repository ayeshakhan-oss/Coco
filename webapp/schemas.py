"""Pydantic response schemas for the API."""

from __future__ import annotations

import datetime as dt
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field


class _Base(BaseModel):
    model_config = ConfigDict(extra="ignore", from_attributes=True)


class CurrentUserOut(_Base):
    id: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    app_role: str


class UserOut(_Base):
    id: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    app_role: str
    active: bool
    last_login_at: Optional[dt.datetime] = None
    created_at: Optional[dt.datetime] = None


class UserCreate(_Base):
    email: str
    app_role: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserUpdate(_Base):
    app_role: Optional[str] = None
    active: Optional[bool] = None


class JobItem(_Base):
    job_pk: int
    job_code: Optional[str] = None
    title: Optional[str] = None
    job_status: Optional[str] = None
    department: Optional[str] = None


class QueueRow(_Base):
    application_id: int
    candidate_id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    job_pk: Optional[int] = None
    job_code: Optional[str] = None
    job_title: Optional[str] = None
    job_status: Optional[str] = None
    status: Optional[str] = None
    values_filled: bool = False
    gwc_filled: bool = False
    values_interview_result: Optional[str] = None
    scorecard_date: Optional[dt.datetime] = None
    interviewer: Optional[str] = None
    sent_count: int = 0
    active_count: int = 0
    last_sent_at: Optional[dt.datetime] = None
    prior_platform_comms: int = 0
    bucket: str
    # Markaz <-> Gmail communication-sync dimensions (Phase 1+).
    applied_at: Optional[dt.datetime] = None
    days_waiting: Optional[int] = None
    gmail_status: str = "not_checked"
    comm_required: bool = False
    required_email_type: Optional[str] = None
    is_high_priority: bool = False
    has_evidence: bool = False
    manual_marked: bool = False
    ignored: bool = False
    display_status: Optional[str] = None


class QueueStats(_Base):
    needs_comms: int
    high_priority: int = 0
    in_progress: int
    sent: int
    needs_review: int = 0
    shortlisted: int = 0
    awaiting_scorecard: int
    ignored: int = 0
    scored: int
    total: int
    total_applications: int = 0
    total_candidates: int = 0
    open_positions: int = 0


class PositionSummary(_Base):
    job_pk: int
    job_code: Optional[str] = None
    job_title: Optional[str] = None
    needs_comms: int
    high_priority: int = 0
    in_progress: int
    sent: int
    needs_review: int = 0
    shortlisted: int = 0
    awaiting_scorecard: int = 0
    scored: int
    total: int = 0
    last_gmail_sync_at: Optional[dt.datetime] = None


class ScorecardValueItem(_Base):
    name: str
    rating: str = ""
    deep_dive: str = ""
    curve_ball: str = ""
    micro_case: str = ""


class ScorecardResponse(_Base):
    application_id: int
    values: Optional[dict[str, Any]] = None  # normalized values scorecard
    gwc: Optional[dict[str, Any]] = None  # normalized gwc scorecard


class CommHistoryItem(_Base):
    sent_at: Optional[str] = None
    sent_by: Optional[str] = None
    status: Optional[str] = None
    subject: Optional[str] = None
    template_name: Optional[str] = None
    recipient_email: Optional[str] = None
    cc_emails: list[str] = []
    source: str = "markaz"


class EvalViolation(_Base):
    rule: str
    severity: str
    detail: str


class EvalResult(_Base):
    passed: bool
    word_count: int
    violations: list[EvalViolation] = []


class GenerateRequest(_Base):
    application_id: int
    email_type: str
    role_title: Optional[str] = None


class DraftUpdate(_Base):
    # Structured content edited in the section editor; the body HTML is rendered
    # from this server-side (so the locked v8 layout can't drift).
    title_line: str
    role_title: Optional[str] = None
    content: dict[str, Any]


class CommunicationOut(_Base):
    id: str
    application_id: Optional[int] = None
    candidate_id: int
    job_id: Optional[int] = None
    email_type: str
    subject: Optional[str] = None
    title_line: Optional[str] = None
    role_title: Optional[str] = None
    body_html: Optional[str] = None
    draft_content: Optional[dict[str, Any]] = None
    status: str
    mode: Optional[str] = None
    word_count: Optional[int] = None
    eval_result: Optional[dict[str, Any]] = None
    eval_passed: Optional[bool] = None
    sent_to: Optional[list[str]] = None
    message_id: Optional[str] = None
    error_detail: Optional[str] = None
    created_by: Optional[str] = None
    approved_by: Optional[str] = None
    created_at: Optional[dt.datetime] = None
    updated_at: Optional[dt.datetime] = None
    submitted_at: Optional[dt.datetime] = None
    approved_at: Optional[dt.datetime] = None
    sent_at: Optional[dt.datetime] = None


class GenerateResponse(_Base):
    communication: CommunicationOut
    eval: EvalResult
    attempts: int
    drafter_used: str


class SendRequest(_Base):
    mode: str = "pilot"  # 'pilot' | 'live'


class SendResponse(_Base):
    communication: CommunicationOut
    mode: str
    subject: str
    recipients: list[str]
    message_id: Optional[str] = None


class ApplicationDetail(_Base):
    application_id: int
    candidate_id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    job_pk: Optional[int] = None
    job_code: Optional[str] = None
    job_title: Optional[str] = None
    job_status: Optional[str] = None
    status: Optional[str] = None
    stage: Optional[str] = None
    values_filled: bool = False
    gwc_filled: bool = False
    values_interview_result: Optional[str] = None
    values_interview_date: Optional[dt.datetime] = None
    values_interviewer_name: Optional[str] = None
    gwc_interview_result: Optional[str] = None
    gwc_interview_date: Optional[dt.datetime] = None
    gwc_interviewer_name: Optional[str] = None
    comm_history: list[CommHistoryItem] = []
    # Markaz <-> Gmail communication-sync dimensions + evidence (Phase 1+).
    applied_at: Optional[dt.datetime] = None
    days_waiting: Optional[int] = None
    comm_required: bool = False
    required_email_type: Optional[str] = None
    is_high_priority: bool = False
    has_evidence: bool = False
    manual_marked: bool = False
    ignored: bool = False
    display_status: Optional[str] = None
    gmail_status: str = "not_checked"
    gmail_match: Optional["GmailMatch"] = None


class GmailMatch(_Base):
    """The Gmail Sent evidence for one application (drives 'View Gmail match')."""
    gmail_status: str = "not_checked"
    match_method: Optional[str] = None
    matched_message_id: Optional[str] = None
    gmail_thread_id: Optional[str] = None
    internal_date: Optional[dt.datetime] = None
    matched_subject: Optional[str] = None
    matched_to: Optional[str] = None
    matched_snippet: Optional[str] = None
    uncertain_reason: Optional[str] = None
    marked_sent_at: Optional[dt.datetime] = None
    marked_sent_by: Optional[str] = None
    marked_sent_reason: Optional[str] = None
    ignored: bool = False
    ignored_at: Optional[dt.datetime] = None
    checked_at: Optional[dt.datetime] = None


class GmailSyncStatusOut(_Base):
    last_sync_at: Optional[dt.datetime] = None
    status: Optional[str] = None
    trigger: Optional[str] = None
    messages_scanned: Optional[int] = None
    candidates_evaluated: Optional[int] = None
    found_count: Optional[int] = None
    uncertain_count: Optional[int] = None
    none_count: Optional[int] = None
    started_at: Optional[dt.datetime] = None
    finished_at: Optional[dt.datetime] = None
    error_detail: Optional[str] = None


class MarkSentRequest(_Base):
    reason: Optional[str] = None


class IgnoreRequest(_Base):
    ignored: bool = True


class BulkMarkSentRequest(_Base):
    application_ids: list[int]
    reason: Optional[str] = None


class BulkIgnoreRequest(_Base):
    application_ids: list[int]
    ignored: bool = True


class BulkResult(_Base):
    updated: int


class TimelineItem(_Base):
    source: str  # 'markaz' | 'gmail' | 'coco'
    ts: Optional[str] = None
    subject: Optional[str] = None
    actor: Optional[str] = None
    snippet: Optional[str] = None
    link: Optional[str] = None


# Resolve the forward reference (GmailMatch is defined after ApplicationDetail).
ApplicationDetail.model_rebuild()


class ScreenedJob(_Base):
    job_id: int
    job_title: Optional[str] = None
    rubric_version: int
    rubric_status: str
    seniority: Optional[str] = None
    scored: int
    unusable: int
    last_run_at: Optional[dt.datetime] = None


class TierBucket(_Base):
    tier: str
    status: Optional[str] = None
    n: int
    avg_pct: Optional[float] = None
    min_pct: Optional[float] = None
    max_pct: Optional[float] = None
    is_unusable: bool
    is_unscored: bool = False


class EvaluationSummary(_Base):
    tiers: list[TierBucket]
    scored: int
    unusable: int
    # Rows counted in `scored` whose score is meaningless (MANUAL_REVIEW, and
    # any future tier in UNSCORED_TIERS) because the document never cleared
    # the readability floor. `scored` and `unusable` keep their existing
    # meaning; this is an additional, overlapping count so a caller can see
    # how many "scored" candidates actually need a human to open the CV.
    unscored: int = 0
    total: int


class EvaluationRow(_Base):
    application_id: Optional[int] = None
    candidate_id: Optional[int] = None
    candidate_name: Optional[str] = None
    candidate_email: Optional[str] = None
    score_pct: Optional[float] = None
    tier: Optional[str] = None
    tier_reason: Optional[str] = None
    confidence: Optional[str] = None
    resume_health: Optional[int] = None
    is_unusable: bool = False
    is_unscored: bool = False


class CandidatePage(_Base):
    """Response shape for GET /api/evaluations/jobs/{job_id}/candidates.

    Was a bare `list[EvaluationRow]`; changed to an object carrying `total`
    (finding 3) so a caller can tell there are more rows beyond the current
    page. NOTE: this is a response-shape change — the frontend consuming
    this endpoint needs updating to read `.rows` instead of the bare array.
    """

    rows: list[EvaluationRow]
    total: int


class EvaluationDetail(EvaluationRow):
    # `dimension_scores` and `hard_filter_flags` dropped (finding 7): raw
    # rubric internals with no frontend consumer.
    strengths: Optional[list[Any]] = None
    gaps: Optional[list[Any]] = None
    verdict: Optional[str] = None
    rubric_version: Optional[int] = None
    model: Optional[str] = None
    evaluated_at: Optional[dt.datetime] = None


# --------------------------------------------------------------------------
# Values scorecard draft lifecycle (webapp/routers/values_scorecards.py).
# --------------------------------------------------------------------------


class ValuesScorecardGenerateRequest(_Base):
    application_id: int
    transcript: str
    host: str
    # The actual interview date (not the date the scorecard is generated or
    # submitted). Optional: submit() falls back to today, visibly, when this
    # is never supplied.
    interview_date: Optional[dt.date] = None


class ValuesScorecardEdit(_Base):
    """Edit evidence text and/or ratings on a draft. Supplying `values`
    re-runs validate_values and RECOMPUTES the verdict from the edited
    ratings server-side; the verdict is never taken from the client."""

    values: Optional[list[dict[str, Any]]] = None
    final_comments: Optional[str] = None
    proceed: Optional[bool] = None
    # Same "None means unchanged" convention as the other fields above --
    # there is no PATCH-time way to explicitly clear it back to unset.
    interview_date: Optional[dt.date] = None


class ValuesScorecardSubmitRequest(_Base):
    """`overwrite=True` is the explicit, deliberate override required to
    replace an application's EXISTING Markaz `values_scorecard`. Defaulted so
    a plain POST with no body still submits normally in the (far more common)
    case where the target application has no scorecard yet."""

    overwrite: bool = False


class ValuesScorecardOut(_Base):
    id: str
    application_id: int
    candidate_name: str
    host: str
    transcript_sha256: str
    interview_date: Optional[dt.date] = None
    values: list[dict[str, Any]]
    gwc: Optional[dict[str, Any]] = None
    final_comments: str
    proceed: bool
    tally: dict[str, int]
    verdict: str
    status: str
    model: str
    created_by: str
    created_at: Optional[dt.datetime] = None
    approved_by: Optional[str] = None
    approved_at: Optional[dt.datetime] = None
    submitted_at: Optional[dt.datetime] = None
    markaz_payload: Optional[dict[str, Any]] = None
    replaced_payload: Optional[dict[str, Any]] = None


# --------------------------------------------------------------------------
# Case-study benchmark + scoring lifecycle (webapp/routers/case_studies.py).
# --------------------------------------------------------------------------


class CaseStudyBenchmarkCreateRequest(_Base):
    job_id: int
    title: str
    body: str
    kind: str = "case_study"
    source_path: Optional[str] = None


class CaseStudyBenchmarkOut(_Base):
    id: str
    job_id: int
    kind: str
    title: str
    body: str
    source_path: Optional[str] = None
    created_by: str
    created_at: Optional[dt.datetime] = None
    qa_approved_by: Optional[str] = None
    qa_approved_at: Optional[dt.datetime] = None
    status: str


class CaseStudyScoreRequest(_Base):
    application_id: int


class CaseStudyDimensionOut(_Base):
    """One rubric dimension's metadata (IMPORTANT 4): key/label/weight,
    mirrored verbatim from `case_study_scoring.DIMENSIONS` so the frontend
    never has to keep its own copy in sync by hand."""

    key: str
    label: str
    weight: int


class CaseStudyEvaluationOut(_Base):
    id: str
    application_id: int
    job_id: int
    benchmark_id: str
    candidate_name: str
    role: str
    scores: dict[str, int]
    evidence: dict[str, str]
    flags: list[str]
    total: float
    band: str
    model: str
    sources: list[str]
    rubric_sha256: str
    corpus_chars: int
    created_by: str
    created_at: Optional[dt.datetime] = None
    # IMPORTANT 4: the rubric's dimension metadata, carried on every response
    # so the page can render from `evaluation.dimensions` instead of a local
    # TypeScript constant that can drift from case_study_scoring.DIMENSIONS.
    dimensions: list[CaseStudyDimensionOut] = []


# --------------------------------------------------------------------------
# CV screening (Skill 02, cv-screening). Coco's OWN criteria -- never Nugget's.
# --------------------------------------------------------------------------


class CVScreenCriterionOut(_Base):
    """One criterion's metadata, mirrored verbatim from
    `cv_screening.CRITERIA` so the frontend never keeps its own copy."""

    key: str
    label: str
    weight: int
    priority: str


class CVScreenRequest(_Base):
    application_id: int


class CVScreenOut(_Base):
    id: str
    application_id: int
    job_id: int
    candidate_name: str
    role: str
    scores: dict[str, int]
    evidence: dict[str, str]
    strengths: list[str]
    gaps: list[str]
    # Two figures, never one.
    total_experience_years: float
    relevant_experience_years: float
    relevant_experience_note: str
    match: float
    tier: str
    model: str
    sop_sha256: str
    jd_sha256: str
    cv_chars: int
    cv_truncated: bool
    is_current: bool
    superseded_by: Optional[str] = None
    created_by: str
    created_at: Optional[dt.datetime] = None
    criteria: list[CVScreenCriterionOut] = []


class CVScreenSkipOut(_Base):
    """Why a candidate has no screen, when the reason is their CV.

    🔴 NOT A RESULT AND NOT A LOW SCORE. A CV that will not open is a
    document problem needing a person; scoring what could not be read is the
    failure mode `cv_screening` refuses in order to avoid (CLAUDE.md Rule 32).
    Surfaced so "could not be read" stops reading as "not looked at yet".
    """

    application_id: int
    # no_cv | unreadable | too_short
    kind: str
    # The screener's own words, kept verbatim.
    reason: str
    # What the file was called in Markaz, which is what somebody chasing a
    # missing CV actually needs.
    cv_file_name: Optional[str] = None
    recorded_at: Optional[dt.datetime] = None


class CVScreenApplicationOut(_Base):
    """One application in a job's screening list: who they are, the profile
    fields the SOP requires captured, and their CURRENT screen if there is one."""

    application_id: int
    candidate_name: str
    email: Optional[str] = None
    status: Optional[str] = None
    applied_at: Optional[dt.datetime] = None
    # The SOP requires these captured for every candidate. None means the
    # candidate was not asked or did not answer -- never a guess.
    expected_salary: Optional[str] = None
    city: Optional[str] = None
    willing_to_relocate: Optional[str] = None
    cv_available: bool = False
    cv_error: Optional[str] = None
    screen: Optional[CVScreenOut] = None
    # Set when the CV could not be read. A row carries a screen or a skip,
    # never both: a successful screen deletes the skip.
    skip: Optional[CVScreenSkipOut] = None


class CVScreenJobSummaryOut(_Base):
    """The four stat boxes the locked report format requires, which must sum."""

    job_id: int
    title: Optional[str] = None
    total: int
    shortlist: int
    maybe: int
    no_hire: int
    # Work REMAINING. Excludes candidates whose CV cannot be read, which is not
    # work anyone can do by screening again.
    unscreened: int
    # Attempted and refused: no resume stored, an unreadable file, or too few
    # words to screen on. shortlist + maybe + no_hire + unreadable + unscreened
    # == total.
    unreadable: int = 0
    jd_chars: int
    jd_error: Optional[str] = None


# --------------------------------------------------------------------------
# Case-study tracking (Skill 02, case-study-evaluation). Tracking and
# completeness only -- scoring is CaseStudyEvaluationOut above.
# --------------------------------------------------------------------------


class CaseStudyFlagOut(_Base):
    """A content-dump signal, always with the evidence that raised it: a flag
    a human cannot check is an accusation rather than a signal."""

    flag: str
    count: int
    evidence: str
    meaning: str


class CaseStudyProbeOut(_Base):
    id: str
    application_id: int
    job_id: int
    channels: list[str]
    # 🔴 send_found=False means "we could not find a send", NEVER "not sent":
    # Markaz records no case-study send anywhere.
    send_found: bool
    send_subject: Optional[str] = None
    send_at: Optional[dt.datetime] = None
    status: str
    corpus_chars: int
    sources: list[str] = []
    corpus_error: Optional[str] = None
    flags: list[CaseStudyFlagOut] = []
    completeness: dict = {}
    probed_by: str
    probed_at: Optional[dt.datetime] = None


class CaseStudyTrackingRowOut(_Base):
    application_id: int
    candidate_name: str
    email: Optional[str] = None
    # What Markaz holds, read live on every request (cheap).
    channels: list[str]
    submitted_at: Optional[dt.datetime] = None
    markaz_status: Optional[str] = None
    # The reconciled status, which folds in the last probe if there is one.
    status: str
    probe: Optional[CaseStudyProbeOut] = None


class CaseStudyTrackingSummaryOut(_Base):
    job_id: int
    title: Optional[str] = None
    total: int
    submitted: int
    awaiting: int
    no_record_of_a_send: int
    submitted_without_send_record: int
    # The number of candidates a reader must NOT describe as "not sent one".
    unproven_absence: int
    probed: int


class CaseStudyProbeRequest(_Base):
    application_id: int
    # The assignment's own section names. Without them completeness is reported
    # as unknown rather than guessed from the submission's own headings.
    required_parts: Optional[list[str]] = None


class CaseStudyMirrorPairOut(_Base):
    """Two submissions sharing long verbatim runs. Carries the shared text and
    NO cause: two candidates quoting the same paragraph of the assignment look
    identical to two sharing an assistant."""

    application_ids: list[int]
    candidate_names: list[str] = []
    shared_runs: int
    examples: list[str]


# --------------------------------------------------------------------------
# KCD evaluation (Skill 02, kcd-evaluation). A human evaluation with the rules
# enforced -- NOT a model score. "KCD" is internal; reports say "case study".
# --------------------------------------------------------------------------


class KCDDimensionOut(_Base):
    key: str
    label: str
    weight: int
    asks: str


class KCDFrameworkOut(_Base):
    """Everything the UI needs to render the form without a local copy of the
    rules that could drift from the service."""

    dimensions: list[KCDDimensionOut]
    scores: list[float]
    verdicts: list[str]
    gwc_threshold: float
    cap_insight_without_evidence: float
    cap_evidence_without_interpretation: float


class KCDCapsIn(_Base):
    insight_without_evidence: list[str] = []
    evidence_without_interpretation: list[str] = []


class KCDEvaluationRequest(_Base):
    application_id: int
    scores: dict[str, float]
    evidence: dict[str, str]
    weights: Optional[dict[str, float]] = None
    caps: KCDCapsIn = KCDCapsIn()
    # Required when the computed verdict is CONDITIONAL; the request is
    # refused otherwise, because a conditional with no condition is not
    # actionable.
    condition: Optional[str] = None
    incomplete: bool = False
    missing_parts: list[str] = []
    integrity_flags: list[dict] = []
    second_evaluator: Optional[str] = None
    second_total: Optional[float] = None


class KCDCrossCheckOut(_Base):
    status: str
    delta: Optional[float] = None
    note: str


class KCDEvaluationOut(_Base):
    id: str
    application_id: int
    job_id: int
    candidate_name: str
    role: str
    scores: dict[str, float]
    evidence: dict[str, str]
    weights: Optional[dict[str, float]] = None
    caps_applied: dict = {}
    total: float
    verdict: str
    condition: Optional[str] = None
    advances_to_gwc: bool
    incomplete: bool
    missing_parts: list[str] = []
    integrity_flags: list[dict] = []
    second_evaluator: Optional[str] = None
    second_total: Optional[float] = None
    cross_check: Optional[KCDCrossCheckOut] = None
    is_current: bool
    superseded_by: Optional[str] = None
    created_by: str
    created_at: Optional[dt.datetime] = None
    dimensions: list[KCDDimensionOut] = []
    # An incomplete submission's score rendered the SOP's way: asterisk plus a
    # plain statement that it is a floor.
    display_score: Optional[str] = None


class KCDCohortOut(_Base):
    """A job's evaluations, ranked -- with incomplete submissions in their own
    list so one can never be ranked above a complete one."""

    job_id: int
    ranked: list[KCDEvaluationOut]
    incomplete: list[KCDEvaluationOut]
    note: Optional[str] = None
    gwc_threshold: float
    advancing: int


class CVScreenSkippedOut(_Base):
    """A candidate the batch could not screen. RETURNED, never dropped: a CV
    that would not open must be visible as needing a human, not absent."""

    application_id: int
    reason: str


class CVScreenBatchRequest(_Base):
    job_id: int
    # A small slice per request. Each CV is a model call of roughly 15 seconds,
    # so a whole position in one request would exceed any HTTP timeout.
    limit: int = Field(default=4, ge=1, le=10)
    # Cursor: the highest application id already processed. It is what makes
    # the loop terminate, since a candidate whose CV cannot be read never gets
    # a screen row and would otherwise be handed back for ever.
    after: Optional[int] = None
    # Deliberately try the CVs already recorded as unreadable, after the files
    # have been fixed in Markaz. Off by default: re-reading a JPEG costs real
    # time and changes nothing, and a run that keeps retrying them never ends
    # in a state anyone can act on.
    retry_skipped: bool = False


class CVScreenBatchOut(_Base):
    job_id: int
    screened: list[CVScreenOut] = []
    skipped: list[CVScreenSkippedOut] = []
    last_application_id: Optional[int] = None
    remaining: int


# --------------------------------------------------------------------------
# Hiring Operations: daily attendance (Skill 03, attendance-reports)
# --------------------------------------------------------------------------


class AttendancePersonOut(_Base):
    user_id: int
    name: Optional[str] = None
    payroll_entity: Optional[str] = None
    department: Optional[str] = None
    job_title: Optional[str] = None
    category: str
    leave_type: Optional[str] = None
    sub_category: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    is_half_day: bool = False


class AttendanceCorrectionOut(_Base):
    """A leave record whose dates cannot be true. Shown so somebody fixes it in
    Markaz: excluding it silently leaves tomorrow's report wrong too."""

    user_id: Optional[int] = None
    name: Optional[str] = None
    leave_type: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    problem: str


class AttendanceStatBoxOut(_Base):
    label: str
    value: int
    colour: str


class AttendanceReportOut(_Base):
    date: str
    weekday: str
    entities: list[str]
    total_on_payroll: int
    # 🔴 Never "onsite" or "present". Markaz records absence, not attendance.
    no_absence_recorded: int
    on_leave: list[AttendancePersonOut] = []
    working_from_home: list[AttendancePersonOut] = []
    needs_correction: list[AttendanceCorrectionOut] = []
    stat_boxes: list[AttendanceStatBoxOut] = []
    presence_caveat: str
    source: str


# --------------------------------------------------------------------------
# Hiring Operations: decision brief (Skill 03, decision-briefs)
# --------------------------------------------------------------------------


class DecisionBriefPersonOut(_Base):
    application_id: int
    name: str
    # Served by this app from Markaz, so no manual Drive upload stands between
    # the brief and a working link. The SOP calls this non-negotiable.
    cv_url: str
    has_cv: bool
    status: Optional[str] = None
    # None means no values interview on record. False means interviewed and did
    # not pass. Collapsing the two puts people in the wrong group.
    passed_values: Optional[bool] = None
    values_disagreement: Optional[str] = None
    values_comments: Optional[str] = None
    submitted_case_study: bool = False
    case_study_band: Optional[str] = None
    case_study_total: Optional[float] = None
    cv_screen_tier: Optional[str] = None
    cv_screen_match: Optional[float] = None
    debrief_verdict: str
    debrief_date: Optional[str] = None
    group: str


class DecisionBriefGroupOut(_Base):
    key: str
    title: str
    people: list[DecisionBriefPersonOut] = []


class DecisionBriefNotRecordedOut(_Base):
    """Counted and stated, never left as a blank for a reader to interpret."""

    debrief_verdicts: int
    case_study_scores: int
    missing_cv: int


class DecisionBriefStatBoxOut(_Base):
    label: str
    value: int
    colour: str


class DecisionBriefOut(_Base):
    job_id: Optional[int] = None
    job_title: Optional[str] = None
    generated_on: str
    total_applications: int
    values_interviews: int
    shortlisted: int
    leading: list[DecisionBriefPersonOut] = []
    # Set when nothing can separate the leading candidates, so their
    # order is never mistaken for a ranking.
    leading_note: Optional[str] = None
    groups: list[DecisionBriefGroupOut] = []
    debrief_schedule: list[DecisionBriefPersonOut] = []
    not_recorded: DecisionBriefNotRecordedOut
    evidence_caveat: str
    stat_boxes: list[DecisionBriefStatBoxOut] = []


# --------------------------------------------------------------------------
# Hiring Operations: hiring decision brief (Skill 03, hiring-decision-brief)
# The funnel PLUS the recommendations, which is what that SOP asks for.
# --------------------------------------------------------------------------


class FunnelStageOut(_Base):
    key: str
    title: str
    # None means the stage could not be established, which the page renders as
    # "not visible". Never 0, which would read as "nobody".
    count: Optional[int] = None
    source: str
    is_floor: bool = False
    note: Optional[str] = None


class HiringBriefOut(_Base):
    job_id: Optional[int] = None
    job_title: Optional[str] = None
    total_applications: int
    stages: list[FunnelStageOut] = []
    evidence_synced_at: Optional[str] = None
    caveat: str
    # Stages where the funnel widened instead of narrowing.
    inconsistencies: list[str] = []
    brief: DecisionBriefOut


# --------------------------------------------------------------------------
# Technical screening (Skill 02, technical-screening). These are NUGGET's
# tiers and rubric vocabulary, deliberately distinct from Coco's own CV
# screening, which uses shortlist/maybe/no_hire and must never borrow P1-P4
# (Ayesha, 2026-09-15). The two remain separate systems that now share one
# engine for launching runs.
# --------------------------------------------------------------------------


class TechJobOut(_Base):
    job_pk: int
    job_code: Optional[str] = None
    title: str
    department: Optional[str] = None
    job_status: Optional[str] = None
    applications: int = 0
    scored: int = 0
    has_rubric: bool = False
    rubric_version: Optional[int] = None
    # Set when a run is already live for this job, so Confirm can be disabled
    # with the reason rather than failing on uq_nsrun_one_active_per_job.
    live_run_id: Optional[str] = None
    live_run_status: Optional[str] = None


class TechDimensionOut(_Base):
    key: str
    label: str
    weight: Optional[float] = None
    core: Optional[bool] = None


class TechHardFilterOut(_Base):
    key: Optional[str] = None
    label: Optional[str] = None
    action: Optional[str] = None


class TechRubricOut(_Base):
    id: str
    version: int
    title: Optional[str] = None
    seniority: Optional[str] = None
    min_years: Optional[float] = None
    dimensions: list[TechDimensionOut] = []
    max_score: float = 100
    thresholds: dict[str, Any] = {}
    hard_filters: list[TechHardFilterOut] = []
    source: Optional[str] = None
    created_by: Optional[str] = None
    activated_at: Optional[dt.datetime] = None


class TechRubricStepOut(_Base):
    job_id: int
    job_title: Optional[str] = None
    department: Optional[str] = None
    jd_source: Optional[str] = None
    rubric: Optional[TechRubricOut] = None
    # Why a rubric cannot be drafted, when it cannot.
    blocked_reason: Optional[str] = None


class TechRubricDraftRequest(_Base):
    job_id: int


class TechRubricPublishRequest(_Base):
    job_id: int
    draft: dict[str, Any]


class TechPlanRequest(_Base):
    job_id: int
    mode: str = "new_only"
    since_days: Optional[int] = None
    max_candidates: Optional[int] = None
    model: str
    use_batch: bool = False


class TechPlanOut(_Base):
    job_id: int
    mode: str
    model: str
    use_batch: bool = False
    rubric_version: int
    people: int
    duplicates_merged: int
    no_cv: int
    already_scored_in_pool: int = 0
    newest_application: Optional[str] = None
    oldest_application: Optional[str] = None
    est_input_tokens: int = 0
    est_cached_tokens: int = 0
    est_output_tokens: int = 0
    est_cost_usd: float = 0
    cache_saving_usd: float = 0
    batch_saving_usd: float = 0
    live_run_id: Optional[str] = None


class TechCreateRunRequest(_Base):
    job_id: int
    mode: str = "new_only"
    since_days: Optional[int] = None
    max_candidates: Optional[int] = None
    model: str
    use_batch: bool = False
    effort: str = "medium"
    cost_cap_usd: Optional[float] = None


class TechRunOut(_Base):
    id: str
    job_id: int
    job_title: Optional[str] = None
    status: str
    mode: str
    model: str
    rubric_version: int
    pause_reason: Optional[str] = None
    total: int = 0
    done: int = 0
    scored: int = 0
    failed: int = 0
    skipped: int = 0
    unusable: int = 0
    percent: float = 0
    est_cost_usd: float = 0
    actual_cost_usd: float = 0
    cost_cap_usd: Optional[float] = None
    requested_by: Optional[str] = None
    created_at: Optional[dt.datetime] = None
    started_at: Optional[dt.datetime] = None
    finished_at: Optional[dt.datetime] = None
    error: Optional[str] = None
    last_warning: Optional[str] = None


class TechScreenedOut(_Base):
    application_id: int
    candidate_name: Optional[str] = None
    tier: Optional[str] = None
    score_pct: Optional[float] = None


class TechSkippedOut(_Base):
    application_id: int
    reason: str
    candidate_name: Optional[str] = None
    tier: Optional[str] = None


class TechWorkRequest(_Base):
    # Small on purpose: each candidate is a model call of roughly twelve
    # seconds, so a big slice risks the platform's request timeout.
    limit: int = Field(default=3, ge=1, le=8)


class TechWorkOut(_Base):
    run_id: str
    screened: list[TechScreenedOut] = []
    # Could not be read: a person must open the document. Rule 32.
    skipped: list[TechSkippedOut] = []
    # 🔴 A SEPARATE FACT. The screener broke on this candidate, which is our
    # defect and needs an engineer, not somebody chasing a CV. These used to
    # arrive inside `skipped`, so a run in which every candidate failed on a
    # schema mismatch reported twenty unreadable CVs that were perfectly fine.
    failed: list[TechSkippedOut] = []
    # Named to match what frontend/src/lib/screenAll.ts already consumes, so
    # that tested retry loop is reused rather than reimplemented.
    last_application_id: Optional[int] = None
    remaining: int = 0
    status: str
    run: Optional[TechRunOut] = None


class TechModelOut(_Base):
    model: str
    label: str
    input_per_mtok: float
    output_per_mtok: float


# --------------------------------------------------------------------------
# Talent sourcing (Skill 05). The web search stays in Claude Code; the pool,
# the outreach state and the Markaz gate live here.
# --------------------------------------------------------------------------


class SourcedCandidateOut(_Base):
    id: str
    name: str
    organization: Optional[str] = None
    title: Optional[str] = None
    location: Optional[str] = None
    linkedin_url: Optional[str] = None
    # Nullable on purpose, with the original text kept: a column that admits it
    # does not know beats one that invents a number.
    years: Optional[int] = None
    years_note: Optional[str] = None
    # Four states, never a boolean. "not_found" is not evidence of invention.
    verification_state: str
    verification_note: Optional[str] = None
    is_verified: bool
    tier: Optional[str] = None
    confidence: Optional[str] = None
    outreach_state: str
    contacted_at: Optional[dt.datetime] = None
    contacted_by: Optional[str] = None
    reply_note: Optional[str] = None
    markaz_application_id: Optional[int] = None
    job_id: Optional[int] = None
    role_label: Optional[str] = None
    source: Optional[str] = None
    notes: Optional[str] = None
    # Why they may not enter Markaz yet, or null if they may.
    blocked_from_markaz: Optional[str] = None


class SourcingOutreachUpdate(_Base):
    outreach_state: Optional[str] = None
    reply_note: Optional[str] = None
    notes: Optional[str] = None


class SourcingPushRequest(_Base):
    """Links a sourced person to a Markaz application created by hand.

    Not a create: Markaz already holds 298 duplicate (candidate, job) pairs and
    adding more from here, usually without an email, would make that worse in
    somebody else's system.
    """

    application_id: int
    email: Optional[str] = None


class SourcingSummaryOut(_Base):
    total: int
    verification: dict[str, int]
    outreach: dict[str, int]
    in_markaz: int
    ready_for_markaz: int
    caveat: str


# --------------------------------------------------------------------------
# Candidate invites (Skill 06)
# --------------------------------------------------------------------------


class InviteTypeOut(_Base):
    key: str
    label: str
    # "booking" needs a verified link, "reply" confirms by replying, "none" has
    # nothing to arrange. Carried to the client so the form can refuse to show
    # a booking field on a type that forbids one.
    confirm: str
    note: str
    required: list[str]


class InviteLinkOut(_Base):
    id: str
    job_id: Optional[int] = None
    invite_type: str
    label: Optional[str] = None
    booking_url: Optional[str] = None
    jd_url: Optional[str] = None
    prep_url: Optional[str] = None
    expected_title: Optional[str] = None
    # The title the page ACTUALLY returned, and when. Null means unproven, and
    # a live send refuses while it is null.
    verified_title: Optional[str] = None
    verified_at: Optional[dt.datetime] = None
    verify_error: Optional[str] = None
    # Whether the fetched title matches expected_title. Null when there is
    # nothing to compare against, which is not the same as a match.
    title_matches_expected: Optional[bool] = None
    cc_list: Optional[list[str]] = None


class InviteLinkUpsert(_Base):
    job_id: Optional[int] = None
    invite_type: str
    label: Optional[str] = None
    booking_url: Optional[str] = None
    jd_url: Optional[str] = None
    prep_url: Optional[str] = None
    expected_title: Optional[str] = None
    cc_list: Optional[list[str]] = None


class InvitePreviewRequest(_Base):
    invite_type: str
    application_id: Optional[int] = None
    job_id: Optional[int] = None
    # Everything the chosen type declares in invite_render.REQUIRED, plus the
    # optional extras (meet_url, maps_url, context, previous_role).
    fields: dict = {}


class InvitePreviewOut(_Base):
    invite_type: str
    subject: str
    body_html: str
    missing: list[str] = []
    # Reasons a LIVE send would be refused right now, so the operator sees them
    # before drafting rather than at the moment of sending.
    blockers: list[str] = []
    warnings: list[str] = []


class InviteSendRequest(_Base):
    invite_type: str
    application_id: Optional[int] = None
    job_id: Optional[int] = None
    candidate_email: Optional[str] = None
    candidate_name: Optional[str] = None
    subject: Optional[str] = None
    live: bool = False
    fields: dict = {}
    cc: Optional[list[str]] = None


class InviteSendOut(_Base):
    id: str
    invite_type: str
    application_id: Optional[int] = None
    candidate_name: Optional[str] = None
    to_address: str
    cc_list: Optional[list[str]] = None
    subject: str
    is_live: bool
    booking_url: Optional[str] = None
    booking_verified_title: Optional[str] = None
    sent_at: dt.datetime
    sent_by: Optional[str] = None
