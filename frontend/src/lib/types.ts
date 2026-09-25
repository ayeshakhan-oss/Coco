export type AppRole = 'viewer' | 'editor' | 'approver' | 'super_admin'
export type Bucket = 'awaiting_scorecard' | 'needs_comms' | 'in_progress' | 'sent'
export type DisplayStatus =
  | Bucket
  | 'high_priority'
  | 'needs_review'
  | 'ignored'
  | 'shortlisted'
  | 'interview_scheduled'
  | 'case_study'
export type GmailStatus = 'not_checked' | 'none' | 'found' | 'uncertain'

export interface CurrentUser {
  id: string
  email: string
  first_name?: string | null
  last_name?: string | null
  app_role: AppRole
}

export interface ManagedUser {
  id: string
  email: string
  first_name?: string | null
  last_name?: string | null
  app_role: AppRole
  active: boolean
  last_login_at?: string | null
  created_at?: string | null
}

export interface QueueRow {
  application_id: number
  candidate_id: number
  first_name?: string | null
  last_name?: string | null
  email?: string | null
  job_pk?: number | null
  job_code?: string | null
  job_title?: string | null
  job_status?: string | null
  status?: string | null
  values_filled: boolean
  gwc_filled: boolean
  values_interview_result?: string | null
  scorecard_date?: string | null
  interviewer?: string | null
  sent_count: number
  active_count: number
  last_sent_at?: string | null
  prior_platform_comms: number
  bucket: Bucket
  // Markaz <-> Gmail communication-sync dimensions
  applied_at?: string | null
  days_waiting?: number | null
  gmail_status: GmailStatus
  comm_required: boolean
  required_email_type?: string | null
  is_high_priority: boolean
  has_evidence: boolean
  manual_marked: boolean
  ignored: boolean
  display_status: DisplayStatus
}

export interface QueueStats {
  needs_comms: number
  high_priority: number
  in_progress: number
  sent: number
  needs_review: number
  shortlisted: number
  awaiting_scorecard: number
  ignored: number
  scored: number
  total: number
  total_applications: number
  total_candidates: number
  open_positions: number
}

export interface GmailMatch {
  gmail_status: GmailStatus
  match_method?: string | null
  matched_message_id?: string | null
  gmail_thread_id?: string | null
  internal_date?: string | null
  matched_subject?: string | null
  matched_to?: string | null
  matched_snippet?: string | null
  uncertain_reason?: string | null
  marked_sent_at?: string | null
  marked_sent_by?: string | null
  marked_sent_reason?: string | null
  ignored?: boolean
  ignored_at?: string | null
  checked_at?: string | null
}

export interface TimelineItem {
  source: 'markaz' | 'gmail' | 'coco'
  ts?: string | null
  subject?: string | null
  actor?: string | null
  snippet?: string | null
  link?: string | null
}

export interface GmailSyncStatus {
  last_sync_at?: string | null
  status?: string | null
  trigger?: string | null
  messages_scanned?: number | null
  candidates_evaluated?: number | null
  found_count?: number | null
  uncertain_count?: number | null
  none_count?: number | null
  started_at?: string | null
  finished_at?: string | null
  error_detail?: string | null
}

export interface JobItem {
  job_pk: number
  job_code?: string | null
  title?: string | null
  job_status?: string | null
  department?: string | null
}

export interface PositionSummary {
  job_pk: number
  job_code?: string | null
  job_title?: string | null
  needs_comms: number
  high_priority: number
  in_progress: number
  sent: number
  needs_review: number
  shortlisted: number
  awaiting_scorecard: number
  scored: number
  total: number
  last_gmail_sync_at?: string | null
}

export interface ScorecardValueItem {
  name: string
  rating: string
  deep_dive: string
  curve_ball: string
  micro_case: string
}

export interface ValuesScorecard {
  kind: 'values'
  candidate_name: string
  host: string
  note_taker: string
  date: string
  proceed_to_right_seat: string
  final_comments: string
  values: ScorecardValueItem[]
}

export interface GwcCompetency {
  name: string
  score: number | null
  weight: number | null
}

export interface GwcScorecard {
  kind: 'gwc'
  candidate_name: string
  hiring_manager: string
  final_mark: string
  get_it: Record<string, string>
  want_it: Record<string, string>
  capacity_to_do_it: Record<string, string>
  competencies: GwcCompetency[]
  recording_link: string
  additional_comments: string
}

export interface ScorecardResponse {
  application_id: number
  values: ValuesScorecard | null
  gwc: GwcScorecard | null
}

export interface CommHistoryItem {
  sent_at?: string | null
  sent_by?: string | null
  status?: string | null
  subject?: string | null
  template_name?: string | null
  recipient_email?: string | null
  cc_emails: string[]
  source: string
}

export interface DraftSection {
  heading?: string
  subhead?: string | null
  paragraphs: string[]
}

export interface DraftContent {
  title_line?: string
  greeting?: string
  opening?: string[]
  sections?: DraftSection[]
  ps?: string
}

export interface EvalViolation {
  rule: string
  severity: 'HARD_BLOCK' | 'WARNING'
  detail: string
}

export interface EvalResult {
  word_minimum?: number
  passed: boolean
  word_count: number
  violations: EvalViolation[]
}

export type CommStatus = 'draft' | 'in_review' | 'approved' | 'sent' | 'failed'

export interface Communication {
  id: string
  application_id?: number | null
  candidate_id: number
  job_id?: number | null
  email_type: string
  subject?: string | null
  title_line?: string | null
  role_title?: string | null
  body_html?: string | null
  draft_content?: DraftContent | null
  status: CommStatus
  mode?: string | null
  word_count?: number | null
  eval_result?: EvalResult | null
  eval_passed?: boolean | null
  sent_to?: string[] | null
  message_id?: string | null
  created_by?: string | null
  approved_by?: string | null
  created_at?: string | null
  updated_at?: string | null
  sent_at?: string | null
}

export interface GenerateResponse {
  communication: Communication
  eval: EvalResult
  attempts: number
  drafter_used: string
}

export interface SendResponse {
  communication: Communication
  mode: string
  subject: string
  recipients: string[]
  message_id?: string | null
}

export const EMAIL_TYPES: { value: string; label: string }[] = [
  { value: 'values_feedback', label: 'Values feedback' },
  { value: 'gwc_rejection', label: 'GWC rejection' },
  { value: 'warm_bench', label: 'Warm bench' },
  { value: 'cv_rejection', label: 'CV rejection' },
  // Skill 01 type #8 (2026-09-08): submitted a case study, below the 70% benchmark.
  { value: 'case_study_outcome', label: 'Case study outcome (below benchmark)' },
]

export interface ApplicationDetail {
  application_id: number
  candidate_id: number
  first_name?: string | null
  last_name?: string | null
  email?: string | null
  phone?: string | null
  job_pk?: number | null
  job_code?: string | null
  job_title?: string | null
  job_status?: string | null
  status?: string | null
  stage?: string | null
  values_filled: boolean
  gwc_filled: boolean
  values_interview_result?: string | null
  values_interview_date?: string | null
  values_interviewer_name?: string | null
  gwc_interview_result?: string | null
  gwc_interview_date?: string | null
  gwc_interviewer_name?: string | null
  comm_history: CommHistoryItem[]
  // Markaz <-> Gmail communication-sync dimensions
  applied_at?: string | null
  days_waiting?: number | null
  comm_required?: boolean
  required_email_type?: string | null
  is_high_priority?: boolean
  has_evidence?: boolean
  manual_marked?: boolean
  ignored?: boolean
  display_status?: DisplayStatus
  gmail_status?: GmailStatus
}

// Candidate evaluation (Nugget technical screening, read-only)
export interface ScreenedJob {
  job_id: number
  job_title: string | null
  rubric_version: number
  rubric_status: string
  seniority: string | null
  scored: number
  unusable: number
  last_run_at: string | null
}

export interface TierBucket {
  tier: string
  status: string | null
  n: number
  avg_pct: number | null
  min_pct: number | null
  max_pct: number | null
  is_unusable: boolean
  is_unscored: boolean
}

export interface EvaluationSummary {
  tiers: TierBucket[]
  scored: number
  unusable: number
  // Rows where `is_unscored` is true: UNUSABLE plus MANUAL_REVIEW, spanning
  // both the `scored` and `unusable` buckets, not a subset of `scored`. This
  // is the number that reveals a broken job: a job can report a healthy
  // `scored` count while most of it is actually unreadable.
  unscored: number
  total: number
}

export interface EvaluationRow {
  application_id: number | null
  candidate_id: number | null
  candidate_name: string | null
  candidate_email: string | null
  score_pct: number | null
  tier: string | null
  tier_reason: string | null
  confidence: string | null
  resume_health: number | null
  is_unusable: boolean
  is_unscored: boolean
}

export interface EvaluationDetail extends EvaluationRow {
  strengths: string[] | null
  gaps: string[] | null
  verdict: string | null
  rubric_version: number | null
  model: string | null
  evaluated_at: string | null
}

// Response shape for GET /api/evaluations/jobs/{job_id}/candidates. Carries
// `total` so the caller can tell there are more rows beyond the current page.
export interface CandidatePage {
  rows: EvaluationRow[]
  total: number
}

// --------------------------------------------------------------------------
// Values scorecard draft lifecycle (webapp/routers/values_scorecards.py).
// Field names on `values` items (deepDive/curveBall/microCase) and on `gwc`
// (gets_it/wants_it/capacity) are camelCase/snake_case exactly as the model
// writes them and the backend validates them -- not the same shape as the
// already-in-Markaz ScorecardValueItem/GwcScorecard types above.
// --------------------------------------------------------------------------

export interface ValuesScorecardDraftValue {
  name: string
  rating: string // '+' | '+/-' | '-'
  deepDive: string
  curveBall: string
  microCase: string
}

export interface ValuesScorecardGwc {
  gets_it: string // 'Yes' | 'No'
  wants_it: string
  capacity: string
}

export interface ValuesScorecardTally {
  plus: number
  plus_minus: number
  minus: number
}

// --------------------------------------------------------------------------
// Case-study benchmark + scoring lifecycle (webapp/routers/case_studies.py).
// 🔒 Rule 0: scoring is refused (409) unless an APPROVED benchmark exists for
// the target application's own job. `total` / `band` below are ALWAYS taken
// verbatim from the server (webapp/services/case_study_scoring.py) -- never
// recomputed in the browser.
// --------------------------------------------------------------------------

export type CaseStudyBenchmarkStatus = 'draft' | 'approved' | 'retired'

export interface CaseStudyBenchmark {
  id: string
  job_id: number
  kind: string
  title: string
  body: string
  source_path?: string | null
  created_by: string
  created_at?: string | null
  qa_approved_by?: string | null
  qa_approved_at?: string | null
  status: CaseStudyBenchmarkStatus
}

// One rubric dimension's metadata, exactly as `case_study_scoring.DIMENSIONS`
// defines it server-side. A TYPE only -- there is no browser-side constant of
// these any more (see the removed CASE_STUDY_DIMENSIONS below). Every
// CaseStudyEvaluationOut response now carries its own `dimensions` list, so a
// weight or dimension change in Python can never go stale on the page.
export interface CaseStudyDimensionMeta {
  key: string
  label: string
  weight: number
}

export interface CaseStudyEvaluation {
  id: string
  application_id: number
  job_id: number
  benchmark_id: string
  candidate_name: string
  role: string
  scores: Record<string, number>
  evidence: Record<string, string>
  flags: string[]
  total: number
  band: string
  model: string
  sources: string[]
  created_by: string
  created_at?: string | null
  // The rubric's dimension metadata, taken verbatim from the response. A
  // score key with no matching entry here (an unknown/renamed dimension)
  // must still render -- see CaseStudyPage.tsx's fallback rendering.
  dimensions: CaseStudyDimensionMeta[]
}

// Display-only mirror of the locked FLAGS vocabulary in the same file. Only
// `disqualifying` changes the server-computed band -- that override already
// happened server-side by the time a flag reaches the browser; this map only
// controls how prominently each flag renders.
export const CASE_STUDY_FLAGS: Record<string, { label: string; severity: 'disqualifying' | 'serious' | 'note' }> = {
  fabricated_data: { label: 'Fabricated data', severity: 'disqualifying' },
  undisclosed_ai: { label: 'Undisclosed AI use', severity: 'serious' },
  materially_incomplete: { label: 'Materially incomplete', severity: 'serious' },
  instruction_breach: { label: 'Instruction breach', severity: 'note' },
  consent_blindness: { label: 'Consent blindness', severity: 'note' },
}

export interface ValuesScorecardDraft {
  id: string
  application_id: number
  candidate_name: string
  host: string
  transcript_sha256: string
  // The actual interview date (ISO "YYYY-MM-DD"), not the date the
  // scorecard was generated or submitted. Null until captured -- submit()
  // then falls back to today and writes that fallback back here, so it is
  // never silently missing after a submission.
  interview_date: string | null
  values: ValuesScorecardDraftValue[]
  gwc: ValuesScorecardGwc | null
  final_comments: string
  proceed: boolean
  // Both are always RECOMPUTED server-side from `values` -- never trust a
  // cached copy, and never compute either of these in the browser.
  tally: ValuesScorecardTally
  verdict: 'PASS' | 'OUT'
  status: 'draft' | 'submitted'
  model: string
  created_by: string
  created_at?: string | null
  approved_by?: string | null
  approved_at?: string | null
  submitted_at?: string | null
  markaz_payload?: Record<string, unknown> | null
  replaced_payload?: Record<string, unknown> | null
}

// --- CV screening (Skill 02, cv-screening) -------------------------------
// Coco's OWN criteria. Nugget's technical screening is a separate skill with
// a separate rubric (EvaluationSummary / EvaluationDetail above); the two
// never share a type, a tier vocabulary or a page.

export interface CVScreenCriterion {
  key: string
  label: string
  weight: number
  priority: string
}

export type CVScreenTier = 'shortlist' | 'maybe' | 'no_hire'

export interface CVScreen {
  id: string
  application_id: number
  job_id: number
  candidate_name: string
  role: string
  scores: Record<string, number>
  evidence: Record<string, string>
  strengths: string[]
  gaps: string[]
  // Two figures, never one: conflating them is the SOP's named mistake.
  total_experience_years: number
  relevant_experience_years: number
  relevant_experience_note: string
  match: number
  tier: CVScreenTier
  model: string
  sop_sha256: string
  jd_sha256: string
  cv_chars: number
  cv_truncated: boolean
  is_current: boolean
  superseded_by: string | null
  created_by: string
  created_at: string | null
  criteria: CVScreenCriterion[]
}

/** Why a candidate has no screen, when the reason is their CV.
 *  Not a result and not a low score: a CV that will not open is a document
 *  problem needing a person. */
export interface CVScreenSkip {
  application_id: number
  kind: 'no_cv' | 'unreadable' | 'too_short'
  reason: string
  cv_file_name: string | null
  recorded_at: string | null
}

export interface CVScreenApplication {
  application_id: number
  candidate_name: string
  email: string | null
  status: string | null
  applied_at: string | null
  expected_salary: string | null
  city: string | null
  willing_to_relocate: string | null
  cv_available: boolean
  cv_error: string | null
  screen: CVScreen | null
  // A row carries a screen or a skip, never both.
  skip: CVScreenSkip | null
}

export interface CVScreenJobSummary {
  job_id: number
  title: string | null
  total: number
  shortlist: number
  maybe: number
  no_hire: number
  // Work remaining. Excludes CVs that cannot be read, which no amount of
  // screening again will resolve.
  unscreened: number
  // Attempted and refused. shortlist + maybe + no_hire + unreadable +
  // unscreened === total.
  unreadable: number
  jd_chars: number
  jd_error: string | null
}

// --- Case-study tracking (Skill 02, case-study-evaluation) ---------------
// Tracking and completeness only. Scoring is CaseStudyEvaluation above.

export interface CaseStudyFlag {
  flag: string
  count: number
  evidence: string
  meaning: string
}

// 🔴 There is deliberately no 'not_sent'. Markaz records no case-study send,
// so we can never assert one did not happen.
export type CaseStudyStatus =
  | 'submitted'
  | 'awaiting'
  | 'no_record_of_a_send'
  | 'submitted_without_send_record'

export interface CaseStudyProbe {
  id: string
  application_id: number
  job_id: number
  channels: string[]
  send_found: boolean
  send_subject: string | null
  send_at: string | null
  status: CaseStudyStatus
  corpus_chars: number
  sources: string[]
  corpus_error: string | null
  flags: CaseStudyFlag[]
  completeness: {
    known?: boolean
    present?: string[]
    missing?: string[]
    note?: string | null
  }
  probed_by: string
  probed_at: string | null
}

export interface CaseStudyTrackingRow {
  application_id: number
  candidate_name: string
  email: string | null
  channels: string[]
  submitted_at: string | null
  markaz_status: string | null
  status: CaseStudyStatus
  probe: CaseStudyProbe | null
}

export interface CaseStudyTrackingSummary {
  job_id: number
  title: string | null
  total: number
  submitted: number
  awaiting: number
  no_record_of_a_send: number
  submitted_without_send_record: number
  unproven_absence: number
  probed: number
}

export interface CaseStudyMirrorPair {
  application_ids: number[]
  candidate_names: string[]
  shared_runs: number
  examples: string[]
}

// --- KCD evaluation (Skill 02, kcd-evaluation) ---------------------------
// A human evaluation with the rules enforced, not a model score.
// 🔒 "KCD" is internal only. Anything leaving the team says "case study".

export interface KCDDimension {
  key: string
  label: string
  weight: number
  asks: string
}

export interface KCDFramework {
  dimensions: KCDDimension[]
  // Includes 0.0: a real zero, not the SOP's 1-to-5 floor.
  scores: number[]
  verdicts: string[]
  gwc_threshold: number
  cap_insight_without_evidence: number
  cap_evidence_without_interpretation: number
}

export interface KCDCrossCheck {
  status: 'aligned' | 'review' | 'divergent' | 'not_available'
  delta: number | null
  note: string
}

export interface KCDEvaluation {
  id: string
  application_id: number
  job_id: number
  candidate_name: string
  role: string
  scores: Record<string, number>
  evidence: Record<string, string>
  weights: Record<string, number> | null
  caps_applied: {
    insight_without_evidence?: string[]
    evidence_without_interpretation?: string[]
  }
  total: number
  verdict: string
  condition: string | null
  advances_to_gwc: boolean
  incomplete: boolean
  missing_parts: string[]
  integrity_flags: Array<Record<string, unknown>>
  second_evaluator: string | null
  second_total: number | null
  cross_check: KCDCrossCheck | null
  is_current: boolean
  superseded_by: string | null
  created_by: string
  created_at: string | null
  dimensions: KCDDimension[]
  // Present only on an incomplete submission: the score with its asterisk and
  // the plain statement that it is a floor.
  display_score: string | null
}

export interface KCDCohort {
  job_id: number
  ranked: KCDEvaluation[]
  // A separate list, never merged: an incomplete submission must never be
  // ranked above a complete one.
  incomplete: KCDEvaluation[]
  note: string | null
  gwc_threshold: number
  advancing: number
}

export interface KCDEvaluationInput {
  application_id: number
  scores: Record<string, number>
  evidence: Record<string, string>
  caps?: {
    insight_without_evidence: string[]
    evidence_without_interpretation: string[]
  }
  condition?: string | null
  incomplete?: boolean
  missing_parts?: string[]
  second_evaluator?: string | null
  second_total?: number | null
}

export interface CVScreenSkipped {
  application_id: number
  reason: string
}

export interface CVScreenBatch {
  job_id: number
  screened: CVScreen[]
  // Candidates the batch could not screen. Shown, never dropped.
  skipped: CVScreenSkipped[]
  last_application_id: number | null
  remaining: number
}

// --- Hiring Operations: attendance (Skill 03) ----------------------------
// 🔴 Markaz records ABSENCE, not attendance. There is deliberately no
// "onsite" or "present" field: a leave system cannot see who walked in.

export interface AttendancePerson {
  user_id: number
  name: string | null
  payroll_entity: string | null
  department: string | null
  job_title: string | null
  category: string
  leave_type: string | null
  sub_category: string | null
  start_date: string | null
  end_date: string | null
  is_half_day: boolean
}

export interface AttendanceCorrection {
  user_id: number | null
  name: string | null
  leave_type: string | null
  start_date: string | null
  end_date: string | null
  problem: string
}

export interface AttendanceStatBox {
  label: string
  value: number
  colour: string
}

export interface AttendanceReport {
  date: string
  weekday: string
  entities: string[]
  total_on_payroll: number
  no_absence_recorded: number
  on_leave: AttendancePerson[]
  working_from_home: AttendancePerson[]
  needs_correction: AttendanceCorrection[]
  stat_boxes: AttendanceStatBox[]
  presence_caveat: string
  source: string
}

export interface AttendanceEntities {
  entities: { payroll_entity: string; n: number }[]
  default: string[]
}

// --- Hiring Operations: decision brief (Skill 03) ------------------------

export interface DecisionBriefPerson {
  application_id: number
  name: string
  cv_url: string
  has_cv: boolean
  status: string | null
  // null means no values interview on record; false means interviewed and did
  // not pass. The two must not be collapsed.
  passed_values: boolean | null
  values_disagreement: string | null
  values_comments: string | null
  submitted_case_study: boolean
  case_study_band: string | null
  case_study_total: number | null
  cv_screen_tier: string | null
  cv_screen_match: number | null
  debrief_verdict: string
  debrief_date: string | null
  group: string
}

export interface DecisionBrief {
  job_id: number | null
  job_title: string | null
  generated_on: string
  total_applications: number
  values_interviews: number
  shortlisted: number
  leading: DecisionBriefPerson[]
  leading_note: string | null
  groups: { key: string; title: string; people: DecisionBriefPerson[] }[]
  debrief_schedule: DecisionBriefPerson[]
  not_recorded: {
    debrief_verdicts: number
    case_study_scores: number
    missing_cv: number
  }
  evidence_caveat: string
  stat_boxes: { label: string; value: number; colour: string }[]
}

// --- Hiring Operations: hiring decision brief (funnel + recommendations) ---

export interface FunnelStage {
  key: string
  title: string
  // null means the stage could not be established. Rendered as "not visible",
  // never 0, which would read as "nobody".
  count: number | null
  source: string
  is_floor: boolean
  note: string | null
}

export interface HiringBrief {
  job_id: number | null
  job_title: string | null
  total_applications: number
  stages: FunnelStage[]
  evidence_synced_at: string | null
  caveat: string
  inconsistencies: string[]
  brief: DecisionBrief
}

// --- Technical screening wizard (Skill 02) -------------------------------
// 🔒 NOT CV screening. Nugget's rubric, Nugget's tables, tiers P1-P4 /
// MANUAL_REVIEW / UNUSABLE. The two skills never merge (CLAUDE.md Rule 33),
// so nothing here reuses a CVScreen* type and nothing there reuses these.

export interface TechJob {
  job_pk: number
  job_code?: string | null
  title: string
  department?: string | null
  job_status?: string | null
  applications: number
  scored: number
  has_rubric: boolean
  rubric_version?: number | null
  // Set when a run is already live, so Confirm can be disabled with a reason
  // rather than failing on the one-active-run-per-job constraint.
  live_run_id?: string | null
  live_run_status?: string | null
}

export interface TechDimension {
  key: string
  label: string
  weight?: number | null
  core?: boolean | null
}

export interface TechHardFilter {
  key?: string | null
  label?: string | null
  action?: string | null
}

export interface TechRubric {
  id: string
  version: number
  title?: string | null
  seniority?: string | null
  min_years?: number | null
  dimensions: TechDimension[]
  max_score: number
  thresholds: Record<string, unknown>
  hard_filters: TechHardFilter[]
  source?: string | null
  created_by?: string | null
  activated_at?: string | null
}

export interface TechRubricStep {
  job_id: number
  job_title?: string | null
  department?: string | null
  jd_source?: string | null
  rubric?: TechRubric | null
  // Why a rubric cannot be drafted, when it cannot.
  blocked_reason?: string | null
}

export interface TechPlan {
  job_id: number
  mode: string
  model: string
  use_batch: boolean
  rubric_version: number
  people: number
  duplicates_merged: number
  // 🔴 "No file on record", NOT "unreadable". A CV that will not extract is
  // only discovered during the run and comes back as skipped.
  no_cv: number
  already_scored_in_pool: number
  newest_application?: string | null
  oldest_application?: string | null
  est_input_tokens: number
  est_cached_tokens: number
  est_output_tokens: number
  est_cost_usd: number
  cache_saving_usd: number
  batch_saving_usd: number
  live_run_id?: string | null
}

export interface TechRun {
  id: string
  job_id: number
  job_title?: string | null
  status: string
  mode: string
  model: string
  rubric_version: number
  pause_reason?: string | null
  total: number
  done: number
  scored: number
  failed: number
  skipped: number
  unusable: number
  percent: number
  est_cost_usd: number
  actual_cost_usd: number
  cost_cap_usd?: number | null
  requested_by?: string | null
  created_at?: string | null
  started_at?: string | null
  finished_at?: string | null
  error?: string | null
  last_warning?: string | null
}

export interface TechScreened {
  application_id: number
  candidate_name?: string | null
  tier?: string | null
  score_pct?: number | null
}

export interface TechSkipped {
  application_id: number
  reason: string
  candidate_name?: string | null
  tier?: string | null
}

// Field names match BatchLike in screenAll.ts so the tested retry loop drives
// this run too, without either screening skill learning the other's types.
export interface TechWork {
  run_id: string
  screened: TechScreened[]
  skipped: TechSkipped[]
  last_application_id: number | null
  remaining: number
  status: string
  run?: TechRun | null
}

export interface TechModel {
  model: string
  label: string
  input_per_mtok: number
  output_per_mtok: number
}

// --- Talent sourcing (Skill 05) ------------------------------------------
// The 3-layer web search stays in Claude Code. This is the pool, the outreach
// state, and the gate into Markaz.

export type SourcingVerification = 'confirmed' | 'unconfirmed' | 'not_found' | 'no_url'
export type SourcingOutreach =
  | 'not_contacted'
  | 'contacted'
  | 'replied_interested'
  | 'replied_not_interested'
  | 'no_reply'

export interface SourcedCandidate {
  id: string
  name: string
  organization: string | null
  title: string | null
  location: string | null
  linkedin_url: string | null
  // Null on purpose where the note did not actually say. The original text is
  // kept so a person can read it themselves.
  years: number | null
  years_note: string | null
  verification_state: SourcingVerification
  verification_note: string | null
  is_verified: boolean
  tier: string | null
  confidence: string | null
  outreach_state: SourcingOutreach
  contacted_at: string | null
  contacted_by: string | null
  reply_note: string | null
  markaz_application_id: number | null
  job_id: number | null
  role_label: string | null
  source: string | null
  notes: string | null
  // Why they may not enter Markaz yet, or null if they may.
  blocked_from_markaz: string | null
}

export interface SourcingSummary {
  total: number
  verification: Record<string, number>
  outreach: Record<string, number>
  in_markaz: number
  ready_for_markaz: number
  caveat: string
}
