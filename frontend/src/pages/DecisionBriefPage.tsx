import { useEffect, useRef, useState } from 'react'
import { AlertTriangle, ExternalLink, Info } from 'lucide-react'
import { Spinner } from '../components/Spinner'
import { api } from '../lib/api'
import type { DecisionBrief, DecisionBriefPerson, JobItem } from '../lib/types'

const GENERIC_LOAD_ERROR = 'Could not load the decision brief. Try reloading the page.'

// The SOP's four labels plus the one it does not have. "No debrief recorded"
// is a statement about our records; "Overdue" is a claim about the candidate,
// and the two must not look alike.
const VERDICT_CLASS: Record<string, string> = {
  'PANEL DECISION': 'bg-success/10 text-success border-success/30',
  'DEBRIEF CONFIRMED': 'bg-success/10 text-success border-success/30',
  'DEBRIEF SCHEDULED': 'bg-blurple/10 text-blurple border-blurple/30',
  OVERDUE: 'bg-danger/10 text-danger border-danger/30',
  'NO DEBRIEF RECORDED': 'bg-ink-dim/10 text-ink-dim border-hairline',
}

function Verdict({ label }: { label: string }) {
  return (
    <span
      className={`inline-block rounded-full border px-2 py-0.5 text-[11px] font-semibold ${
        VERDICT_CLASS[label] ?? 'border-hairline text-ink-dim'
      }`}
    >
      {label}
    </span>
  )
}

// Every candidate name is a link to their CV. The SOP calls this
// non-negotiable; the app serves it from Markaz so no manual Drive upload
// stands in the way.
function CandidateName({ p }: { p: DecisionBriefPerson }) {
  if (!p.has_cv) {
    return (
      <span className="font-medium text-ink">
        {p.name}{' '}
        <span className="text-xs font-normal text-warning">(no CV on file)</span>
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

function Evidence({ p }: { p: DecisionBriefPerson }) {
  const bits: string[] = []
  if (p.cv_screen_match != null) bits.push(`CV screen ${p.cv_screen_match}%`)
  if (p.case_study_total != null) bits.push(`case study ${p.case_study_total}`)
  else if (p.submitted_case_study) bits.push('case study submitted, not scored')
  return <span className="text-xs text-ink-muted">{bits.join(' · ') || '—'}</span>
}

export function DecisionBriefPage() {
  const [jobs, setJobs] = useState<JobItem[]>([])
  const [jobId, setJobId] = useState<number | null>(null)
  const [brief, setBrief] = useState<DecisionBrief | null>(null)
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
      .decisionBrief(jobId)
      .then((b) => {
        if (genRef.current !== gen) return
        setBrief(b)
        setError(null)
        setLoaded(true)
      })
      .catch(() => {
        if (genRef.current !== gen) return
        setError(GENERIC_LOAD_ERROR)
        setLoaded(true)
      })
  }, [jobId])

  return (
    <div className="mx-auto max-w-7xl px-8 py-7">
      <header className="mb-5">
        <h1 className="font-display text-2xl font-bold text-ink">Decision Brief</h1>
        <p className="mt-1 text-sm text-ink-muted">
          Where every candidate on a position stands, with each name linked to their CV.
          Read only.
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
      ) : brief ? (
        <>
          <div className="mt-5 grid grid-cols-2 gap-3 lg:grid-cols-4">
            {brief.stat_boxes.map((b) => (
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

          {/* What is missing is stated, not left as blanks for a reader to
              interpret as a negative finding. */}
          <div className="mt-3 flex gap-2.5 rounded-xl border border-hairline bg-surface px-4 py-3 text-sm text-ink-muted">
            <Info className="mt-0.5 h-4 w-4 shrink-0 text-ink-dim" />
            <div>
              <p>{brief.evidence_caveat}</p>
              <p className="mt-1 text-xs">
                Not on record for this position: {brief.not_recorded.debrief_verdicts} debrief
                verdicts, {brief.not_recorded.case_study_scores} case-study scores,{' '}
                {brief.not_recorded.missing_cv} CVs.
              </p>
            </div>
          </div>

          <h2 className="mt-6 font-display text-sm font-bold text-ink">
            Leading <span className="font-normal text-ink-dim">({brief.leading.length})</span>
          </h2>
          {brief.leading_note && (
            <div className="mt-1 flex gap-2 rounded-xl border border-warning/30 bg-warning/5 px-3 py-2 text-xs text-ink-muted">
              <AlertTriangle className="mt-0.5 h-3.5 w-3.5 shrink-0 text-warning" />
              <p>{brief.leading_note}</p>
            </div>
          )}
          {brief.leading.length === 0 ? (
            <p className="mt-1 text-sm text-ink-dim">
              Nobody has both passed values and submitted a case study yet.
            </p>
          ) : (
            <div className="mt-2 overflow-hidden rounded-2xl border border-hairline bg-surface">
              <table className="w-full text-sm">
                <tbody>
                  {brief.leading.map((p) => (
                    <tr key={p.application_id} className="border-b border-hairline/60 last:border-0">
                      <td className="px-4 py-2.5">
                        <CandidateName p={p} />
                        {p.values_comments && (
                          <div className="mt-0.5 line-clamp-2 text-xs text-ink-muted">
                            {p.values_comments}
                          </div>
                        )}
                      </td>
                      <td className="px-4 py-2.5">
                        <Evidence p={p} />
                      </td>
                      <td className="px-4 py-2.5 text-right">
                        <Verdict label={p.debrief_verdict} />
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {brief.groups.map((g) => (
            <div key={g.key} className="mt-6">
              <h2 className="font-display text-sm font-bold text-ink">
                {g.title} <span className="font-normal text-ink-dim">({g.people.length})</span>
              </h2>
              {g.people.length === 0 ? (
                <p className="mt-1 text-sm text-ink-dim">Nobody.</p>
              ) : (
                <div className="mt-2 overflow-hidden rounded-2xl border border-hairline bg-surface">
                  <table className="w-full text-sm">
                    <tbody>
                      {g.people.slice(0, 40).map((p) => (
                        <tr
                          key={p.application_id}
                          className="border-b border-hairline/60 last:border-0"
                        >
                          <td className="px-4 py-2">
                            <CandidateName p={p} />
                            {p.values_disagreement && (
                              <div className="mt-0.5 text-xs text-warning">
                                {p.values_disagreement}
                              </div>
                            )}
                          </td>
                          <td className="px-4 py-2">
                            <Evidence p={p} />
                          </td>
                          <td className="px-4 py-2 text-right text-xs text-ink-dim">
                            {p.status}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                  {g.people.length > 40 && (
                    <div className="border-t border-hairline px-4 py-2 text-xs text-ink-dim">
                      Showing the first 40 of {g.people.length}.
                    </div>
                  )}
                </div>
              )}
            </div>
          ))}

          {brief.debrief_schedule.length > 0 && (
            <div className="mt-6">
              <h2 className="font-display text-sm font-bold text-ink">Debrief schedule</h2>
              <ul className="mt-2 space-y-1 text-sm text-ink-muted">
                {brief.debrief_schedule.map((p) => (
                  <li key={p.application_id}>
                    <CandidateName p={p} /> — {p.debrief_date}
                  </li>
                ))}
              </ul>
            </div>
          )}

          <p className="mt-6 text-xs text-ink-dim">Generated {brief.generated_on}.</p>
        </>
      ) : null}
    </div>
  )
}
