import { useQuery } from '@tanstack/react-query'
import type { ReactNode } from 'react'
import { useState } from 'react'
import { ArrowLeft, Loader2, Mail, PenLine } from 'lucide-react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { Pill } from '../components/StatusBadge'
import { ScorecardView } from '../components/ScorecardView'
import { Spinner } from '../components/Spinner'
import { ApiError, api } from '../lib/api'
import { formatDate, fullName } from '../lib/format'
import { canEdit } from '../lib/roles'
import { EMAIL_TYPES } from '../lib/types'

export function ApplicationDetailPage() {
  const { id } = useParams()
  const appId = Number(id)
  const navigate = useNavigate()

  const meQ = useQuery({ queryKey: ['me'], queryFn: api.me, retry: false })
  const detailQuery = useQuery({ queryKey: ['candidate', appId], queryFn: () => api.candidate(appId), enabled: !Number.isNaN(appId) })
  const scorecardQuery = useQuery({ queryKey: ['scorecard', appId], queryFn: () => api.scorecard(appId), enabled: !Number.isNaN(appId) })

  const [emailType, setEmailType] = useState('values_feedback')
  const [generating, setGenerating] = useState(false)
  const [genErr, setGenErr] = useState<string | null>(null)
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

  return (
    <div className="mx-auto max-w-6xl px-8 py-7">
      <Link to="/" className="mb-4 inline-flex items-center gap-1.5 text-sm text-ink-dim hover:text-ink">
        <ArrowLeft className="h-4 w-4" /> Back to queue
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
        <div>
          <Card title="Email history (on record)">
            {d.comm_history.length === 0 ? (
              <p className="text-sm text-ink-dim">No prior emails recorded for this application.</p>
            ) : (
              <ul className="space-y-3">
                {d.comm_history.map((h, i) => (
                  <li key={i} className="rounded-lg border border-hairline bg-surface-2 p-3">
                    <div className="flex items-center gap-2 text-xs text-ink-dim">
                      <Mail className="h-3.5 w-3.5" />
                      {formatDate(h.sent_at)} · {h.source}
                    </div>
                    <div className="mt-1 text-sm font-medium text-ink">{h.subject || h.template_name || '(no subject)'}</div>
                    {h.sent_by && <div className="text-xs text-ink-dim">by {h.sent_by}</div>}
                  </li>
                ))}
              </ul>
            )}
          </Card>
        </div>
      </div>
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
