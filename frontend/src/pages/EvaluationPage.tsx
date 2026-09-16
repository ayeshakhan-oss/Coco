import { Fragment, useEffect, useRef, useState } from 'react'
import { ChevronDown, FileSearch, Loader2 } from 'lucide-react'
import { Spinner } from '../components/Spinner'
import { api } from '../lib/api'
import type { EvaluationDetail, EvaluationRow, EvaluationSummary, ScreenedJob } from '../lib/types'

const GENERIC_LOAD_ERROR = 'Could not load screening results. Try reloading the page.'
const PAGE_SIZE = 100

export function EvaluationPage() {
  const [jobs, setJobs] = useState<ScreenedJob[]>([])
  const [jobsLoaded, setJobsLoaded] = useState(false)
  const [jobsError, setJobsError] = useState<string | null>(null)
  const [jobId, setJobId] = useState<number | null>(null)
  const [summary, setSummary] = useState<EvaluationSummary | null>(null)
  const [summaryError, setSummaryError] = useState<string | null>(null)
  const [rows, setRows] = useState<EvaluationRow[]>([])
  const [total, setTotal] = useState(0)
  const [rowsLoaded, setRowsLoaded] = useState(false)
  const [loadingMore, setLoadingMore] = useState(false)
  const [candidatesError, setCandidatesError] = useState<string | null>(null)
  const [tier, setTier] = useState<string | undefined>(undefined)
  const [openId, setOpenId] = useState<number | null>(null)
  const [detail, setDetail] = useState<EvaluationDetail | null>(null)
  const [detailError, setDetailError] = useState<string | null>(null)

  // Tracks which application_id the in-flight detail request is FOR. A
  // response is only applied if it still matches this ref when it lands, so
  // a slow response for a row the user already closed (or moved on from)
  // can never overwrite what's currently open.
  const openRequestRef = useRef<number | null>(null)

  // Bumped every time (jobId, tier) changes, and read back by every summary /
  // candidates / load-more response before it is applied. A late response
  // for a selection the user has since navigated away from (e.g. clicking P1
  // then P4 quickly) is a stale generation and is dropped.
  const listGenRef = useRef(0)

  const openRow = (applicationId: number | null) => {
    if (applicationId === null) return
    if (openId === applicationId) {
      setOpenId(null)
      setDetail(null)
      setDetailError(null)
      openRequestRef.current = null
      return
    }
    setOpenId(applicationId)
    setDetail(null)
    setDetailError(null)
    openRequestRef.current = applicationId
    api
      .evaluationDetail(applicationId)
      .then((d) => {
        if (openRequestRef.current !== applicationId) return // stale response for a row no longer open
        setDetail(d)
      })
      .catch(() => {
        if (openRequestRef.current !== applicationId) return
        setDetailError("Could not load this candidate's evaluation. Try again.")
      })
  }

  useEffect(() => {
    api
      .evaluationJobs()
      .then((j) => {
        setJobs(j)
        setJobsError(null)
        setJobsLoaded(true)
        if (j.length && jobId === null) setJobId(j[0].job_id)
      })
      .catch(() => {
        setJobsError(GENERIC_LOAD_ERROR)
        setJobsLoaded(true)
      })
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  useEffect(() => {
    if (jobId === null) return
    const gen = ++listGenRef.current

    // A detail panel opened against the previous (job, tier) selection can
    // never stay meaningful once that selection changes.
    setOpenId(null)
    setDetail(null)
    setDetailError(null)
    openRequestRef.current = null

    setSummaryError(null)
    setCandidatesError(null)
    setRowsLoaded(false)
    setRows([])
    setTotal(0)

    api
      .evaluationSummary(jobId)
      .then((s) => {
        if (listGenRef.current !== gen) return // stale: job/tier changed since this request was sent
        setSummary(s)
      })
      .catch(() => {
        if (listGenRef.current !== gen) return
        setSummaryError(GENERIC_LOAD_ERROR)
      })
    api
      .evaluationCandidates(jobId, tier, PAGE_SIZE, 0)
      .then((page) => {
        if (listGenRef.current !== gen) return
        setRows(page.rows)
        setTotal(page.total)
        setRowsLoaded(true)
      })
      .catch(() => {
        if (listGenRef.current !== gen) return
        setCandidatesError(GENERIC_LOAD_ERROR)
        setRowsLoaded(true)
      })
  }, [jobId, tier])

  const loadMore = () => {
    if (jobId === null || loadingMore) return
    const gen = listGenRef.current // this page belongs to the currently displayed (jobId, tier)
    setLoadingMore(true)
    api
      .evaluationCandidates(jobId, tier, PAGE_SIZE, rows.length)
      .then((page) => {
        if (listGenRef.current !== gen) return // the selection moved on while this page was in flight
        setRows((prev) => [...prev, ...page.rows])
        setTotal(page.total)
      })
      .catch(() => {
        if (listGenRef.current !== gen) return
        setCandidatesError(GENERIC_LOAD_ERROR)
      })
      .finally(() => {
        if (listGenRef.current === gen) setLoadingMore(false)
      })
  }

  // Copy for a tier whose score is suppressed. UNUSABLE means the CV never
  // opened; MANUAL_REVIEW means it opened but fell below the rubric's
  // readability floor. Both need a human on the document, neither is a 0%.
  const unscoredLabel = (isUnusable: boolean) =>
    isUnusable ? 'CV could not be read, needs a human' : 'Below the readability floor, needs a human'

  return (
    <div className="mx-auto max-w-7xl px-8 py-7">
      <header className="mb-5">
        <h1 className="font-display text-2xl font-bold text-ink">Candidate Evaluation</h1>
        <p className="mt-1 text-sm text-ink-muted">
          Technical screening results produced by Nugget's screening engine. Read only.
        </p>
      </header>

      {jobsError ? (
        <p className="text-sm text-danger">{jobsError}</p>
      ) : jobsLoaded && jobs.length === 0 ? (
        <p className="text-sm text-ink-dim">No screened jobs found.</p>
      ) : !jobsLoaded ? (
        <Spinner label="Loading jobs…" />
      ) : (
        <select
          value={jobId ?? ''}
          onChange={(e) => {
            setJobId(Number(e.target.value))
            setTier(undefined)
          }}
          className="input w-auto"
        >
          {jobs.map((j) => (
            <option key={j.job_id} value={j.job_id}>
              {j.job_title ?? `Job ${j.job_id}`} (rubric v{j.rubric_version})
            </option>
          ))}
        </select>
      )}

      {summaryError ? (
        <p className="mt-4 text-sm text-danger">{summaryError}</p>
      ) : (
        summary && (
          <div className="mt-5 grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-5">
            {summary.unscored > 0 && (
              <div className="col-span-full rounded-xl border border-danger/30 bg-danger/5 px-4 py-2.5 text-sm text-danger">
                {summary.unscored} of {summary.total} candidate{summary.unscored === 1 ? '' : 's'} on this job could
                not be read by Nugget's engine and need a human to open the CV.
              </div>
            )}
            {summary.tiers.map((t) => {
              const active = tier === t.tier
              return (
                <button
                  key={t.tier}
                  type="button"
                  onClick={() => setTier(active ? undefined : t.tier)}
                  className={`rounded-2xl border p-4 text-left transition-colors ${
                    active ? 'border-blurple bg-blurple/5 ring-2 ring-blurple/30' : 'border-hairline bg-surface hover:bg-elevated'
                  }`}
                >
                  <div className="font-display text-base font-bold text-ink">{t.tier}</div>
                  <div className="mt-1 text-2xl font-bold tabular-nums text-ink">{t.n}</div>
                  {t.is_unscored ? (
                    <div className="mt-1 text-xs font-medium text-danger">{unscoredLabel(t.is_unusable)}</div>
                  ) : (
                    t.avg_pct !== null && <div className="mt-1 text-xs text-ink-dim">avg {t.avg_pct}%</div>
                  )}
                </button>
              )
            })}
          </div>
        )
      )}

      <div className="card mt-6 overflow-hidden">
        {candidatesError ? (
          <div className="p-8 text-center text-sm text-danger">{candidatesError}</div>
        ) : !rowsLoaded ? (
          <Spinner label="Loading candidates…" />
        ) : rows.length === 0 ? (
          <div className="p-12 text-center text-sm text-ink-dim">No candidates in this tier.</div>
        ) : (
          <table className="w-full text-left text-sm">
            <thead className="border-b border-hairline bg-surface-2 text-xs uppercase tracking-wide text-ink-dim">
              <tr>
                <th className="px-5 py-3 font-medium">Candidate</th>
                <th className="px-5 py-3 font-medium">Tier</th>
                <th className="px-5 py-3 font-medium">Score</th>
                <th className="px-5 py-3 font-medium">Why</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-hairline">
              {rows.map((r) => (
                <Fragment key={r.application_id ?? r.candidate_email}>
                  <tr onClick={() => openRow(r.application_id)} className="cursor-pointer transition-colors hover:bg-elevated">
                    <td className="px-5 py-3 font-medium text-ink">{r.candidate_name}</td>
                    <td className="px-5 py-3 text-ink-muted">{r.tier}</td>
                    <td className="px-5 py-3 text-ink-muted">{r.is_unscored ? 'Not scored' : `${r.score_pct}%`}</td>
                    <td className="px-5 py-3 text-xs text-ink-dim">{r.tier_reason}</td>
                  </tr>
                  {openId === r.application_id && (
                    <tr>
                      <td colSpan={4} className="bg-surface-2 px-5 py-4">
                        {detailError ? (
                          <div className="text-sm text-danger">{detailError}</div>
                        ) : !detail ? (
                          <div className="flex items-center gap-2 text-sm text-ink-dim">
                            <Loader2 className="h-4 w-4 animate-spin" /> Loading…
                          </div>
                        ) : (
                          <div>
                            <p className="mt-0 text-sm text-ink">{detail.verdict}</p>
                            {detail.strengths && detail.strengths.length > 0 && (
                              <>
                                <strong className="mt-3 block text-xs font-semibold uppercase tracking-wide text-ink-dim">
                                  Strengths
                                </strong>
                                <ul className="mt-1 list-disc pl-5 text-sm text-ink-muted">
                                  {detail.strengths.map((s, i) => (
                                    <li key={i}>{String(s)}</li>
                                  ))}
                                </ul>
                              </>
                            )}
                            {detail.gaps && detail.gaps.length > 0 && (
                              <>
                                <strong className="mt-3 block text-xs font-semibold uppercase tracking-wide text-ink-dim">
                                  Gaps
                                </strong>
                                <ul className="mt-1 list-disc pl-5 text-sm text-ink-muted">
                                  {detail.gaps.map((g, i) => (
                                    <li key={i}>{String(g)}</li>
                                  ))}
                                </ul>
                              </>
                            )}
                            <p className="mt-3 flex items-center gap-1.5 text-xs text-ink-dim">
                              <FileSearch className="h-3.5 w-3.5" />
                              Screened by Nugget's engine, rubric v{detail.rubric_version}, model {detail.model}.
                            </p>
                          </div>
                        )}
                      </td>
                    </tr>
                  )}
                </Fragment>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {rowsLoaded && rows.length > 0 && (
        <div className="mt-4 flex items-center justify-between text-sm text-ink-dim">
          <span>
            Showing {rows.length} of {total}
          </span>
          {rows.length < total && (
            <button type="button" onClick={loadMore} disabled={loadingMore} className="btn btn-ghost h-8 text-sm">
              {loadingMore ? <Loader2 className="h-4 w-4 animate-spin" /> : <ChevronDown className="h-4 w-4" />}
              {loadingMore ? 'Loading…' : 'Load more'}
            </button>
          )}
        </div>
      )}
    </div>
  )
}
