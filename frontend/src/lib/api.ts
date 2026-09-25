import type {
  ApplicationDetail,
  AttendanceEntities,
  AttendanceReport,
  DecisionBrief,
  HiringBrief,
  CandidatePage,
  CaseStudyBenchmark,
  CaseStudyEvaluation,
  CaseStudyMirrorPair,
  CaseStudyProbe,
  CaseStudyTrackingRow,
  CaseStudyTrackingSummary,
  Communication,
  CurrentUser,
  CVScreen,
  CVScreenApplication,
  CVScreenBatch,
  CVScreenCriterion,
  CVScreenJobSummary,
  DraftContent,
  EvalResult,
  EvaluationDetail,
  EvaluationSummary,
  GenerateResponse,
  GmailMatch,
  GmailSyncStatus,
  InviteLink,
  InvitePreview,
  InviteSendRecord,
  InviteType,
  JobItem,
  KCDCohort,
  KCDEvaluation,
  KCDEvaluationInput,
  KCDFramework,
  ManagedUser,
  PositionSummary,
  QueueRow,
  QueueStats,
  ScorecardResponse,
  ScreenedJob,
  SkillLibrary,
  SourcedCandidate,
  SourcingSummary,
  SystemActivity,
  SystemHealth,
  SendResponse,
  TechJob,
  TechModel,
  TechPlan,
  TechRubricStep,
  TechRun,
  TechWork,
  TimelineItem,
  ValuesScorecardDraft,
  ValuesScorecardDraftValue,
} from './types'

export class ApiError extends Error {
  status: number
  detail: unknown
  constructor(status: number, message: string, detail?: unknown) {
    super(message)
    this.status = status
    this.detail = detail
  }
}

async function request<T>(method: string, path: string, body?: unknown): Promise<T> {
  const res = await fetch(path, {
    method,
    credentials: 'include',
    headers: body !== undefined ? { 'Content-Type': 'application/json', Accept: 'application/json' } : { Accept: 'application/json' },
    body: body !== undefined ? JSON.stringify(body) : undefined,
  })
  if (res.status === 401) {
    if (!location.pathname.startsWith('/login')) location.assign('/login')
    throw new ApiError(401, 'Not authenticated')
  }
  if (!res.ok) {
    let detail: unknown
    let text = ''
    try {
      detail = await res.json()
      const inner = typeof detail === 'object' && detail && 'detail' in detail ? (detail as { detail: unknown }).detail : detail
      // A plain-string detail is a message written for the user (e.g. "no
      // evidence exists for this email type"). Show it as prose, not as JSON.
      text = typeof inner === 'string' ? inner : JSON.stringify(inner)
    } catch {
      text = await res.text().catch(() => '')
    }
    throw new ApiError(res.status, `${res.status}: ${text}`, detail)
  }
  if (res.status === 204) return undefined as T
  return res.json() as Promise<T>
}

const get = <T>(p: string) => request<T>('GET', p)
const post = <T>(p: string, b?: unknown) => request<T>('POST', p, b ?? {})
const put = <T>(p: string, b: unknown) => request<T>('PUT', p, b)
const patch = <T>(p: string, b: unknown) => request<T>('PATCH', p, b)

export interface CandidateQuery {
  status?: string
  job?: number | null
  q?: string
  limit?: number
}

export const api = {
  me: () => get<CurrentUser>('/api/me'),
  stats: () => get<QueueStats>('/api/candidates/stats'),
  positions: () => get<PositionSummary[]>('/api/positions'),
  jobs: () => get<JobItem[]>('/api/jobs'),
  candidates: (p: CandidateQuery = {}) => {
    const qs = new URLSearchParams()
    if (p.status) qs.set('status', p.status)
    if (p.job != null) qs.set('job', String(p.job))
    if (p.q) qs.set('q', p.q)
    qs.set('limit', String(p.limit ?? 200))
    return get<QueueRow[]>(`/api/candidates?${qs.toString()}`)
  },
  candidate: (id: number) => get<ApplicationDetail>(`/api/candidates/${id}`),
  scorecard: (id: number) => get<ScorecardResponse>(`/api/candidates/${id}/scorecard`),

  // Communications
  generate: (application_id: number, email_type: string, role_title?: string) =>
    post<GenerateResponse>('/api/communications/generate', { application_id, email_type, role_title }),
  communication: (id: string) => get<Communication>(`/api/communications/${id}`),
  updateDraft: (id: string, payload: { title_line: string; role_title?: string | null; content: DraftContent }) =>
    put<GenerateResponse>(`/api/communications/${id}`, payload),
  evalDraft: (id: string, mode: 'pilot' | 'live' = 'pilot') => post<EvalResult>(`/api/communications/${id}/eval?mode=${mode}`),
  submit: (id: string) => post<Communication>(`/api/communications/${id}/submit`),
  approve: (id: string) => post<Communication>(`/api/communications/${id}/approve`),
  requestChanges: (id: string) => post<Communication>(`/api/communications/${id}/request-changes`),
  send: (id: string, mode: 'pilot' | 'live') => post<SendResponse>(`/api/communications/${id}/send`, { mode }),
  listCommunications: (params: { status?: string; candidate_id?: number; mine?: boolean } = {}) => {
    const qs = new URLSearchParams()
    if (params.status) qs.set('status', params.status)
    if (params.candidate_id != null) qs.set('candidate_id', String(params.candidate_id))
    if (params.mine) qs.set('mine', 'true')
    return get<Communication[]>(`/api/communications?${qs.toString()}`)
  },
  previewUrl: (id: string) => `/api/communications/${id}/preview`,

  // Gmail evidence sync + manual overrides
  gmailSyncStatus: () => get<GmailSyncStatus>('/api/gmail-sync/status'),
  refreshGmailSync: (full = false) => post<GmailSyncStatus>(`/api/gmail-sync/refresh?full=${full}`),
  gmailMatch: (applicationId: number) => get<GmailMatch>(`/api/candidates/${applicationId}/gmail-match`),
  timeline: (applicationId: number) => get<TimelineItem[]>(`/api/candidates/${applicationId}/timeline`),
  markSent: (applicationId: number, reason?: string) =>
    post<GmailMatch>(`/api/candidates/${applicationId}/mark-sent`, { reason }),
  clearMark: (applicationId: number) => request<GmailMatch>('DELETE', `/api/candidates/${applicationId}/mark-sent`),
  setIgnore: (applicationId: number, ignored: boolean) =>
    post<GmailMatch>(`/api/candidates/${applicationId}/ignore`, { ignored }),
  bulkMarkSent: (application_ids: number[], reason?: string) =>
    post<{ updated: number }>('/api/candidates/bulk/mark-sent', { application_ids, reason }),
  bulkIgnore: (application_ids: number[], ignored: boolean) =>
    post<{ updated: number }>('/api/candidates/bulk/ignore', { application_ids, ignored }),

  // User management (super admin)
  listUsers: () => get<ManagedUser[]>('/api/users'),
  createUser: (payload: { email: string; app_role: string; first_name?: string; last_name?: string }) =>
    post<ManagedUser>('/api/users', payload),
  updateUser: (id: string, payload: { app_role?: string; active?: boolean }) =>
    request<ManagedUser>('PATCH', `/api/users/${id}`, payload),

  // Candidate evaluation (Nugget technical screening, read-only)
  evaluationJobs: () => get<ScreenedJob[]>('/api/evaluations/jobs'),
  evaluationSummary: (jobId: number) =>
    get<EvaluationSummary>(`/api/evaluations/jobs/${jobId}/summary`),
  evaluationCandidates: (jobId: number, tier?: string, limit = 100, offset = 0) => {
    const qs = new URLSearchParams()
    if (tier) qs.set('tier', tier)
    qs.set('limit', String(limit))
    qs.set('offset', String(offset))
    return get<CandidatePage>(`/api/evaluations/jobs/${jobId}/candidates?${qs.toString()}`)
  },
  evaluationDetail: (applicationId: number) =>
    get<EvaluationDetail>(`/api/evaluations/applications/${applicationId}`),

  // Values scorecard draft lifecycle: generate -> read -> edit -> submit.
  generateValuesScorecard: (
    application_id: number,
    transcript: string,
    host: string,
    interview_date?: string | null,
  ) =>
    post<ValuesScorecardDraft>('/api/values-scorecards/generate', {
      application_id,
      transcript,
      host,
      interview_date: interview_date || undefined,
    }),
  valuesScorecardDraft: (draftId: string) => get<ValuesScorecardDraft>(`/api/values-scorecards/${draftId}`),
  editValuesScorecardDraft: (
    draftId: string,
    payload: {
      values?: ValuesScorecardDraftValue[]
      final_comments?: string
      proceed?: boolean
      interview_date?: string | null
    },
  ) => patch<ValuesScorecardDraft>(`/api/values-scorecards/${draftId}`, payload),
  submitValuesScorecardDraft: (draftId: string, overwrite = false) =>
    post<ValuesScorecardDraft>(`/api/values-scorecards/${draftId}/submit`, { overwrite }),

  // Case-study benchmark + scoring lifecycle. Rule 0: /score 409s unless an
  // approved benchmark exists for the target application's own job (looked
  // up server-side, never trusted from the client).
  createCaseStudyBenchmark: (payload: {
    job_id: number
    title: string
    body: string
    kind?: string
    source_path?: string | null
  }) => post<CaseStudyBenchmark>('/api/case-studies/benchmarks', payload),
  approveCaseStudyBenchmark: (benchmarkId: string) =>
    post<CaseStudyBenchmark>(`/api/case-studies/benchmarks/${benchmarkId}/approve`),
  // IMPORTANT 5a: every benchmark on record for a job, newest first, so the
  // page can recover its current (approved) one after a reload instead of
  // depending on an id pasted in by hand.
  listCaseStudyBenchmarks: (jobId: number) =>
    get<CaseStudyBenchmark[]>(`/api/case-studies/benchmarks?job_id=${jobId}`),
  scoreCaseStudy: (applicationId: number) =>
    post<CaseStudyEvaluation>('/api/case-studies/score', { application_id: applicationId }),
  caseStudyEvaluation: (evaluationId: string) =>
    get<CaseStudyEvaluation>(`/api/case-studies/evaluations/${evaluationId}`),
  // IMPORTANT 5b: every evaluation on record for an application, newest
  // first -- the first entry is the current one, the rest are superseded.
  listCaseStudyEvaluations: (applicationId: number) =>
    get<CaseStudyEvaluation[]>(`/api/case-studies/evaluations?application_id=${applicationId}`),

  // --- CV screening (Coco's own criteria; NOT Nugget's technical screening) ---
  cvScreenCriteria: () => get<CVScreenCriterion[]>('/api/cv-screening/criteria'),
  cvScreenJobs: () => get<JobItem[]>('/api/cv-screening/jobs'),
  cvScreenJobSummary: (jobId: number) =>
    get<CVScreenJobSummary>(`/api/cv-screening/jobs/${jobId}/summary`),
  cvScreenApplications: (jobId: number) =>
    get<CVScreenApplication[]>(`/api/cv-screening/jobs/${jobId}/applications`),
  cvScreenHistory: (applicationId: number) =>
    get<CVScreen[]>(`/api/cv-screening/screens?application_id=${applicationId}`),
  cvScreen: (application_id: number) =>
    post<CVScreen>('/api/cv-screening/screen', { application_id }),
  // `retry_skipped` deliberately re-reads the CVs already recorded as
  // unreadable, for after the files have been fixed in Markaz.
  cvScreenBatch: (job_id: number, after: number | null, retry_skipped = false, limit = 4) =>
    post<CVScreenBatch>('/api/cv-screening/screen-batch', {
      job_id, after, limit, retry_skipped,
    }),


  // --- Case-study tracking (who submitted, who has not, what the pool shares) ---
  caseStudyTracking: (jobId: number) =>
    get<CaseStudyTrackingRow[]>(`/api/case-study-tracking/jobs/${jobId}`),
  caseStudyTrackingSummary: (jobId: number) =>
    get<CaseStudyTrackingSummary>(`/api/case-study-tracking/jobs/${jobId}/summary`),
  caseStudyMirrors: (jobId: number) =>
    get<CaseStudyMirrorPair[]>(`/api/case-study-tracking/jobs/${jobId}/mirrors`),
  caseStudyProbe: (application_id: number, required_parts?: string[]) =>
    post<CaseStudyProbe>('/api/case-study-tracking/probe', { application_id, required_parts }),


  // --- KCD evaluation (internal name; reports say "case study") ---
  kcdFramework: () => get<KCDFramework>('/api/kcd-evaluations/framework'),
  kcdCohort: (jobId: number) =>
    get<KCDCohort>(`/api/kcd-evaluations/jobs/${jobId}/cohort`),
  kcdHistory: (applicationId: number) =>
    get<KCDEvaluation[]>(`/api/kcd-evaluations/evaluations?application_id=${applicationId}`),
  kcdEvaluate: (input: KCDEvaluationInput) =>
    post<KCDEvaluation>('/api/kcd-evaluations/evaluations', input),


  // --- Hiring Operations ---
  decisionBrief: (jobId: number) =>
    get<DecisionBrief>(`/api/operations/decision-brief/${jobId}`),
  hiringBrief: (jobId: number) =>
    get<HiringBrief>(`/api/operations/hiring-brief/${jobId}`),
  attendanceEntities: () => get<AttendanceEntities>('/api/operations/attendance/entities'),
  attendance: (on?: string, entities?: string[]) => {
    const qs = new URLSearchParams()
    if (on) qs.set('on', on)
    if (entities?.length) qs.set('entities', entities.join(','))
    const q = qs.toString()
    return get<AttendanceReport>(`/api/operations/attendance${q ? `?${q}` : ''}`)
  },

  // --- Technical screening wizard (Nugget's rubric; NOT Coco's CV screening) ---
  // 🔒 These write to public.nugget_screening_*. /api/evaluations above stays
  // read-only and is untouched. The two screening skills never merge (Rule 33).
  techJobs: () => get<TechJob[]>('/api/tech-screening/jobs'),
  techModels: () => get<TechModel[]>('/api/tech-screening/models'),
  techRubric: (jobId: number) =>
    get<TechRubricStep>(`/api/tech-screening/jobs/${jobId}/rubric`),
  // Drafts a rubric from the JD and WRITES NOTHING. Publishing is a separate,
  // deliberate call because a rubric decides how everyone on the role is judged.
  techDraftRubric: (job_id: number) =>
    post<{ job_id: number; draft: Record<string, unknown> }>(
      '/api/tech-screening/rubric/draft', { job_id },
    ),
  techPublishRubric: (job_id: number, draft: Record<string, unknown>) =>
    post<{ job_id: number; id: string; version: number }>(
      '/api/tech-screening/rubric', { job_id, draft },
    ),
  techPlan: (payload: {
    job_id: number
    mode?: string
    since_days?: number | null
    max_candidates?: number | null
    model: string
    use_batch?: boolean
  }) => post<TechPlan>('/api/tech-screening/runs/plan', payload),
  techCreateRun: (payload: {
    job_id: number
    mode?: string
    since_days?: number | null
    max_candidates?: number | null
    model: string
    use_batch?: boolean
    effort?: string
    cost_cap_usd?: number | null
  }) => post<{ run_id: string; job_id: number; total_items: number }>(
    '/api/tech-screening/runs', payload,
  ),
  techRun: (runId: string) => get<TechRun>(`/api/tech-screening/runs/${runId}`),
  techJobRuns: (jobId: number) =>
    get<TechRun[]>(`/api/tech-screening/jobs/${jobId}/runs`),
  // One slice. The page loops on `remaining` via runScreenAll, which retries
  // through a redeploy rather than losing the run.
  techWork: (runId: string, limit = 3) =>
    post<TechWork>(`/api/tech-screening/runs/${runId}/work`, { limit }),
  techCancelRun: (runId: string) =>
    post<TechRun>(`/api/tech-screening/runs/${runId}/cancel`),


  // --- Talent sourcing ---
  sourcingPool: (p: { job_id?: number; outreach_state?: string; verification_state?: string } = {}) => {
    const qs = new URLSearchParams()
    if (p.job_id != null) qs.set('job_id', String(p.job_id))
    if (p.outreach_state) qs.set('outreach_state', p.outreach_state)
    if (p.verification_state) qs.set('verification_state', p.verification_state)
    const q = qs.toString()
    return get<SourcedCandidate[]>(`/api/sourcing/pool${q ? `?${q}` : ''}`)
  },
  sourcingSummary: () => get<SourcingSummary>('/api/sourcing/summary'),
  sourcingUpdate: (id: string, body: { outreach_state?: string; reply_note?: string; notes?: string }) =>
    patch<SourcedCandidate>(`/api/sourcing/${id}`, body),

  // --- Candidate invites ---
  inviteTypes: () => get<InviteType[]>('/api/invites/types'),
  inviteLinks: (jobId?: number) =>
    get<InviteLink[]>(`/api/invites/links${jobId != null ? `?job_id=${jobId}` : ''}`),
  inviteLinkSave: (body: {
    job_id?: number | null
    invite_type: string
    label?: string | null
    booking_url?: string | null
    jd_url?: string | null
    prep_url?: string | null
    expected_title?: string | null
    cc_list?: string[] | null
  }) => post<InviteLink>('/api/invites/links', body),
  // Fetches the page and stores the title it actually returned. This is the
  // Rule 24 check; a live send refuses until it has run.
  inviteLinkVerify: (id: string) => post<InviteLink>(`/api/invites/links/${id}/verify`, {}),
  invitePreview: (body: {
    invite_type: string
    application_id?: number | null
    job_id?: number | null
    fields?: Record<string, string>
  }) => post<InvitePreview>('/api/invites/preview', body),
  inviteSend: (body: {
    invite_type: string
    application_id?: number | null
    job_id?: number | null
    candidate_email?: string | null
    candidate_name?: string | null
    subject?: string | null
    live: boolean
    fields?: Record<string, string>
    cc?: string[] | null
  }) => post<InviteSendRecord>('/api/invites/send', body),
  inviteSends: (p: { application_id?: number; invite_type?: string; live_only?: boolean } = {}) => {
    const qs = new URLSearchParams()
    if (p.application_id != null) qs.set('application_id', String(p.application_id))
    if (p.invite_type) qs.set('invite_type', p.invite_type)
    if (p.live_only) qs.set('live_only', 'true')
    const q = qs.toString()
    return get<InviteSendRecord[]>(`/api/invites/sends${q ? `?${q}` : ''}`)
  },

  // --- Skill library ---
  skills: () => get<SkillLibrary>('/api/skills'),
  skillFile: (path: string) =>
    get<{ path: string; body: string; words: number }>(
      `/api/skills/file?path=${encodeURIComponent(path)}`,
    ),

  // --- System health (Skill 04) ---
  systemHealth: () => get<SystemHealth>('/api/system/health'),
  systemActivity: () => get<SystemActivity>('/api/system/activity'),
}
