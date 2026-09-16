import { Fragment, useEffect, useState } from 'react'
import { api } from '../lib/api'
import type { EvaluationDetail, EvaluationRow, EvaluationSummary, ScreenedJob } from '../lib/types'

export function EvaluationPage() {
  const [jobs, setJobs] = useState<ScreenedJob[]>([])
  const [jobId, setJobId] = useState<number | null>(null)
  const [summary, setSummary] = useState<EvaluationSummary | null>(null)
  const [rows, setRows] = useState<EvaluationRow[]>([])
  const [tier, setTier] = useState<string | undefined>(undefined)
  const [openId, setOpenId] = useState<number | null>(null)
  const [detail, setDetail] = useState<EvaluationDetail | null>(null)

  const openRow = (applicationId: number | null) => {
    if (applicationId === null) return
    if (openId === applicationId) {
      setOpenId(null)
      setDetail(null)
      return
    }
    setOpenId(applicationId)
    setDetail(null)
    api.evaluationDetail(applicationId).then(setDetail)
  }

  useEffect(() => {
    api.evaluationJobs().then((j) => {
      setJobs(j)
      if (j.length && jobId === null) setJobId(j[0].job_id)
    })
  }, [])

  useEffect(() => {
    if (jobId === null) return
    api.evaluationSummary(jobId).then(setSummary)
    api.evaluationCandidates(jobId, tier).then(setRows)
  }, [jobId, tier])

  return (
    <div style={{ padding: 24 }}>
      <h1>Candidate Evaluation</h1>
      <p style={{ color: '#555' }}>
        Technical screening results produced by Nugget's screening engine. Read only.
      </p>

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

      {summary && (
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
                background: t.is_unusable ? '#fff7ed' : '#fff',
                cursor: 'pointer',
              }}
            >
              <div style={{ fontWeight: 700 }}>{t.tier}</div>
              <div>{t.n}</div>
              {t.is_unusable ? (
                <div style={{ fontSize: 12, color: '#9a3412' }}>CV could not be read, needs a human</div>
              ) : (
                t.avg_pct !== null && <div style={{ fontSize: 12, color: '#555' }}>avg {t.avg_pct}%</div>
              )}
            </button>
          ))}
        </div>
      )}

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
                <td>{r.is_unusable ? 'Not scored' : `${r.score_pct}%`}</td>
                <td style={{ fontSize: 13, color: '#555' }}>{r.tier_reason}</td>
              </tr>
              {openId === r.application_id && (
                <tr>
                  <td colSpan={4} style={{ background: '#fafafa', padding: 16 }}>
                    {!detail ? (
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
    </div>
  )
}
