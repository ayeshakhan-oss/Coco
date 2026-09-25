import { useEffect, useRef, useState } from 'react'
import { AlertTriangle, ArrowLeft, Check, Loader2, Search } from 'lucide-react'
import { Spinner } from '../components/Spinner'
import { formatDate } from '../lib/format'
import { ApiError, api } from '../lib/api'
import { runScreenAll } from '../lib/screenAll'
import type {
  TechJob,
  TechModel,
  TechPlan,
  TechRubricStep,
  TechRun,
  TechWork,
} from '../lib/types'

// The technical screening wizard: a jobs list, then pick the job, review the
// rubric, check the pool and cost, confirm, and watch the run.
//
// 🔒 THIS IS NOT CV SCREENING. That is /cv-screening, a separate skill with
// Coco's own criteria and shortlist/maybe/no_hire tiers. This one uses Nugget's
// weighted rubric and tiers P1-P4 / MANUAL_REVIEW / UNUSABLE, and a score from
// one means nothing in the other's vocabulary. The two never merge (Ayesha,
// non-negotiable, CLAUDE.md Rule 33), which is why this file shares no type,
// no component and no helper with CVScreeningPage.
//
// The four steps exist so that nothing is spent before a person has seen what
// will be spent and what everyone will be judged against. Drafting a rubric
// writes nothing; publishing it is its own deliberate call.

const STEPS = ['Pick the job', 'Review the rubric', 'Check the pool and cost', 'Confirm'] as const
type Step = 0 | 1 | 2 | 3

const GENERIC_ERROR = 'Could not load technical screening. Try reloading the page.'

// Modes the server accepts. `single` and `window` are driven by the fields
// below rather than being offered as bare names nobody could interpret.
const MODES: { value: string; label: string; help: string }[] = [
  {
    value: 'new_only',
    label: 'Not yet screened',
    help: 'Everyone on this job without a current score. The usual choice.',
  },
  {
    value: 'backlog',
    label: 'Whole backlog',
    help: 'Every application on the job, including ones already scored under an older rubric.',
  },
  {
    value: 'rescore',
    label: 'Re-score everyone',
    help: 'Score every applicant again under the current rubric. Earlier scores are superseded, not deleted.',
  },
]

function money(n: number | null | undefined): string {
  if (n === null || n === undefined) return '—'
  return n < 0.01 && n > 0 ? '<$0.01' : `$${n.toFixed(2)}`
}

function errorText(e: unknown, fallback: string): string {
  if (e instanceof ApiError && typeof e.message === 'string') {
    return e.message.replace(/^\d+:\s*/, '')
  }
  return fallback
}

// Dates go through the shared helper, which renders "Jul 8, 2026" rather than
// a bare toLocaleDateString(): "7/8/2026" is read as 7 August by half the
// people who will open this page.

export function TechScreeningPage() {
  const [step, setStep] = useState<Step>(0)

  const [jobs, setJobs] = useState<TechJob[]>([])
  const [jobsLoaded, setJobsLoaded] = useState(false)
  const [jobsError, setJobsError] = useState<string | null>(null)
  const [query, setQuery] = useState('')

  const [job, setJob] = useState<TechJob | null>(null)
  const [models, setModels] = useState<TechModel[]>([])

  useEffect(() => {
    Promise.all([api.techJobs(), api.techModels()])
      .then(([j, m]) => {
        setJobs(j)
        setModels(m)
        setJobsLoaded(true)
        setJobsError(null)
      })
      .catch(() => {
        setJobsLoaded(true)
        setJobsError(GENERIC_ERROR)
      })
  }, [])

  const openJob = (j: TechJob) => {
    setJob(j)
    setStep(1)
  }

  const backToJobs = () => {
    setJob(null)
    setStep(0)
  }

  const visible = jobs.filter((j) => {
    if (!query.trim()) return true
    const q = query.toLowerCase()
    return (
      (j.title ?? '').toLowerCase().includes(q) ||
      (j.department ?? '').toLowerCase().includes(q) ||
      (j.job_code ?? '').toLowerCase().includes(q)
    )
  })

  return (
    <div className="mx-auto max-w-7xl px-8 py-7">
      <header className="mb-5">
        <h1 className="font-display text-2xl font-bold text-ink">Technical Screening</h1>
        <p className="mt-1 text-sm text-ink-muted">
          Every applicant read against this role's own rubric, tiered P1 to P4. Separate from CV
          Screening, which uses Coco's own criteria and its own tiers. A score from one does not
          mean the same thing as a score from the other.
        </p>
      </header>

      {step === 0 ? (
        <JobsList
          jobs={visible}
          total={jobs.length}
          loaded={jobsLoaded}
          error={jobsError}
          query={query}
          onQuery={setQuery}
          onPick={openJob}
        />
      ) : job ? (
        <Wizard
          key={job.job_pk}
          job={job}
          models={models}
          step={step}
          setStep={setStep}
          onBack={backToJobs}
        />
      ) : null}
    </div>
  )
}

// --- Step 0: the jobs list --------------------------------------------------

function JobsList({
  jobs, total, loaded, error, query, onQuery, onPick,
}: {
  jobs: TechJob[]
  total: number
  loaded: boolean
  error: string | null
  query: string
  onQuery: (q: string) => void
  onPick: (j: TechJob) => void
}) {
  if (error) return <p className="text-sm text-danger">{error}</p>
  if (!loaded) return <Spinner label="Loading positions…" />
  if (total === 0) return <p className="text-sm text-ink-dim">No positions found.</p>

  return (
    <>
      <div className="mb-3 flex items-center justify-between gap-4">
        <p className="text-sm text-ink-muted">
          Scored out of total on each position. Every position ever posted is listed, live first.
        </p>
        <div className="relative">
          <Search className="pointer-events-none absolute left-2.5 top-1/2 h-4 w-4 -translate-y-1/2 text-ink-dim" />
          <input
            className="input w-64 pl-8"
            placeholder="Search positions…"
            value={query}
            onChange={(e) => onQuery(e.target.value)}
          />
        </div>
      </div>

      <div className="overflow-hidden rounded-2xl border border-hairline bg-surface">
        <table className="w-full text-sm">
          <thead className="border-b border-hairline bg-elevated text-left text-xs uppercase tracking-wide text-ink-dim">
            <tr>
              <th className="px-4 py-2.5 font-semibold">Position</th>
              <th className="px-4 py-2.5 text-right font-semibold">Screened</th>
              <th className="px-4 py-2.5 font-semibold">Rubric</th>
              <th className="px-4 py-2.5" />
            </tr>
          </thead>
          <tbody>
            {jobs.map((j) => (
              <tr key={j.job_pk} className="border-b border-hairline/60 last:border-0">
                <td className="px-4 py-2.5">
                  <div className="font-medium text-ink">{j.title}</div>
                  <div className="text-xs text-ink-dim">
                    {j.job_code ?? `Job ${j.job_pk}`}
                    {j.department ? ` · ${j.department}` : ''}
                    {j.job_status && j.job_status !== 'Active' ? ` · ${j.job_status}` : ''}
                  </div>
                </td>
                <td className="px-4 py-2.5 text-right tabular-nums text-ink">
                  {j.scored}
                  <span className="text-ink-dim">/{j.applications}</span>
                </td>
                <td className="px-4 py-2.5 text-xs">
                  {j.has_rubric ? (
                    <span className="text-ink-muted">v{j.rubric_version}</span>
                  ) : (
                    <span className="text-warning">none yet</span>
                  )}
                </td>
                <td className="px-4 py-2.5 text-right">
                  {j.live_run_id ? (
                    <button type="button" className="btn btn-ghost text-xs" onClick={() => onPick(j)}>
                      {j.live_run_status === 'running' ? 'Run in progress' : 'Resume'}
                    </button>
                  ) : (
                    <button type="button" className="btn btn-primary text-xs" onClick={() => onPick(j)}>
                      Screen
                    </button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {jobs.length === 0 && (
        <p className="mt-3 text-sm text-ink-dim">No position matches that search.</p>
      )}
    </>
  )
}

// --- Steps 1 to 4 -----------------------------------------------------------

function Wizard({
  job, models, step, setStep, onBack,
}: {
  job: TechJob
  models: TechModel[]
  step: Step
  setStep: (s: Step) => void
  onBack: () => void
}) {
  // Step 2
  const [rubricStep, setRubricStep] = useState<TechRubricStep | null>(null)
  const [rubricError, setRubricError] = useState<string | null>(null)
  const [draft, setDraft] = useState<Record<string, unknown> | null>(null)
  const [drafting, setDrafting] = useState(false)
  const [publishing, setPublishing] = useState(false)

  // Step 3
  const [mode, setMode] = useState('new_only')
  const [sinceDays, setSinceDays] = useState<number | null>(null)
  const [maxCandidates, setMaxCandidates] = useState<number | null>(null)
  // Derived, not synced in an effect: the default is simply the first model
  // the server offers (cheapest first), and a choice overrides it.
  const [modelChoice, setModelChoice] = useState<string | null>(null)
  const model = modelChoice ?? models[0]?.model ?? ''
  const [useBatch, setUseBatch] = useState(false)
  const [costCap, setCostCap] = useState<number | null>(null)
  const [plan, setPlan] = useState<TechPlan | null>(null)
  const [planning, setPlanning] = useState(false)
  const [planError, setPlanError] = useState<string | null>(null)

  // Step 4
  const [run, setRun] = useState<TechRun | null>(null)
  const [starting, setStarting] = useState(false)
  const [runError, setRunError] = useState<string | null>(null)
  const [progress, setProgress] = useState<
    { done: number; skipped: number; failed: number; retrying: number; retryInSeconds: number } | null
  >(null)
  const [outcome, setOutcome] = useState<
    { kind: 'done' | 'stopped' | 'error'; done: number; skipped: number; failed: number; message?: string } | null
  >(null)
  const stopRef = useRef(false)
  const abandoned = useRef(false)

  useEffect(() => () => { abandoned.current = true }, [])

  useEffect(() => {
    api
      .techRubric(job.job_pk)
      .then((r) => { setRubricStep(r); setRubricError(null) })
      .catch((e) => setRubricError(errorText(e, GENERIC_ERROR)))
  }, [job.job_pk])

  const rubric = rubricStep?.rubric ?? null

  const doDraft = () => {
    setDrafting(true)
    setRubricError(null)
    api
      .techDraftRubric(job.job_pk)
      .then((r) => setDraft(r.draft))
      .catch((e) => setRubricError(errorText(e, 'Could not draft a rubric.')))
      .finally(() => setDrafting(false))
  }

  const doPublish = () => {
    if (!draft) return
    setPublishing(true)
    setRubricError(null)
    api
      .techPublishRubric(job.job_pk, draft)
      .then(() => api.techRubric(job.job_pk))
      .then((r) => { setRubricStep(r); setDraft(null) })
      .catch((e) => setRubricError(errorText(e, 'Could not publish the rubric.')))
      .finally(() => setPublishing(false))
  }

  // Step 3 re-plans whenever anything that changes the pool or the price
  // changes, so the number on Confirm is never stale.
  useEffect(() => {
    if (step !== 2 || !rubric || !model) return
    let live = true
    setPlanning(true)
    setPlanError(null)
    api
      .techPlan({
        job_id: job.job_pk,
        mode,
        since_days: sinceDays,
        max_candidates: maxCandidates,
        model,
        use_batch: useBatch,
      })
      .then((p) => { if (live) setPlan(p) })
      .catch((e) => { if (live) { setPlan(null); setPlanError(errorText(e, 'Could not work out the pool.')) } })
      .finally(() => { if (live) setPlanning(false) })
    return () => { live = false }
  }, [step, rubric, job.job_pk, mode, sinceDays, maxCandidates, model, useBatch])

  const startRun = async () => {
    if (!plan) return
    setStarting(true)
    setRunError(null)
    setOutcome(null)
    stopRef.current = false
    try {
      const created = await api.techCreateRun({
        job_id: job.job_pk,
        mode,
        since_days: sinceDays,
        max_candidates: maxCandidates,
        model,
        use_batch: useBatch,
        cost_cap_usd: costCap,
      })
      const started = await api.techRun(created.run_id)
      setRun(started)
      setProgress({ done: 0, skipped: 0, failed: 0, retrying: 0, retryInSeconds: 0 })
      await drive(created.run_id)
    } catch (e) {
      setRunError(errorText(e, 'Could not start the run.'))
    } finally {
      setStarting(false)
    }
  }

  // The loop. Reuses the tested runner from CV screening's fifty-minute
  // failure: a redeploy costs one slice, not the run. Each candidate commits
  // as it finishes, so stopping loses nothing.
  const drive = async (runId: string) => {
    const result = await runScreenAll<TechWork>({
      runBatch: () => api.techWork(runId, 3),
      shouldStop: () => stopRef.current,
      isAbandoned: () => abandoned.current,
      onBatch: (batch) => { if (batch.run) setRun(batch.run) },
      onProgress: (p) => setProgress(p),
    })
    if (abandoned.current) return
    setProgress(null)
    api.techRun(runId).then(setRun).catch(() => undefined)
    setOutcome({
      kind: result.error ? 'error' : result.stopped ? 'stopped' : 'done',
      done: result.done,
      skipped: result.skipped,
      failed: result.failed,
      message: result.error ?? undefined,
    })
  }

  const resumeExisting = async () => {
    if (!job.live_run_id) return
    setRunError(null)
    setOutcome(null)
    stopRef.current = false
    try {
      setRun(await api.techRun(job.live_run_id))
      setProgress({ done: 0, skipped: 0, failed: 0, retrying: 0, retryInSeconds: 0 })
      await drive(job.live_run_id)
    } catch (e) {
      setRunError(errorText(e, 'Could not resume the run.'))
    }
  }

  const cancel = () => {
    stopRef.current = true
    if (run) api.techCancelRun(run.id).then(setRun).catch(() => undefined)
  }

  return (
    <>
      <button type="button" className="btn btn-ghost mb-4 text-xs" onClick={onBack}>
        <ArrowLeft className="mr-1 inline h-3.5 w-3.5" />
        All positions
      </button>

      <Steps current={step} />

      <div className="mt-5 rounded-2xl border border-hairline bg-surface p-6">
        {step === 1 && (
          <RubricStep
            job={job}
            rubricStep={rubricStep}
            error={rubricError}
            draft={draft}
            drafting={drafting}
            publishing={publishing}
            onDraft={doDraft}
            onPublish={doPublish}
            onDiscard={() => setDraft(null)}
            onContinue={() => setStep(2)}
          />
        )}

        {step === 2 && (
          <PoolStep
            plan={plan}
            planning={planning}
            error={planError}
            models={models}
            mode={mode} setMode={setMode}
            sinceDays={sinceDays} setSinceDays={setSinceDays}
            maxCandidates={maxCandidates} setMaxCandidates={setMaxCandidates}
            model={model} setModel={setModelChoice}
            useBatch={useBatch} setUseBatch={setUseBatch}
            onBack={() => setStep(1)}
            onContinue={() => setStep(3)}
          />
        )}

        {step === 3 && (
          <ConfirmStep
            job={job}
            plan={plan}
            model={model}
            useBatch={useBatch}
            costCap={costCap}
            setCostCap={setCostCap}
            starting={starting}
            run={run}
            progress={progress}
            outcome={outcome}
            error={runError}
            onStart={startRun}
            onResume={resumeExisting}
            onStop={cancel}
            onBack={() => setStep(2)}
          />
        )}
      </div>
    </>
  )
}

function Steps({ current }: { current: Step }) {
  return (
    <div className="flex overflow-hidden rounded-xl border border-hairline">
      {STEPS.map((label, i) => {
        const done = i < current
        const active = i === current
        return (
          <div
            key={label}
            className={`flex-1 border-r border-hairline px-4 py-3 text-sm last:border-r-0 ${
              active
                ? 'bg-blurple/10 font-semibold text-blurple'
                : done
                  ? 'bg-success/5 text-success'
                  : 'bg-elevated text-ink-dim'
            }`}
          >
            {done && <Check className="mr-1.5 inline h-3.5 w-3.5" />}
            {label}
          </div>
        )
      })}
    </div>
  )
}

// --- Step 2: the rubric -----------------------------------------------------

function RubricStep({
  job, rubricStep, error, draft, drafting, publishing,
  onDraft, onPublish, onDiscard, onContinue,
}: {
  job: TechJob
  rubricStep: TechRubricStep | null
  error: string | null
  draft: Record<string, unknown> | null
  drafting: boolean
  publishing: boolean
  onDraft: () => void
  onPublish: () => void
  onDiscard: () => void
  onContinue: () => void
}) {
  const rubric = rubricStep?.rubric ?? null
  const blocked = rubricStep?.blocked_reason ?? null

  return (
    <>
      <h2 className="font-display text-base font-bold text-ink">The rubric</h2>
      <p className="mt-1 text-sm text-ink-muted">
        The rubric decides how every applicant to this role is judged, so it is drafted from the job
        description and read by a person before anything is scored. Publishing freezes it. A later
        change becomes a new version, which leaves earlier scores explainable rather than rewritten.
      </p>

      <div className="mt-4 rounded-xl border border-hairline bg-elevated p-4">
        <div className="font-semibold text-ink">{rubricStep?.job_title ?? job.title}</div>
        <div className="text-xs text-ink-dim">
          {rubricStep?.department ?? job.department ?? 'No department'}
          {rubricStep?.jd_source ? ` · JD from ${rubricStep.jd_source}` : ''}
        </div>
      </div>

      {error && <p className="mt-3 text-sm text-danger">{error}</p>}

      {blocked && (
        <div className="mt-3 rounded-xl border border-danger/30 bg-danger/5 px-4 py-2.5 text-sm text-danger">
          {blocked}
        </div>
      )}

      {!rubricStep ? (
        <div className="mt-4"><Spinner label="Loading the rubric…" /></div>
      ) : rubric && !draft ? (
        <>
          <div className="mt-4 rounded-xl border border-success/30 bg-success/5 px-4 py-3 text-sm text-ink">
            Using published rubric <strong>v{rubric.version}</strong> with{' '}
            {rubric.dimensions.length} dimension{rubric.dimensions.length === 1 ? '' : 's'} and{' '}
            {rubric.max_score} points.{' '}
            {thresholdLine(rubric.thresholds)}
          </div>
          <RubricBody rubric={rubric} />
          <div className="mt-5 flex gap-2">
            <button type="button" className="btn btn-primary text-sm" onClick={onContinue}>
              Continue with v{rubric.version}
            </button>
            <button
              type="button"
              className="btn btn-ghost text-sm"
              disabled={drafting}
              onClick={onDraft}
            >
              {drafting ? 'Drafting…' : 'Write a new version'}
            </button>
          </div>
        </>
      ) : draft ? (
        <>
          <div className="mt-4 rounded-xl border border-warning/30 bg-warning/5 px-4 py-2.5 text-sm text-ink">
            This is a draft and nothing has been saved. Read it before publishing: every applicant
            to this role will be judged against it.
          </div>
          <pre className="mt-3 max-h-96 overflow-auto rounded-xl border border-hairline bg-elevated p-3 text-xs text-ink-muted">
            {JSON.stringify(draft, null, 2)}
          </pre>
          <div className="mt-5 flex gap-2">
            <button
              type="button"
              className="btn btn-primary text-sm"
              disabled={publishing}
              onClick={onPublish}
            >
              {publishing ? 'Publishing…' : 'Publish this rubric'}
            </button>
            <button type="button" className="btn btn-ghost text-sm" onClick={onDiscard}>
              Discard
            </button>
          </div>
        </>
      ) : (
        <>
          <p className="mt-4 text-sm text-ink-muted">
            This position has no rubric yet, so nothing can be screened against it.
          </p>
          <button
            type="button"
            className="btn btn-primary mt-3 text-sm"
            disabled={drafting || !!blocked}
            onClick={onDraft}
          >
            {drafting ? 'Drafting from the job description…' : 'Draft a rubric from the JD'}
          </button>
        </>
      )}
    </>
  )
}

function thresholdLine(thresholds: Record<string, unknown>): string {
  const parts: string[] = []
  for (const key of ['p1', 'p2', 'p3']) {
    const v = thresholds?.[key]
    if (typeof v === 'number') parts.push(`${key.toUpperCase()} at or above ${v}`)
  }
  return parts.length ? `Thresholds ${parts.join(', ')}.` : ''
}

function RubricBody({ rubric }: { rubric: NonNullable<TechRubricStep['rubric']> }) {
  return (
    <div className="mt-4 grid gap-4 lg:grid-cols-2">
      <div>
        <h3 className="mb-2 font-display text-sm font-bold text-ink">Dimensions</h3>
        <div className="space-y-1.5">
          {rubric.dimensions.map((d) => (
            <div
              key={d.key}
              className="flex items-baseline justify-between rounded-lg border border-hairline bg-elevated px-3 py-2 text-sm"
            >
              <span className="text-ink">{d.label}</span>
              <span className="tabular-nums text-xs text-ink-muted">
                weight {d.weight ?? '—'}
                {d.core ? ' · core' : ''}
              </span>
            </div>
          ))}
        </div>
      </div>
      <div>
        <h3 className="mb-2 font-display text-sm font-bold text-ink">Hard filters</h3>
        {rubric.hard_filters.length === 0 ? (
          <p className="text-xs text-ink-dim">None. Every applicant in the pool is scored.</p>
        ) : (
          <>
            <div className="space-y-1.5">
              {rubric.hard_filters.map((f, i) => (
                <div
                  key={f.key ?? i}
                  className="rounded-lg border border-hairline bg-elevated px-3 py-2 text-sm text-ink"
                >
                  {f.label ?? f.key}
                  {f.action ? <span className="text-xs text-ink-muted"> · {f.action}</span> : null}
                </div>
              ))}
            </div>
            {/* A filter that removes someone means nobody reads them. Say so
                here, where it can still be changed, rather than leaving it to
                be discovered in the results. */}
            <p className="mt-2 text-xs text-ink-dim">
              A filter set to reject removes a candidate before they are scored, so no one reads
              them. Anything meant only to inform a decision belongs as a flag instead.
            </p>
          </>
        )}
        {rubric.min_years !== null && rubric.min_years !== undefined && (
          <p className="mt-2 text-xs text-ink-dim">Minimum {rubric.min_years} years.</p>
        )}
      </div>
    </div>
  )
}

// --- Step 3: the pool and the cost -----------------------------------------

function PoolStep({
  plan, planning, error, models,
  mode, setMode, sinceDays, setSinceDays, maxCandidates, setMaxCandidates,
  model, setModel, useBatch, setUseBatch, onBack, onContinue,
}: {
  plan: TechPlan | null
  planning: boolean
  error: string | null
  models: TechModel[]
  mode: string
  setMode: (v: string) => void
  sinceDays: number | null
  setSinceDays: (v: number | null) => void
  maxCandidates: number | null
  setMaxCandidates: (v: number | null) => void
  model: string
  setModel: (v: string) => void
  useBatch: boolean
  setUseBatch: (v: boolean) => void
  onBack: () => void
  onContinue: () => void
}) {
  const chosen = models.find((m) => m.model === model)
  const modeHelp = MODES.find((m) => m.value === mode)?.help

  return (
    <>
      <h2 className="font-display text-base font-bold text-ink">Who gets screened, and what it costs</h2>

      <div className="mt-4 grid gap-4 sm:grid-cols-3">
        <label className="block">
          <span className="mb-1 block text-sm font-medium text-ink">Who</span>
          <select className="input w-full" value={mode} onChange={(e) => setMode(e.target.value)}>
            {MODES.map((m) => (
              <option key={m.value} value={m.value}>{m.label}</option>
            ))}
          </select>
        </label>

        <label className="block">
          <span className="mb-1 block text-sm font-medium text-ink">Applied within</span>
          <select
            className="input w-full"
            value={sinceDays ?? ''}
            onChange={(e) => setSinceDays(e.target.value ? Number(e.target.value) : null)}
          >
            <option value="">any time</option>
            <option value="30">the last 30 days</option>
            <option value="90">the last 90 days</option>
            <option value="180">the last 180 days</option>
          </select>
        </label>

        <label className="block">
          <span className="mb-1 block text-sm font-medium text-ink">At most</span>
          <input
            className="input w-full"
            type="number"
            min={1}
            placeholder="no limit"
            value={maxCandidates ?? ''}
            onChange={(e) => setMaxCandidates(e.target.value ? Number(e.target.value) : null)}
          />
        </label>
      </div>
      {modeHelp && <p className="mt-2 text-xs text-ink-dim">{modeHelp}</p>}

      <div className="mt-5 grid gap-4 sm:grid-cols-2">
        <label className="block">
          <span className="mb-1 block text-sm font-medium text-ink">Scored by</span>
          <select className="input w-full" value={model} onChange={(e) => setModel(e.target.value)}>
            {models.map((m) => (
              <option key={m.model} value={m.model}>{m.label}</option>
            ))}
          </select>
          {chosen && (
            <span className="mt-1 block text-xs text-ink-dim">
              ${chosen.input_per_mtok}/${chosen.output_per_mtok} per million tokens. This model
              decides who gets read first, so it is worth more thought than the price alone.
            </span>
          )}
        </label>

        <label className="flex items-start gap-2 pt-7">
          <input
            type="checkbox"
            className="mt-0.5"
            checked={useBatch}
            onChange={(e) => setUseBatch(e.target.checked)}
          />
          <span className="text-sm text-ink">
            Use the batch API
            <span className="block text-xs text-ink-dim">
              About half the cost, and slower because it runs asynchronously.
            </span>
          </span>
        </label>
      </div>

      {error && <p className="mt-4 text-sm text-danger">{error}</p>}

      {planning ? (
        <div className="mt-5"><Spinner label="Working out the pool…" /></div>
      ) : plan ? (
        <>
          <div className="mt-5 grid grid-cols-2 gap-3 lg:grid-cols-4">
            <Stat label="People" value={plan.people} />
            <Stat label="Duplicates merged" value={plan.duplicates_merged} />
            <Stat label="No CV on record" value={plan.no_cv} />
            <Stat label="Estimated cost" value={money(plan.est_cost_usd)} />
          </div>

          <p className="mt-3 text-xs text-ink-dim">
            Newest application {formatDate(plan.newest_application)}, oldest {formatDate(plan.oldest_application)}.
            The newest are scored first.
            {plan.already_scored_in_pool > 0 &&
              ` ${plan.already_scored_in_pool} of these already carry a score and would be superseded.`}
          </p>

          {/* 🔴 "No CV on record" is not the same as "unreadable". A CV that
              will not extract is only discovered during the run, and an
              extraction failure is a document problem, never a weak candidate. */}
          <p className="mt-2 text-xs text-ink-dim">
            No CV on record counts applicants with no file at all. A file that turns out not to be
            readable can only be found by opening it, so those appear during the run as skipped and
            need a person, never a low score.
          </p>

          <p className="mt-2 text-xs text-ink-dim">
            Prompt caching saves about {money(plan.cache_saving_usd)} on this run
            {!useBatch && plan.batch_saving_usd > 0
              ? `, and the batch API would save roughly ${money(plan.batch_saving_usd)} more`
              : ''}
            . The estimate is from character counts, not exact tokens, so the cost cap on the next
            step and the recorded actuals are the real controls.
          </p>

          {plan.people === 0 && (
            <p className="mt-3 rounded-xl border border-warning/30 bg-warning/5 px-4 py-2.5 text-sm text-ink">
              Nobody matches these filters, so there is nothing to run.
            </p>
          )}
        </>
      ) : null}

      <div className="mt-6 flex gap-2">
        <button
          type="button"
          className="btn btn-primary text-sm"
          disabled={!plan || plan.people === 0 || planning}
          onClick={onContinue}
        >
          Continue
        </button>
        <button type="button" className="btn btn-ghost text-sm" onClick={onBack}>
          Back
        </button>
      </div>
    </>
  )
}

function Stat({ label, value }: { label: string; value: number | string }) {
  return (
    <div className="rounded-2xl border border-hairline bg-elevated p-4">
      <div className="text-2xl font-bold tabular-nums text-ink">{value}</div>
      <div className="mt-0.5 text-xs uppercase tracking-wide text-ink-dim">{label}</div>
    </div>
  )
}

// --- Step 4: confirm, then the run -----------------------------------------

function ConfirmStep({
  job, plan, model, useBatch, costCap, setCostCap, starting, run, progress, outcome, error,
  onStart, onResume, onStop, onBack,
}: {
  job: TechJob
  plan: TechPlan | null
  model: string
  useBatch: boolean
  costCap: number | null
  setCostCap: (v: number | null) => void
  starting: boolean
  run: TechRun | null
  progress: { done: number; skipped: number; failed: number; retrying: number; retryInSeconds: number } | null
  outcome: { kind: 'done' | 'stopped' | 'error'; done: number; skipped: number; failed: number; message?: string } | null
  error: string | null
  onStart: () => void
  onResume: () => void
  onStop: () => void
  onBack: () => void
}) {
  const running = progress !== null

  if (run || running) {
    return <RunPanel run={run} progress={progress} outcome={outcome} error={error} onStop={onStop} />
  }

  return (
    <>
      <h2 className="font-display text-base font-bold text-ink">Confirm</h2>

      {job.live_run_id && (
        <div className="mt-4 rounded-xl border border-warning/30 bg-warning/5 px-4 py-3 text-sm text-ink">
          A run is already {job.live_run_status} on this position. Starting a second one is refused,
          so pick it up where it stopped instead.
          <button type="button" className="btn btn-ghost ml-3 text-xs" onClick={onResume}>
            Resume that run
          </button>
        </div>
      )}

      {plan && (
        <>
          <p className="mt-4 text-sm text-ink">
            About to score <strong>{plan.people}</strong> candidate
            {plan.people === 1 ? '' : 's'} on <strong>{job.title}</strong> against rubric{' '}
            <strong>v{plan.rubric_version}</strong>, using {model}
            {useBatch ? ' through the batch API' : ''}. Estimated{' '}
            <strong>{money(plan.est_cost_usd)}</strong>.
          </p>

          <label className="mt-4 block max-w-xs">
            <span className="mb-1 block text-sm font-medium text-ink">Stop spending at</span>
            <input
              className="input w-full"
              type="number"
              min={0}
              step="0.5"
              placeholder="no cap"
              value={costCap ?? ''}
              onChange={(e) => setCostCap(e.target.value ? Number(e.target.value) : null)}
            />
          </label>
          {/* Newest-first plus a cap means the cap decides who is NOT reached.
              That is a real consequence and it is said here, not discovered. */}
          <p className="mt-1.5 max-w-xl text-xs text-ink-dim">
            The cap is the real control, because the figure above is an estimate. If the run hits it
            the remaining candidates are left unscored, and since the newest are scored first, those
            will be the oldest applications in the pool.
          </p>
        </>
      )}

      {error && <p className="mt-4 text-sm text-danger">{error}</p>}

      <div className="mt-6 flex gap-2">
        <button
          type="button"
          className="btn btn-primary text-sm"
          disabled={!plan || starting || !!job.live_run_id}
          onClick={onStart}
        >
          {starting ? 'Starting…' : `Screen ${plan?.people ?? 0} candidates`}
        </button>
        <button type="button" className="btn btn-ghost text-sm" onClick={onBack}>
          Back
        </button>
      </div>
    </>
  )
}

function RunPanel({
  run, progress, outcome, error, onStop,
}: {
  run: TechRun | null
  progress: { done: number; skipped: number; failed: number; retrying: number; retryInSeconds: number } | null
  outcome: { kind: 'done' | 'stopped' | 'error'; done: number; skipped: number; failed: number; message?: string } | null
  error: string | null
  onStop: () => void
}) {
  const total = run?.total ?? 0
  const done = run?.done ?? progress?.done ?? 0
  const percent = total ? Math.round((done / total) * 100) : 0

  return (
    <>
      <h2 className="font-display text-base font-bold text-ink">The run</h2>

      {progress && (
        <>
          <div className="mt-4 flex items-center justify-between gap-4">
            <div className="flex items-center gap-2.5 text-sm text-ink">
              <Loader2 className="h-4 w-4 animate-spin text-blurple" />
              <span className="font-medium">Reading CVs: {done} of {total}</span>
              {/* A redeploy takes the server away for minutes. Say so, or a
                  waiting run reads as a frozen page. */}
              {progress.retrying > 0 && (
                <span className="text-xs text-warning">
                  Lost the server. Retrying in {progress.retryInSeconds}s (attempt {progress.retrying})
                </span>
              )}
            </div>
            <button type="button" className="btn btn-ghost text-xs" onClick={onStop}>
              Stop
            </button>
          </div>
          <div className="mt-2.5 h-1.5 overflow-hidden rounded-full bg-elevated">
            <div className="h-full rounded-full bg-blurple transition-all" style={{ width: `${percent}%` }} />
          </div>
          <p className="mt-2 text-xs text-ink-dim">
            Each candidate is saved as they finish, so stopping loses nothing and starting again
            continues from here.
          </p>
        </>
      )}

      {run && (
        <div className="mt-5 grid grid-cols-2 gap-3 lg:grid-cols-4">
          <Stat label="Scored" value={run.scored} />
          {/* Unreadable is kept apart from low-scoring on purpose: one needs a
              person to open a document, the other is a judgement. */}
          <Stat label="Could not be read" value={run.unusable + run.skipped} />
          <Stat label="Failed" value={run.failed} />
          <Stat label="Spent" value={money(run.actual_cost_usd)} />
        </div>
      )}

      {run && (
        <p className="mt-3 text-xs text-ink-dim">
          Run {run.id.slice(0, 8)} · {run.status} · rubric v{run.rubric_version} · {run.model}
          {run.cost_cap_usd ? ` · cap ${money(run.cost_cap_usd)}` : ''}
        </p>
      )}

      {run?.last_warning && (
        <p className="mt-2 flex items-start gap-1.5 text-xs text-warning">
          <AlertTriangle className="mt-0.5 h-3.5 w-3.5 shrink-0" />
          {run.last_warning}
        </p>
      )}

      {error && <p className="mt-3 text-sm text-danger">{error}</p>}

      {!progress && outcome && (
        <div
          className={`mt-4 rounded-lg border px-3 py-2 text-xs ${
            outcome.kind === 'error'
              ? 'border-danger/30 bg-danger/5 text-danger'
              : 'border-hairline bg-elevated text-ink-muted'
          }`}
        >
          {outcome.kind === 'error' ? (
            <>
              <span className="font-semibold">
                The run stopped after {outcome.done} candidate{outcome.done === 1 ? '' : 's'}.
              </span>{' '}
              {outcome.message} Everything scored so far is saved, and starting again picks up from
              where it stopped.
            </>
          ) : (
            <>
              {outcome.kind === 'stopped' ? 'Stopped' : 'Finished'} after {outcome.done} candidate
              {outcome.done === 1 ? '' : 's'}.
              {outcome.skipped > 0 && (
                <>
                  {' '}
                  <span className="text-warning">
                    {outcome.skipped} could not be read and need a person.
                  </span>{' '}
                  A CV that will not open is a document problem, not a weak candidate, so they are
                  not scored at all.
                </>
              )}
              {/* 🔴 NOT the same sentence, and never merged into it. These
                  candidates' CVs may be perfectly fine: the screener broke.
                  Saying "could not be read" here sent Ayesha to chase twenty
                  documents while the defect was ours. */}
              {outcome.failed > 0 && (
                <>
                  {' '}
                  <span className="text-danger">
                    {outcome.failed} failed to score.
                  </span>{' '}
                  That is a fault in the screener, not in their CVs, and it needs an engineer
                  rather than a person opening documents. Nothing was written for them.
                </>
              )}
            </>
          )}
        </div>
      )}
    </>
  )
}
