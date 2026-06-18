import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import {
  AlertTriangle,
  ArrowLeft,
  Briefcase,
  CheckCircle2,
  ClipboardList,
  Clock,
  HelpCircle,
  Mail,
  RefreshCw,
  Search,
} from 'lucide-react'
import { useEffect, useState } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { GmailMatchModal } from '../components/GmailMatchModal'
import { StatCard } from '../components/StatCard'
import { StatusBadge } from '../components/StatusBadge'
import { Spinner } from '../components/Spinner'
import { api } from '../lib/api'
import { fullName, relativeTime, suggestedAction } from '../lib/format'
import { canEdit } from '../lib/roles'
import type { GmailStatus, PositionSummary, QueueRow } from '../lib/types'

type Filter = 'relevant' | 'needs_comms' | 'high_priority' | 'already_sent' | 'awaiting_scorecard' | 'needs_review'
const FILTER_CHIPS: { key: Filter; label: string }[] = [
  { key: 'relevant', label: 'All' },
  { key: 'needs_comms', label: 'Needs comms' },
  { key: 'high_priority', label: 'High priority' },
  { key: 'already_sent', label: 'Sent' },
  { key: 'awaiting_scorecard', label: 'Awaiting' },
  { key: 'needs_review', label: 'Needs review' },
]

export function QueuePage() {
  const [params] = useSearchParams()
  const job = params.get('job') ? Number(params.get('job')) : null
  return job == null ? <PositionsView /> : <CandidatesView job={job} />
}

/* ── Gmail sync bar (global) ─────────────────────────────────────────────── */
function SyncBar() {
  const qc = useQueryClient()
  const meQ = useQuery({ queryKey: ['me'], queryFn: api.me, retry: false })
  const statusQ = useQuery({ queryKey: ['gmail-sync-status'], queryFn: api.gmailSyncStatus })
  const refresh = useMutation({
    mutationFn: () => api.refreshGmailSync(false),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['gmail-sync-status'] })
      qc.invalidateQueries({ queryKey: ['stats'] })
      qc.invalidateQueries({ queryKey: ['positions'] })
      qc.invalidateQueries({ queryKey: ['candidates'] })
    },
  })
  const s = statusQ.data
  const mayRefresh = canEdit(meQ.data?.app_role)

  return (
    <div className="mb-5 flex flex-wrap items-center justify-between gap-3 rounded-xl border border-hairline bg-surface px-4 py-2.5">
      <div className="flex items-center gap-2 text-sm text-ink-muted">
        <Mail className="h-4 w-4 text-blurple" />
        <span>
          Gmail sync: <span className="font-medium text-ink">synced {relativeTime(s?.last_sync_at)}</span>
        </span>
        {s?.status === 'failed' && (
          <span className="inline-flex items-center gap-1 text-xs text-danger">
            <AlertTriangle className="h-3.5 w-3.5" /> last run failed
          </span>
        )}
        {s?.status === 'running' && <span className="text-xs text-ink-dim">running…</span>}
      </div>
      {mayRefresh && (
        <button
          type="button"
          onClick={() => refresh.mutate()}
          disabled={refresh.isPending}
          className="btn btn-ghost h-8 text-sm"
          title="Re-check Gmail Sent mail for new evidence"
        >
          <RefreshCw className={`h-4 w-4 ${refresh.isPending ? 'animate-spin' : ''}`} />
          {refresh.isPending ? 'Syncing…' : 'Refresh Gmail sync'}
        </button>
      )}
      {refresh.isError && <span className="text-xs text-danger">Sync failed or already running.</span>}
    </div>
  )
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
    { label: 'High priority', value: s?.high_priority ?? 0, icon: AlertTriangle, tone: 'danger' },
    { label: 'Sent', value: s?.sent ?? 0, icon: CheckCircle2, tone: 'green' },
    { label: 'Needs review', value: s?.needs_review ?? 0, icon: HelpCircle, tone: 'cyan' },
  ] as const

  return (
    <div className="mx-auto max-w-7xl px-8 py-7">
      <header className="mb-5">
        <h1 className="font-display text-2xl font-bold text-ink">Candidate Queue</h1>
        <p className="mt-1 text-sm text-ink-muted">Pick a position to see its candidates. Totals across all positions:</p>
      </header>

      <SyncBar />

      <div className="mb-7 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {cards.map((c) => (
          <StatCard key={c.label} label={c.label} value={c.value} icon={c.icon} tone={c.tone} />
        ))}
      </div>

      <h2 className="mb-3 text-xs font-semibold uppercase tracking-wide text-ink-dim">Open positions</h2>
      {positionsQuery.isLoading ? (
        <Spinner label="Loading positions…" />
      ) : !positionsQuery.data?.length ? (
        <div className="card p-12 text-center text-sm text-ink-dim">No positions with comms-relevant candidates yet.</div>
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
        {p.high_priority > 0 && <span className="chip shrink-0 bg-danger/15 text-danger">{p.high_priority} high</span>}
      </div>
      <div className="mt-4 flex flex-wrap gap-x-4 gap-y-1 pl-10 text-sm text-ink-muted">
        {p.needs_comms > 0 && <span className="text-magenta">{p.needs_comms} need comms</span>}
        {p.sent > 0 && <span className="text-green">{p.sent} sent</span>}
        {p.needs_review > 0 && <span className="text-cyan">{p.needs_review} review</span>}
        {p.awaiting_scorecard > 0 && <span className="text-ink-dim">{p.awaiting_scorecard} awaiting</span>}
      </div>
      <div className="mt-3 pl-10 text-[11px] text-ink-dim">Gmail synced {relativeTime(p.last_gmail_sync_at)}</div>
    </button>
  )
}

/* ── Level 2: candidates within a position ──────────────────────────────── */
function CandidatesView({ job }: { job: number }) {
  const navigate = useNavigate()
  const [params, setParams] = useSearchParams()
  const meQ = useQuery({ queryKey: ['me'], queryFn: api.me, retry: false })
  const bucket = (params.get('status') as Filter) || 'relevant'
  const [match, setMatch] = useState<{ appId: number; name: string } | null>(null)

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
    if (next === 'relevant') p.delete('status')
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
        <p className="mt-1 text-sm text-ink-muted">Communication status from Markaz decisions cross-checked with Gmail.</p>
      </header>

      <div className="mb-4 flex flex-wrap items-center gap-3">
        <div className="flex flex-wrap gap-1.5">
          {FILTER_CHIPS.map((c) => (
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
                <th className="px-5 py-3 font-medium">Status</th>
                <th className="px-5 py-3 font-medium">Waiting</th>
                <th className="px-5 py-3 font-medium">Gmail</th>
                <th className="px-5 py-3 font-medium">Next action</th>
                <th className="px-5 py-3" />
              </tr>
            </thead>
            <tbody className="divide-y divide-hairline">
              {candidatesQuery.data.map((row) => (
                <Row
                  key={row.application_id}
                  row={row}
                  onOpen={() => navigate(`/applications/${row.application_id}`)}
                  onMatch={() => setMatch({ appId: row.application_id, name: fullName(row) })}
                />
              ))}
            </tbody>
          </table>
        )}
      </div>

      {match && (
        <GmailMatchModal
          applicationId={match.appId}
          candidateName={match.name}
          role={meQ.data?.app_role}
          onClose={() => setMatch(null)}
        />
      )}
    </div>
  )
}

const GMAIL_DOT: Record<GmailStatus, { cls: string; label: string }> = {
  found: { cls: 'text-green', label: 'found' },
  uncertain: { cls: 'text-cyan', label: 'review' },
  none: { cls: 'text-ink-dim', label: 'none' },
  not_checked: { cls: 'text-ink-dim', label: '—' },
}

const BORDER_TONE: Record<string, string> = {
  sent: 'border-l-green',
  high_priority: 'border-l-danger',
  needs_comms: 'border-l-magenta',
  needs_review: 'border-l-cyan',
  in_progress: 'border-l-blurple',
  awaiting_scorecard: 'border-l-ink-dim',
}

function Row({ row, onOpen, onMatch }: { row: QueueRow; onOpen: () => void; onMatch: () => void }) {
  const tone = BORDER_TONE[row.display_status] ?? 'border-l-ink-dim'
  const dot = GMAIL_DOT[row.gmail_status] ?? GMAIL_DOT.not_checked
  const overdue = row.display_status === 'high_priority'

  return (
    <tr onClick={onOpen} className={`cursor-pointer border-l-4 ${tone} transition-colors hover:bg-elevated`}>
      <td className="px-5 py-3">
        <div className="font-medium text-ink">{fullName(row)}{row.ignored && <span className="ml-2 text-[11px] text-ink-dim">(ignored)</span>}</div>
        <div className="text-xs text-ink-dim">{row.email}</div>
      </td>
      <td className="px-5 py-3"><StatusBadge status={row.display_status} /></td>
      <td className="px-5 py-3">
        {row.days_waiting != null ? (
          <span className={`inline-flex items-center gap-1 ${overdue ? 'font-semibold text-danger' : 'text-ink-muted'}`}>
            <Clock className="h-3.5 w-3.5" /> {row.days_waiting}d
          </span>
        ) : (
          <span className="text-ink-dim">—</span>
        )}
      </td>
      <td className="px-5 py-3">
        <span className={`inline-flex items-center gap-1.5 text-xs ${dot.cls}`}>
          <span className="h-1.5 w-1.5 rounded-full bg-current" /> {dot.label}
        </span>
      </td>
      <td className="px-5 py-3 text-ink-muted">{suggestedAction(row)}</td>
      <td className="px-5 py-3 text-right">
        <button
          type="button"
          onClick={(e) => { e.stopPropagation(); onMatch() }}
          className="rounded-lg p-1.5 text-ink-dim transition-colors hover:bg-surface-2 hover:text-[#4752c4]"
          title="View Gmail match / mark sent / ignore"
        >
          <Mail className="h-4 w-4" />
        </button>
      </td>
    </tr>
  )
}
