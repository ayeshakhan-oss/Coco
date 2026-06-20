export type AppRole = 'viewer' | 'editor' | 'approver' | 'super_admin'
export type Bucket = 'awaiting_scorecard' | 'needs_comms' | 'in_progress' | 'sent'
export type DisplayStatus = Bucket | 'high_priority' | 'needs_review' | 'ignored'
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
