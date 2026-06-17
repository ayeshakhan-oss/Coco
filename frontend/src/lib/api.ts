import type {
  ApplicationDetail,
  Communication,
  CurrentUser,
  DraftContent,
  EvalResult,
  GenerateResponse,
  JobItem,
  ManagedUser,
  QueueRow,
  QueueStats,
  ScorecardResponse,
  SendResponse,
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
      text = typeof detail === 'object' && detail && 'detail' in detail ? JSON.stringify((detail as { detail: unknown }).detail) : JSON.stringify(detail)
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

export interface CandidateQuery {
  status?: string
  job?: number | null
  q?: string
  limit?: number
}

export const api = {
  me: () => get<CurrentUser>('/api/me'),
  stats: () => get<QueueStats>('/api/candidates/stats'),
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

  // User management (super admin)
  listUsers: () => get<ManagedUser[]>('/api/users'),
  createUser: (payload: { email: string; app_role: string; first_name?: string; last_name?: string }) =>
    post<ManagedUser>('/api/users', payload),
  updateUser: (id: string, payload: { app_role?: string; active?: boolean }) =>
    request<ManagedUser>('PATCH', `/api/users/${id}`, payload),
}
