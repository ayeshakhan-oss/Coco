import { Fragment, useEffect, useRef, useState } from 'react'
import { api } from '../lib/api'
import type { EvaluationDetail, EvaluationRow, EvaluationSummary, ScreenedJob } from '../lib/types'

const GENERIC_LOAD_ERROR = 'Could not load screening results. Try reloading the page.'

export function EvaluationPage() {
  const [jobs, setJobs] = useState<ScreenedJob[]>([])
  const [jobsLoaded, setJobsLoaded] = useState(false)
  const [jobsError, setJobsError] = useState<string | null>(null)
  const [jobId, setJobId] = useState<number | null>(null)
  const [summary, setSummary] = useState<EvaluationSummary | null>(null)
  const [summaryError, setSummaryError] = useState<string | null>(null)
  const [rows, setRows] = useState<EvaluationRow[]>([])
  const [rowsLoaded, setRowsLoaded] = useState(false)
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
    setSummaryError(null)
    setCandidatesError(null)
    setRowsLoaded(false)
    api
      .evaluationSummary(jobId)
      .then(setSummary)
      .catch(() => setSummaryError(GENERIC_LOAD_ERROR))
    api
      .evaluationCandidates(jobId, tier)
      .then((r) => {
        setRows(r)
        setRowsLoaded(true)
      })
      .catch(() => {
        setCandidatesError(GENERIC_LOAD_ERROR)
        setRowsLoaded(true)
      })
  }, [jobId, tier])

  // Copy for a tier whose score is suppressed. UNUSABLE means the CV never
  // opened; MANUAL_REVIEW means it opened but fell below the rubric's
  // readability floor. Both need a human on the document, neither is a 0%.
  const unscoredLabel = (isUnusable: boolean) =>
    isUnusable ? 'CV could not be read, needs a human' : 'Below the readability floor, needs a human'

  return (
    <div style={{ padding: 24 }}>
      <h1>Candidate Evaluation</h1>
      <p style={{ color: '#555' }}>
        Technical screening results produced by Nugget's screening engine. Read only.
      </p>

      {jobsError ? (
        <p style={{ color: '#9a3412' }}>{jobsError}</p>
      ) : jobsLoaded && jobs.length === 0 ? (
        <p style={{ color: '#555' }}>No screened jobs found.</p>
      ) : (
        <select
          value={jobId ?? ''}
          onChange={(e) => {
            setJobId(Number(e.target.value))
            setTier(undefined)
          }}
        >
          {jobs.map((j) => (
            <option key={j.job_id} value={j.job_id}>
              {j.job_title ?? `Job ${j.job_id}`} (rubric v{j.rubric_version})
            </option>
          ))}
        </select>
      )}

      {summaryError ? (
        <p style={{ color: '#9a3412', margin: '16px 0' }}>{summaryError}</p>
      ) : (
        summary && (
          <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap', margin: '16px 0' }}>
            {summary.tiers.map((t) => (
              <button
                key={t.tier}
                onClick={() => setTier(tier === t.tier ? undefined : t.tier)}
                style={{
                  padding: 12,
                  minWidth: 140,
                  textAlign: 'left',
                  border: tier === t.tier ? '2px solid #2f4fa2' : '1px solid #ddd',
                  background: t.is_unscored ? '#fff7ed' : '#fff',
                  cursor: 'pointer',
                }}
              >
                <div style={{ fontWeight: 700 }}>{t.tier}</div>
                <div>{t.n}</div>
                {t.is_unscored ? (
                  <div style={{ fontSize: 12, color: '#9a3412' }}>{unscoredLabel(t.is_unusable)}</div>
                ) : (
                  t.avg_pct !== null && <div style={{ fontSize: 12, color: '#555' }}>avg {t.avg_pct}%</div>
                )}
              </button>
            ))}
          </div>
        )
      )}

      {candidatesError ? (
        <p style={{ color: '#9a3412' }}>{candidatesError}</p>
      ) : rowsLoaded && rows.length === 0 ? (
        <p style={{ color: '#555' }}>No candidates in this tier.</p>
      ) : (
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr>
              <th style={{ textAlign: 'left' }}>Candidate</th>
              <th style={{ textAlign: 'left' }}>Tier</th>
              <th style={{ textAlign: 'left' }}>Score</th>
              <th style={{ textAlign: 'left' }}>Why</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((r) => (
              <Fragment key={r.application_id ?? r.candidate_email}>
                <tr
                  onClick={() => openRow(r.application_id)}
                  style={{ borderTop: '1px solid #eee', cursor: 'pointer' }}
                >
                  <td>{r.candidate_name}</td>
                  <td>{r.tier}</td>
                  <td>{r.is_unscored ? 'Not scored' : `${r.score_pct}%`}</td>
                  <td style={{ fontSize: 13, color: '#555' }}>{r.tier_reason}</td>
                </tr>
                {openId === r.application_id && (
                  <tr>
                    <td colSpan={4} style={{ background: '#fafafa', padding: 16 }}>
                      {detailError ? (
                        <div style={{ color: '#9a3412' }}>{detailError}</div>
                      ) : !detail ? (
                        <div>Loading...</div>
                      ) : (
                        <div>
                          <p style={{ marginTop: 0 }}>{detail.verdict}</p>
                          {detail.strengths && detail.strengths.length > 0 && (
                            <>
                              <strong>Strengths</strong>
                              <ul>
                                {detail.strengths.map((s, i) => (
                                  <li key={i}>{String(s)}</li>
                                ))}
                              </ul>
                            </>
                          )}
                          {detail.gaps && detail.gaps.length > 0 && (
                            <>
                              <strong>Gaps</strong>
                              <ul>
                                {detail.gaps.map((g, i) => (
                                  <li key={i}>{String(g)}</li>
                                ))}
                              </ul>
                            </>
                          )}
                          <p style={{ fontSize: 12, color: '#777' }}>
                            Screened by Nugget's engine, rubric v{detail.rubric_version}, model{' '}
                            {detail.model}.
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
  )
}
