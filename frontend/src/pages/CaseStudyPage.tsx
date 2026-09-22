import { useQuery } from '@tanstack/react-query'
import { AlertTriangle, CheckCircle2, ClipboardCheck, FileWarning, Loader2, Search, ShieldCheck } from 'lucide-react'
import { useEffect, useRef, useState } from 'react'
import { Spinner } from '../components/Spinner'
import { ApiError, api } from '../lib/api'
import { fullName } from '../lib/format'
import { canApprove, canEdit } from '../lib/roles'
import { CASE_STUDY_FLAGS } from '../lib/types'
import type { CaseStudyBenchmark, CaseStudyEvaluation, JobItem, QueueRow } from '../lib/types'

const stripStatus = (msg: string) => msg.replace(/^\d+:\s*/, '')

const BAND_LABEL: Record<string, string> = {
  disqualified: 'Disqualified',
  strong_yes: 'Strong yes',
  yes: 'Yes',
  borderline: 'Borderline',
  no: 'No',
}
const BAND_TONE: Record<string, string> = {
  disqualified: 'bg-danger/15 text-danger',
  strong_yes: 'bg-green/15 text-green',
  yes: 'bg-green/15 text-green',
  borderline: 'bg-[#b7791f]/15 text-[#b7791f]',
  no: 'bg-danger/15 text-danger',
}

export function CaseStudyPage() {
  const meQ = useQuery({ queryKey: ['me'], queryFn: api.me, retry: false })
  const role = meQ.data?.app_role
  const isEditor = canEdit(role)
  const isApprover = canApprove(role)

  /* ── Jobs, for the benchmark's job picker ────────────────────────────── */
  const [jobs, setJobs] = useState<JobItem[]>([])
  const [jobsLoaded, setJobsLoaded] = useState(false)
  const [jobsError, setJobsError] = useState<string | null>(null)

  useEffect(() => {
    if (!isEditor) return
    api
      .jobs()
      .then((j) => {
        setJobs(j)
        setJobsLoaded(true)
      })
      .catch(() => {
        setJobsError('Could not load jobs. Try reloading the page.')
        setJobsLoaded(true)
      })
  }, [isEditor])

  /* ── Step 1: the benchmark (answer key) ──────────────────────────────── */
  const [benchmark, setBenchmark] = useState<CaseStudyBenchmark | null>(null)

  const [jobId, setJobId] = useState<number | ''>('')
  const [title, setTitle] = useState('')
  const [body, setBody] = useState('')
  const [creating, setCreating] = useState(false)
  const [createError, setCreateError] = useState<string | null>(null)

  // IMPORTANT 5a/c: load the job's own benchmarks on mount and whenever the
  // selected job changes, so a reload (or a first job pick) recovers the
  // server's real state instead of showing "approve the benchmark" while an
  // approved one already exists. The most recently APPROVED row (by
  // qa_approved_at) wins, matching the server's own Rule 0 ordering exactly;
  // failing that, the most recently created DRAFT is shown so nobody
  // re-authors a duplicate without knowing one is already pending approval.
  const [benchmarksLoading, setBenchmarksLoading] = useState(false)
  const [benchmarksError, setBenchmarksError] = useState<string | null>(null)

  useEffect(() => {
    if (!isEditor || !jobId) return
    let cancelled = false
    setBenchmarksLoading(true)
    setBenchmarksError(null)
    api
      .listCaseStudyBenchmarks(Number(jobId))
      .then((rows) => {
        if (cancelled) return
        const approved = rows
          .filter((b) => b.status === 'approved')
          .sort((a, b) => (b.qa_approved_at ?? '').localeCompare(a.qa_approved_at ?? ''))
        const draft = rows.find((b) => b.status === 'draft')
        setBenchmark(approved[0] ?? draft ?? null)
      })
      .catch(() => {
        if (cancelled) return
        setBenchmarksError('Could not load this job’s benchmarks. Try reloading the page.')
      })
      .finally(() => {
        if (!cancelled) setBenchmarksLoading(false)
      })
    return () => {
      cancelled = true
    }
  }, [isEditor, jobId])

  async function createBenchmark() {
    if (!jobId || !title.trim() || !body.trim()) return
    setCreating(true)
    setCreateError(null)
    try {
      const b = await api.createCaseStudyBenchmark({ job_id: Number(jobId), title: title.trim(), body })
      setBenchmark(b)
    } catch (e) {
      setCreateError(stripStatus((e as ApiError).message))
    } finally {
      setCreating(false)
    }
  }

  // An approver may approve a benchmark authored earlier or by someone else --
  // there is no endpoint to list or look one up by job, so the id has to be
  // handed over (e.g. in chat) and pasted in here.
  const [approveId, setApproveId] = useState('')
  const [approving, setApproving] = useState(false)
  const [approveError, setApproveError] = useState<string | null>(null)

  async function approveById() {
    if (!approveId.trim()) return
    const ok = window.confirm(
      `Approve benchmark ${approveId.trim()}? Every later score for its job will calibrate against this answer key.`,
    )
    if (!ok) return
    setApproving(true)
    setApproveError(null)
    try {
      const b = await api.approveCaseStudyBenchmark(approveId.trim())
      setBenchmark(b)
    } catch (e) {
      setApproveError(stripStatus((e as ApiError).message))
    } finally {
      setApproving(false)
    }
  }

  async function approveLoadedBenchmark() {
    if (!benchmark) return
    const ok = window.confirm(
      `Approve the benchmark "${benchmark.title}" for job ${benchmark.job_id}? Every later score for this job will calibrate against this answer key.`,
    )
    if (!ok) return
    setApproving(true)
    setApproveError(null)
    try {
      const b = await api.approveCaseStudyBenchmark(benchmark.id)
      setBenchmark(b)
    } catch (e) {
      setApproveError(stripStatus((e as ApiError).message))
    } finally {
      setApproving(false)
    }
  }

  function resetBenchmark() {
    setBenchmark(null)
    setJobId('')
    setTitle('')
    setBody('')
    setCreateError(null)
    setApproveId('')
    setApproveError(null)
    setBenchmarksError(null)
  }

  const benchmarkApproved = benchmark?.status === 'approved'

  /* ── Step 2: score a submission against the approved benchmark ──────── */
  const [query, setQuery] = useState('')
  const [debouncedQuery, setDebouncedQuery] = useState('')
  useEffect(() => {
    const t = setTimeout(() => setDebouncedQuery(query.trim()), 300)
    return () => clearTimeout(t)
  }, [query])

  const [results, setResults] = useState<QueueRow[]>([])
  const [searching, setSearching] = useState(false)
  const [searchError, setSearchError] = useState<string | null>(null)
  const searchGenRef = useRef(0)

  useEffect(() => {
    if (!debouncedQuery || !benchmarkApproved) {
      setResults([])
      return
    }
    const gen = ++searchGenRef.current
    setSearching(true)
    setSearchError(null)
    api
      .candidates({ q: debouncedQuery, limit: 15 })
      .then((rows) => {
        if (searchGenRef.current !== gen) return // stale: query changed since this request was sent
        setResults(rows)
      })
      .catch(() => {
        if (searchGenRef.current !== gen) return
        setSearchError('Could not search candidates. Try again.')
      })
      .finally(() => {
        if (searchGenRef.current === gen) setSearching(false)
      })
  }, [debouncedQuery, benchmarkApproved])

  const [selected, setSelected] = useState<QueueRow | null>(null)
  const [scoring, setScoring] = useState(false)
  const [scoreError, setScoreError] = useState<string | null>(null)
  const [evaluation, setEvaluation] = useState<CaseStudyEvaluation | null>(null)

  // IMPORTANT 5b/d: the full scoring history for whichever application
  // `evaluation` belongs to -- newest first, so index 0 is always the
  // current row and the rest render as visibly superseded. /score is not
  // idempotent, so this is the legibility fix; there is no `is_current`
  // column or retirement workflow behind it (still outstanding, see the
  // fix report).
  const [evaluationHistory, setEvaluationHistory] = useState<CaseStudyEvaluation[]>([])

  async function loadEvaluationHistory(applicationId: number) {
    try {
      const rows = await api.listCaseStudyEvaluations(applicationId)
      setEvaluationHistory(rows)
    } catch {
      // Non-fatal: the just-scored/just-opened evaluation above still
      // renders in full either way, this only powers the superseded list.
      setEvaluationHistory([])
    }
  }

  // A client-side heads-up only -- the server is the real Rule 0 gate and
  // re-derives the application's job itself, never trusting anything sent
  // from here.
  const jobMismatch = !!(selected && benchmark && selected.job_pk != null && selected.job_pk !== benchmark.job_id)

  async function scoreSelected() {
    if (!selected || !benchmarkApproved) return
    const ok = window.confirm(
      `Score ${fullName(selected)} (application ${selected.application_id}) against the approved benchmark "${benchmark?.title}"?`,
    )
    if (!ok) return
    setScoring(true)
    setScoreError(null)
    setEvaluation(null)
    setEvaluationHistory([])
    try {
      const ev = await api.scoreCaseStudy(selected.application_id)
      setEvaluation(ev)
      await loadEvaluationHistory(ev.application_id)
    } catch (e) {
      setScoreError(stripStatus((e as ApiError).message))
    } finally {
      setScoring(false)
    }
  }

  /* ── Open a previously scored evaluation by id ───────────────────────── */
  const [lookupId, setLookupId] = useState('')
  const [lookupLoading, setLookupLoading] = useState(false)
  const [lookupError, setLookupError] = useState<string | null>(null)

  async function lookupEvaluation() {
    if (!lookupId.trim()) return
    setLookupLoading(true)
    setLookupError(null)
    setEvaluationHistory([])
    try {
      const ev = await api.caseStudyEvaluation(lookupId.trim())
      setEvaluation(ev)
      await loadEvaluationHistory(ev.application_id)
    } catch (e) {
      setLookupError(stripStatus((e as ApiError).message))
    } finally {
      setLookupLoading(false)
    }
  }

  if (meQ.isLoading) return <Spinner label="Loading…" />

  if (!isEditor) {
    return (
      <div className="mx-auto max-w-3xl px-8 py-7">
        <header className="mb-4">
          <h1 className="font-display text-2xl font-bold text-ink">Case Studies</h1>
        </header>
        <div className="card p-8 text-center text-sm text-ink-dim">
          You need editor access to write or score a case-study benchmark. Ask an admin to change your role if you
          believe this is wrong.
        </div>
      </div>
    )
  }

  return (
    <div className="mx-auto max-w-4xl px-8 py-7">
      <header className="mb-5">
        <h1 className="font-display text-2xl font-bold text-ink">Case Studies</h1>
        <p className="mt-1 text-sm text-ink-muted">
          Write and approve the benchmark answer key for a job, then score submissions against it.
        </p>
      </header>

      {/* ── Step 1: benchmark ───────────────────────────────────────────── */}
      <div className="card p-5">
        <div className="mb-3 flex items-center justify-between gap-3">
          <h2 className="text-sm font-semibold text-ink">1. Benchmark (answer key)</h2>
          {benchmark && (
            <button type="button" onClick={resetBenchmark} className="btn btn-ghost h-8 text-sm">
              Start a different benchmark
            </button>
          )}
        </div>

        {!benchmark ? (
          <div className="space-y-4">
            <div className="rounded-xl border border-hairline bg-surface-2 px-4 py-3 text-xs text-ink-muted">
              Rule 0: write and QA the benchmark before any submission is opened. Reading a submission first
              calibrates scoring to whoever is read first.
            </div>

            {jobId && benchmarksLoading && (
              <p className="text-xs text-ink-dim">Checking for an existing benchmark on this job…</p>
            )}
            {benchmarksError && <p className="text-xs text-danger">{benchmarksError}</p>}

            <div className="grid grid-cols-1 gap-3 md:grid-cols-2">
              <div>
                <label className="mb-1 block text-xs font-semibold uppercase tracking-wide text-ink-dim">Job</label>
                {jobsError ? (
                  <p className="text-xs text-danger">{jobsError}</p>
                ) : !jobsLoaded ? (
                  <p className="text-xs text-ink-dim">Loading jobs…</p>
                ) : (
                  <select
                    value={jobId}
                    onChange={(e) => setJobId(e.target.value ? Number(e.target.value) : '')}
                    className="input"
                  >
                    <option value="">Select a job…</option>
                    {jobs.map((j) => (
                      <option key={j.job_pk} value={j.job_pk}>
                        {j.title ?? `Job ${j.job_pk}`}
                        {j.job_code ? ` (${j.job_code})` : ''}
                      </option>
                    ))}
                  </select>
                )}
              </div>
              <div>
                <label className="mb-1 block text-xs font-semibold uppercase tracking-wide text-ink-dim">Title</label>
                <input
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder="e.g. Growth Manager case study, round 2"
                  className="input"
                />
              </div>
            </div>

            <div>
              <label className="mb-1 block text-xs font-semibold uppercase tracking-wide text-ink-dim">
                Answer key
              </label>
              <textarea
                value={body}
                onChange={(e) => setBody(e.target.value)}
                placeholder="Paste or write the benchmark answer key here. No candidate names or responses -- it must calibrate against the case, not the cohort."
                rows={10}
                className="input font-mono text-xs leading-relaxed"
              />
            </div>

            {createError && (
              <div className="flex items-start gap-2 rounded-xl border border-danger/30 bg-danger/5 px-4 py-2.5 text-sm text-danger">
                <AlertTriangle className="mt-0.5 h-4 w-4 shrink-0" />
                <span>{createError}</span>
              </div>
            )}

            <button
              type="button"
              onClick={createBenchmark}
              disabled={creating || !jobId || !title.trim() || !body.trim()}
              className="btn btn-primary"
            >
              {creating ? <Loader2 className="h-4 w-4 animate-spin" /> : <ClipboardCheck className="h-4 w-4" />}
              {creating ? 'Saving…' : 'Save as draft'}
            </button>

            <div className="border-t border-hairline pt-4">
              <p className="mb-2 text-xs text-ink-dim">
                Already have a benchmark id from a review elsewhere? Paste it to approve it directly.
              </p>
              <div className="flex items-center gap-2">
                <input
                  value={approveId}
                  onChange={(e) => setApproveId(e.target.value)}
                  placeholder="Benchmark id"
                  className="input"
                />
                <button
                  type="button"
                  onClick={approveById}
                  disabled={!isApprover || approving || !approveId.trim()}
                  className="btn btn-ghost h-9 whitespace-nowrap text-sm"
                  title={!isApprover ? 'Only an approver can approve a benchmark' : undefined}
                >
                  {approving ? <Loader2 className="h-4 w-4 animate-spin" /> : <ShieldCheck className="h-4 w-4" />}
                  Approve
                </button>
              </div>
              {approveError && <p className="mt-2 text-xs text-danger">{approveError}</p>}
            </div>
          </div>
        ) : (
          <div className="space-y-3">
            <div className="flex flex-wrap items-center justify-between gap-3 rounded-xl border border-hairline bg-surface-2 px-4 py-3">
              <div>
                <div className="text-sm font-medium text-ink">{benchmark.title}</div>
                <div className="text-xs text-ink-dim">
                  Benchmark {benchmark.id} · Job {benchmark.job_id} · Created by {benchmark.created_by}
                </div>
              </div>
              <span
                className={`chip text-xs font-bold ${
                  benchmarkApproved ? 'bg-green/15 text-green' : 'bg-[#b7791f]/15 text-[#b7791f]'
                }`}
              >
                {benchmarkApproved ? 'Approved' : 'Draft'}
              </span>
            </div>

            <details className="rounded-xl border border-hairline px-4 py-2.5 text-xs text-ink-muted">
              <summary className="cursor-pointer select-none font-medium text-ink">View answer key</summary>
              <pre className="mt-2 whitespace-pre-wrap font-sans text-xs leading-relaxed text-ink-muted">
                {benchmark.body}
              </pre>
            </details>

            {benchmarkApproved ? (
              <div className="flex items-center gap-2 rounded-xl border border-green/30 bg-green/10 px-4 py-2.5 text-sm text-ink">
                <CheckCircle2 className="h-4 w-4 text-green" />
                Approved by {benchmark.qa_approved_by || 'an approver'}
                {benchmark.qa_approved_at ? ` on ${new Date(benchmark.qa_approved_at).toLocaleString()}` : ''}.
                Submissions for this job can now be scored.
              </div>
            ) : (
              <div className="space-y-2 rounded-xl border border-[#b7791f]/30 bg-[#b7791f]/5 px-4 py-2.5 text-sm text-ink">
                <div className="flex items-start gap-2">
                  <AlertTriangle className="mt-0.5 h-4 w-4 shrink-0 text-[#b7791f]" />
                  <span>
                    Approve the benchmark before scoring. Scoring calibrates to whoever is read first, so no
                    submission for this job can be opened until an approver signs off on this answer key.
                  </span>
                </div>
                {isApprover ? (
                  <button
                    type="button"
                    onClick={approveLoadedBenchmark}
                    disabled={approving}
                    className="btn btn-primary h-9 text-sm"
                  >
                    {approving ? <Loader2 className="h-4 w-4 animate-spin" /> : <ShieldCheck className="h-4 w-4" />}
                    {approving ? 'Approving…' : 'Approve this benchmark'}
                  </button>
                ) : (
                  <p className="text-xs text-ink-dim">Only an approver can approve it. Ask one to review it.</p>
                )}
                {approveError && <p className="text-xs text-danger">{approveError}</p>}
              </div>
            )}
          </div>
        )}
      </div>

      {/* ── Step 2: score a submission ──────────────────────────────────── */}
      <div className="card mt-5 p-5">
        <h2 className="mb-3 text-sm font-semibold text-ink">2. Score a submission</h2>

        {!benchmarkApproved ? (
          <p className="text-sm text-ink-dim">
            Approve the benchmark before scoring. Scoring calibrates to whoever is read first.
          </p>
        ) : (
          <div className="space-y-3">
            {selected ? (
              <div className="flex items-center justify-between rounded-xl border border-blurple/40 bg-blurple/5 px-4 py-2.5">
                <div>
                  <div className="text-sm font-medium text-ink">{fullName(selected)}</div>
                  <div className="text-xs text-ink-dim">
                    Application #{selected.application_id} · {selected.job_title ?? 'Unknown role'}
                  </div>
                </div>
                <button type="button" onClick={() => setSelected(null)} className="btn btn-ghost h-8 text-sm">
                  Change
                </button>
              </div>
            ) : (
              <div>
                <div className="relative">
                  <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-ink-dim" />
                  <input
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="Search candidate name or email…"
                    className="input pl-9"
                  />
                </div>
                {searchError && <p className="mt-2 text-xs text-danger">{searchError}</p>}
                {searching && <p className="mt-2 text-xs text-ink-dim">Searching…</p>}
                {!searching && debouncedQuery && results.length === 0 && !searchError && (
                  <p className="mt-2 text-xs text-ink-dim">No candidates match "{debouncedQuery}".</p>
                )}
                {results.length > 0 && (
                  <ul className="mt-2 divide-y divide-hairline overflow-hidden rounded-xl border border-hairline">
                    {results.map((r) => (
                      <li key={r.application_id}>
                        <button
                          type="button"
                          onClick={() => setSelected(r)}
                          className="flex w-full items-center justify-between px-4 py-2.5 text-left text-sm transition-colors hover:bg-elevated"
                        >
                          <span className="font-medium text-ink">{fullName(r)}</span>
                          <span className="text-xs text-ink-dim">
                            #{r.application_id} · {r.job_title ?? 'Unknown role'}
                          </span>
                        </button>
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            )}

            {jobMismatch && (
              <div className="flex items-start gap-2 rounded-xl border border-danger/30 bg-danger/5 px-4 py-2.5 text-sm text-danger">
                <AlertTriangle className="mt-0.5 h-4 w-4 shrink-0" />
                <span>
                  This candidate applied to job {selected?.job_pk}, but the approved benchmark above is for job{' '}
                  {benchmark?.job_id}. Scoring will be refused for a different job's benchmark.
                </span>
              </div>
            )}

            {scoreError && (
              <div className="flex items-start gap-2 rounded-xl border border-danger/30 bg-danger/5 px-4 py-2.5 text-sm text-danger">
                <AlertTriangle className="mt-0.5 h-4 w-4 shrink-0" />
                <span>{scoreError}</span>
              </div>
            )}

            <button
              type="button"
              onClick={scoreSelected}
              disabled={!selected || scoring || jobMismatch}
              className="btn btn-primary"
            >
              {scoring ? <Loader2 className="h-4 w-4 animate-spin" /> : <ClipboardCheck className="h-4 w-4" />}
              {scoring ? 'Scoring…' : 'Score against the approved benchmark'}
            </button>
          </div>
        )}

        <div className="mt-4 border-t border-hairline pt-4">
          <p className="mb-2 text-xs text-ink-dim">Or open an evaluation already scored elsewhere, by id.</p>
          <div className="flex items-center gap-2">
            <input
              value={lookupId}
              onChange={(e) => setLookupId(e.target.value)}
              placeholder="Evaluation id"
              className="input"
            />
            <button
              type="button"
              onClick={lookupEvaluation}
              disabled={lookupLoading || !lookupId.trim()}
              className="btn btn-ghost h-9 whitespace-nowrap text-sm"
            >
              {lookupLoading ? <Loader2 className="h-4 w-4 animate-spin" /> : <Search className="h-4 w-4" />}
              Open
            </button>
          </div>
          {lookupError && <p className="mt-2 text-xs text-danger">{lookupError}</p>}
        </div>
      </div>

      {/* ── Result ──────────────────────────────────────────────────────── */}
      {evaluation && (
        <div className="card mt-5 p-5">
          <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
            <div>
              <div className="flex items-center gap-2">
                <div className="text-sm font-medium text-ink">{evaluation.candidate_name}</div>
                {/* IMPORTANT 5d: a /score re-run is not idempotent, so an
                    application can carry several evaluations -- this says,
                    plainly, whether the one on screen is the newest. */}
                {evaluationHistory.length > 0 &&
                  (evaluationHistory[0]?.id === evaluation.id ? (
                    <span className="chip bg-green/15 text-xs font-bold text-green">Current</span>
                  ) : (
                    <span className="chip bg-[#b7791f]/15 text-xs font-bold text-[#b7791f]">
                      Superseded -- a newer evaluation exists
                    </span>
                  ))}
              </div>
              <div className="text-xs text-ink-dim">
                Application #{evaluation.application_id} · {evaluation.role} · Evaluation {evaluation.id}
              </div>
            </div>
            <div className="flex items-center gap-3">
              {/* The total and band are exactly what the server computed -- never
                  recomputed here from the individual dimension scores. */}
              <span className="text-sm text-ink-dim">
                Total <span className="font-bold text-ink">{evaluation.total}</span>
              </span>
              <span className={`chip text-sm font-bold ${BAND_TONE[evaluation.band] ?? 'bg-surface-2 text-ink-dim'}`}>
                {BAND_LABEL[evaluation.band] ?? evaluation.band}
              </span>
            </div>
          </div>

          {evaluationHistory.length > 1 && (
            <div className="mb-4 rounded-xl border border-hairline bg-surface-2 px-4 py-3">
              <p className="mb-1.5 text-xs font-semibold uppercase tracking-wide text-ink-dim">
                Other evaluations for this application
              </p>
              <ul className="space-y-1 text-xs text-ink-muted">
                {evaluationHistory
                  .filter((row) => row.id !== evaluation.id)
                  .map((row) => (
                    <li key={row.id} className="flex flex-wrap items-center gap-2">
                      <span className="chip bg-surface-2 text-[10px] font-bold text-ink-dim">
                        {row.id === evaluationHistory[0]?.id ? 'Current' : 'Superseded'}
                      </span>
                      <span>{row.id}</span>
                      <span>
                        Total {row.total} · {BAND_LABEL[row.band] ?? row.band}
                      </span>
                      {row.created_at && <span>{new Date(row.created_at).toLocaleString()}</span>}
                    </li>
                  ))}
              </ul>
            </div>
          )}

          {/* A disqualifying flag outranks the total -- shown first and loudly,
              never quietly beside a total that on its own would look fine. */}
          {evaluation.flags.length > 0 && (
            <div className="mb-4 space-y-2">
              {evaluation.flags.map((f) => {
                const meta = CASE_STUDY_FLAGS[f] ?? { label: f, severity: 'note' as const }
                const tone =
                  meta.severity === 'disqualifying'
                    ? 'border-danger/40 bg-danger/10 text-danger'
                    : meta.severity === 'serious'
                      ? 'border-[#b7791f]/40 bg-[#b7791f]/10 text-[#b7791f]'
                      : 'border-hairline bg-surface-2 text-ink-muted'
                return (
                  <div key={f} className={`flex items-start gap-2 rounded-xl border px-4 py-2.5 text-sm ${tone}`}>
                    <FileWarning className="mt-0.5 h-4 w-4 shrink-0" />
                    <span>
                      <strong>{meta.label}.</strong>
                      {meta.severity === 'disqualifying' &&
                        ' This overrides the total above; the band is disqualified regardless of the score.'}
                    </span>
                  </div>
                )
              })}
            </div>
          )}

          <div className="space-y-3">
            {/* IMPORTANT 4b: rendered from the RESPONSE's own dimension
                metadata, never a local TypeScript constant -- a weight or
                label change in case_study_scoring.DIMENSIONS shows up here
                on the very next score, with no separate deploy. */}
            {evaluation.dimensions.map((d) => (
              <div key={d.key} className="rounded-xl border border-hairline p-4">
                <div className="mb-1.5 flex items-center justify-between gap-3">
                  <h3 className="text-sm font-semibold text-ink">{d.label}</h3>
                  <span className="text-xs text-ink-dim">
                    <span className="font-bold text-ink">{evaluation.scores[d.key] ?? 'n/a'}</span>/5 · weight{' '}
                    {d.weight}%
                  </span>
                </div>
                <p className="text-xs leading-relaxed text-ink-muted">
                  {evaluation.evidence[d.key] || 'No evidence citation returned.'}
                </p>
              </div>
            ))}
            {/* IMPORTANT 4c: a score key the metadata above does not cover
                (a renamed or newly added dimension the frontend has not
                been told about yet) still renders here -- "the evaluation
                renders in full" stays true regardless of drift, instead of
                the key silently vanishing. */}
            {Object.keys(evaluation.scores)
              .filter((key) => !evaluation.dimensions.some((d) => d.key === key))
              .map((key) => (
                <div key={key} className="rounded-xl border border-dashed border-hairline p-4">
                  <div className="mb-1.5 flex items-center justify-between gap-3">
                    <h3 className="text-sm font-semibold text-ink">{key}</h3>
                    <span className="text-xs text-ink-dim">
                      <span className="font-bold text-ink">{evaluation.scores[key]}</span>/5 · weight unknown
                    </span>
                  </div>
                  <p className="text-xs leading-relaxed text-ink-muted">
                    {evaluation.evidence[key] || 'No evidence citation returned.'}
                  </p>
                </div>
              ))}
          </div>

          <p className="mt-4 text-xs text-ink-dim">
            Scored against benchmark {evaluation.benchmark_id} by {evaluation.model}. Sources:{' '}
            {evaluation.sources.join(', ') || 'none recorded'}.
          </p>
        </div>
      )}
    </div>
  )
}
