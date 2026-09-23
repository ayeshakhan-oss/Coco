import { useEffect, useRef, useState } from 'react'
import { AlertTriangle, ExternalLink, Info } from 'lucide-react'
import { Spinner } from '../components/Spinner'
import { api } from '../lib/api'
import type { DecisionBriefPerson, HiringBrief, JobItem } from '../lib/types'

const GENERIC_LOAD_ERROR = 'Could not load the hiring brief. Try reloading the page.'

function CandidateName({ p }: { p: DecisionBriefPerson }) {
  if (!p.has_cv) {
    return (
      <span className="font-medium text-ink">
        {p.name} <span className="text-xs font-normal text-warning">(no CV on file)</span>
      </span>
    )
  }
  return (
    <a
      href={p.cv_url}
      target="_blank"
      rel="noreferrer"
      className="font-medium text-blurple hover:underline"
    >
      {p.name}
      <ExternalLink className="ml-1 inline h-3 w-3" />
    </a>
  )
}

export function HiringBriefPage() {
  const [jobs, setJobs] = useState<JobItem[]>([])
  const [jobId, setJobId] = useState<number | null>(null)
  const [data, setData] = useState<HiringBrief | null>(null)
  const [loaded, setLoaded] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const genRef = useRef(0)

  useEffect(() => {
    api
      .cvScreenJobs()
      .then((j) => {
        setJobs(j)
        if (j.length && jobId === null) setJobId(j[0].job_pk)
      })
      .catch(() => setError(GENERIC_LOAD_ERROR))
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  useEffect(() => {
    if (jobId === null) return
    const gen = ++genRef.current
    setLoaded(false)
    api
      .hiringBrief(jobId)
      .then((d) => {
        if (genRef.current !== gen) return
        setData(d)
        setError(null)
        setLoaded(true)
      })
      .catch(() => {
        if (genRef.current !== gen) return
        setError(GENERIC_LOAD_ERROR)
        setLoaded(true)
      })
  }, [jobId])

  const widest = data
    ? Math.max(1, ...data.stages.map((s) => s.count ?? 0))
    : 1

  return (
    <div className="mx-auto max-w-7xl px-8 py-7">
      <header className="mb-5">
        <h1 className="font-display text-2xl font-bold text-ink">Hiring Decision Brief</h1>
        <p className="mt-1 text-sm text-ink-muted">
          How far the position has actually got, stage by stage, and who is left. Read only.
        </p>
      </header>

      {jobs.length > 0 && (
        <select
          value={jobId ?? ''}
          onChange={(e) => setJobId(Number(e.target.value))}
          className="input w-auto"
        >
          {jobs.map((j) => (
            <option key={j.job_pk} value={j.job_pk}>
              {j.title ?? `Job ${j.job_pk}`}
              {j.job_status && j.job_status !== 'Active' ? ` (${j.job_status})` : ''}
            </option>
          ))}
        </select>
      )}

      {error && <p className="mt-5 text-sm text-danger">{error}</p>}

      {!loaded ? (
        jobId !== null && (
          <div className="mt-5">
            <Spinner label="Building the brief…" />
          </div>
        )
      ) : data ? (
        <>
          <p className="mt-5 text-sm text-ink-muted">
            <span className="font-semibold text-ink">{data.total_applications}</span>{' '}
            applications on {data.job_title}.
          </p>

          <div className="mt-3 overflow-hidden rounded-2xl border border-hairline bg-surface">
            {data.stages.map((s) => (
              <div
                key={s.key}
                className="flex items-center gap-4 border-b border-hairline/60 px-4 py-2.5 last:border-0"
              >
                <div className="w-64 shrink-0 text-sm text-ink">{s.title}</div>
                <div className="w-20 shrink-0 text-right">
                  {s.count === null ? (
                    // Never 0: we did not recognise an email, which is not the
                    // same as nobody being sent one.
                    <span className="text-xs italic text-ink-dim">not visible</span>
                  ) : (
                    <span className="tabular-nums text-lg font-bold text-ink">
                      {s.is_floor ? '≥' : ''}
                      {s.count}
                    </span>
                  )}
                </div>
                <div className="h-2 min-w-0 flex-1 overflow-hidden rounded-full bg-elevated">
                  <div
                    className={`h-full rounded-full ${s.is_floor ? 'bg-blurple/40' : 'bg-blurple'}`}
                    style={{ width: `${((s.count ?? 0) / widest) * 100}%` }}
                  />
                </div>
                <div className="w-40 shrink-0 text-right text-xs text-ink-dim">{s.source}</div>
              </div>
            ))}
          </div>

          {data.inconsistencies.length > 0 && (
            <div className="mt-3 rounded-xl border border-danger/30 bg-danger/5 px-4 py-3 text-sm">
              <div className="flex items-center gap-2 font-semibold text-ink">
                <AlertTriangle className="h-4 w-4 text-danger" />
                The funnel widens, so one of these numbers is wrong
              </div>
              <ul className="mt-1 list-disc pl-5 text-xs text-ink-muted">
                {data.inconsistencies.map((p, i) => (
                  <li key={i}>{p}</li>
                ))}
              </ul>
            </div>
          )}

          <div className="mt-3 flex gap-2.5 rounded-xl border border-hairline bg-surface px-4 py-3 text-sm text-ink-muted">
            <Info className="mt-0.5 h-4 w-4 shrink-0 text-ink-dim" />
            <div>
              <p>{data.caveat}</p>
              {data.evidence_synced_at && (
                <p className="mt-1 text-xs">
                  Mailbox evidence last synced{' '}
                  {new Date(data.evidence_synced_at).toLocaleDateString()}. Anything sent
                  since then is not counted.
                </p>
              )}
            </div>
          </div>

          <h2 className="mt-6 font-display text-sm font-bold text-ink">
            Leading{' '}
            <span className="font-normal text-ink-dim">({data.brief.leading.length})</span>
          </h2>
          {data.brief.leading_note && (
            <div className="mt-1 flex gap-2 rounded-xl border border-warning/30 bg-warning/5 px-3 py-2 text-xs text-ink-muted">
              <AlertTriangle className="mt-0.5 h-3.5 w-3.5 shrink-0 text-warning" />
              <p>{data.brief.leading_note}</p>
            </div>
          )}
          {data.brief.leading.length === 0 ? (
            <p className="mt-1 text-sm text-ink-dim">
              Nobody has both passed values and submitted a case study yet.
            </p>
          ) : (
            <div className="mt-2 overflow-hidden rounded-2xl border border-hairline bg-surface">
              <table className="w-full text-sm">
                <tbody>
                  {data.brief.leading.map((p) => (
                    <tr
                      key={p.application_id}
                      className="border-b border-hairline/60 last:border-0"
                    >
                      <td className="px-4 py-2.5">
                        <CandidateName p={p} />
                      </td>
                      <td className="px-4 py-2.5 text-xs text-ink-muted">
                        {p.case_study_total != null
                          ? `case study ${p.case_study_total}`
                          : p.submitted_case_study
                            ? 'case study submitted, not scored'
                            : '—'}
                      </td>
                      <td className="px-4 py-2.5 text-right text-xs text-ink-dim">
                        {p.debrief_verdict}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          <div className="mt-6 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
            {data.brief.groups.map((g) => (
              <div key={g.key} className="rounded-2xl border border-hairline bg-surface p-4">
                <div className="text-sm font-medium text-ink-muted">{g.title}</div>
                <div className="mt-1 text-2xl font-bold tabular-nums text-ink">
                  {g.people.length}
                </div>
              </div>
            ))}
          </div>

          <p className="mt-4 text-xs text-ink-dim">
            Candidate detail, with every name linked to their CV, is on the Decision Briefs
            page.
          </p>
        </>
      ) : null}
    </div>
  )
}
