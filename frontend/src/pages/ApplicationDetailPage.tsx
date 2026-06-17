import { useQuery } from '@tanstack/react-query'
import type { ReactNode } from 'react'
import { useState } from 'react'
import { ArrowLeft, Loader2, Mail, PenLine } from 'lucide-react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { Pill } from '../components/StatusBadge'
import { Spinner } from '../components/Spinner'
import { ApiError, api } from '../lib/api'
import { formatDate, fullName } from '../lib/format'
import { EMAIL_TYPES } from '../lib/types'
import type { GwcScorecard, ValuesScorecard } from '../lib/types'

const RATING_TONE: Record<string, string> = {
  '+': 'bg-sent-bg text-sent',
  '+/-': 'bg-review-bg text-review',
  '-': 'bg-block-bg text-block',
}

export function ApplicationDetailPage() {
  const { id } = useParams()
  const appId = Number(id)

  const detailQuery = useQuery({
    queryKey: ['candidate', appId],
    queryFn: () => api.candidate(appId),
    enabled: !Number.isNaN(appId),
  })
  const scorecardQuery = useQuery({
    queryKey: ['scorecard', appId],
    queryFn: () => api.scorecard(appId),
    enabled: !Number.isNaN(appId),
  })

  const navigate = useNavigate()
  const [emailType, setEmailType] = useState('values_feedback')
  const [generating, setGenerating] = useState(false)
  const [genErr, setGenErr] = useState<string | null>(null)

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
  if (detailQuery.isError || !detailQuery.data)
    return <div className="p-8 text-sm text-block">Could not load this application.</div>

  const d = detailQuery.data

  return (
    <div className="mx-auto max-w-6xl px-8 py-7">
      <Link to="/" className="mb-4 inline-flex items-center gap-1.5 text-sm text-slate-500 hover:text-slate-800">
        <ArrowLeft className="h-4 w-4" /> Back to queue
      </Link>

      <div className="mb-6 flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="text-xl font-semibold text-slate-900">{fullName(d)}</h1>
          <div className="mt-1 flex flex-wrap items-center gap-2 text-sm text-slate-500">
            <span>{d.email}</span>
            <span className="text-slate-300">·</span>
            <span>{d.job_title}</span>
            {d.job_code && <Pill tone="slate">{d.job_code}</Pill>}
            {d.status && <Pill tone="brand">{d.status}</Pill>}
          </div>
        </div>
        <div className="flex flex-col items-end gap-1">
          <div className="flex items-center gap-2">
            <select
              value={emailType}
              onChange={(e) => setEmailType(e.target.value)}
              disabled={generating}
              className="h-9 rounded-lg border border-slate-200 bg-white px-2.5 text-sm text-slate-700 outline-none focus:border-brand-500"
            >
              {EMAIL_TYPES.map((t) => (
                <option key={t.value} value={t.value}>{t.label}</option>
              ))}
            </select>
            <button
              type="button"
              onClick={generateDraft}
              disabled={generating}
              className="inline-flex items-center gap-2 rounded-lg bg-brand-500 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-brand-600 disabled:opacity-60"
            >
              {generating ? <Loader2 className="h-4 w-4 animate-spin" /> : <PenLine className="h-4 w-4" />}
              {generating ? 'Generating…' : 'Draft communication'}
            </button>
          </div>
          {genErr && <span className="text-xs text-block">{genErr}</span>}
        </div>
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        {/* Scorecards */}
        <div className="space-y-6 lg:col-span-2">
          {scorecardQuery.isLoading && <Spinner label="Loading scorecard…" />}
          {scorecardQuery.data?.values && <ValuesPanel sc={scorecardQuery.data.values} />}
          {scorecardQuery.data?.gwc && <GwcPanel sc={scorecardQuery.data.gwc} />}
          {scorecardQuery.data && !scorecardQuery.data.values && !scorecardQuery.data.gwc && (
            <div className="rounded-xl border border-slate-200 bg-white p-6 text-sm text-slate-500">
              No interview scorecard on file yet.
            </div>
          )}
        </div>

        {/* Comm history */}
        <div>
          <Card title="Email history (on record)">
            {d.comm_history.length === 0 ? (
              <p className="text-sm text-slate-500">No prior emails recorded for this application.</p>
            ) : (
              <ul className="space-y-3">
                {d.comm_history.map((h, i) => (
                  <li key={i} className="rounded-lg border border-slate-100 bg-slate-50 p-3">
                    <div className="flex items-center gap-2 text-xs text-slate-500">
                      <Mail className="h-3.5 w-3.5" />
                      {formatDate(h.sent_at)} · {h.source}
                    </div>
                    <div className="mt-1 text-sm font-medium text-slate-800">
                      {h.subject || h.template_name || '(no subject)'}
                    </div>
                    {h.sent_by && <div className="text-xs text-slate-400">by {h.sent_by}</div>}
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
    <div className="rounded-xl border border-slate-200 bg-white shadow-sm">
      <div className="border-b border-slate-100 px-5 py-3 text-sm font-semibold text-slate-900">
        {title}
      </div>
      <div className="p-5">{children}</div>
    </div>
  )
}

function ValuesPanel({ sc }: { sc: ValuesScorecard }) {
  return (
    <Card title="Values Interview Scorecard">
      <div className="mb-4 flex flex-wrap gap-x-6 gap-y-2 text-sm">
        <Meta label="Host" value={sc.host} />
        <Meta label="Date" value={sc.date} />
        <Meta label="Proceed" value={sc.proceed_to_right_seat} />
      </div>
      <ul className="space-y-3">
        {sc.values.map((v, i) => (
          <li key={i} className="rounded-lg border border-slate-100 p-3">
            <div className="flex items-center justify-between gap-2">
              <span className="text-sm font-medium text-slate-800">{v.name}</span>
              {v.rating && (
                <span className={`rounded px-2 py-0.5 text-xs font-semibold ${RATING_TONE[v.rating] || 'bg-slate-100 text-slate-600'}`}>
                  {v.rating}
                </span>
              )}
            </div>
            {(v.deep_dive || v.curve_ball || v.micro_case) && (
              <div className="mt-2 space-y-1 text-sm text-slate-600">
                {v.deep_dive && <p><span className="text-slate-400">Deep dive: </span>{v.deep_dive}</p>}
                {v.curve_ball && <p><span className="text-slate-400">Curveball: </span>{v.curve_ball}</p>}
                {v.micro_case && <p><span className="text-slate-400">Micro-case: </span>{v.micro_case}</p>}
              </div>
            )}
          </li>
        ))}
      </ul>
      {sc.final_comments && (
        <div className="mt-4 rounded-lg bg-brand-50 p-3 text-sm text-slate-700">
          <span className="font-medium text-brand-700">Final comments: </span>
          {sc.final_comments}
        </div>
      )}
    </Card>
  )
}

function GwcPanel({ sc }: { sc: GwcScorecard }) {
  return (
    <Card title="GWC Interview Scorecard">
      <div className="mb-4 flex flex-wrap gap-x-6 gap-y-2 text-sm">
        <Meta label="Hiring manager" value={sc.hiring_manager} />
        <Meta label="Final mark" value={sc.final_mark} />
      </div>
      <div className="grid grid-cols-3 gap-3">
        {sc.competencies.map((c, i) => (
          <div key={i} className="rounded-lg border border-slate-100 p-3 text-center">
            <div className="text-xs text-slate-500">{c.name}</div>
            <div className="mt-1 text-lg font-semibold text-slate-900">{c.score ?? '—'}</div>
            {c.weight != null && <div className="text-[11px] text-slate-400">weight {c.weight}</div>}
          </div>
        ))}
      </div>
      {sc.additional_comments && (
        <div className="mt-4 rounded-lg bg-brand-50 p-3 text-sm text-slate-700">
          <span className="font-medium text-brand-700">Comments: </span>
          {sc.additional_comments}
        </div>
      )}
    </Card>
  )
}

function Meta({ label, value }: { label: string; value?: string }) {
  return (
    <div>
      <span className="text-xs uppercase tracking-wide text-slate-400">{label}</span>
      <div className="font-medium text-slate-800">{value || '—'}</div>
    </div>
  )
}
