import { useQuery } from '@tanstack/react-query'
import type { ReactNode } from 'react'
import { useState } from 'react'
import { ArrowLeft, Clock, Loader2, Mail, PenLine, Sparkles } from 'lucide-react'
import { Link, useLocation, useNavigate, useParams } from 'react-router-dom'
import { GmailMatchModal } from '../components/GmailMatchModal'
import { Pill, StatusBadge } from '../components/StatusBadge'
import { ScorecardView } from '../components/ScorecardView'
import { Spinner } from '../components/Spinner'
import { ApiError, api } from '../lib/api'
import { emailTypeLabel, formatDate, fullName } from '../lib/format'
import { canEdit } from '../lib/roles'
import { EMAIL_TYPES } from '../lib/types'
import type { TimelineItem } from '../lib/types'

export function ApplicationDetailPage() {
  const { id } = useParams()
  const appId = Number(id)
  const navigate = useNavigate()
  const location = useLocation()
  const navState = (location.state as { backTo?: string; backLabel?: string } | null) || null

  const meQ = useQuery({ queryKey: ['me'], queryFn: api.me, retry: false })
  const detailQuery = useQuery({ queryKey: ['candidate', appId], queryFn: () => api.candidate(appId), enabled: !Number.isNaN(appId) })
  const scorecardQuery = useQuery({ queryKey: ['scorecard', appId], queryFn: () => api.scorecard(appId), enabled: !Number.isNaN(appId) })
  const timelineQuery = useQuery({ queryKey: ['timeline', appId], queryFn: () => api.timeline(appId), enabled: !Number.isNaN(appId) })

  const [emailType, setEmailType] = useState('values_feedback')
  const [generating, setGenerating] = useState(false)
  const [genErr, setGenErr] = useState<string | null>(null)
  const [matchOpen, setMatchOpen] = useState(false)
  const mayDraft = canEdit(meQ.data?.app_role)

  async function generateDraft() {
    setGenerating(true)
    setGenErr(null)
    try {
      const r = await api.generate(appId, emailType)
      navigate(`/drafts/${r.communication.id}`)
    } catch (e) {
      setGenErr((e as ApiError).message)
      setGenerating(false)
    }
  }

  if (detailQuery.isLoading) return <Spinner label="Loading candidate…" />
  if (detailQuery.isError || !detailQuery.data) return <div className="p-8 text-sm text-danger">Could not load this application.</div>

  const d = detailQuery.data
  const backTo = navState?.backTo ?? (d.job_pk ? `/?job=${d.job_pk}` : '/')
  const backLabel = navState?.backLabel ?? d.job_title ?? 'queue'

  return (
    <div className="mx-auto max-w-6xl px-8 py-7">
      <Link to={backTo} className="mb-4 inline-flex items-center gap-1.5 text-sm text-ink-dim hover:text-ink">
        <ArrowLeft className="h-4 w-4" /> Back to {backLabel}
      </Link>

      <div className="mb-6 flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="font-display text-2xl font-bold text-ink">{fullName(d)}</h1>
          <div className="mt-1 flex flex-wrap items-center gap-2 text-sm text-ink-muted">
            <span>{d.email}</span>
            <span className="text-ink-dim">·</span>
            <span>{d.job_title}</span>
            {d.job_code && <Pill tone="slate">{d.job_code}</Pill>}
            {d.status && <Pill tone="brand">{d.status}</Pill>}
            {d.display_status && <StatusBadge status={d.display_status} />}
          </div>
        </div>
        {mayDraft && (
          <div className="flex flex-col items-end gap-1">
            <div className="flex items-center gap-2">
              <select value={emailType} onChange={(e) => setEmailType(e.target.value)} disabled={generating} className="input h-9 w-auto">
                {EMAIL_TYPES.map((t) => (
                  <option key={t.value} value={t.value}>{t.label}</option>
                ))}
              </select>
              <button type="button" onClick={generateDraft} disabled={generating} className="btn btn-primary">
                {generating ? <Loader2 className="h-4 w-4 animate-spin" /> : <PenLine className="h-4 w-4" />}
                {generating ? 'Generating…' : 'Draft communication'}
              </button>
            </div>
            {genErr && <span className="text-xs text-danger">{genErr}</span>}
          </div>
        )}
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        <div className="lg:col-span-2">
          <Card title="Interview scorecard">
            {scorecardQuery.isLoading ? <Spinner /> : <ScorecardView values={scorecardQuery.data?.values ?? null} gwc={scorecardQuery.data?.gwc ?? null} />}
          </Card>
        </div>
        <div className="space-y-6">
          <Card title="Communication status">
            <div className="space-y-3 text-sm">
              <div className="flex flex-wrap items-center gap-2">
                <StatusBadge status={d.display_status} />
                {d.days_waiting != null && (
                  <span className="inline-flex items-center gap-1 text-xs text-ink-dim">
                    <Clock className="h-3.5 w-3.5" /> {d.days_waiting} days since applied
                  </span>
                )}
              </div>
              <p className="text-ink-muted">{statusReason(d)}</p>
              {d.comm_required && d.required_email_type && (
                <div className="text-ink-muted">Suggested: <span className="font-medium text-ink">{emailTypeLabel(d.required_email_type)}</span></div>
              )}
              <button type="button" onClick={() => setMatchOpen(true)} className="btn btn-ghost h-8 text-sm">
                <Mail className="h-4 w-4" /> Gmail match · mark sent · ignore
              </button>
            </div>
          </Card>

          <Card title="Communication timeline">
            {timelineQuery.isLoading ? (
              <Spinner label="Loading timeline…" />
            ) : (
              <Timeline items={timelineQuery.data ?? []} />
            )}
          </Card>
        </div>
      </div>

      {matchOpen && (
        <GmailMatchModal
          applicationId={appId}
          candidateName={fullName(d)}
          role={meQ.data?.app_role}
          onClose={() => setMatchOpen(false)}
        />
      )}
    </div>
  )
}

function statusReason(d: { display_status?: string | null; days_waiting?: number | null }): string {
  switch (d.display_status) {
    case 'sent':
      return 'Communication is on record (found in Gmail and/or Markaz, or marked sent).'
    case 'needs_review':
      return 'Coco found a possible match it could not confirm — please verify the Gmail match.'
    case 'in_progress':
      return 'A draft is in progress for this candidate.'
    case 'high_priority':
      return `High priority — no counted communication found and waiting ${d.days_waiting ?? '7+'} days.`
    case 'needs_comms':
      return 'No counted communication found yet — this candidate still needs an email.'
    case 'awaiting_scorecard':
      return 'Decision still pending — no communication required yet.'
    default:
      return ''
  }
}

const SOURCE_STYLE: Record<string, { label: string; cls: string }> = {
  gmail: { label: 'Gmail', cls: 'bg-blurple/15 text-[#4752c4]' },
  markaz: { label: 'Markaz', cls: 'bg-elevated text-ink-muted' },
  coco: { label: 'Coco', cls: 'bg-green/15 text-green' },
}

function Timeline({ items }: { items: TimelineItem[] }) {
  if (!items.length) {
    return <p className="text-sm text-ink-dim">Coco found no emails for this candidate yet — in Gmail or Markaz.</p>
  }
  const g = items.filter((i) => i.source === 'gmail').length
  const m = items.filter((i) => i.source === 'markaz').length
  const c = items.filter((i) => i.source === 'coco').length
  const parts = [g && `${g} via Gmail`, m && `${m} via Markaz`, c && `${c} via Coco`].filter(Boolean)

  return (
    <div className="space-y-3">
      <div className="flex items-start gap-2 rounded-lg bg-surface-2 px-3 py-2 text-xs text-ink-muted">
        <Sparkles className="mt-0.5 h-3.5 w-3.5 flex-shrink-0 text-blurple" />
        <span>Coco found <span className="font-semibold text-ink">{items.length}</span> {items.length === 1 ? 'email' : 'emails'} for this candidate{parts.length ? ` — ${parts.join(', ')}` : ''}.</span>
      </div>
      <ul className="space-y-3">
        {items.map((h, i) => {
          const s = SOURCE_STYLE[h.source] ?? SOURCE_STYLE.markaz
          return (
            <li key={i} className="rounded-lg border border-hairline bg-surface p-3">
              <div className="flex items-center gap-2 text-xs text-ink-dim">
                <span className={`rounded px-1.5 py-0.5 text-[10px] font-semibold uppercase tracking-wide ${s.cls}`}>{s.label}</span>
                {formatDate(h.ts)}
              </div>
              <div className="mt-1 text-sm font-medium text-ink">{h.subject || '(no subject)'}</div>
              {h.actor && <div className="text-xs text-ink-dim">{h.source === 'gmail' ? `from ${h.actor}` : `by ${h.actor}`}</div>}
              {h.snippet && <div className="mt-1 text-xs italic text-ink-muted line-clamp-2">“{h.snippet}”</div>}
              {h.link && (
                <a href={h.link} target="_blank" rel="noreferrer" className="mt-1 inline-block text-xs font-medium text-[#4752c4] hover:underline">
                  Open in Gmail →
                </a>
              )}
            </li>
          )
        })}
      </ul>
    </div>
  )
}

function Card({ title, children }: { title: string; children: ReactNode }) {
  return (
    <div className="card">
      <div className="border-b border-hairline px-5 py-3 text-sm font-semibold text-ink">{title}</div>
      <div className="p-5">{children}</div>
    </div>
  )
}
