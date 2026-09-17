import { useQuery } from '@tanstack/react-query'
import { AlertTriangle, CheckCircle2, ClipboardCheck, Loader2, Search } from 'lucide-react'
import { useEffect, useRef, useState } from 'react'
import { Spinner } from '../components/Spinner'
import { ApiError, api } from '../lib/api'
import { fullName } from '../lib/format'
import { canApprove, canEdit } from '../lib/roles'
import type { QueueRow, ValuesScorecardDraft, ValuesScorecardDraftValue } from '../lib/types'

const RATING_OPTIONS = ['+', '+/-', '-'] as const
const RATING_TONE: Record<string, string> = {
  '+': 'bg-green/15 text-green',
  '+/-': 'bg-[#b7791f]/15 text-[#b7791f]',
  '-': 'bg-danger/15 text-danger',
}
const EVIDENCE_FIELDS: { key: 'deepDive' | 'curveBall' | 'microCase'; label: string }[] = [
  { key: 'deepDive', label: 'Deep Dive' },
  { key: 'curveBall', label: 'Curve Ball' },
  { key: 'microCase', label: 'Micro Case' },
]

// The three distinct 409s the submit endpoint can return, each needing its
// own plain-language message and its own follow-up (or none). Detected by
// matching the router's actual error text, not by guessing a shape.
type SubmitConflict =
  | { kind: 'submitted' }
  | { kind: 'has_scorecard' }
  | { kind: 'stale'; newerId: number | null; raw: string }

const stripStatus = (msg: string) => msg.replace(/^\d+:\s*/, '')

export function ValuesScorecardPage() {
  const meQ = useQuery({ queryKey: ['me'], queryFn: api.me, retry: false })
  const role = meQ.data?.app_role
  const isEditor = canEdit(role)
  const isApprover = canApprove(role)

  /* ── Step 1: pick an application ─────────────────────────────────────── */
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
    if (!debouncedQuery || !isEditor) {
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
  }, [debouncedQuery, isEditor])

  const [selected, setSelected] = useState<QueueRow | null>(null)
  const [transcript, setTranscript] = useState('')
  const [host, setHost] = useState('')
  const [generating, setGenerating] = useState(false)
  const [generateError, setGenerateError] = useState<string | null>(null)

  /* ── Step 2: the draft ───────────────────────────────────────────────── */
  const [draft, setDraft] = useState<ValuesScorecardDraft | null>(null)
  const [loadedDraftId, setLoadedDraftId] = useState<string | null>(null)
  const [localValues, setLocalValues] = useState<ValuesScorecardDraftValue[]>([])
  const [localFinalComments, setLocalFinalComments] = useState('')
  const dirty = useRef(false)
  const [saving, setSaving] = useState(false)
  const [saveError, setSaveError] = useState<string | null>(null)

  // Reinitialise the editable local copy ONLY when a *different* draft has
  // loaded -- never on every server response, or a save's own response would
  // overwrite whatever the user is mid-typing.
  useEffect(() => {
    if (draft && draft.id !== loadedDraftId) {
      setLocalValues(draft.values)
      setLocalFinalComments(draft.final_comments)
      setLoadedDraftId(draft.id)
      dirty.current = false
    }
  }, [draft, loadedDraftId])

  async function generate() {
    if (!selected || !host.trim()) return
    setGenerating(true)
    setGenerateError(null)
    try {
      const d = await api.generateValuesScorecard(selected.application_id, transcript, host.trim())
      setDraft(d)
    } catch (e) {
      setGenerateError(stripStatus((e as ApiError).message))
    } finally {
      setGenerating(false)
    }
  }

  async function save() {
    if (!draft) return
    setSaving(true)
    setSaveError(null)
    try {
      // The response is the ONLY source for verdict/tally/gwc/proceed --
      // they are never recomputed here, only displayed from what comes back.
      const d = await api.editValuesScorecardDraft(draft.id, {
        values: localValues,
        final_comments: localFinalComments,
      })
      setDraft(d)
      dirty.current = false
    } catch (e) {
      setSaveError(stripStatus((e as ApiError).message))
    } finally {
      setSaving(false)
    }
  }

  useEffect(() => {
    if (!draft || draft.status !== 'draft' || !isEditor || !dirty.current) return
    const t = setTimeout(save, 900)
    return () => clearTimeout(t)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [localValues, localFinalComments])

  function updateEvidence(i: number, field: 'deepDive' | 'curveBall' | 'microCase', value: string) {
    dirty.current = true
    setLocalValues((prev) => prev.map((v, idx) => (idx === i ? { ...v, [field]: value } : v)))
  }
  function updateRating(i: number, rating: string) {
    dirty.current = true
    setLocalValues((prev) => prev.map((v, idx) => (idx === i ? { ...v, rating } : v)))
  }

  /* ── Step 3: submit to Markaz (approver only) ────────────────────────── */
  const [submitting, setSubmitting] = useState(false)
  const [submitError, setSubmitError] = useState<string | null>(null)
  const [conflict, setConflict] = useState<SubmitConflict | null>(null)

  async function doSubmit(overwrite: boolean) {
    if (!draft) return
    const ok = window.confirm(
      `Submit this values scorecard for ${draft.candidate_name} (application ${draft.application_id}) to Markaz?` +
        (overwrite ? ' This will overwrite the scorecard already on file for this application.' : ' This writes a permanent hiring record.'),
    )
    if (!ok) return
    setSubmitting(true)
    setSubmitError(null)
    setConflict(null)
    try {
      const d = await api.submitValuesScorecardDraft(draft.id, overwrite)
      setDraft(d)
    } catch (e) {
      const err = e as ApiError
      if (err.status === 409) {
        const msg = err.message
        if (msg.includes('already been submitted to Markaz')) {
          setConflict({ kind: 'submitted' })
          // Our copy of the draft is stale (it still says "draft") -- re-read it.
          api.valuesScorecardDraft(draft.id).then(setDraft).catch(() => {})
        } else if (msg.includes('already has a values scorecard in Markaz')) {
          setConflict({ kind: 'has_scorecard' })
        } else if (msg.includes('is not the most recently updated application')) {
          const m = msg.match(/application (\d+) is newer/)
          setConflict({ kind: 'stale', newerId: m ? Number(m[1]) : null, raw: stripStatus(msg) })
        } else {
          setSubmitError(stripStatus(msg))
        }
      } else {
        setSubmitError(stripStatus(err.message))
      }
    } finally {
      setSubmitting(false)
    }
  }

  function startOver() {
    setSelected(null)
    setTranscript('')
    setHost('')
    setGenerateError(null)
    setDraft(null)
    setLoadedDraftId(null)
    setLocalValues([])
    setLocalFinalComments('')
    setSaveError(null)
    setSubmitError(null)
    setConflict(null)
    setQuery('')
    setResults([])
  }

  if (meQ.isLoading) return <Spinner label="Loading…" />

  if (!isEditor) {
    return (
      <div className="mx-auto max-w-3xl px-8 py-7">
        <header className="mb-4">
          <h1 className="font-display text-2xl font-bold text-ink">Values Scorecards</h1>
        </header>
        <div className="card p-8 text-center text-sm text-ink-dim">
          You need editor access to draft a values scorecard. Ask an admin to change your role if you believe this is wrong.
        </div>
      </div>
    )
  }

  return (
    <div className="mx-auto max-w-4xl px-8 py-7">
      <header className="mb-5 flex items-center justify-between gap-3">
        <div>
          <h1 className="font-display text-2xl font-bold text-ink">Values Scorecards</h1>
          <p className="mt-1 text-sm text-ink-muted">
            Paste a values interview transcript, review the full draft, then submit it to Markaz.
          </p>
        </div>
        {(draft || selected) && (
          <button type="button" onClick={startOver} className="btn btn-ghost h-8 text-sm">
            New scorecard
          </button>
        )}
      </header>

      {!draft && (
        <div className="card p-5">
          <h2 className="mb-3 text-sm font-semibold text-ink">1. Pick an application</h2>
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

          {selected && (
            <div className="mt-5 space-y-3">
              <h2 className="text-sm font-semibold text-ink">2. Paste the transcript</h2>
              <input
                value={host}
                onChange={(e) => setHost(e.target.value)}
                placeholder="Interview host name"
                className="input"
              />
              <textarea
                value={transcript}
                onChange={(e) => setTranscript(e.target.value)}
                placeholder="Paste the full values interview transcript here…"
                rows={10}
                className="input font-mono text-xs leading-relaxed"
              />
              {generateError && (
                <div className="flex items-start gap-2 rounded-xl border border-danger/30 bg-danger/5 px-4 py-2.5 text-sm text-danger">
                  <AlertTriangle className="mt-0.5 h-4 w-4 shrink-0" />
                  <span>{generateError}</span>
                </div>
              )}
              <button
                type="button"
                onClick={generate}
                disabled={generating || !transcript.trim() || !host.trim()}
                className="btn btn-primary"
              >
                {generating ? <Loader2 className="h-4 w-4 animate-spin" /> : <ClipboardCheck className="h-4 w-4" />}
                {generating ? 'Scoring…' : 'Generate draft'}
              </button>
            </div>
          )}
        </div>
      )}

      {draft && (
        <div className="mt-6 space-y-5">
          {/* The draft is ALWAYS shown in full before any write is possible --
              this is the locked process rule and the reason this screen exists. */}
          <div className="card flex flex-wrap items-center justify-between gap-3 p-5">
            <div>
              <div className="text-sm font-medium text-ink">{draft.candidate_name}</div>
              <div className="text-xs text-ink-dim">
                Application #{draft.application_id} · Host: {draft.host} · Status: {draft.status}
              </div>
            </div>
            <div className="flex items-center gap-3">
              <span
                className={`chip text-sm font-bold ${draft.verdict === 'PASS' ? 'bg-green/15 text-green' : 'bg-danger/15 text-danger'}`}
              >
                {draft.verdict}
              </span>
              <span className="text-xs text-ink-dim">
                {draft.tally.plus}(+) / {draft.tally.plus_minus}(+/-) / {draft.tally.minus}(-)
              </span>
              <span className="text-xs text-ink-dim">Proceed to right seat: {draft.proceed ? 'Yes' : 'No'}</span>
            </div>
          </div>

          <div className="space-y-4">
            {localValues.map((v, i) => (
              <div key={v.name} className="card p-5">
                <div className="mb-3 flex items-center justify-between gap-3">
                  <h3 className="font-display text-sm font-bold text-ink">{v.name}</h3>
                  <select
                    value={v.rating}
                    onChange={(e) => updateRating(i, e.target.value)}
                    disabled={draft.status !== 'draft'}
                    className={`input w-24 text-center text-sm font-semibold ${RATING_TONE[v.rating] ?? ''}`}
                  >
                    {RATING_OPTIONS.map((r) => (
                      <option key={r} value={r}>
                        {r}
                      </option>
                    ))}
                  </select>
                </div>
                <div className="grid grid-cols-1 gap-3 md:grid-cols-3">
                  {EVIDENCE_FIELDS.map((f) => (
                    <div key={f.key}>
                      <label className="mb-1 block text-xs font-semibold uppercase tracking-wide text-ink-dim">
                        {f.label}
                      </label>
                      <textarea
                        value={v[f.key]}
                        onChange={(e) => updateEvidence(i, f.key, e.target.value)}
                        disabled={draft.status !== 'draft'}
                        rows={5}
                        className="input text-xs leading-relaxed"
                      />
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>

          <div className="card p-5">
            <label className="mb-1 block text-xs font-semibold uppercase tracking-wide text-ink-dim">
              Final comments
            </label>
            <textarea
              value={localFinalComments}
              onChange={(e) => {
                dirty.current = true
                setLocalFinalComments(e.target.value)
              }}
              disabled={draft.status !== 'draft'}
              rows={3}
              className="input text-sm"
            />
            <p className="mt-1 text-xs text-ink-dim">
              The verdict/tally prefix here is always rewritten by the server from the current ratings; only the
              narrative after it is yours to edit.
            </p>
          </div>

          {/* GWC is shown only when the server actually returned it (dropped on OUT). */}
          {draft.gwc && (
            <div className="card p-5">
              <h3 className="mb-3 font-display text-sm font-bold text-ink">Get It, Want It, Capacity to Do It</h3>
              <div className="grid grid-cols-3 gap-3 text-sm">
                <div>
                  <div className="text-xs text-ink-dim">Gets it</div>
                  <div className="font-medium text-ink">{draft.gwc.gets_it}</div>
                </div>
                <div>
                  <div className="text-xs text-ink-dim">Wants it</div>
                  <div className="font-medium text-ink">{draft.gwc.wants_it}</div>
                </div>
                <div>
                  <div className="text-xs text-ink-dim">Capacity</div>
                  <div className="font-medium text-ink">{draft.gwc.capacity}</div>
                </div>
              </div>
            </div>
          )}

          {saveError && <p className="text-sm text-danger">Could not save your edit: {saveError}</p>}
          {saving && <p className="text-xs text-ink-dim">Saving…</p>}

          {/* ── Submit to Markaz — approver only ──────────────────────────── */}
          <div className="card p-5">
            {draft.status === 'submitted' && !conflict ? (
              <div className="flex items-center gap-2 rounded-xl border border-green/30 bg-green/10 px-4 py-2.5 text-sm text-ink">
                <CheckCircle2 className="h-4 w-4 text-green" />
                Submitted to Markaz{draft.submitted_at ? ` at ${new Date(draft.submitted_at).toLocaleString()}` : ''}.
              </div>
            ) : !isApprover ? (
              <p className="text-sm text-ink-dim">
                Only an approver can submit this scorecard to Markaz. Ask an approver to review and submit it.
              </p>
            ) : (
              <div className="space-y-3">
                {conflict?.kind === 'submitted' && (
                  <div className="flex items-center gap-2 rounded-xl border border-hairline bg-surface-2 px-4 py-2.5 text-sm text-ink-muted">
                    <CheckCircle2 className="h-4 w-4 text-green" />
                    This scorecard has already been submitted to Markaz. Nothing more to do here.
                  </div>
                )}
                {conflict?.kind === 'has_scorecard' && (
                  <div className="space-y-2 rounded-xl border border-danger/30 bg-danger/5 px-4 py-2.5 text-sm text-ink">
                    <div className="flex items-start gap-2 text-danger">
                      <AlertTriangle className="mt-0.5 h-4 w-4 shrink-0" />
                      <span>
                        Application {draft.application_id} already has a values scorecard in Markaz. Submitting
                        again would replace it.
                      </span>
                    </div>
                    <button
                      type="button"
                      onClick={() => doSubmit(true)}
                      disabled={submitting}
                      className="btn btn-ghost h-8 border-danger/40 text-danger text-sm"
                    >
                      Overwrite the existing scorecard
                    </button>
                  </div>
                )}
                {conflict?.kind === 'stale' && (
                  <div className="flex items-start gap-2 rounded-xl border border-danger/30 bg-danger/5 px-4 py-2.5 text-sm text-danger">
                    <AlertTriangle className="mt-0.5 h-4 w-4 shrink-0" />
                    <span>
                      Application {draft.application_id} is not the most recently updated application for this
                      candidate and job
                      {conflict.newerId ? ` — application ${conflict.newerId} is newer` : ''}. This draft cannot be
                      forced through; retarget it to the newer application instead.
                    </span>
                  </div>
                )}
                {submitError && (
                  <div className="flex items-start gap-2 rounded-xl border border-danger/30 bg-danger/5 px-4 py-2.5 text-sm text-danger">
                    <AlertTriangle className="mt-0.5 h-4 w-4 shrink-0" />
                    <span>{submitError}</span>
                  </div>
                )}
                {draft.status === 'draft' && (!conflict || conflict.kind === 'has_scorecard') && (
                  <button
                    type="button"
                    onClick={() => doSubmit(false)}
                    disabled={submitting || saving}
                    className="btn btn-primary"
                  >
                    {submitting ? <Loader2 className="h-4 w-4 animate-spin" /> : <ClipboardCheck className="h-4 w-4" />}
                    {submitting ? 'Submitting…' : 'Submit to Markaz'}
                  </button>
                )}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
