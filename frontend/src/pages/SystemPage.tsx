import { useEffect, useState } from 'react'
import { AlertTriangle, CheckCircle2, Database, Info, XCircle } from 'lucide-react'
import { Spinner } from '../components/Spinner'
import { api } from '../lib/api'
import type { SystemActivity, SystemHealth } from '../lib/types'

// Skill 04 is infrastructure, so this page answers one question: is Coco
// healthy, and if not, where. It shows the known-broken things even when
// everything else is green, because a page that only ever shows green teaches
// people that the absence of an alarm means everything works.

const SEVERITY_CLASS: Record<string, string> = {
  high: 'border-danger/30 bg-danger/5 text-danger',
  medium: 'border-warning/40 bg-warning/5 text-warning',
  low: 'border-hairline bg-elevated text-ink-muted',
}

export function SystemPage() {
  const [health, setHealth] = useState<SystemHealth | null>(null)
  const [activity, setActivity] = useState<SystemActivity | null>(null)
  const [loaded, setLoaded] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    api
      .systemHealth()
      .then(setHealth)
      .catch(() => setError('Could not read system health.'))
      .finally(() => setLoaded(true))
    // Activity is editor-gated, so a viewer simply does not get this panel.
    // That is not an error worth showing them.
    api.systemActivity().then(setActivity).catch(() => setActivity(null))
  }, [])

  if (!loaded) {
    return (
      <div className="mx-auto max-w-6xl px-8 py-7">
        <Spinner label="Checking…" />
      </div>
    )
  }

  const ok = health?.summary.status === 'ok'

  return (
    <div className="mx-auto max-w-6xl px-8 py-7">
      <header className="mb-5">
        <h1 className="font-display text-2xl font-bold text-ink">Data &amp; Systems</h1>
        <p className="mt-1 text-sm text-ink-muted">
          What is configured, what exists in the database, and what is known to be
          broken.
        </p>
      </header>

      {error && <p className="mb-4 text-sm text-danger">{error}</p>}

      {health && (
        <>
          <div
            className={`flex gap-3 rounded-2xl border px-4 py-3.5 ${
              ok
                ? 'border-success/30 bg-success/5'
                : 'border-warning/40 bg-warning/5'
            }`}
          >
            {ok ? (
              <CheckCircle2 className="mt-0.5 h-5 w-5 shrink-0 text-success" />
            ) : (
              <AlertTriangle className="mt-0.5 h-5 w-5 shrink-0 text-warning" />
            )}
            <div>
              <p className={`text-sm font-semibold ${ok ? 'text-success' : 'text-warning'}`}>
                {health.summary.headline}
              </p>
              <p className="mt-0.5 text-xs text-ink-muted">
                {health.summary.known_gaps} known gap
                {health.summary.known_gaps === 1 ? '' : 's'} listed below. Checked{' '}
                {new Date(health.summary.checked_at).toLocaleString()}.
              </p>
            </div>
          </div>

          {/* Integrations */}
          <section className="mt-4 grid gap-3 sm:grid-cols-2">
            {health.integrations.map((i) => (
              <div
                key={i.key}
                className="rounded-2xl border border-hairline bg-surface p-4"
              >
                <div className="flex items-center gap-2">
                  {i.configured ? (
                    <CheckCircle2 className="h-4 w-4 text-success" />
                  ) : (
                    <XCircle className="h-4 w-4 text-danger" />
                  )}
                  <span className="text-sm font-semibold text-ink">{i.label}</span>
                </div>
                <p className="mt-1 text-xs text-ink-muted">{i.detail}</p>
              </div>
            ))}
          </section>
          <p className="mt-2 text-[11px] text-ink-dim">
            Configured means the app could use it, not that it currently works. A
            token can be present and expired.
          </p>

          {/* Tables */}
          <section className="mt-5 overflow-hidden rounded-2xl border border-hairline bg-surface">
            <div className="flex items-center gap-2 border-b border-hairline bg-elevated px-4 py-2.5 text-xs font-semibold uppercase tracking-wide text-ink-dim">
              <Database className="h-3.5 w-3.5" /> App-owned tables
            </div>
            <table className="w-full text-sm">
              <tbody>
                {health.tables.tables.map((t) => (
                  <tr key={t.name} className="border-b border-hairline/60 last:border-0">
                    <td className="px-4 py-2">
                      <div className="font-mono text-xs text-ink">{t.name}</div>
                      <div className="text-[11px] text-ink-dim">{t.purpose}</div>
                    </td>
                    <td className="px-4 py-2 text-right tabular-nums">
                      {!t.exists ? (
                        <span className="text-xs font-semibold text-danger">missing</span>
                      ) : t.rows == null ? (
                        <span className="text-xs text-ink-dim">unreadable</span>
                      ) : (
                        <span className="text-ink">{t.rows.toLocaleString()}</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            <p className="flex gap-2 border-t border-hairline px-4 py-3 text-xs text-ink-muted">
              <Info className="mt-0.5 h-3.5 w-3.5 shrink-0 text-ink-dim" />
              <span>{health.tables.note}</span>
            </p>
          </section>

          {/* Known gaps — shown even when everything above is green */}
          <section className="mt-5 space-y-2">
            <h2 className="text-xs font-semibold uppercase tracking-wide text-ink-dim">
              Known gaps
            </h2>
            {health.known_gaps.map((g) => (
              <div
                key={g.key}
                className={`rounded-xl border px-4 py-3 ${SEVERITY_CLASS[g.severity] ?? SEVERITY_CLASS.low}`}
              >
                <div className="text-sm font-semibold">{g.title}</div>
                <p className="mt-1 text-xs opacity-90">{g.detail}</p>
              </div>
            ))}
          </section>
        </>
      )}

      {/* What Coco has sent — letters and invites together */}
      {activity && (
        <section className="mt-5 overflow-hidden rounded-2xl border border-hairline bg-surface">
          <div className="border-b border-hairline bg-elevated px-4 py-2.5 text-xs font-semibold uppercase tracking-wide text-ink-dim">
            Recent sends
          </div>
          {activity.last_sync && (
            <p className="border-b border-hairline px-4 py-2 text-xs text-ink-muted">
              Mailbox last read{' '}
              {new Date(activity.last_sync.started_at).toLocaleString()} (
              {activity.last_sync.status}, {activity.last_sync.messages_scanned} messages
              scanned).
            </p>
          )}
          {activity.error ? (
            <p className="px-4 py-4 text-sm text-warning">{activity.error}</p>
          ) : activity.items.length === 0 ? (
            <p className="px-4 py-4 text-sm text-ink-dim">Nothing sent yet.</p>
          ) : (
            <table className="w-full text-sm">
              <tbody>
                {activity.items.map((a, idx) => (
                  <tr key={idx} className="border-b border-hairline/60 last:border-0">
                    <td className="px-4 py-2">
                      <span className="text-ink">{a.who || '(unnamed)'}</span>
                      <span className="ml-2 text-xs text-ink-dim">{a.what}</span>
                    </td>
                    <td className="px-4 py-2 text-right text-xs">
                      <span
                        className={
                          a.kind === 'invite' ? 'text-blurple' : 'text-ink-muted'
                        }
                      >
                        {a.kind}
                      </span>
                      {!a.is_live && (
                        <span className="ml-2 text-ink-dim">pilot</span>
                      )}
                      <div className="text-ink-dim">
                        {new Date(a.at).toLocaleDateString()}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </section>
      )}
    </div>
  )
}
