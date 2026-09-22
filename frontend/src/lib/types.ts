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
}

// Display-only mirror of the locked DIMENSIONS tuple in
// webapp/services/case_study_scoring.py. The API never returns dimension
// labels or weights (CaseStudyEvaluationOut carries only `scores`/`evidence`
// keyed by dimension key), so this exists purely to render a label and a
// weight next to each score. It is NEVER read to compute a total or a band --
// those come verbatim from the server on every response. If the Python
// weights ever change, update this list to match; nothing here feeds back
// into any calculation.
export const CASE_STUDY_DIMENSIONS: { key: string; label: string; weight: number }[] = [
  { key: 'data_judgment', label: 'Data judgment', weight: 20 },
  { key: 'execution_specificity', label: 'Execution specificity', weight: 25 },
  { key: 'stakeholder_craft', label: 'Stakeholder craft', weight: 20 },
  { key: 'commercial_honesty', label: 'Commercial honesty', weight: 15 },
  { key: 'decision_discipline', label: 'Decision discipline', weight: 10 },
  { key: 'signal_self_awareness', label: 'Signal & self-awareness', weight: 10 },
]

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
