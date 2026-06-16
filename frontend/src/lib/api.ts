import type {
  ApplicationDetail,
  CurrentUser,
  JobItem,
  QueueRow,
  QueueStats,
  ScorecardResponse,
} from './types'

export class ApiError extends Error {
  status: number
  constructor(status: number, message: string) {
    super(message)
    this.status = status
  }
}

async function get<T>(path: string): Promise<T> {
  const res = await fetch(path, {
    credentials: 'include',
    headers: { Accept: 'application/json' },
  })
  if (res.status === 401) {
    // Not authenticated — bounce to login (real SSO lands in Phase 3).
    if (!location.pathname.startsWith('/login')) location.assign('/login')
    throw new ApiError(401, 'Not authenticated')
  }
  if (!res.ok) {
    throw new ApiError(res.status, `${res.status}: ${await res.text()}`)
  }
  return res.json() as Promise<T>
}

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
}
