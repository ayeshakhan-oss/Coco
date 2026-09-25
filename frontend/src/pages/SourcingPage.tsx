import { useEffect, useRef, useState } from 'react'
import { ExternalLink, Info, Loader2 } from 'lucide-react'
import { Spinner } from '../components/Spinner'
import { ApiError, api } from '../lib/api'
import type { SourcedCandidate, SourcingSummary } from '../lib/types'

// The 3-layer web search stays in Claude Code: it drives a local headless
// browser against a SearXNG instance answering an anti-bot proof-of-work, and
// the built-in search is blind to Pakistani LinkedIn. This page owns
// everything after the search.

const GENERIC_LOAD_ERROR = 'Could not load the sourcing pool. Try reloading the page.'

const OUTREACH_LABEL: Record<string, string> = {
  not_contacted: 'Not contacted',
  contacted: 'Contacted',
  replied_interested: 'Interested',
  replied_not_interested: 'Not interested',
  no_reply: 'No reply',
}

const OUTREACH_CLASS: Record<string, string> = {
  not_contacted: 'bg-ink-dim/10 text-ink-dim border-hairline',
  contacted: 'bg-blurple/10 text-blurple border-blurple/30',
  replied_interested: 'bg-success/10 text-success border-success/30',
  replied_not_interested: 'bg-ink-dim/10 text-ink-dim border-hairline',
  no_reply: 'bg-warning/10 text-warning border-warning/30',
}

// 🔴 Four states, never a boolean. "Not found" means the check did not come
// back; it is NOT evidence the person is invented, and must not be styled as
// though it were.
const VERIFICATION_LABEL: Record<string, string> = {
  confirmed: 'Verified',
  unconfirmed: 'Not re-checked',
  not_found: 'Check found nothing',
  no_url: 'No profile link',
}

export function SourcingPage() {
  const [rows, setRows] = useState<SourcedCandidate[]>([])
  const [summary, setSummary] = useState<SourcingSummary | null>(null)
  const [outreach, setOutreach] = useState<string>('')
  const [loaded, setLoaded] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [saving, setSaving] = useState<string | null>(null)
  const genRef = useRef(0)

  const load = () => {
    const gen = ++genRef.current
    setLoaded(false)
    Promise.all([
      api.sourcingPool(outreach ? { outreach_state: outreach } : {}),
      api.sourcingSummary(),
    ])
      .then(([p, s]) => {
        if (genRef.current !== gen) return
        setRows(p)
        setSummary(s)
        setError(null)
        setLoaded(true)
      })
      .catch(() => {
        if (genRef.current !== gen) return
        setError(GENERIC_LOAD_ERROR)
        setLoaded(true)
      })
  }

  useEffect(load, [outreach])

  const setState = (row: SourcedCandidate, state: string) => {
    if (saving) return
    setSaving(row.id)
    api
      .sourcingUpdate(row.id, { outreach_state: state })
      .then((updated) => {
        setRows((prev) => prev.map((r) => (r.id === row.id ? updated : r)))
        return api.sourcingSummary().then(setSummary)
      })
      .catch((e) => {
        setError(
          e instanceof ApiError
            ? e.message.replace(/^\d+:\s*/, '')
            : 'Could not update that.',
        )
      })
      .finally(() => setSaving(null))
  }

  return (
    <div className="mx-auto max-w-7xl px-8 py-7">
      <header className="mb-5">
        <h1 className="font-display text-2xl font-bold text-ink">Talent Sourcing</h1>
        <p className="mt-1 text-sm text-ink-muted">
          The passive candidate pool and who has been approached. Searching for new
          people still runs in Claude Code.
        </p>
      </header>

      {summary && (
        <>
          <div className="grid grid-cols-2 gap-3 lg:grid-cols-5">
            {[
              ['In the pool', summary.total],
              ['Not contacted', summary.outreach.not_contacted ?? 0],
              ['Contacted', summary.outreach.contacted ?? 0],
              ['Said yes', summary.outreach.replied_interested ?? 0],
              ['In Markaz', summary.in_markaz],
            ].map(([label, value]) => (
              <div key={String(label)} className="rounded-2xl border border-hairline bg-surface p-4">
                <div className="text-sm font-medium text-ink-muted">{label}</div>
                <div className="mt-1 text-2xl font-bold tabular-nums text-ink">{value}</div>
              </div>
            ))}
          </div>

          {/* The verification breakdown is shown in full rather than folded
              into a single "verified" number. */}
          <div className="mt-3 flex gap-2.5 rounded-xl border border-hairline bg-surface px-4 py-3 text-sm text-ink-muted">
            <Info className="mt-0.5 h-4 w-4 shrink-0 text-ink-dim" />
            <div>
              <p>
                Profiles:{' '}
                {Object.entries(summary.verification)
                  .filter(([, n]) => n)
                  .map(([k, n]) => `${n} ${VERIFICATION_LABEL[k]?.toLowerCase() ?? k}`)
                  .join(' · ')}
                .
              </p>
              <p className="mt-1 text-xs">{summary.caveat}</p>
            </div>
          </div>
        </>
      )}

      <div className="mt-4 flex flex-wrap gap-2">
        {['', 'not_contacted', 'contacted', 'replied_interested', 'no_reply'].map((s) => (
          <button
            key={s || 'all'}
            type="button"
            onClick={() => setOutreach(s)}
            className={`rounded-full border px-3 py-1 text-xs font-medium transition-colors ${
              outreach === s
                ? 'border-blurple bg-blurple/10 text-blurple'
                : 'border-hairline text-ink-muted hover:bg-elevated'
            }`}
          >
            {s ? OUTREACH_LABEL[s] : 'Everyone'}
          </button>
        ))}
      </div>

      {error && <p className="mt-4 text-sm text-danger">{error}</p>}

      {!loaded ? (
        <div className="mt-5">
          <Spinner label="Loading the pool…" />
        </div>
      ) : rows.length === 0 ? (
        <p className="mt-5 text-sm text-ink-dim">Nobody matches that filter.</p>
      ) : (
        <div className="mt-4 overflow-hidden rounded-2xl border border-hairline bg-surface">
          <table className="w-full text-sm">
            <thead className="border-b border-hairline bg-elevated text-left text-xs uppercase tracking-wide text-ink-dim">
              <tr>
                <th className="px-4 py-2.5 font-semibold">Person</th>
                <th className="px-4 py-2.5 font-semibold">Experience</th>
                <th className="px-4 py-2.5 font-semibold">Profile</th>
                <th className="px-4 py-2.5 font-semibold">Outreach</th>
                <th className="px-4 py-2.5" />
              </tr>
            </thead>
            <tbody>
              {rows.map((r) => (
                <tr key={r.id} className="border-b border-hairline/60 last:border-0 align-top">
                  <td className="px-4 py-2.5">
                    <div className="font-medium text-ink">{r.name}</div>
                    <div className="text-xs text-ink-dim">
                      {[r.title, r.organization, r.location].filter(Boolean).join(' · ') || '—'}
                    </div>
                    {r.role_label && (
                      <div className="text-[11px] text-ink-dim">sourced for {r.role_label}</div>
                    )}
                  </td>
                  <td className="px-4 py-2.5 text-xs text-ink-muted">
                    {/* Unknown, not zero, where the note did not actually say. */}
                    {r.years != null ? (
                      `${r.years} years`
                    ) : (
                      <span className="italic text-ink-dim" title={r.years_note ?? ''}>
                        not established
                      </span>
                    )}
                  </td>
                  <td className="px-4 py-2.5 text-xs">
                    {r.linkedin_url ? (
                      <a
                        href={r.linkedin_url}
                        target="_blank"
                        rel="noreferrer"
                        className="text-blurple hover:underline"
                      >
                        profile <ExternalLink className="inline h-3 w-3" />
                      </a>
                    ) : (
                      <span className="text-ink-dim">none</span>
                    )}
                    <div className="text-[11px] text-ink-dim">
                      {VERIFICATION_LABEL[r.verification_state] ?? r.verification_state}
                    </div>
                  </td>
                  <td className="px-4 py-2.5">
                    <span
                      className={`inline-block rounded-full border px-2 py-0.5 text-[11px] font-semibold ${
                        OUTREACH_CLASS[r.outreach_state]
                      }`}
                    >
                      {OUTREACH_LABEL[r.outreach_state]}
                    </span>
                    {r.markaz_application_id && (
                      <div className="mt-1 text-[11px] text-success">
                        in Markaz · application {r.markaz_application_id}
                      </div>
                    )}
                  </td>
                  <td className="px-4 py-2.5 text-right">
                    {saving === r.id ? (
                      <Loader2 className="ml-auto h-4 w-4 animate-spin text-ink-dim" />
                    ) : (
                      <select
                        className="input w-40 text-xs"
                        value={r.outreach_state}
                        onChange={(e) => setState(r, e.target.value)}
                        disabled={!!r.markaz_application_id}
                        title={
                          r.markaz_application_id
                            ? 'Already in Markaz, so their state is fixed'
                            : undefined
                        }
                      >
                        {Object.entries(OUTREACH_LABEL).map(([k, v]) => (
                          <option key={k} value={k}>
                            {v}
                          </option>
                        ))}
                      </select>
                    )}
                    {/* Explains why, rather than silently disabling a button. */}
                    {r.blocked_from_markaz && !r.markaz_application_id && (
                      <div className="mt-1 max-w-[16rem] text-[11px] text-ink-dim">
                        Markaz: {r.blocked_from_markaz}
                      </div>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
