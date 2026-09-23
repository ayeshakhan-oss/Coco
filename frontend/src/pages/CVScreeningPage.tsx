import { Fragment, useEffect, useRef, useState } from 'react'
import { ChevronDown, FileText, Loader2 } from 'lucide-react'
import { Spinner } from '../components/Spinner'
import { ApiError, api } from '../lib/api'
import { runScreenAll } from '../lib/screenAll'
import type {
  CVScreen,
  CVScreenApplication,
  CVScreenJobSummary,
  CVScreenTier,
  JobItem,
} from '../lib/types'

// Coco's own CV screening. Nugget's technical screening lives on
// /evaluations and is a separate skill with a separate rubric: no tier
// vocabulary, no gate and no score from that engine appears on this page.

const GENERIC_LOAD_ERROR = 'Could not load CV screening. Try reloading the page.'

const TIER_LABEL: Record<CVScreenTier, string> = {
  shortlist: 'Shortlist',
  maybe: 'Maybe',
  no_hire: 'No hire',
}

const TIER_CLASS: Record<CVScreenTier, string> = {
  shortlist: 'bg-success/10 text-success border-success/30',
  maybe: 'bg-warning/10 text-warning border-warning/30',
  no_hire: 'bg-ink-dim/10 text-ink-dim border-hairline',
}

function TierBadge({ tier }: { tier: CVScreenTier }) {
  return (
    <span className={`inline-block rounded-full border px-2.5 py-0.5 text-xs font-semibold ${TIER_CLASS[tier]}`}>
      {TIER_LABEL[tier]}
    </span>
  )
}

function years(n: number) {
  return `${n % 1 === 0 ? n.toFixed(0) : n.toFixed(1)}y`
}

export function CVScreeningPage() {
  const [jobs, setJobs] = useState<JobItem[]>([])
  const [jobsLoaded, setJobsLoaded] = useState(false)
  const [jobsError, setJobsError] = useState<string | null>(null)
  const [jobId, setJobId] = useState<number | null>(null)

  const [summary, setSummary] = useState<CVScreenJobSummary | null>(null)
  const [rows, setRows] = useState<CVScreenApplication[]>([])
  const [rowsLoaded, setRowsLoaded] = useState(false)
  const [listError, setListError] = useState<string | null>(null)

  const [openId, setOpenId] = useState<number | null>(null)
  const [screening, setScreening] = useState<number | null>(null)
  const [screenError, setScreenError] = useState<{ id: number; message: string } | null>(null)
  // The outcome of the last whole-position run, shown until the next one
  // starts. The run's own failures used to be written into `screenError` with
  // id -1, which is rendered only against a row whose application_id matches,
  // so it matched nothing: a run that died showed the user no message at all.
  const [runOutcome, setRunOutcome] = useState<
    { kind: 'done' | 'stopped' | 'error'; done: number; skipped: number; message?: string } | null
  >(null)

  // Bumped whenever the selected job changes, and read back by every response
  // before it is applied, so a slow response for a job the user has navigated
  // away from cannot overwrite the current one.
  const genRef = useRef(0)
  // Synchronous double-click guard: `screening` state only lands on the next
  // render, so two fast clicks can both read it as null and screen twice.
  const screeningRef = useRef<number | null>(null)

  useEffect(() => {
    api
      .cvScreenJobs()
      .then((j) => {
        setJobs(j)
        setJobsLoaded(true)
        setJobsError(null)
        if (j.length && jobId === null) setJobId(j[0].job_pk)
      })
      .catch(() => {
        setJobsLoaded(true)
        setJobsError(GENERIC_LOAD_ERROR)
      })
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  useEffect(() => {
    if (jobId === null) return
    const gen = ++genRef.current
    setRowsLoaded(false)
    setSummary(null)
    setOpenId(null)
    setScreenError(null)
    setRunOutcome(null)
    Promise.all([api.cvScreenJobSummary(jobId), api.cvScreenApplications(jobId)])
      .then(([s, a]) => {
        if (genRef.current !== gen) return
        setSummary(s)
        setRows(a)
        setListError(null)
        setRowsLoaded(true)
      })
      .catch(() => {
        if (genRef.current !== gen) return
        setListError(GENERIC_LOAD_ERROR)
        setRowsLoaded(true)
      })
  }, [jobId])

  const runScreen = (applicationId: number) => {
    if (screeningRef.current !== null) return
    screeningRef.current = applicationId
    setScreening(applicationId)
    setScreenError(null)
    const gen = genRef.current
    api
      .cvScreen(applicationId)
      .then((screen) => {
        if (genRef.current !== gen) return
        setRows((prev) =>
          prev.map((r) => (r.application_id === applicationId ? { ...r, screen } : r)),
        )
        setOpenId(applicationId)
        if (jobId !== null) {
          api
            .cvScreenJobSummary(jobId)
            .then((s) => genRef.current === gen && setSummary(s))
            .catch(() => undefined)
        }
      })
      .catch((e) => {
        if (genRef.current !== gen) return
        // The API's refusals are written for a person to read ("no resume on
        // file for this candidate"), so show them rather than a generic line.
        const message =
          e instanceof ApiError && typeof e.message === 'string'
            ? e.message.replace(/^\d+:\s*/, '')
            : 'Screening failed. Try again.'
        setScreenError({ id: applicationId, message })
      })
      .finally(() => {
        screeningRef.current = null
        setScreening(null)
      })
  }

  // --- Screen the whole position -------------------------------------
  // The server does a few candidates per request on purpose: each CV is a
  // model call of roughly 15 seconds, so 74 candidates is about 20 minutes
  // and no single HTTP request survives that. This loops, so progress is
  // visible and the run can be stopped.
  //
  // 🔴 The loop itself lives in lib/screenAll.ts and RETRIES. A fifty-minute
  // run of this page died at 236 of 410 on 2026-09-23 because Railway
  // redeployed underneath it and one dead request used to end the run.
  const [runAll, setRunAll] = useState<{
    done: number
    total: number
    skipped: number
    stopping: boolean
    retrying: number
    retryInSeconds: number
  } | null>(null)
  const stopRef = useRef(false)

  const screenWholePosition = async () => {
    if (jobId === null || runAll) return
    const gen = genRef.current
    const total = summary?.unscreened ?? rows.filter((r) => !r.screen).length
    stopRef.current = false
    setRunAll({ done: 0, total, skipped: 0, stopping: false, retrying: 0, retryInSeconds: 0 })
    setScreenError(null)
    setRunOutcome(null)

    // The stat boxes are refreshed as the run goes, not only at the end. They
    // used to be refreshed once, after the loop, INSIDE the try -- so a run
    // that ended on an error left them frozen at whatever they read when the
    // page was opened. Ayesha's page said 67 screened while the database held
    // 236, which is why a run that had done most of the work looked like one
    // that had barely started.
    const refreshSummary = () => {
      if (jobId === null) return
      api
        .cvScreenJobSummary(jobId)
        .then((s) => genRef.current === gen && setSummary(s))
        .catch(() => undefined)
    }

    const result = await runScreenAll({
      runBatch: (after) => api.cvScreenBatch(jobId, after),
      shouldStop: () => stopRef.current,
      isAbandoned: () => genRef.current !== gen,
      onBatch: (batch) => {
        const byId = new Map(batch.screened.map((x) => [x.application_id, x]))
        setRows((prev) =>
          prev.map((r) => (byId.has(r.application_id)
            ? { ...r, screen: byId.get(r.application_id)! }
            : r)),
        )
        refreshSummary()
      },
      onProgress: (p) =>
        setRunAll({
          done: p.done,
          total,
          skipped: p.skipped,
          stopping: stopRef.current,
          retrying: p.retrying,
          retryInSeconds: p.retryInSeconds,
        }),
    })

    if (genRef.current !== gen) return
    setRunAll(null)
    refreshSummary()
    setRunOutcome({
      kind: result.error ? 'error' : result.stopped ? 'stopped' : 'done',
      done: result.done,
      skipped: result.skipped,
      message: result.error ?? undefined,
    })
  }

  const boxes = summary
    ? [
        { label: 'Total applications', value: summary.total },
        { label: 'Shortlisted', value: summary.shortlist },
        { label: 'Maybe', value: summary.maybe },
        { label: 'No hire', value: summary.no_hire },
      ]
    : []

  return (
    <div className="mx-auto max-w-7xl px-8 py-7">
      <header className="mb-5">
        <h1 className="font-display text-2xl font-bold text-ink">CV Screening</h1>
        <p className="mt-1 text-sm text-ink-muted">
          Every CV read against its own job description on Coco's three criteria: skills and
          experience first, fit as support. Separate from technical screening, which is Nugget's
          engine and has its own rubric.
        </p>
      </header>

      {jobsError ? (
        <p className="text-sm text-danger">{jobsError}</p>
      ) : !jobsLoaded ? (
        <Spinner label="Loading jobs…" />
      ) : jobs.length === 0 ? (
        <p className="text-sm text-ink-dim">No positions found.</p>
      ) : (
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

      {summary && (
        <>
          {summary.jd_error ? (
            <div className="mt-5 rounded-xl border border-danger/30 bg-danger/5 px-4 py-2.5 text-sm text-danger">
              This job has no readable description, so nothing can be screened against it.{' '}
              {summary.jd_error}
            </div>
          ) : (
            <p className="mt-4 text-xs text-ink-dim">
              Screening against {summary.jd_chars.toLocaleString()} characters of job description.
            </p>
          )}

          <div className="mt-3 grid grid-cols-2 gap-3 lg:grid-cols-4">
            {boxes.map((b) => (
              <div key={b.label} className="rounded-2xl border border-hairline bg-surface p-4">
                <div className="text-sm font-medium text-ink-muted">{b.label}</div>
                <div className="mt-1 text-2xl font-bold tabular-nums text-ink">{b.value}</div>
              </div>
            ))}
          </div>

          {summary.unscreened > 0 && (
            <p className="mt-2 text-xs text-ink-dim">
              {summary.unscreened} of {summary.total} not yet screened. The three tiers sum to{' '}
              {summary.shortlist + summary.maybe + summary.no_hire}; the stat boxes only balance
              once every CV has been read.
            </p>
          )}

          {/* Run the whole position. The per-row Screen button is for one
              candidate; this is how a position actually gets screened. */}
          {/* `runOutcome` keeps the panel alive after a run that finished the
              position, so the result is still readable once unscreened hits 0. */}
          {!summary.jd_error && (summary.unscreened > 0 || runAll || runOutcome) && (
            <div className="mt-4 rounded-xl border border-hairline bg-surface p-4">
              {runAll ? (
                <>
                  <div className="flex items-center justify-between gap-4">
                    <div className="flex items-center gap-2.5 text-sm text-ink">
                      <Loader2 className="h-4 w-4 animate-spin text-blurple" />
                      <span className="font-medium">
                        Reading CVs: {runAll.done} of {runAll.total}
                      </span>
                      {runAll.skipped > 0 && (
                        <span className="text-xs text-warning">
                          {runAll.skipped} could not be read
                        </span>
                      )}
                      {/* A redeploy takes the server away for minutes. Say so,
                          or a waiting run reads as a frozen page. */}
                      {runAll.retrying > 0 && (
                        <span className="text-xs text-warning">
                          Lost the server. Retrying in {runAll.retryInSeconds}s (attempt{' '}
                          {runAll.retrying})
                        </span>
                      )}
                    </div>
                    <button
                      type="button"
                      className="btn-secondary text-xs"
                      disabled={runAll.stopping}
                      onClick={() => {
                        stopRef.current = true
                        setRunAll((r) => (r ? { ...r, stopping: true } : r))
                      }}
                    >
                      {runAll.stopping ? 'Stopping after this batch…' : 'Stop'}
                    </button>
                  </div>
                  <div className="mt-2.5 h-1.5 overflow-hidden rounded-full bg-elevated">
                    <div
                      className="h-full rounded-full bg-blurple transition-all"
                      style={{
                        width: `${runAll.total ? Math.round((runAll.done / runAll.total) * 100) : 0}%`,
                      }}
                    />
                  </div>
                  {/* Nothing is lost by stopping: each candidate is saved as
                      they finish, and starting again picks up where it left off. */}
                  <p className="mt-2 text-xs text-ink-dim">
                    Each CV takes about 15 seconds. Every candidate is saved as they
                    finish, so stopping loses nothing and starting again continues
                    from here.
                  </p>
                </>
              ) : summary.unscreened === 0 ? (
                <div className="text-sm font-semibold text-ink">
                  Every CV on this position has been read.
                </div>
              ) : (
                <div className="flex flex-wrap items-center justify-between gap-3">
                  <div>
                    <div className="text-sm font-semibold text-ink">
                      Screen this whole position
                    </div>
                    <p className="text-xs text-ink-muted">
                      {summary.unscreened} candidate{summary.unscreened === 1 ? '' : 's'} still
                      to read, roughly{' '}
                      {Math.max(1, Math.round((summary.unscreened * 15) / 60))} minutes. You can
                      stop at any point.
                    </p>
                  </div>
                  <button
                    type="button"
                    className="btn-primary text-sm"
                    onClick={screenWholePosition}
                  >
                    Screen all {summary.unscreened}
                  </button>
                </div>
              )}

              {/* How the last run ended, said out loud. A run that failed used
                  to leave nothing on screen at all. */}
              {!runAll && runOutcome && (
                <div
                  className={`mt-3 rounded-lg border px-3 py-2 text-xs ${
                    runOutcome.kind === 'error'
                      ? 'border-danger/30 bg-danger/5 text-danger'
                      : 'border-hairline bg-elevated text-ink-muted'
                  }`}
                >
                  {runOutcome.kind === 'error' ? (
                    <>
                      <span className="font-semibold">
                        The run stopped after {runOutcome.done} candidate
                        {runOutcome.done === 1 ? '' : 's'}.
                      </span>{' '}
                      {runOutcome.message} Everything screened so far is saved. Starting again
                      picks up from where it stopped.
                    </>
                  ) : (
                    <>
                      {runOutcome.kind === 'stopped' ? 'Stopped' : 'Finished'} after{' '}
                      {runOutcome.done} candidate{runOutcome.done === 1 ? '' : 's'}.
                      {runOutcome.skipped > 0 && (
                        <>
                          {' '}
                          <span className="text-warning">
                            {runOutcome.skipped} CV{runOutcome.skipped === 1 ? '' : 's'} could not
                            be read and {runOutcome.skipped === 1 ? 'needs' : 'need'} a person.
                          </span>{' '}
                          A CV that will not open is a document problem, not a weak candidate, so
                          {runOutcome.skipped === 1 ? ' it stays' : ' they stay'} counted as
                          unscreened.
                        </>
                      )}
                    </>
                  )}
                </div>
              )}
            </div>
          )}

        </>
      )}

      {listError ? (
        <p className="mt-5 text-sm text-danger">{listError}</p>
      ) : !rowsLoaded ? (
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
                <th className="px-4 py-2.5 font-semibold">Tier</th>
                <th className="px-4 py-2.5 text-right font-semibold">Match</th>
                {/* Two figures, never one: the SOP names conflating them as a mistake. */}
                <th className="px-4 py-2.5 text-right font-semibold">Total exp</th>
                <th className="px-4 py-2.5 text-right font-semibold">Relevant exp</th>
                <th className="px-4 py-2.5 font-semibold">Salary / City / Relocate</th>
                <th className="px-4 py-2.5" />
              </tr>
            </thead>
            <tbody>
              {rows.map((r) => {
                const s = r.screen
                const open = openId === r.application_id
                const busy = screening === r.application_id
                return (
                  <Fragment key={r.application_id}>
                    <tr className="border-b border-hairline/60 last:border-0">
                      <td className="px-4 py-2.5">
                        <div className="font-medium text-ink">{r.candidate_name}</div>
                        <div className="text-xs text-ink-dim">
                          {r.email ?? 'no email'} · app {r.application_id}
                        </div>
                      </td>
                      <td className="px-4 py-2.5">{s ? <TierBadge tier={s.tier} /> : <span className="text-xs text-ink-dim">not screened</span>}</td>
                      <td className="px-4 py-2.5 text-right tabular-nums text-ink">{s ? `${s.match}%` : '—'}</td>
                      <td className="px-4 py-2.5 text-right tabular-nums text-ink">
                        {s ? years(s.total_experience_years) : '—'}
                      </td>
                      <td className="px-4 py-2.5 text-right tabular-nums text-ink">
                        {s ? years(s.relevant_experience_years) : '—'}
                      </td>
                      <td className="px-4 py-2.5 text-xs text-ink-muted">
                        {/* A dash means the candidate was never asked, not zero. */}
                        {r.expected_salary ?? '—'} · {r.city ?? '—'} · {r.willing_to_relocate ?? '—'}
                      </td>
                      <td className="px-4 py-2.5 text-right">
                        <div className="flex items-center justify-end gap-2">
                          <button
                            type="button"
                            className="btn-secondary text-xs"
                            disabled={busy || !r.cv_available || !!summary?.jd_error}
                            title={
                              !r.cv_available
                                ? 'No CV on file for this candidate'
                                : summary?.jd_error
                                  ? 'This job has no readable description'
                                  : undefined
                            }
                            onClick={() => runScreen(r.application_id)}
                          >
                            {busy ? (
                              <span className="flex items-center gap-1.5">
                                <Loader2 className="h-3.5 w-3.5 animate-spin" /> Reading…
                              </span>
                            ) : s ? (
                              'Re-screen'
                            ) : (
                              'Screen'
                            )}
                          </button>
                          {s && (
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

                    {screenError?.id === r.application_id && (
                      <tr className="border-b border-hairline/60">
                        <td colSpan={7} className="bg-danger/5 px-4 py-2.5 text-sm text-danger">
                          {screenError.message}
                        </td>
                      </tr>
                    )}

                    {open && s && (
                      <tr className="border-b border-hairline/60">
                        <td colSpan={7} className="bg-elevated/50 px-4 py-4">
                          <ScreenDetail screen={s} />
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

function ScreenDetail({ screen }: { screen: CVScreen }) {
  return (
    <div className="grid gap-5 lg:grid-cols-3">
      <div className="lg:col-span-2">
        <h3 className="mb-2 font-display text-sm font-bold text-ink">Criteria</h3>
        <div className="space-y-2.5">
          {/* Rendered from the criteria the API carries on every screen, so
              this never drifts from cv_screening.CRITERIA. */}
          {screen.criteria.map((c) => (
            <div key={c.key} className="rounded-xl border border-hairline bg-surface p-3">
              <div className="flex items-baseline justify-between">
                <span className="text-sm font-semibold text-ink">
                  {c.label}{' '}
                  <span className="text-xs font-normal text-ink-dim">
                    {c.priority} priority · weight {c.weight}
                  </span>
                </span>
                <span className="tabular-nums text-sm font-bold text-ink">
                  {screen.scores[c.key]} / 5
                </span>
              </div>
              <p className="mt-1 text-xs leading-relaxed text-ink-muted">{screen.evidence[c.key]}</p>
            </div>
          ))}
        </div>

        <div className="mt-4 grid gap-4 sm:grid-cols-2">
          <div>
            <h3 className="mb-1.5 font-display text-sm font-bold text-ink">Strengths</h3>
            <ul className="list-disc space-y-1 pl-4 text-xs text-ink-muted">
              {screen.strengths.map((x, i) => (
                <li key={i}>{x}</li>
              ))}
            </ul>
          </div>
          <div>
            <h3 className="mb-1.5 font-display text-sm font-bold text-ink">Gaps</h3>
            <ul className="list-disc space-y-1 pl-4 text-xs text-ink-muted">
              {screen.gaps.map((x, i) => (
                <li key={i}>{x}</li>
              ))}
            </ul>
          </div>
        </div>
      </div>

      <div className="space-y-3 text-xs text-ink-muted">
        <div className="rounded-xl border border-hairline bg-surface p-3">
          <div className="font-semibold text-ink">Experience</div>
          <p className="mt-1">
            {years(screen.total_experience_years)} total, of which{' '}
            {years(screen.relevant_experience_years)} relevant.
          </p>
          <p className="mt-1 leading-relaxed">{screen.relevant_experience_note}</p>
        </div>

        <div className="rounded-xl border border-hairline bg-surface p-3">
          <div className="font-semibold text-ink">What this was read from</div>
          <p className="mt-1">
            <FileText className="mr-1 inline h-3 w-3" />
            {screen.cv_chars.toLocaleString()} characters of CV
            {screen.cv_truncated && ' (truncated at the reading limit)'}
          </p>
          <p className="mt-1">Model {screen.model}</p>
          <p className="mt-1">SOP {screen.sop_sha256.slice(0, 12)}</p>
          <p className="mt-0.5">JD {screen.jd_sha256.slice(0, 12)}</p>
          {screen.created_at && <p className="mt-1">{new Date(screen.created_at).toLocaleString()}</p>}
          {!screen.is_current && (
            <p className="mt-1 font-semibold text-warning">
              Superseded by a later screen. Not the live result.
            </p>
          )}
        </div>
      </div>
    </div>
  )
}
