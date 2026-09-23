import { useEffect, useRef, useState } from 'react'
import { AlertTriangle, Info } from 'lucide-react'
import { Spinner } from '../components/Spinner'
import { api } from '../lib/api'
import type { AttendancePerson, AttendanceReport } from '../lib/types'

// 🔴 Markaz records ABSENCE, not attendance. This page never says "onsite" or
// "present": a leave system cannot see who walked into the office, and a
// number under that label would be read as something we do not know.

const GENERIC_LOAD_ERROR = 'Could not load attendance. Try reloading the page.'

function today() {
  return new Date().toISOString().slice(0, 10)
}

function PeopleTable({
  title,
  rows,
  tint,
  empty,
}: {
  title: string
  rows: AttendancePerson[]
  tint: string
  empty: string
}) {
  return (
    <div className="mt-5">
      <h2 className="mb-2 font-display text-sm font-bold text-ink">
        {title} <span className="font-normal text-ink-dim">({rows.length})</span>
      </h2>
      {rows.length === 0 ? (
        <p className="text-sm text-ink-dim">{empty}</p>
      ) : (
        <div className="overflow-hidden rounded-2xl border border-hairline bg-surface">
          <table className="w-full text-sm">
            <thead className="border-b border-hairline bg-elevated text-left text-xs uppercase tracking-wide text-ink-dim">
              <tr>
                <th className="px-4 py-2.5 font-semibold">Name</th>
                <th className="px-4 py-2.5 font-semibold">Team</th>
                <th className="px-4 py-2.5 font-semibold">Type</th>
                <th className="px-4 py-2.5 font-semibold">Dates</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((p, i) => (
                <tr
                  key={p.user_id}
                  className="border-b border-hairline/60 last:border-0"
                  // Alternating tint, from the locked template.
                  style={i % 2 === 1 ? { backgroundColor: tint } : undefined}
                >
                  <td className="px-4 py-2.5">
                    <div className="font-medium text-ink">{p.name ?? '(no name)'}</div>
                    {p.job_title && (
                      <div className="text-xs text-ink-dim">{p.job_title}</div>
                    )}
                  </td>
                  <td className="px-4 py-2.5 text-xs text-ink-muted">
                    {p.department ?? '—'}
                    {p.payroll_entity ? ` · ${p.payroll_entity}` : ''}
                  </td>
                  <td className="px-4 py-2.5 text-xs text-ink-muted">
                    {(p.leave_type ?? '').replace(/_/g, ' ')}
                    {p.sub_category ? ` · ${p.sub_category}` : ''}
                    {p.is_half_day ? ' · half day' : ''}
                  </td>
                  <td className="px-4 py-2.5 text-xs tabular-nums text-ink-muted">
                    {p.start_date === p.end_date
                      ? p.start_date
                      : `${p.start_date} to ${p.end_date}`}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}

export function AttendancePage() {
  const [date, setDate] = useState(today())
  const [entities, setEntities] = useState<string[]>([])
  const [available, setAvailable] = useState<{ payroll_entity: string; n: number }[]>([])
  const [report, setReport] = useState<AttendanceReport | null>(null)
  const [loaded, setLoaded] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const genRef = useRef(0)

  useEffect(() => {
    api
      .attendanceEntities()
      .then((e) => {
        setAvailable(e.entities)
        setEntities(e.default)
      })
      .catch(() => setError(GENERIC_LOAD_ERROR))
  }, [])

  useEffect(() => {
    if (!entities.length) return
    const gen = ++genRef.current
    setLoaded(false)
    api
      .attendance(date, entities)
      .then((r) => {
        if (genRef.current !== gen) return
        setReport(r)
        setError(null)
        setLoaded(true)
      })
      .catch(() => {
        if (genRef.current !== gen) return
        setError(GENERIC_LOAD_ERROR)
        setLoaded(true)
      })
  }, [date, entities])

  const toggle = (name: string) =>
    setEntities((prev) =>
      prev.includes(name) ? prev.filter((e) => e !== name) : [...prev, name],
    )

  return (
    <div className="mx-auto max-w-7xl px-8 py-7">
      <header className="mb-5">
        <h1 className="font-display text-2xl font-bold text-ink">Attendance</h1>
        <p className="mt-1 text-sm text-ink-muted">
          Who has recorded an absence today, from Markaz leave records. Read only.
        </p>
      </header>

      <div className="flex flex-wrap items-end gap-4">
        <label className="text-xs font-semibold text-ink-muted">
          Date
          <input
            type="date"
            className="input mt-1 block w-44"
            value={date}
            onChange={(e) => setDate(e.target.value)}
          />
        </label>
        <div className="text-xs font-semibold text-ink-muted">
          Office
          <div className="mt-1 flex flex-wrap gap-3">
            {available.map((e) => (
              <label key={e.payroll_entity} className="flex items-center gap-1.5 font-normal">
                <input
                  type="checkbox"
                  checked={entities.includes(e.payroll_entity)}
                  onChange={() => toggle(e.payroll_entity)}
                />
                {e.payroll_entity}{' '}
                <span className="text-ink-dim">({e.n})</span>
              </label>
            ))}
          </div>
        </div>
      </div>

      {error && <p className="mt-5 text-sm text-danger">{error}</p>}

      {!loaded ? (
        entities.length > 0 && (
          <div className="mt-5">
            <Spinner label="Loading…" />
          </div>
        )
      ) : report ? (
        <>
          <p className="mt-5 text-sm font-medium text-ink">
            {report.weekday} {report.date} · {report.entities.join(', ')}
          </p>

          <div className="mt-3 grid grid-cols-2 gap-3 lg:grid-cols-5">
            {report.stat_boxes.map((b) => (
              <div
                key={b.label}
                className="rounded-2xl border border-hairline p-4"
                style={{ backgroundColor: b.colour }}
              >
                <div className="text-sm font-medium text-ink/80">{b.label}</div>
                <div className="mt-1 text-2xl font-bold tabular-nums text-ink">{b.value}</div>
              </div>
            ))}
          </div>

          {/* Not a footnote. The headline number is the one most likely to be
              misread, so the caveat sits directly under it. */}
          <div className="mt-3 flex gap-2.5 rounded-xl border border-hairline bg-surface px-4 py-3 text-sm text-ink-muted">
            <Info className="mt-0.5 h-4 w-4 shrink-0 text-ink-dim" />
            <p>{report.presence_caveat}</p>
          </div>

          {report.needs_correction.length > 0 && (
            <div className="mt-3 rounded-xl border border-danger/30 bg-danger/5 px-4 py-3">
              <div className="flex items-center gap-2 text-sm font-semibold text-ink">
                <AlertTriangle className="h-4 w-4 text-danger" />
                {report.needs_correction.length} leave record
                {report.needs_correction.length === 1 ? '' : 's'} cannot be true and need
                fixing in Markaz
              </div>
              {/* These are excluded from the counts above. Left alone they would
                  mark the same people absent every day, for ever. */}
              <p className="mt-1 text-xs text-ink-muted">
                They are left out of the numbers above. Until someone corrects them in
                Markaz they would mark these people absent every day indefinitely.
              </p>
              <ul className="mt-2 space-y-1 text-xs">
                {report.needs_correction.map((c, i) => (
                  <li key={i} className="text-ink-muted">
                    <span className="font-medium text-ink">{c.name ?? '(no name)'}</span>
                    {' · '}
                    {(c.leave_type ?? '').replace(/_/g, ' ')}
                    {' · '}
                    <span className="font-mono">
                      {c.start_date} to {c.end_date}
                    </span>
                    {' — '}
                    {c.problem}
                  </li>
                ))}
              </ul>
            </div>
          )}

          <PeopleTable
            title="On leave"
            rows={report.on_leave}
            tint="#ffe0b2"
            empty="Nobody has recorded leave for this date."
          />
          <PeopleTable
            title="Working from home"
            rows={report.working_from_home}
            tint="#e3f2fd"
            empty="Nobody has recorded working from home for this date."
          />

          <p className="mt-6 text-xs text-ink-dim">Source: {report.source}.</p>
        </>
      ) : null}
    </div>
  )
}
