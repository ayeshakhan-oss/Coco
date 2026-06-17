import { useQuery } from '@tanstack/react-query'
import { ArrowLeft, Briefcase, CheckCircle2, ClipboardList, Clock, FileQuestion, Search } from 'lucide-react'
import { useEffect, useState } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { StatCard } from '../components/StatCard'
import { Pill, StatusBadge } from '../components/StatusBadge'
import { Spinner } from '../components/Spinner'
import { api } from '../lib/api'
import { formatDate, fullName, scorecardLabel } from '../lib/format'
import type { Bucket, PositionSummary, QueueRow } from '../lib/types'

type Filter = Bucket | 'scored'
const BUCKET_CHIPS: { key: Filter; label: string }[] = [
  { key: 'scored', label: 'All' },
  { key: 'needs_comms', label: 'Needs comms' },
  { key: 'in_progress', label: 'In progress' },
  { key: 'sent', label: 'Sent' },
]

export function QueuePage() {
  const [params] = useSearchParams()
  const job = params.get('job') ? Number(params.get('job')) : null
  return job == null ? <PositionsView /> : <CandidatesView job={job} />
}

/* ── Level 1: positions ─────────────────────────────────────────────────── */
function PositionsView() {
  const [, setParams] = useSearchParams()
  const onOpen = (jobPk: number) => setParams({ job: String(jobPk) }, { replace: true })
  const statsQuery = useQuery({ queryKey: ['stats'], queryFn: api.stats })
  const positionsQuery = useQuery({ queryKey: ['positions'], queryFn: api.positions })
  const s = statsQuery.data

  const cards = [
    { label: 'Needs comms', value: s?.needs_comms ?? 0, icon: ClipboardList, tone: 'amber' },
    { label: 'In progress', value: s?.in_progress ?? 0, icon: Clock, tone: 'brand' },
    { label: 'Sent', value: s?.sent ?? 0, icon: CheckCircle2, tone: 'green' },
    { label: 'Awaiting scorecard', value: s?.awaiting_scorecard ?? 0, icon: FileQuestion, tone: 'slate' },
  ] as const

  return (
    <div className="mx-auto max-w-7xl px-8 py-7">
      <header className="mb-6">
        <h1 className="font-display text-2xl font-bold text-ink">Candidate Queue</h1>
        <p className="mt-1 text-sm text-ink-muted">Pick a position to see its candidates. Totals across all positions:</p>
      </header>

      <div className="mb-7 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {cards.map((c) => (
          <StatCard key={c.label} label={c.label} value={c.value} icon={c.icon} tone={c.tone} />
        ))}
      </div>

      <h2 className="mb-3 text-xs font-semibold uppercase tracking-wide text-ink-dim">Open positions</h2>
      {positionsQuery.isLoading ? (
        <Spinner label="Loading positions…" />
      ) : !positionsQuery.data?.length ? (
        <div className="card p-12 text-center text-sm text-ink-dim">No positions with completed scorecards yet.</div>
      ) : (
        <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
          {positionsQuery.data.map((p) => (
            <PositionCard key={p.job_pk} p={p} onClick={() => onOpen(p.job_pk)} />
          ))}
        </div>
      )}
    </div>
  )
}

function PositionCard({ p, onClick }: { p: PositionSummary; onClick: () => void }) {
  return (
    <button type="button" onClick={onClick} className="card flex flex-col p-5 text-left transition-colors hover:bg-elevated">
      <div className="flex items-start justify-between gap-3">
        <div>
          <div className="flex items-center gap-2">
            <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-blurple/15 text-blurple"><Briefcase className="h-4 w-4" /></span>
            <span className="font-display text-base font-bold leading-tight text-ink">{p.job_title}</span>
          </div>
          <div className="mt-1 pl-10 text-xs text-ink-dim">{p.job_code}</div>
        </div>
        {p.needs_comms > 0 && <span className="chip shrink-0 bg-magenta/15 text-magenta">{p.needs_comms} need comms</span>}
      </div>
      <div className="mt-4 flex flex-wrap gap-x-4 gap-y-1 pl-10 text-sm text-ink-muted">
        <span>{p.scored} scored</span>
        {p.in_progress > 0 && <span className="text-[#4752c4]">{p.in_progress} in progress</span>}
        {p.sent > 0 && <span className="text-green">{p.sent} sent</span>}
      </div>
    </button>
  )
}

/* ── Level 2: candidates within a position ──────────────────────────────── */
function CandidatesView({ job }: { job: number }) {
  const navigate = useNavigate()
  const [params, setParams] = useSearchParams()
  const bucket = (params.get('status') as Filter) || 'scored'

  const [search, setSearch] = useState(params.get('q') || '')
  const [debouncedQ, setDebouncedQ] = useState(search)
  useEffect(() => {
    const t = setTimeout(() => setDebouncedQ(search), 300)
    return () => clearTimeout(t)
  }, [search])

  const positionsQuery = useQuery({ queryKey: ['positions'], queryFn: api.positions })
  const candidatesQuery = useQuery({
    queryKey: ['candidates', bucket, job, debouncedQ],
    queryFn: () => api.candidates({ status: bucket, job, q: debouncedQ || undefined }),
  })

  const title = positionsQuery.data?.find((p) => p.job_pk === job)?.job_title || candidatesQuery.data?.[0]?.job_title || 'Position'

  function setBucket(next: Filter) {
    const p = new URLSearchParams(params)
    if (next === 'scored') p.delete('status')
    else p.set('status', next)
    setParams(p, { replace: true })
  }
  function back() {
    setParams(new URLSearchParams(), { replace: true })
  }

  return (
    <div className="mx-auto max-w-7xl px-8 py-7">
      <button type="button" onClick={back} className="mb-4 inline-flex items-center gap-1.5 text-sm text-ink-dim hover:text-ink">
        <ArrowLeft className="h-4 w-4" /> All positions
      </button>
      <header className="mb-5">
        <h1 className="font-display text-2xl font-bold text-ink">{title}</h1>
        <p className="mt-1 text-sm text-ink-muted">Candidates for this position with a completed scorecard.</p>
      </header>

      <div className="mb-4 flex flex-wrap items-center gap-3">
        <div className="flex flex-wrap gap-1.5">
          {BUCKET_CHIPS.map((c) => (
            <button
              key={c.key}
              type="button"
              onClick={() => setBucket(c.key)}
              className={`rounded-full px-3 py-1.5 text-sm font-medium transition-colors ${
                bucket === c.key ? 'bg-blurple text-white' : 'bg-surface-2 text-ink-muted hover:bg-elevated'
              }`}
            >
              {c.label}
            </button>
          ))}
        </div>
        <div className="relative ml-auto">
          <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-ink-dim" />
          <input value={search} onChange={(e) => setSearch(e.target.value)} placeholder="Search name or email…" className="input h-9 w-64 pl-9" />
        </div>
      </div>

      <div className="card overflow-hidden">
        {candidatesQuery.isLoading ? (
          <Spinner label="Loading candidates…" />
        ) : candidatesQuery.isError ? (
          <div className="p-8 text-center text-sm text-danger">Failed to load candidates.</div>
        ) : !candidatesQuery.data?.length ? (
          <div className="p-12 text-center text-sm text-ink-dim">No candidates match this view.</div>
        ) : (
          <table className="w-full text-left text-sm">
            <thead className="border-b border-hairline bg-surface-2 text-xs uppercase tracking-wide text-ink-dim">
              <tr>
                <th className="px-5 py-3 font-medium">Candidate</th>
                <th className="px-5 py-3 font-medium">Scorecard</th>
                <th className="px-5 py-3 font-medium">Status</th>
                <th className="px-5 py-3 font-medium">Interview date</th>
                <th className="px-5 py-3 font-medium">Prior emails</th>
                <th className="px-5 py-3" />
              </tr>
            </thead>
            <tbody className="divide-y divide-hairline">
              {candidatesQuery.data.map((row) => (
                <Row key={row.application_id} row={row} onOpen={() => navigate(`/applications/${row.application_id}`)} />
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}

function Row({ row, onOpen }: { row: QueueRow; onOpen: () => void }) {
  const borderTone =
    row.bucket === 'sent'
      ? 'border-l-green'
      : row.bucket === 'needs_comms'
        ? 'border-l-magenta'
        : row.bucket === 'in_progress'
          ? 'border-l-blurple'
          : 'border-l-ink-dim'

  return (
    <tr onClick={onOpen} className={`cursor-pointer border-l-4 ${borderTone} transition-colors hover:bg-elevated`}>
      <td className="px-5 py-3">
        <div className="font-medium text-ink">{fullName(row)}</div>
        <div className="text-xs text-ink-dim">{row.email}</div>
      </td>
      <td className="px-5 py-3">
        <div className="flex items-center gap-1.5">
          <span className="text-ink-muted">{scorecardLabel(row)}</span>
          {row.values_interview_result && (
            <Pill tone={row.values_interview_result === 'pass' ? 'green' : 'red'}>{row.values_interview_result}</Pill>
          )}
        </div>
      </td>
      <td className="px-5 py-3"><StatusBadge bucket={row.bucket} /></td>
      <td className="px-5 py-3 text-ink-muted">{formatDate(row.scorecard_date)}</td>
      <td className="px-5 py-3">
        {row.prior_platform_comms > 0 ? <Pill tone="slate">{row.prior_platform_comms} on record</Pill> : <span className="text-ink-dim">—</span>}
      </td>
      <td className="px-5 py-3 text-right">
        <span className="text-sm font-medium text-[#4752c4]">
          {row.bucket === 'sent' ? 'View' : row.bucket === 'in_progress' ? 'Continue' : 'Draft'} →
        </span>
      </td>
    </tr>
  )
}
