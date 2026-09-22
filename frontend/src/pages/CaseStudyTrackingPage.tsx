import { Fragment, useEffect, useRef, useState } from 'react'
import { AlertTriangle, ChevronDown, Copy, Loader2 } from 'lucide-react'
import { Spinner } from '../components/Spinner'
import { ApiError, api } from '../lib/api'
import type {
  CaseStudyMirrorPair,
  CaseStudyStatus,
  CaseStudyTrackingRow,
  CaseStudyTrackingSummary,
  JobItem,
} from '../lib/types'

// Tracking only. Scoring a submission against a benchmark is /case-studies.

const GENERIC_LOAD_ERROR = 'Could not load case-study tracking. Try reloading the page.'

// 🔴 The wording matters more than the layout here. Markaz records no
// case-study send, so "no record of a send" must never be shortened to
// "not sent" anywhere a person can read it.
const STATUS_LABEL: Record<CaseStudyStatus, string> = {
  submitted: 'Submitted',
  awaiting: 'Awaiting submission',
  no_record_of_a_send: 'No record of a send',
  submitted_without_send_record: 'Submitted, no send on record',
}

const STATUS_CLASS: Record<CaseStudyStatus, string> = {
  submitted: 'bg-success/10 text-success border-success/30',
  awaiting: 'bg-warning/10 text-warning border-warning/30',
  no_record_of_a_send: 'bg-ink-dim/10 text-ink-dim border-hairline',
  submitted_without_send_record: 'bg-blurple/10 text-blurple border-blurple/30',
}

function StatusBadge({ status }: { status: CaseStudyStatus }) {
  return (
    <span className={`inline-block rounded-full border px-2.5 py-0.5 text-xs font-semibold ${STATUS_CLASS[status]}`}>
      {STATUS_LABEL[status]}
    </span>
  )
}

export function CaseStudyTrackingPage() {
  const [jobs, setJobs] = useState<JobItem[]>([])
  const [jobsLoaded, setJobsLoaded] = useState(false)
  const [jobsError, setJobsError] = useState<string | null>(null)
  const [jobId, setJobId] = useState<number | null>(null)

  const [summary, setSummary] = useState<CaseStudyTrackingSummary | null>(null)
  const [rows, setRows] = useState<CaseStudyTrackingRow[]>([])
  const [mirrors, setMirrors] = useState<CaseStudyMirrorPair[]>([])
  const [loaded, setLoaded] = useState(false)
  const [listError, setListError] = useState<string | null>(null)

  const [openId, setOpenId] = useState<number | null>(null)
  const [probing, setProbing] = useState<number | null>(null)
  const [probeError, setProbeError] = useState<{ id: number; message: string } | null>(null)

  const genRef = useRef(0)
  const probingRef = useRef<number | null>(null)

  useEffect(() => {
    api
      .cvScreenJobs()
      .then((j) => {
        setJobs(j)
        setJobsLoaded(true)
        if (j.length && jobId === null) setJobId(j[0].job_pk)
      })
      .catch(() => {
        setJobsLoaded(true)
        setJobsError(GENERIC_LOAD_ERROR)
      })
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  const reload = (id: number, gen: number) =>
    Promise.all([
      api.caseStudyTrackingSummary(id),
      api.caseStudyTracking(id),
      api.caseStudyMirrors(id),
    ]).then(([s, r, m]) => {
      if (genRef.current !== gen) return
      setSummary(s)
      setRows(r)
      setMirrors(m)
      setListError(null)
      setLoaded(true)
    })

  useEffect(() => {
    if (jobId === null) return
    const gen = ++genRef.current
    setLoaded(false)
    setOpenId(null)
    setProbeError(null)
    reload(jobId, gen).catch(() => {
      if (genRef.current !== gen) return
      setListError(GENERIC_LOAD_ERROR)
      setLoaded(true)
    })
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [jobId])

  const runProbe = (applicationId: number) => {
    if (probingRef.current !== null) return
    probingRef.current = applicationId
    setProbing(applicationId)
    setProbeError(null)
    const gen = genRef.current
    api
      .caseStudyProbe(applicationId)
      .then(() => {
        if (genRef.current !== gen || jobId === null) return
        setOpenId(applicationId)
        return reload(jobId, gen)
      })
      .catch((e) => {
        if (genRef.current !== gen) return
        const message =
          e instanceof ApiError ? e.message.replace(/^\d+:\s*/, '') : 'Probe failed. Try again.'
        setProbeError({ id: applicationId, message })
      })
      .finally(() => {
        probingRef.current = null
        setProbing(null)
      })
  }

  return (
    <div className="mx-auto max-w-7xl px-8 py-7">
      <header className="mb-5">
        <h1 className="font-display text-2xl font-bold text-ink">Case Study Evaluation</h1>
        <p className="mt-1 text-sm text-ink-muted">
          Who has submitted, who has not, what came in and what the pool has in common.
          Scoring a submission against a benchmark is on Case Study Scoring.
        </p>
      </header>

      {jobsError ? (
        <p className="text-sm text-danger">{jobsError}</p>
      ) : !jobsLoaded ? (
        <Spinner label="Loading jobs…" />
      ) : (
        <select
          value={jobId ?? ''}
          onChange={(e) => setJobId(Number(e.target.value))}
          className="input w-auto"
        >
          {jobs.map((j) => (
            <option key={j.job_pk} value={j.job_pk}>
              {j.title ?? `Job ${j.job_pk}`}
            </option>
          ))}
        </select>
      )}

      {summary && (
        <>
          <div className="mt-5 grid grid-cols-2 gap-3 lg:grid-cols-4">
            {(
              [
                ['Submitted', summary.submitted],
                ['Awaiting submission', summary.awaiting],
                ['No record of a send', summary.no_record_of_a_send],
                ['Submitted, no send on record', summary.submitted_without_send_record],
              ] as const
            ).map(([label, value]) => (
              <div key={label} className="rounded-2xl border border-hairline bg-surface p-4">
                <div className="text-sm font-medium text-ink-muted">{label}</div>
                <div className="mt-1 text-2xl font-bold tabular-nums text-ink">{value}</div>
              </div>
            ))}
          </div>

          {/* The caveat is not a footnote. Markaz stores no send at all, so
              this count is the number of people we simply cannot speak for. */}
          {summary.unproven_absence > 0 && (
            <div className="mt-3 flex gap-2.5 rounded-xl border border-warning/30 bg-warning/5 px-4 py-3 text-sm text-ink-muted">
              <AlertTriangle className="mt-0.5 h-4 w-4 shrink-0 text-warning" />
              <p>
                <span className="font-semibold text-ink">
                  {summary.unproven_absence} of {summary.total} cannot be described as
                  &ldquo;not sent a case study&rdquo;.
                </span>{' '}
                Markaz records no case-study send anywhere, so the only evidence of one is in
                Ayesha&rsquo;s mailbox. Probe a candidate to look. {summary.probed} of{' '}
                {summary.total} have been probed so far.
              </p>
            </div>
          )}

          {mirrors.length > 0 && (
            <div className="mt-3 rounded-xl border border-blurple/30 bg-blurple/5 px-4 py-3">
              <div className="flex items-center gap-2 text-sm font-semibold text-ink">
                <Copy className="h-4 w-4 text-blurple" />
                {mirrors.length} pair{mirrors.length === 1 ? '' : 's'} of submissions share long
                identical passages
              </div>
              {/* Evidence, never a verdict: two candidates quoting the same
                  paragraph of the assignment look exactly like this. */}
              <p className="mt-1 text-xs text-ink-muted">
                Worth reading side by side. Candidates quoting the same part of the assignment
                look identical to candidates sharing an assistant, and only a person reading both
                can tell which.
              </p>
              <ul className="mt-2 space-y-2">
                {mirrors.map((m) => (
                  <li key={m.application_ids.join('-')} className="text-xs text-ink-muted">
                    <span className="font-medium text-ink">{m.candidate_names.join(' and ')}</span>
                    {' · '}
                    {m.shared_runs} shared passage{m.shared_runs === 1 ? '' : 's'}
                    {m.examples[0] && (
                      <div className="mt-1 rounded-lg bg-surface px-2.5 py-1.5 font-mono text-[11px] leading-relaxed">
                        &ldquo;{m.examples[0]}&rdquo;
                      </div>
                    )}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </>
      )}

      {listError ? (
        <p className="mt-5 text-sm text-danger">{listError}</p>
      ) : !loaded ? (
        jobId !== null && (
          <div className="mt-5">
            <Spinner label="Loading applications…" />
          </div>
        )
      ) : rows.length === 0 ? (
        <p className="mt-5 text-sm text-ink-dim">No applications on this job.</p>
      ) : (
        <div className="mt-5 overflow-hidden rounded-2xl border border-hairline bg-surface">
          <table className="w-full text-sm">
            <thead className="border-b border-hairline bg-elevated text-left text-xs uppercase tracking-wide text-ink-dim">
              <tr>
                <th className="px-4 py-2.5 font-semibold">Candidate</th>
                <th className="px-4 py-2.5 font-semibold">Status</th>
                <th className="px-4 py-2.5 font-semibold">Channels</th>
                <th className="px-4 py-2.5 font-semibold">Flags</th>
                <th className="px-4 py-2.5 font-semibold">Last looked</th>
                <th className="px-4 py-2.5" />
              </tr>
            </thead>
            <tbody>
              {rows.map((r) => {
                const p = r.probe
                const open = openId === r.application_id
                const busy = probing === r.application_id
                return (
                  <Fragment key={r.application_id}>
                    <tr className="border-b border-hairline/60 last:border-0">
                      <td className="px-4 py-2.5">
                        <div className="font-medium text-ink">{r.candidate_name}</div>
                        <div className="text-xs text-ink-dim">
                          {r.email ?? 'no email'} · app {r.application_id}
                        </div>
                      </td>
                      <td className="px-4 py-2.5">
                        <StatusBadge status={r.status} />
                      </td>
                      <td className="px-4 py-2.5 text-xs text-ink-muted">
                        {r.channels.length ? r.channels.join(', ') : '—'}
                      </td>
                      <td className="px-4 py-2.5 text-xs">
                        {p?.corpus_error ? (
                          <span className="text-danger">could not read</span>
                        ) : p?.flags.length ? (
                          <span className="text-warning">{p.flags.length}</span>
                        ) : p ? (
                          <span className="text-ink-dim">none</span>
                        ) : (
                          <span className="text-ink-dim">—</span>
                        )}
                      </td>
                      <td className="px-4 py-2.5 text-xs text-ink-dim">
                        {p?.probed_at ? new Date(p.probed_at).toLocaleDateString() : 'never'}
                      </td>
                      <td className="px-4 py-2.5 text-right">
                        <div className="flex items-center justify-end gap-2">
                          <button
                            type="button"
                            className="btn-secondary text-xs"
                            disabled={busy}
                            onClick={() => runProbe(r.application_id)}
                          >
                            {busy ? (
                              <span className="flex items-center gap-1.5">
                                <Loader2 className="h-3.5 w-3.5 animate-spin" /> Looking…
                              </span>
                            ) : p ? (
                              'Look again'
                            ) : (
                              'Look'
                            )}
                          </button>
                          {p && (
                            <button
                              type="button"
                              className="rounded-lg p-1 text-ink-dim hover:bg-elevated"
                              onClick={() => setOpenId(open ? null : r.application_id)}
                              aria-label={open ? 'Collapse' : 'Expand'}
                            >
                              <ChevronDown
                                className={`h-4 w-4 transition-transform ${open ? 'rotate-180' : ''}`}
                              />
                            </button>
                          )}
                        </div>
                      </td>
                    </tr>

                    {probeError?.id === r.application_id && (
                      <tr className="border-b border-hairline/60">
                        <td colSpan={6} className="bg-danger/5 px-4 py-2.5 text-sm text-danger">
                          {probeError.message}
                        </td>
                      </tr>
                    )}

                    {open && p && (
                      <tr className="border-b border-hairline/60">
                        <td colSpan={6} className="bg-elevated/50 px-4 py-4">
                          <div className="grid gap-4 text-xs text-ink-muted lg:grid-cols-3">
                            <div>
                              <div className="font-semibold text-ink">The send</div>
                              {p.send_found ? (
                                <p className="mt-1">
                                  &ldquo;{p.send_subject}&rdquo;
                                  {p.send_at && ` · ${new Date(p.send_at).toLocaleDateString()}`}
                                </p>
                              ) : (
                                <p className="mt-1">
                                  Nothing found in the mailbox. That means our records are silent,
                                  not that nothing was sent.
                                </p>
                              )}
                            </div>

                            <div>
                              <div className="font-semibold text-ink">The submission</div>
                              {p.corpus_error ? (
                                <p className="mt-1 text-danger">{p.corpus_error}</p>
                              ) : p.corpus_chars ? (
                                <p className="mt-1">
                                  {p.corpus_chars.toLocaleString()} characters read from{' '}
                                  {p.sources.length || 'no'} source
                                  {p.sources.length === 1 ? '' : 's'}
                                  {p.sources.length > 0 && `: ${p.sources.join('; ')}`}
                                </p>
                              ) : (
                                <p className="mt-1">Nothing to read yet.</p>
                              )}
                              {p.completeness?.known === false && (
                                <p className="mt-1 italic">{p.completeness.note}</p>
                              )}
                              {p.completeness?.known && (
                                <p className="mt-1">
                                  Missing:{' '}
                                  {p.completeness.missing?.length
                                    ? p.completeness.missing.join(', ')
                                    : 'nothing'}
                                </p>
                              )}
                            </div>

                            <div>
                              <div className="font-semibold text-ink">Flags</div>
                              {p.flags.length === 0 ? (
                                <p className="mt-1">None raised.</p>
                              ) : (
                                <ul className="mt-1 space-y-1.5">
                                  {p.flags.map((f) => (
                                    <li key={f.flag}>
                                      <span className="font-medium text-ink">{f.flag}</span>{' '}
                                      ({f.count}) — {f.meaning}
                                      {f.evidence && (
                                        <div className="mt-0.5 font-mono text-[11px]">
                                          {f.evidence}
                                        </div>
                                      )}
                                    </li>
                                  ))}
                                </ul>
                              )}
                            </div>
                          </div>
                        </td>
                      </tr>
                    )}
                  </Fragment>
                )
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
