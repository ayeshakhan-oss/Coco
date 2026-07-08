import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import {
  AlertTriangle,
  ArrowLeft,
  Briefcase,
  CheckCircle2,
  ClipboardList,
  Clock,
  HelpCircle,
  Inbox,
  Loader2,
  Mail,
  PenLine,
  RefreshCw,
  Search,
  XCircle,
} from 'lucide-react'
import { useEffect, useState } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { GmailMatchModal } from '../components/GmailMatchModal'
import { StatCard } from '../components/StatCard'
import { StatusBadge } from '../components/StatusBadge'
import { Spinner } from '../components/Spinner'
import { api } from '../lib/api'
import { useBulk } from '../lib/bulk'
import { emailTypeLabel, fullName, relativeTime, suggestedAction } from '../lib/format'
import { canApprove, canEdit } from '../lib/roles'
import { EMAIL_TYPES } from '../lib/types'
import type { GmailStatus, PositionSummary, QueueRow } from '../lib/types'

type Filter =
  | 'relevant'
  | 'needs_comms'
  | 'high_priority'
  | 'already_sent'
  | 'awaiting_scorecard'
  | 'needs_review'
  | 'ignored'

const FILTER_CHIPS: { key: Filter; label: string }[] = [
  { key: 'relevant', label: 'All' },
  { key: 'needs_comms', label: 'Needs comms' },
  { key: 'high_priority', label: 'High priority' },
  { key: 'already_sent', label: 'Sent' },
  { key: 'awaiting_scorecard', label: 'Awaiting' },
  { key: 'needs_review', label: 'Needs review' },
  { key: 'ignored', label: 'Ignored' },
]
const FILTER_LABEL: Record<string, string> = Object.fromEntries(FILTER_CHIPS.map((c) => [c.key, c.label]))

export function QueuePage() {
  const [params] = useSearchParams()
  const job = params.get('job') ? Number(params.get('job')) : null
  const status = params.get('status')
  if (job != null) return <CandidatesView job={job} />
  if (status) return <CandidatesView job={null} /> // global, filtered by status
  return <PositionsView />
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
          title="Re-check Gmail for new evidence"
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
  const statsQuery = useQuery({ queryKey: ['stats'], queryFn: api.stats })
  const positionsQuery = useQuery({ queryKey: ['positions'], queryFn: api.positions })
  const s = statsQuery.data

  // Overview cards (volume) + comms cards (status). The comms ones drill into
  // that population across ALL positions; the volume ones are at-a-glance.
  const cards = [
    { label: 'Applications received', value: s?.total_applications ?? 0, icon: Inbox, tone: 'brand', filter: null },
    { label: 'Open positions', value: s?.open_positions ?? 0, icon: Briefcase, tone: 'violet', filter: null },
    { label: 'Needs comms', value: s?.needs_comms ?? 0, icon: ClipboardList, tone: 'amber', filter: 'needs_comms' },
    { label: 'High priority', value: s?.high_priority ?? 0, icon: AlertTriangle, tone: 'danger', filter: 'high_priority' },
    { label: 'Sent', value: s?.sent ?? 0, icon: CheckCircle2, tone: 'green', filter: 'already_sent' },
    { label: 'Needs review', value: s?.needs_review ?? 0, icon: HelpCircle, tone: 'cyan', filter: 'needs_review' },
  ] as const

  return (
    <div className="mx-auto max-w-7xl px-8 py-7">
      <header className="mb-4">
        <h1 className="font-display text-2xl font-bold text-ink">Candidate Queue</h1>
        <p className="mt-1 text-sm text-ink-muted">Click a total to see those candidates across all positions, or open a position below.</p>
      </header>

      <SyncBar />

      <div className="mb-7 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6">
        {cards.map((c) => (
          <StatCard
            key={c.label}
            label={c.label}
            value={c.value}
            icon={c.icon}
            tone={c.tone}
            onClick={c.filter ? () => setParams({ status: c.filter as string }) : undefined}
          />
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
            <PositionCard key={p.job_pk} p={p} onClick={() => setParams({ job: String(p.job_pk) })} />
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

/* ── Level 2: candidate list — per-position (job set) OR global (job null) ── */
function CandidatesView({ job }: { job: number | null }) {
  const navigate = useNavigate()
  const [params, setParams] = useSearchParams()
  const qc = useQueryClient()
  const meQ = useQuery({ queryKey: ['me'], queryFn: api.me, retry: false })
  const role = meQ.data?.app_role
  const global = job == null
  const bucket = ((params.get('status') as Filter) || 'relevant') as Filter
  const [match, setMatch] = useState<{ appId: number; name: string } | null>(null)
  const [selected, setSelected] = useState<Set<number>>(new Set())
  const bulk = useBulk()
  const [showTypes, setShowTypes] = useState(false)
  const [banner, setBanner] = useState<string | null>(null)

  const [search, setSearch] = useState(params.get('q') || '')
  const [debouncedQ, setDebouncedQ] = useState(search)
  useEffect(() => {
    const t = setTimeout(() => setDebouncedQ(search), 300)
    return () => clearTimeout(t)
  }, [search])

  const positionsQuery = useQuery({ queryKey: ['positions'], queryFn: api.positions })
  const candidatesQuery = useQuery({
    queryKey: ['candidates', bucket, job, debouncedQ],
    queryFn: () => api.candidates({ status: bucket, job: job ?? undefined, q: debouncedQ || undefined }),
  })
  const rows = candidatesQuery.data ?? []

  // Clear selection whenever the view (filter / position / search) changes.
  useEffect(() => setSelected(new Set()), [bucket, job, debouncedQ])

  const title = global
    ? `${FILTER_LABEL[bucket] ?? 'Candidates'} · all positions`
    : positionsQuery.data?.find((p) => p.job_pk === job)?.job_title || rows[0]?.job_title || 'Position'

  function setBucket(next: Filter) {
    const p = new URLSearchParams(params)
    if (next === 'relevant' && !global) p.delete('status')
    else p.set('status', next)
    setParams(p, { replace: true })
  }
  function back() {
    setParams(new URLSearchParams(), { replace: true })
  }

  const invalidate = () => {
    qc.invalidateQueries({ queryKey: ['candidates'] })
    qc.invalidateQueries({ queryKey: ['stats'] })
    qc.invalidateQueries({ queryKey: ['positions'] })
    setSelected(new Set())
  }
  const bulkMarkSent = useMutation({ mutationFn: () => api.bulkMarkSent([...selected]), onSuccess: invalidate })
  const bulkIgnore = useMutation({ mutationFn: () => api.bulkIgnore([...selected], true), onSuccess: invalidate })
  const bulkBusy = bulkMarkSent.isPending || bulkIgnore.isPending

  // Bulk-draft: generate a feedback email of the chosen type for each selected
  // candidate and submit it, so the batch lands in Review ready to approve/send.
  async function bulkDraft(emailType: string) {
    setShowTypes(false)
    setBanner(null)
    const ids = [...selected]
    const { failed } = await bulk.run(
      ids,
      async (appId) => {
        const r = await api.generate(appId, emailType)
        await api.submit(r.communication.id)
      },
      (id) => `#${id}`,
    )
    const ok = ids.length - failed.length
    setBanner(
      `Drafted ${ok} of ${ids.length} ${emailTypeLabel(emailType).toLowerCase()} email${ids.length === 1 ? '' : 's'}` +
        (failed.length ? `, ${failed.length} could not be drafted (open them individually)` : '') +
        ' — now in Review for approval.',
    )
    invalidate()
  }

  function toggle(id: number) {
    setSelected((prev) => {
      const next = new Set(prev)
      next.has(id) ? next.delete(id) : next.add(id)
      return next
    })
  }
  const allSelected = rows.length > 0 && rows.every((r) => selected.has(r.application_id))
  function toggleAll() {
    setSelected(allSelected ? new Set() : new Set(rows.map((r) => r.application_id)))
  }

  return (
    <div className="mx-auto max-w-7xl px-8 py-7">
      <button type="button" onClick={back} className="mb-4 inline-flex items-center gap-1.5 text-sm text-ink-dim hover:text-ink">
        <ArrowLeft className="h-4 w-4" /> All positions
      </button>
      <header className="mb-5">
        <h1 className="font-display text-2xl font-bold text-ink">{title}</h1>
        <p className="mt-1 text-sm text-ink-muted">Communication status from Markaz decisions cross-checked with Gmail + Markaz history.</p>
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

      {/* Bulk-draft result banner */}
      {banner && (
        <div className="mb-3 flex items-center gap-3 rounded-xl border border-green/30 bg-green/10 px-4 py-2.5 text-sm text-ink">
          <CheckCircle2 className="h-4 w-4 flex-shrink-0 text-green" />
          <span>{banner}</span>
          <button type="button" onClick={() => navigate('/review')} className="ml-auto whitespace-nowrap font-medium text-blurple-600 hover:underline">
            Go to Review →
          </button>
          <button type="button" onClick={() => setBanner(null)} className="text-ink-dim hover:text-ink" aria-label="Dismiss">
            <XCircle className="h-4 w-4" />
          </button>
        </div>
      )}

      {/* Bulk action bar */}
      {selected.size > 0 && (
        <div className="mb-3 flex flex-wrap items-center gap-3 rounded-xl border border-blurple/40 bg-blurple/5 px-4 py-2.5">
          <span className="text-sm font-semibold text-ink">{selected.size} selected</span>
          {canEdit(role) && (
            <div className="relative">
              <button
                type="button"
                disabled={bulk.running || bulkBusy}
                onClick={() => setShowTypes((v) => !v)}
                className="btn btn-primary h-8 text-sm"
              >
                {bulk.running ? <Loader2 className="h-4 w-4 animate-spin" /> : <PenLine className="h-4 w-4" />}
                {bulk.running ? `Drafting ${bulk.done}/${bulk.total}…` : 'Draft feedback'}
              </button>
              {showTypes && !bulk.running && (
                <div className="absolute left-0 top-full z-20 mt-1 w-60 overflow-hidden rounded-lg border border-hairline bg-surface shadow-lg">
                  <div className="border-b border-hairline px-3 py-1.5 text-xs font-medium text-ink-dim">
                    Draft which email for all {selected.size}?
                  </div>
                  {EMAIL_TYPES.map((t) => (
                    <button
                      key={t.value}
                      type="button"
                      onClick={() => bulkDraft(t.value)}
                      className="block w-full px-3 py-2 text-left text-sm text-ink hover:bg-elevated"
                    >
                      {t.label}
                    </button>
                  ))}
                </div>
              )}
            </div>
          )}
          {canApprove(role) && (
            <button type="button" disabled={bulkBusy} onClick={() => bulkMarkSent.mutate()} className="btn btn-green h-8 text-sm">
              {bulkMarkSent.isPending ? <Loader2 className="h-4 w-4 animate-spin" /> : <CheckCircle2 className="h-4 w-4" />}
              Mark sent
            </button>
          )}
          {canEdit(role) && (
            <button type="button" disabled={bulkBusy} onClick={() => bulkIgnore.mutate()} className="btn btn-ghost h-8 text-sm">
              {bulkIgnore.isPending ? <Loader2 className="h-4 w-4 animate-spin" /> : <XCircle className="h-4 w-4" />}
              Ignore (e.g. interview never scheduled)
            </button>
          )}
          <button type="button" onClick={() => setSelected(new Set())} className="ml-auto text-sm text-ink-dim hover:text-ink">
            Clear
          </button>
        </div>
      )}

      <div className="card overflow-hidden">
        {candidatesQuery.isLoading ? (
          <Spinner label="Loading candidates…" />
        ) : candidatesQuery.isError ? (
          <div className="p-8 text-center text-sm text-danger">Failed to load candidates.</div>
        ) : !rows.length ? (
          <div className="p-12 text-center text-sm text-ink-dim">Nothing here — all clear for this view 🎉</div>
        ) : (
          <table className="w-full text-left text-sm">
            <thead className="border-b border-hairline bg-surface-2 text-xs uppercase tracking-wide text-ink-dim">
              <tr>
                {canEdit(role) && (
                  <th className="w-10 px-4 py-3">
                    <input type="checkbox" checked={allSelected} onChange={toggleAll} aria-label="Select all" />
                  </th>
                )}
                <th className="px-5 py-3 font-medium">Candidate</th>
                {global && <th className="px-5 py-3 font-medium">Position</th>}
                <th className="px-5 py-3 font-medium">Status</th>
                <th className="px-5 py-3 font-medium">Waiting</th>
                <th className="px-5 py-3 font-medium">Gmail</th>
                <th className="px-5 py-3 font-medium">Next action</th>
                <th className="px-5 py-3" />
              </tr>
            </thead>
            <tbody className="divide-y divide-hairline">
              {rows.map((row) => (
                <Row
                  key={row.application_id}
                  row={row}
                  showPosition={global}
                  selectable={canEdit(role)}
                  selected={selected.has(row.application_id)}
                  onToggle={() => toggle(row.application_id)}
                  onOpen={() =>
                    navigate(`/applications/${row.application_id}`, {
                      state: { backTo: `/queue?${params.toString()}`, backLabel: title },
                    })
                  }
                  onMatch={() => setMatch({ appId: row.application_id, name: fullName(row) })}
                />
              ))}
            </tbody>
          </table>
        )}
      </div>

      {match && (
        <GmailMatchModal applicationId={match.appId} candidateName={match.name} role={role} onClose={() => setMatch(null)} />
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
  ignored: 'border-l-ink-dim',
}

function Row({
  row,
  showPosition,
  selectable,
  selected,
  onToggle,
  onOpen,
  onMatch,
}: {
  row: QueueRow
  showPosition: boolean
  selectable: boolean
  selected: boolean
  onToggle: () => void
  onOpen: () => void
  onMatch: () => void
}) {
  const tone = BORDER_TONE[row.display_status] ?? 'border-l-ink-dim'
  const dot = GMAIL_DOT[row.gmail_status] ?? GMAIL_DOT.not_checked
  const overdue = row.display_status === 'high_priority'

  return (
    <tr className={`border-l-4 ${tone} transition-colors hover:bg-elevated ${selected ? 'bg-blurple/5' : ''}`}>
      {selectable && (
        <td className="px-4 py-3" onClick={(e) => e.stopPropagation()}>
          <input type="checkbox" checked={selected} onChange={onToggle} aria-label="Select candidate" />
        </td>
      )}
      <td className="cursor-pointer px-5 py-3" onClick={onOpen}>
        <div className="font-medium text-ink">
          {fullName(row)}
          {row.ignored && <span className="ml-2 text-[11px] text-ink-dim">(ignored)</span>}
        </div>
        <div className="text-xs text-ink-dim">{row.email}</div>
      </td>
      {showPosition && (
        <td className="cursor-pointer px-5 py-3 text-ink-muted" onClick={onOpen}>
          {row.job_title}
        </td>
      )}
      <td className="cursor-pointer px-5 py-3" onClick={onOpen}>
        <StatusBadge status={row.display_status} />
      </td>
      <td className="cursor-pointer px-5 py-3" onClick={onOpen}>
        {row.days_waiting != null ? (
          <span className={`inline-flex items-center gap-1 ${overdue ? 'font-semibold text-danger' : 'text-ink-muted'}`}>
            <Clock className="h-3.5 w-3.5" /> {row.days_waiting}d
          </span>
        ) : (
          <span className="text-ink-dim">—</span>
        )}
      </td>
      <td className="cursor-pointer px-5 py-3" onClick={onOpen}>
        <span className={`inline-flex items-center gap-1.5 text-xs ${dot.cls}`}>
          <span className="h-1.5 w-1.5 rounded-full bg-current" /> {dot.label}
        </span>
      </td>
      <td className="cursor-pointer px-5 py-3 text-ink-muted" onClick={onOpen}>
        {suggestedAction(row)}
      </td>
      <td className="px-5 py-3 text-right">
        <button
          type="button"
          onClick={(e) => {
            e.stopPropagation()
            onMatch()
          }}
          className="rounded-lg p-1.5 text-ink-dim transition-colors hover:bg-surface-2 hover:text-blurple-600"
          title="View Gmail match / mark sent / ignore"
        >
          <Mail className="h-4 w-4" />
        </button>
      </td>
    </tr>
  )
}
