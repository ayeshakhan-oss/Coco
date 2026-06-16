import { useQuery } from '@tanstack/react-query'
import {
  CheckCircle2,
  ClipboardList,
  Clock,
  FileQuestion,
  Search,
} from 'lucide-react'
import { useEffect, useMemo, useState } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { StatCard } from '../components/StatCard'
import { Pill, StatusBadge } from '../components/StatusBadge'
import { Spinner } from '../components/Spinner'
import { api } from '../lib/api'
import { formatDate, fullName, scorecardLabel } from '../lib/format'
import type { Bucket, QueueRow } from '../lib/types'

type Filter = Bucket | 'scored'

export function QueuePage() {
  const navigate = useNavigate()
  const [params, setParams] = useSearchParams()

  const bucket = (params.get('status') as Filter) || 'scored'
  const jobParam = params.get('job')
  const job = jobParam ? Number(jobParam) : null

  const [search, setSearch] = useState(params.get('q') || '')
  const [debouncedQ, setDebouncedQ] = useState(search)
  useEffect(() => {
    const t = setTimeout(() => setDebouncedQ(search), 300)
    return () => clearTimeout(t)
  }, [search])

  const statsQuery = useQuery({ queryKey: ['stats'], queryFn: api.stats })
  const jobsQuery = useQuery({ queryKey: ['jobs'], queryFn: api.jobs })
  const candidatesQuery = useQuery({
    queryKey: ['candidates', bucket, job, debouncedQ],
    queryFn: () => api.candidates({ status: bucket, job, q: debouncedQ || undefined }),
  })

  function setBucket(next: Filter) {
    const p = new URLSearchParams(params)
    if (next === 'scored') p.delete('status')
    else p.set('status', next)
    setParams(p, { replace: true })
  }

  function setJob(next: number | null) {
    const p = new URLSearchParams(params)
    if (next == null) p.delete('job')
    else p.set('job', String(next))
    setParams(p, { replace: true })
  }

  const stats = statsQuery.data
  const cards = useMemo(
    () =>
      [
        { key: 'needs_comms', label: 'Needs comms', value: stats?.needs_comms ?? 0, icon: ClipboardList, tone: 'amber' },
        { key: 'in_progress', label: 'In progress', value: stats?.in_progress ?? 0, icon: Clock, tone: 'brand' },
        { key: 'sent', label: 'Sent', value: stats?.sent ?? 0, icon: CheckCircle2, tone: 'green' },
        { key: 'awaiting_scorecard', label: 'Awaiting scorecard', value: stats?.awaiting_scorecard ?? 0, icon: FileQuestion, tone: 'slate' },
      ] as const,
    [stats],
  )

  return (
    <div className="mx-auto max-w-7xl px-8 py-7">
      <header className="mb-6">
        <h1 className="text-xl font-semibold text-slate-900">Candidate Queue</h1>
        <p className="mt-1 text-sm text-slate-500">
          Candidates with a completed interview scorecard who may need a communication sent.
        </p>
      </header>

      <div className="mb-6 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {cards.map((c) => (
          <StatCard
            key={c.key}
            label={c.label}
            value={c.value}
            icon={c.icon}
            tone={c.tone}
            active={bucket === c.key}
            onClick={() => setBucket(bucket === c.key ? 'scored' : (c.key as Filter))}
          />
        ))}
      </div>

      {/* Filter bar */}
      <div className="mb-4 flex flex-wrap items-center gap-3">
        <div className="relative">
          <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
          <input
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search name or email…"
            className="h-9 w-72 rounded-lg border border-slate-200 bg-white pl-9 pr-3 text-sm text-slate-900 outline-none placeholder:text-slate-400 focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20"
          />
        </div>
        <select
          value={job ?? ''}
          onChange={(e) => setJob(e.target.value ? Number(e.target.value) : null)}
          className="h-9 rounded-lg border border-slate-200 bg-white px-3 text-sm text-slate-700 outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20"
        >
          <option value="">All roles</option>
          {jobsQuery.data?.map((j) => (
            <option key={j.job_pk} value={j.job_pk}>
              {j.title}
            </option>
          ))}
        </select>
        {bucket !== 'scored' && (
          <button
            type="button"
            onClick={() => setBucket('scored')}
            className="h-9 rounded-lg px-3 text-sm font-medium text-brand-600 hover:bg-brand-50"
          >
            Clear filter
          </button>
        )}
        <span className="ml-auto text-sm text-slate-500">
          {candidatesQuery.data ? `${candidatesQuery.data.length} shown` : ''}
        </span>
      </div>

      {/* Table */}
      <div className="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm">
        {candidatesQuery.isLoading ? (
          <Spinner label="Loading candidates…" />
        ) : candidatesQuery.isError ? (
          <div className="p-8 text-center text-sm text-block">Failed to load candidates.</div>
        ) : !candidatesQuery.data?.length ? (
          <div className="p-12 text-center text-sm text-slate-500">
            No candidates match this view.
          </div>
        ) : (
          <table className="w-full text-left text-sm">
            <thead className="border-b border-slate-200 bg-slate-50 text-xs uppercase tracking-wide text-slate-500">
              <tr>
                <th className="px-5 py-3 font-medium">Candidate</th>
                <th className="px-5 py-3 font-medium">Role</th>
                <th className="px-5 py-3 font-medium">Scorecard</th>
                <th className="px-5 py-3 font-medium">Status</th>
                <th className="px-5 py-3 font-medium">Interview date</th>
                <th className="px-5 py-3 font-medium">Prior emails</th>
                <th className="px-5 py-3" />
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
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
      ? 'border-l-sent'
      : row.bucket === 'needs_comms'
        ? 'border-l-review'
        : row.bucket === 'in_progress'
          ? 'border-l-brand-500'
          : 'border-l-slate-300'

  return (
    <tr
      onClick={onOpen}
      className={`cursor-pointer border-l-4 ${borderTone} transition-colors hover:bg-slate-50`}
    >
      <td className="px-5 py-3">
        <div className="font-medium text-slate-900">{fullName(row)}</div>
        <div className="text-xs text-slate-500">{row.email}</div>
      </td>
      <td className="px-5 py-3">
        <div className="text-slate-700">{row.job_title ?? '—'}</div>
        <div className="text-xs text-slate-400">{row.job_code}</div>
      </td>
      <td className="px-5 py-3">
        <div className="flex items-center gap-1.5">
          <span className="text-slate-700">{scorecardLabel(row)}</span>
          {row.values_interview_result && (
            <Pill tone={row.values_interview_result === 'pass' ? 'green' : 'red'}>
              {row.values_interview_result}
            </Pill>
          )}
        </div>
      </td>
      <td className="px-5 py-3">
        <StatusBadge bucket={row.bucket} />
      </td>
      <td className="px-5 py-3 text-slate-600">{formatDate(row.scorecard_date)}</td>
      <td className="px-5 py-3">
        {row.prior_platform_comms > 0 ? (
          <Pill tone="slate">{row.prior_platform_comms} on record</Pill>
        ) : (
          <span className="text-slate-400">—</span>
        )}
      </td>
      <td className="px-5 py-3 text-right">
        <span className="text-sm font-medium text-brand-600">
          {row.bucket === 'sent' ? 'View' : row.bucket === 'in_progress' ? 'Continue' : 'Draft'} →
        </span>
      </td>
    </tr>
  )
}
