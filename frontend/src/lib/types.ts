export type AppRole = 'drafter' | 'approver'
export type Bucket = 'awaiting_scorecard' | 'needs_comms' | 'in_progress' | 'sent'

export interface CurrentUser {
  id: string
  email: string
  first_name?: string | null
  last_name?: string | null
  app_role: AppRole
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
}

export interface QueueStats {
  needs_comms: number
  in_progress: number
  sent: number
  awaiting_scorecard: number
  scored: number
  total: number
}

export interface JobItem {
  job_pk: number
  job_code?: string | null
  title?: string | null
  job_status?: string | null
  department?: string | null
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
}
