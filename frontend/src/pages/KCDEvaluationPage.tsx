import { useEffect, useMemo, useRef, useState } from 'react'
import { AlertTriangle, Loader2 } from 'lucide-react'
import { Spinner } from '../components/Spinner'
import { ApiError, api } from '../lib/api'
import type {
  CVScreenApplication,
  KCDCohort,
  KCDEvaluation,
  KCDFramework,
  JobItem,
} from '../lib/types'

// 🔒 "KCD" is an internal name. This page is behind staff SSO, so it uses it;
// anything that leaves the team says "case study"
// (memory/feedback_terminology.md, Ayesha 2026-04-02).

const GENERIC_LOAD_ERROR = 'Could not load evaluations. Try reloading the page.'

const VERDICT_LABEL: Record<string, string> = {
  strong_hire: 'Strong hire',
  hire: 'Hire',
  conditional: 'Conditional',
  borderline: 'Borderline',
  not_recommended: 'Not recommended',
}

const VERDICT_CLASS: Record<string, string> = {
  strong_hire: 'bg-success/10 text-success border-success/30',
  hire: 'bg-success/10 text-success border-success/30',
  conditional: 'bg-warning/10 text-warning border-warning/30',
  borderline: 'bg-warning/10 text-warning border-warning/30',
  not_recommended: 'bg-ink-dim/10 text-ink-dim border-hairline',
}

function VerdictBadge({ verdict }: { verdict: string }) {
  return (
    <span
      className={`inline-block rounded-full border px-2.5 py-0.5 text-xs font-semibold ${
        VERDICT_CLASS[verdict] ?? 'border-hairline text-ink-dim'
      }`}
    >
      {VERDICT_LABEL[verdict] ?? verdict}
    </span>
  )
}

export function KCDEvaluationPage() {
  const [framework, setFramework] = useState<KCDFramework | null>(null)
  const [jobs, setJobs] = useState<JobItem[]>([])
  const [jobId, setJobId] = useState<number | null>(null)
  const [cohort, setCohort] = useState<KCDCohort | null>(null)
  const [applications, setApplications] = useState<CVScreenApplication[]>([])
  const [loaded, setLoaded] = useState(false)
  const [loadError, setLoadError] = useState<string | null>(null)

  const [formOpen, setFormOpen] = useState(false)
  const genRef = useRef(0)

  useEffect(() => {
    Promise.all([api.kcdFramework(), api.cvScreenJobs()])
      .then(([f, j]) => {
        setFramework(f)
        setJobs(j)
        if (j.length && jobId === null) setJobId(j[0].job_pk)
      })
      .catch(() => setLoadError(GENERIC_LOAD_ERROR))
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  const reload = (id: number, gen: number) =>
    Promise.all([api.kcdCohort(id), api.cvScreenApplications(id)]).then(([c, a]) => {
      if (genRef.current !== gen) return
      setCohort(c)
      setApplications(a)
      setLoadError(null)
      setLoaded(true)
    })

  useEffect(() => {
    if (jobId === null) return
    const gen = ++genRef.current
    setLoaded(false)
    setFormOpen(false)
    reload(jobId, gen).catch(() => {
      if (genRef.current !== gen) return
      setLoadError(GENERIC_LOAD_ERROR)
      setLoaded(true)
    })
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [jobId])

  const evaluated = useMemo(
    () =>
      new Set(
        [...(cohort?.ranked ?? []), ...(cohort?.incomplete ?? [])].map(
          (e) => e.application_id,
        ),
      ),
    [cohort],
  )

  return (
    <div className="mx-auto max-w-7xl px-8 py-7">
      <header className="mb-5">
        <h1 className="font-display text-2xl font-bold text-ink">KCD Evaluation</h1>
        <p className="mt-1 text-sm text-ink-muted">
          Knowledge, Capacity and Design, scored by a person with the rules enforced. Read the
          assignment, the datasets and the answer key before opening a single submission.
        </p>
      </header>

      {loadError && <p className="text-sm text-danger">{loadError}</p>}

      {jobs.length > 0 && (
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

      {cohort && framework && (
        <p className="mt-4 text-sm text-ink-muted">
          <span className="font-semibold text-ink">{cohort.advancing}</span> of{' '}
          {cohort.ranked.length} complete submission{cohort.ranked.length === 1 ? '' : 's'} reach
          the {cohort.gwc_threshold}% mark that advances to GWC.
        </p>
      )}

      {!loaded ? (
        jobId !== null && (
          <div className="mt-5">
            <Spinner label="Loading…" />
          </div>
        )
      ) : (
        <>
          {framework && (
            <div className="mt-5">
              <button
                type="button"
                className="btn-secondary text-xs"
                onClick={() => setFormOpen((o) => !o)}
              >
                {formOpen ? 'Close' : 'Evaluate a submission'}
              </button>
            </div>
          )}

          {formOpen && framework && jobId !== null && (
            <EvaluationForm
              framework={framework}
              applications={applications.filter((a) => !evaluated.has(a.application_id))}
              alreadyEvaluated={applications.filter((a) => evaluated.has(a.application_id))}
              onSaved={() => {
                setFormOpen(false)
                reload(jobId, genRef.current).catch(() => setLoadError(GENERIC_LOAD_ERROR))
              }}
            />
          )}

          {cohort && (
            <>
              <CohortTable title="Ranked" rows={cohort.ranked} threshold={cohort.gwc_threshold} />

              {cohort.incomplete.length > 0 && (
                <>
                  {/* A separate section, never merged into the ranking: the SOP
                      forbids ranking an incomplete submission above a complete
                      one, whatever the numbers say. */}
                  <div className="mt-6 flex gap-2.5 rounded-xl border border-warning/30 bg-warning/5 px-4 py-3 text-sm text-ink-muted">
                    <AlertTriangle className="mt-0.5 h-4 w-4 shrink-0 text-warning" />
                    <p>{cohort.note}</p>
                  </div>
                  <CohortTable
                    title="Incomplete submissions, not ranked"
                    rows={cohort.incomplete}
                    threshold={cohort.gwc_threshold}
                  />
                </>
              )}
            </>
          )}
        </>
      )}
    </div>
  )
}

function CohortTable({
  title,
  rows,
  threshold,
}: {
  title: string
  rows: KCDEvaluation[]
  threshold: number
}) {
  if (rows.length === 0) {
    return (
      <div className="mt-5">
        <h2 className="font-display text-sm font-bold text-ink">{title}</h2>
        <p className="mt-1 text-sm text-ink-dim">Nothing evaluated yet.</p>
      </div>
    )
  }
  return (
    <div className="mt-5">
      <h2 className="mb-2 font-display text-sm font-bold text-ink">{title}</h2>
      <div className="overflow-hidden rounded-2xl border border-hairline bg-surface">
        <table className="w-full text-sm">
          <thead className="border-b border-hairline bg-elevated text-left text-xs uppercase tracking-wide text-ink-dim">
            <tr>
              <th className="px-4 py-2.5 font-semibold">Candidate</th>
              <th className="px-4 py-2.5 text-right font-semibold">Score</th>
              <th className="px-4 py-2.5 font-semibold">Verdict</th>
              <th className="px-4 py-2.5 font-semibold">GWC</th>
              <th className="px-4 py-2.5 font-semibold">Second read</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((e) => (
              <tr key={e.id} className="border-b border-hairline/60 last:border-0 align-top">
                <td className="px-4 py-2.5">
                  <div className="font-medium text-ink">{e.candidate_name}</div>
                  <div className="text-xs text-ink-dim">app {e.application_id}</div>
                  {e.condition && (
                    <div className="mt-1 text-xs text-warning">
                      Condition: {e.condition}
                    </div>
                  )}
                </td>
                <td className="px-4 py-2.5 text-right tabular-nums text-ink">
                  {/* An incomplete score is never shown as a bare number. */}
                  {e.display_score ? (
                    <span className="text-xs text-ink-muted">{e.display_score}</span>
                  ) : (
                    `${e.total}%`
                  )}
                </td>
                <td className="px-4 py-2.5">
                  <VerdictBadge verdict={e.verdict} />
                </td>
                <td className="px-4 py-2.5 text-xs">
                  {e.incomplete ? (
                    <span className="text-ink-dim">not ranked</span>
                  ) : e.advances_to_gwc ? (
                    <span className="text-success">advances ({threshold}%+)</span>
                  ) : (
                    <span className="text-ink-dim">below {threshold}%</span>
                  )}
                </td>
                <td className="px-4 py-2.5 text-xs text-ink-muted">
                  {e.cross_check?.status === 'not_available' ? (
                    <span className="text-ink-dim">—</span>
                  ) : (
                    <span
                      className={
                        e.cross_check?.status === 'divergent' ? 'text-danger' : undefined
                      }
                    >
                      {e.second_evaluator}: {e.second_total}% ({e.cross_check?.delta} apart)
                    </span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

function EvaluationForm({
  framework,
  applications,
  alreadyEvaluated,
  onSaved,
}: {
  framework: KCDFramework
  applications: CVScreenApplication[]
  alreadyEvaluated: CVScreenApplication[]
  onSaved: () => void
}) {
  const all = [...applications, ...alreadyEvaluated]
  const [applicationId, setApplicationId] = useState<number | null>(all[0]?.application_id ?? null)
  const [scores, setScores] = useState<Record<string, number>>(
    Object.fromEntries(framework.dimensions.map((d) => [d.key, 3])),
  )
  const [evidence, setEvidence] = useState<Record<string, string>>(
    Object.fromEntries(framework.dimensions.map((d) => [d.key, ''])),
  )
  const [caps, setCaps] = useState<Record<string, string[]>>({
    insight_without_evidence: [],
    evidence_without_interpretation: [],
  })
  const [condition, setCondition] = useState('')
  const [incomplete, setIncomplete] = useState(false)
  const [secondEvaluator, setSecondEvaluator] = useState('')
  const [secondTotal, setSecondTotal] = useState('')
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // A PREVIEW only. The server recomputes from the same rules and its answer
  // is the one that is stored, so a drift here can never change a record.
  const preview = useMemo(() => {
    const capped = { ...scores }
    for (const key of caps.insight_without_evidence)
      capped[key] = Math.min(capped[key], framework.cap_insight_without_evidence)
    for (const key of caps.evidence_without_interpretation)
      capped[key] = Math.min(capped[key], framework.cap_evidence_without_interpretation)
    const total = framework.dimensions.reduce(
      (sum, d) => sum + (capped[d.key] / 5) * d.weight,
      0,
    )
    const verdict =
      total >= 85 ? 'strong_hire'
        : total >= 70 ? 'hire'
          : total >= 55 ? 'conditional'
            : total >= 40 ? 'borderline'
              : 'not_recommended'
    return { total: Math.round(total * 100) / 100, verdict }
  }, [scores, caps, framework])

  const toggleCap = (rule: string, key: string) =>
    setCaps((c) => ({
      ...c,
      [rule]: c[rule].includes(key) ? c[rule].filter((k) => k !== key) : [...c[rule], key],
    }))

  const save = () => {
    if (applicationId === null || saving) return
    setSaving(true)
    setError(null)
    api
      .kcdEvaluate({
        application_id: applicationId,
        scores,
        evidence,
        caps: {
          insight_without_evidence: caps.insight_without_evidence,
          evidence_without_interpretation: caps.evidence_without_interpretation,
        },
        condition: condition.trim() || null,
        incomplete,
        second_evaluator: secondEvaluator.trim() || null,
        second_total: secondTotal.trim() ? Number(secondTotal) : null,
      })
      .then(onSaved)
      .catch((e) => {
        // The API's refusals are written to be read ("a CONDITIONAL verdict
        // must state its condition"), so show them rather than a generic line.
        setError(
          e instanceof ApiError ? e.message.replace(/^\d+:\s*/, '') : 'Could not save.',
        )
      })
      .finally(() => setSaving(false))
  }

  return (
    <div className="mt-4 rounded-2xl border border-hairline bg-surface p-5">
      <div className="flex flex-wrap items-end gap-3">
        <label className="text-xs font-semibold text-ink-muted">
          Candidate
          <select
            className="input mt-1 block w-72"
            value={applicationId ?? ''}
            onChange={(e) => setApplicationId(Number(e.target.value))}
          >
            {applications.map((a) => (
              <option key={a.application_id} value={a.application_id}>
                {a.candidate_name}
              </option>
            ))}
            {alreadyEvaluated.map((a) => (
              <option key={a.application_id} value={a.application_id}>
                {a.candidate_name} (re-evaluate)
              </option>
            ))}
          </select>
        </label>

        <label className="flex items-center gap-2 pb-2 text-xs text-ink-muted">
          <input
            type="checkbox"
            checked={incomplete}
            onChange={(e) => setIncomplete(e.target.checked)}
          />
          Incomplete submission (listed separately, never ranked)
        </label>
      </div>

      <div className="mt-4 space-y-4">
        {framework.dimensions.map((d) => (
          <div key={d.key} className="rounded-xl border border-hairline bg-elevated/40 p-3">
            <div className="flex flex-wrap items-baseline justify-between gap-2">
              <div>
                <span className="text-sm font-semibold text-ink">{d.label}</span>{' '}
                <span className="text-xs text-ink-dim">weight {d.weight}</span>
                <p className="text-xs text-ink-muted">{d.asks}</p>
              </div>
              <select
                className="input w-28"
                value={scores[d.key]}
                onChange={(e) => setScores((s) => ({ ...s, [d.key]: Number(e.target.value) }))}
              >
                {/* 0 is offered because the scale has a real zero. A form that
                    only went down to 1 would put the floor back however
                    careful the service is. */}
                {framework.scores.map((v) => (
                  <option key={v} value={v}>
                    {v.toFixed(1)}
                  </option>
                ))}
              </select>
            </div>

            <textarea
              className="input mt-2 min-h-[56px] w-full text-xs"
              placeholder="What in the submission puts it there? Quote the line or name the exercise."
              value={evidence[d.key]}
              onChange={(e) => setEvidence((v) => ({ ...v, [d.key]: e.target.value }))}
            />

            <div className="mt-2 flex flex-wrap gap-4 text-xs text-ink-muted">
              <label className="flex items-center gap-1.5">
                <input
                  type="checkbox"
                  checked={caps.insight_without_evidence.includes(d.key)}
                  onChange={() => toggleCap('insight_without_evidence', d.key)}
                />
                Insight without evidence (caps at {framework.cap_insight_without_evidence})
              </label>
              <label className="flex items-center gap-1.5">
                <input
                  type="checkbox"
                  checked={caps.evidence_without_interpretation.includes(d.key)}
                  onChange={() => toggleCap('evidence_without_interpretation', d.key)}
                />
                Evidence without interpretation (caps at{' '}
                {framework.cap_evidence_without_interpretation})
              </label>
            </div>
          </div>
        ))}
      </div>

      <div className="mt-4 flex flex-wrap items-end gap-3">
        <label className="text-xs font-semibold text-ink-muted">
          Second reader
          <input
            className="input mt-1 block w-40"
            value={secondEvaluator}
            onChange={(e) => setSecondEvaluator(e.target.value)}
            placeholder="optional"
          />
        </label>
        <label className="text-xs font-semibold text-ink-muted">
          Their total %
          <input
            className="input mt-1 block w-28"
            value={secondTotal}
            onChange={(e) => setSecondTotal(e.target.value)}
            placeholder="optional"
          />
        </label>
      </div>

      <div className="mt-4 rounded-xl border border-hairline bg-elevated/40 p-3 text-sm">
        <span className="text-ink-muted">Preview: </span>
        <span className="font-semibold tabular-nums text-ink">{preview.total}%</span>{' '}
        <VerdictBadge verdict={preview.verdict} />
        <span className="ml-2 text-xs text-ink-dim">
          the server recomputes this from the same rules
        </span>
      </div>

      {preview.verdict === 'conditional' && (
        <label className="mt-3 block text-xs font-semibold text-ink-muted">
          Condition (required for a conditional verdict)
          <textarea
            className="input mt-1 min-h-[48px] w-full text-xs"
            placeholder="What specifically would have to be true? A conditional with no condition is not actionable."
            value={condition}
            onChange={(e) => setCondition(e.target.value)}
          />
        </label>
      )}

      {error && <p className="mt-3 text-sm text-danger">{error}</p>}

      <div className="mt-4">
        <button type="button" className="btn-primary text-sm" disabled={saving} onClick={save}>
          {saving ? (
            <span className="flex items-center gap-1.5">
              <Loader2 className="h-4 w-4 animate-spin" /> Saving…
            </span>
          ) : (
            'Save evaluation'
          )}
        </button>
      </div>
    </div>
  )
}
