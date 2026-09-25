import { useEffect, useMemo, useRef, useState } from 'react'
import { AlertTriangle, CheckCircle2, Link2, Loader2, Send, ShieldAlert } from 'lucide-react'
import { Spinner } from '../components/Spinner'
import { ApiError, api } from '../lib/api'
import type { InviteLink, InvitePreview, InviteSendRecord, InviteType } from '../lib/types'

// 🔴 THE BOOKING LINK IS THE DANGEROUS PART OF THIS PAGE. Growth Manager runs
// as two live roles, Lahore and Karachi, with separate schedules. Sending the
// wrong one books a candidate into the wrong city and nothing complains, so
// the link must be FETCHED and its page title read before a live send. The
// Verify button is not a convenience; it is the gate.

const GENERIC_LOAD_ERROR = 'Could not load the invite types. Try reloading the page.'

const CONFIRM_LABEL: Record<string, string> = {
  booking: 'Candidate books a slot',
  reply: 'Candidate replies to confirm',
  none: 'Nothing to arrange',
}

// Friendly labels for the field names the API asks for.
const FIELD_LABEL: Record<string, string> = {
  first_name: 'First name',
  full_name: 'Full name',
  position: 'Position',
  jd_url: 'JD link',
  prep_url: 'Prep guide link',
  booking_url: 'Booking link',
  context: 'Why we are reaching out',
  previous_role: 'Role they interviewed for',
  interview_date: 'Interview date',
  interview_time: 'Interview time',
  meet_url: 'Google Meet link',
  activity_date: 'Activity date',
  start_time: 'Start time',
  end_time: 'End time',
  venue: 'Venue',
  maps_url: 'Google Maps link',
  confirm_by_date: 'Calendar invite goes out by',
}

// Optional extras a type accepts but does not require.
const OPTIONAL_BY_TYPE: Record<string, string[]> = {
  interview_reminder: ['meet_url'],
  assessment_center: ['maps_url'],
  warm_bench_opportunity: ['context'],
  keep_in_touch: ['context'],
}

// Fields whose value comes from the verified configuration, not from typing.
const FROM_CONFIG = new Set(['booking_url', 'jd_url', 'prep_url'])

export function InvitesPage() {
  const [types, setTypes] = useState<InviteType[]>([])
  const [links, setLinks] = useState<InviteLink[]>([])
  const [sends, setSends] = useState<InviteSendRecord[]>([])
  const [selected, setSelected] = useState<string>('')
  const [applicationId, setApplicationId] = useState<string>('')
  const [fields, setFields] = useState<Record<string, string>>({})
  const [preview, setPreview] = useState<InvitePreview | null>(null)
  const [loaded, setLoaded] = useState(false)
  const [busy, setBusy] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [notice, setNotice] = useState<string | null>(null)
  const genRef = useRef(0)

  const type = useMemo(() => types.find((t) => t.key === selected), [types, selected])
  const link = useMemo(
    () => links.find((l) => l.invite_type === selected) ?? null,
    [links, selected],
  )

  useEffect(() => {
    Promise.all([api.inviteTypes(), api.inviteLinks(), api.inviteSends()])
      .then(([t, l, s]) => {
        setTypes(t)
        setLinks(l)
        setSends(s)
        if (!selected && t.length) setSelected(t[0].key)
        setLoaded(true)
      })
      .catch(() => {
        setError(GENERIC_LOAD_ERROR)
        setLoaded(true)
      })
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  // Changing type resets the form: carrying a venue across from an assessment
  // centre into a values invite is how a field ends up in the wrong email.
  useEffect(() => {
    setFields({})
    setPreview(null)
    setNotice(null)
  }, [selected])

  const askedFields = useMemo(() => {
    if (!type) return []
    const extras = OPTIONAL_BY_TYPE[type.key] ?? []
    return [...type.required, ...extras].filter((f) => !FROM_CONFIG.has(f))
  }, [type])

  const doPreview = () => {
    if (!type) return
    const gen = ++genRef.current
    setBusy('preview')
    setError(null)
    api
      .invitePreview({
        invite_type: type.key,
        application_id: applicationId ? Number(applicationId) : null,
        fields,
      })
      .then((p) => {
        if (genRef.current !== gen) return
        setPreview(p)
      })
      .catch((e) => setError(e instanceof ApiError ? e.message.replace(/^\d+:\s*/, '') : 'Could not build the preview.'))
      .finally(() => setBusy(null))
  }

  const doVerify = () => {
    if (!link) return
    setBusy('verify')
    api
      .inviteLinkVerify(link.id)
      .then((updated) => {
        setLinks((prev) => prev.map((l) => (l.id === updated.id ? updated : l)))
        setNotice(
          updated.verified_title
            ? `The booking page is titled "${updated.verified_title}".`
            : `The link could not be verified: ${updated.verify_error ?? 'unknown reason'}`,
        )
        if (preview) doPreview()
      })
      .catch((e) => setError(e instanceof ApiError ? e.message.replace(/^\d+:\s*/, '') : 'Could not verify that link.'))
      .finally(() => setBusy(null))
  }

  const doSend = (live: boolean) => {
    if (!type) return
    setBusy(live ? 'live' : 'pilot')
    setError(null)
    api
      .inviteSend({
        invite_type: type.key,
        application_id: applicationId ? Number(applicationId) : null,
        subject: preview?.subject ?? null,
        live,
        fields,
      })
      .then((rec) => {
        setSends((prev) => [rec, ...prev])
        setNotice(
          live
            ? `Sent to ${rec.to_address}.`
            : `Pilot sent to ${rec.to_address}. Nobody else received it.`,
        )
      })
      .catch((e) => setError(e instanceof ApiError ? e.message.replace(/^\d+:\s*/, '') : 'The invite was not sent.'))
      .finally(() => setBusy(null))
  }

  const blocked = (preview?.blockers.length ?? 0) > 0
  const canPilot = !!preview && preview.missing.length === 0

  if (!loaded) {
    return (
      <div className="mx-auto max-w-7xl px-8 py-7">
        <Spinner label="Loading invite types…" />
      </div>
    )
  }

  return (
    <div className="mx-auto max-w-7xl px-8 py-7">
      <header className="mb-5">
        <h1 className="font-display text-2xl font-bold text-ink">Candidate Invites</h1>
        <p className="mt-1 text-sm text-ink-muted">
          Seven invite types in the locked design. A pilot goes to Ayesha alone; a live
          send needs a booking link that has been fetched and checked.
        </p>
      </header>

      {error && (
        <p className="mb-4 rounded-xl border border-danger/30 bg-danger/5 px-4 py-3 text-sm text-danger">
          {error}
        </p>
      )}
      {notice && (
        <p className="mb-4 rounded-xl border border-hairline bg-surface px-4 py-3 text-sm text-ink-muted">
          {notice}
        </p>
      )}

      <div className="grid gap-5 lg:grid-cols-[22rem_1fr]">
        <div className="space-y-4">
          {/* Type */}
          <section className="rounded-2xl border border-hairline bg-surface p-4">
            <label className="text-xs font-semibold uppercase tracking-wide text-ink-dim">
              Invite type
            </label>
            <select
              className="input mt-2 w-full text-sm"
              value={selected}
              onChange={(e) => setSelected(e.target.value)}
            >
              {types.map((t) => (
                <option key={t.key} value={t.key}>
                  {t.label}
                </option>
              ))}
            </select>
            {type && (
              <>
                <p className="mt-2 text-xs text-ink-dim">{type.note}</p>
                <p className="mt-1 text-xs font-medium text-ink-muted">
                  {CONFIRM_LABEL[type.confirm]}
                </p>
              </>
            )}
          </section>

          {/* The booking link and its proof */}
          {type?.confirm === 'booking' && (
            <section className="rounded-2xl border border-hairline bg-surface p-4">
              <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wide text-ink-dim">
                <Link2 className="h-3.5 w-3.5" /> Booking link
              </div>
              {link?.booking_url ? (
                <>
                  <p className="mt-2 break-all text-xs text-ink-muted">{link.booking_url}</p>
                  {link.verified_title ? (
                    <div
                      className={`mt-2 flex gap-2 rounded-lg border px-3 py-2 text-xs ${
                        link.title_matches_expected === false
                          ? 'border-warning/40 bg-warning/5 text-warning'
                          : 'border-success/30 bg-success/5 text-success'
                      }`}
                    >
                      {link.title_matches_expected === false ? (
                        <AlertTriangle className="mt-0.5 h-3.5 w-3.5 shrink-0" />
                      ) : (
                        <CheckCircle2 className="mt-0.5 h-3.5 w-3.5 shrink-0" />
                      )}
                      <span>
                        The page is titled &ldquo;{link.verified_title}&rdquo;
                        {link.expected_title && link.title_matches_expected === false && (
                          <>, which does not look like &ldquo;{link.expected_title}&rdquo;</>
                        )}
                        .
                      </span>
                    </div>
                  ) : (
                    <div className="mt-2 flex gap-2 rounded-lg border border-warning/40 bg-warning/5 px-3 py-2 text-xs text-warning">
                      <ShieldAlert className="mt-0.5 h-3.5 w-3.5 shrink-0" />
                      <span>
                        Nobody has fetched this link. A live send is refused until
                        somebody does.
                        {link.verify_error && <> Last attempt: {link.verify_error}</>}
                      </span>
                    </div>
                  )}
                  <button
                    type="button"
                    className="btn-secondary mt-3 w-full text-xs"
                    onClick={doVerify}
                    disabled={busy === 'verify'}
                  >
                    {busy === 'verify' ? (
                      <Loader2 className="mx-auto h-4 w-4 animate-spin" />
                    ) : (
                      'Fetch it and read the title'
                    )}
                  </button>
                </>
              ) : (
                <p className="mt-2 text-xs text-ink-dim">
                  No booking link is configured for this type yet. It has to be added
                  before this invite can be sent.
                </p>
              )}
            </section>
          )}

          {/* Fields */}
          {type && (
            <section className="space-y-3 rounded-2xl border border-hairline bg-surface p-4">
              <label className="text-xs font-semibold uppercase tracking-wide text-ink-dim">
                Candidate
              </label>
              <input
                className="input w-full text-sm"
                placeholder="Markaz application ID (fills the name and email)"
                value={applicationId}
                onChange={(e) => setApplicationId(e.target.value.replace(/\D/g, ''))}
              />
              <p className="text-[11px] text-ink-dim">
                The address is read from Markaz rather than typed. A hand-typed one is
                how a welcome email sat on a misspelt domain for three months.
              </p>

              {askedFields.map((f) => (
                <div key={f}>
                  <label className="text-xs font-medium text-ink-muted">
                    {FIELD_LABEL[f] ?? f}
                    {!type.required.includes(f) && (
                      <span className="text-ink-dim"> (optional)</span>
                    )}
                  </label>
                  {f === 'context' ? (
                    <textarea
                      className="input mt-1 w-full text-sm"
                      rows={3}
                      value={fields[f] ?? ''}
                      onChange={(e) => setFields({ ...fields, [f]: e.target.value })}
                    />
                  ) : (
                    <input
                      className="input mt-1 w-full text-sm"
                      value={fields[f] ?? ''}
                      onChange={(e) => setFields({ ...fields, [f]: e.target.value })}
                    />
                  )}
                </div>
              ))}
              {type.key === 'interview_reminder' && (
                <p className="text-[11px] text-ink-dim">
                  The date, time and Meet link must come from the calendar event or the
                  booking email. With no verified Meet link the email says to use the
                  one in the calendar invitation, rather than carrying a button that
                  might strand them.
                </p>
              )}
              <button
                type="button"
                className="btn-primary w-full text-sm"
                onClick={doPreview}
                disabled={busy === 'preview'}
              >
                {busy === 'preview' ? (
                  <Loader2 className="mx-auto h-4 w-4 animate-spin" />
                ) : (
                  'Preview'
                )}
              </button>
            </section>
          )}
        </div>

        {/* Preview + send */}
        <div className="space-y-4">
          {preview ? (
            <>
              <section className="rounded-2xl border border-hairline bg-surface p-4">
                <div className="text-xs font-semibold uppercase tracking-wide text-ink-dim">
                  Subject
                </div>
                <p className="mt-1 text-sm font-medium text-ink">{preview.subject}</p>

                {preview.missing.length > 0 && (
                  <p className="mt-3 rounded-lg border border-danger/30 bg-danger/5 px-3 py-2 text-xs text-danger">
                    Nothing is rendered yet. Still needed:{' '}
                    {preview.missing.map((m) => FIELD_LABEL[m] ?? m).join(', ')}.
                  </p>
                )}

                {preview.warnings.map((w) => (
                  <p
                    key={w}
                    className="mt-2 flex gap-2 rounded-lg border border-warning/40 bg-warning/5 px-3 py-2 text-xs text-warning"
                  >
                    <AlertTriangle className="mt-0.5 h-3.5 w-3.5 shrink-0" />
                    <span>{w}</span>
                  </p>
                ))}

                {/* Shown at preview time on purpose. Finding out at the moment
                    of sending is how a check gets skipped under time pressure. */}
                {preview.blockers.length > 0 && (
                  <div className="mt-3 rounded-lg border border-danger/30 bg-danger/5 px-3 py-2 text-xs text-danger">
                    <div className="font-semibold">A live send would be refused:</div>
                    <ul className="mt-1 list-disc space-y-1 pl-4">
                      {preview.blockers.map((b) => (
                        <li key={b}>{b}</li>
                      ))}
                    </ul>
                  </div>
                )}

                <div className="mt-4 flex gap-2">
                  <button
                    type="button"
                    className="btn-secondary text-sm"
                    onClick={() => doSend(false)}
                    disabled={!canPilot || busy === 'pilot'}
                  >
                    {busy === 'pilot' ? (
                      <Loader2 className="h-4 w-4 animate-spin" />
                    ) : (
                      'Pilot to Ayesha'
                    )}
                  </button>
                  <button
                    type="button"
                    className="btn-primary text-sm"
                    onClick={() => doSend(true)}
                    disabled={blocked || busy === 'live'}
                    title={blocked ? 'Resolve the blockers above first' : undefined}
                  >
                    {busy === 'live' ? (
                      <Loader2 className="h-4 w-4 animate-spin" />
                    ) : (
                      <>
                        <Send className="mr-1.5 inline h-3.5 w-3.5" />
                        Send to the candidate
                      </>
                    )}
                  </button>
                </div>
                <p className="mt-2 text-[11px] text-ink-dim">
                  A pilot goes to ayesha.khan@taleemabad.com and nobody else, with no CC.
                </p>
              </section>

              {preview.body_html && (
                <section className="overflow-hidden rounded-2xl border border-hairline bg-surface">
                  {/* Sandboxed: the preview is email HTML and must not run
                      anything or navigate the app. */}
                  <iframe
                    title="Invite preview"
                    sandbox=""
                    className="h-[46rem] w-full border-0 bg-white"
                    srcDoc={preview.body_html}
                  />
                </section>
              )}
            </>
          ) : (
            <section className="rounded-2xl border border-dashed border-hairline bg-surface p-8 text-center text-sm text-ink-dim">
              Choose a type, fill in what it needs, and press Preview.
            </section>
          )}

          {/* What actually went out */}
          <section className="overflow-hidden rounded-2xl border border-hairline bg-surface">
            <div className="border-b border-hairline bg-elevated px-4 py-2.5 text-xs font-semibold uppercase tracking-wide text-ink-dim">
              Recent invites
            </div>
            {sends.length === 0 ? (
              <p className="px-4 py-5 text-sm text-ink-dim">Nothing has been sent yet.</p>
            ) : (
              <table className="w-full text-sm">
                <tbody>
                  {sends.slice(0, 12).map((s) => (
                    <tr key={s.id} className="border-b border-hairline/60 last:border-0">
                      <td className="px-4 py-2.5">
                        <div className="font-medium text-ink">
                          {s.candidate_name ?? s.to_address}
                        </div>
                        <div className="text-xs text-ink-dim">{s.subject}</div>
                      </td>
                      <td className="px-4 py-2.5 text-right">
                        <span
                          className={`inline-block rounded-full border px-2 py-0.5 text-[11px] font-semibold ${
                            s.is_live
                              ? 'border-success/30 bg-success/10 text-success'
                              : 'border-hairline bg-ink-dim/10 text-ink-dim'
                          }`}
                        >
                          {s.is_live ? 'live' : 'pilot'}
                        </span>
                        <div className="mt-1 text-[11px] text-ink-dim">
                          {new Date(s.sent_at).toLocaleDateString()}
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </section>
        </div>
      </div>
    </div>
  )
}
