import { useEffect, useState } from 'react'
import { AlertTriangle, Download, FileText, Info, Loader2, Mail, Send, Upload, Wand2 } from 'lucide-react'
import { Spinner } from '../components/Spinner'
import { ApiError, api } from '../lib/api'
import type {
  ContractMasters,
  ContractPackage,
  ContractOptions,
  ContractPerson,
  ContractPlanFilled,
  JobItem,
} from '../lib/types'

// 🔴 The things this page must never let happen:
//    - a volunteer Fellow offered an employment contract (the engagement does
//      not produce one, and the server refuses it too)
//    - a document downloaded with a placeholder still printed in it
//    - a pre-filled value used as though somebody had checked it
//
// Every filled box shows where its value came from, because a figure with no
// source is a figure nobody can check. Nothing here can see a page, so the
// caveat stays on screen rather than in anyone's memory.

export function ContractsPage() {
  const [options, setOptions] = useState<ContractOptions | null>(null)
  const [masters, setMasters] = useState<ContractMasters | null>(null)
  const [jobs, setJobs] = useState<JobItem[]>([])
  const [people, setPeople] = useState<ContractPerson[]>([])

  const [jobId, setJobId] = useState<string>('')
  const [applicationId, setApplicationId] = useState<string>('')
  const [entity, setEntity] = useState('')
  const [engagement, setEngagement] = useState('')

  const [plan, setPlan] = useState<ContractPlanFilled | null>(null)
  const [values, setValues] = useState<Record<string, Record<string, string>>>({})
  // The three details the EMAIL needs, which are not contract fields.
  const [emailStart, setEmailStart] = useState('')
  const [emailEnd, setEmailEnd] = useState('')
  const [emailPay, setEmailPay] = useState('')
  const [pack, setPack] = useState<ContractPackage | null>(null)
  // A live send is only offered after the pilot has actually been sent.
  const [pilotSent, setPilotSent] = useState(false)
  const [busy, setBusy] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [notice, setNotice] = useState<string | null>(null)
  const [loaded, setLoaded] = useState(false)

  useEffect(() => {
    Promise.all([api.contractOptions(), api.contractMasters(), api.jobs()])
      .then(([o, m, j]) => {
        setOptions(o)
        setMasters(m)
        setJobs(j)
        if (o.entities.length) setEntity(o.entities[0])
        if (o.engagements.length) setEngagement(o.engagements[0].key)
      })
      .catch(() => setError('Could not load contract drafting.'))
      .finally(() => setLoaded(true))
  }, [])

  // Who a contract could be drafted for on this job.
  useEffect(() => {
    setApplicationId('')
    setPlan(null)
    api
      .contractPeople(jobId ? Number(jobId) : undefined)
      .then((r) => setPeople(r.people))
      .catch(() => setPeople([]))
  }, [jobId])

  const person = people.find((p) => String(p.application_id) === applicationId)

  const loadPrefill = () => {
    if (!applicationId || !entity || !engagement) return
    setBusy('prefill')
    setError(null)
    setNotice(null)
    api
      .contractPrefill(Number(applicationId), engagement, entity)
      .then((p) => {
        setPlan(p)
        // Seed every box from the prefill; each stays editable.
        const seeded: Record<string, Record<string, string>> = {}
        for (const doc of p.documents) {
          seeded[doc.doc_type] = { ...(doc.prefill?.values ?? {}) }
        }
        setValues(seeded)
        setPack(null)
        setPilotSent(false)
        // The email needs the same dates and figure the contract
        // does, so seed them from whatever the offer thread gave.
        const first = p.documents[0]?.prefill
        const pick = (needle: string) =>
          Object.entries(first?.values ?? {}).find(([k]) =>
            k.toUpperCase().includes(needle))?.[1] ?? ''
        setEmailStart(pick('JOINING') || pick('EFFECTIVE'))
        setEmailEnd('')
        setEmailPay('')
      })
      .catch((e) =>
        setError(
          e instanceof ApiError ? e.message.replace(/^\d+:\s*/, '') : 'Could not prepare that.',
        ),
      )
      .finally(() => setBusy(null))
  }

  const upload = (relPath: string, file: File) => {
    setBusy(`upload:${relPath}`)
    api
      .contractUploadMaster(relPath, file)
      .then((r) => {
        setNotice(r.warning ?? `Stored. It has ${r.field_count} fields.`)
        return api.contractMasters().then(setMasters)
      })
      .catch((e) =>
        setError(e instanceof ApiError ? e.message.replace(/^\d+:\s*/, '') : 'Upload failed.'),
      )
      .finally(() => setBusy(null))
  }

  const download = (docType: string) => {
    setBusy(`build:${docType}`)
    setError(null)
    api
      .contractBuild({
        entity,
        engagement,
        doc_type: docType,
        person_name: person?.name ?? '',
        application_id: Number(applicationId) || null,
        values: values[docType] ?? {},
      })
      .then(() => setNotice('Downloaded. Open it and look at the page before it goes anywhere.'))
      .catch((e) =>
        setError(e instanceof ApiError ? e.message.replace(/^\d+:\s*/, '') : 'Could not build it.'),
      )
      .finally(() => setBusy(null))
  }

  const setValue = (docType: string, key: string, v: string) => {
    // Any edit invalidates a pilot that was sent from the old values.
    setPilotSent(false)
    setPack(null)
    setValues((prev) => ({ ...prev, [docType]: { ...(prev[docType] ?? {}), [key]: v } }))
  }

  // What the package endpoints need, built once so preview and send cannot
  // disagree about what is being produced.
  const packageBody = () => ({
    entity,
    engagement,
    first_name: (person?.name ?? '').split(' ')[0],
    person_name: person?.name ?? '',
    role: person?.position ?? '',
    application_id: Number(applicationId) || null,
    candidate_email: plan?.person?.email ?? null,
    start_date: emailStart,
    end_date: emailEnd,
    compensation: emailPay,
    values,
  })

  const buildPackage = () => {
    setBusy('package')
    setError(null)
    api
      .contractPackage(packageBody())
      .then((p) => {
        setPack(p)
        setNotice(null)
      })
      .catch((e) =>
        setError(
          e instanceof ApiError ? e.message.replace(/^\d+:\s*/, '') : 'Could not build the package.',
        ),
      )
      .finally(() => setBusy(null))
  }

  const sendPackage = (live: boolean) => {
    setBusy(live ? 'live' : 'pilot')
    setError(null)
    api
      .contractSend({ ...packageBody(), live })
      .then((r) => {
        if (!live) setPilotSent(true)
        setNotice(
          live
            ? `Sent to ${r.to.join(', ')} with ${r.attachments.length} attachments.`
            : `Pilot sent to ${r.to.join(', ')}. Nobody else received it. ${r.caveat}`,
        )
      })
      .catch((e) =>
        setError(e instanceof ApiError ? e.message.replace(/^\d+:\s*/, '') : 'Not sent.'),
      )
      .finally(() => setBusy(null))
  }

  const blocked = (plan?.blockers.length ?? 0) > 0

  if (!loaded) {
    return (
      <div className="mx-auto max-w-6xl px-8 py-7">
        <Spinner label="Loading contract drafting…" />
      </div>
    )
  }

  return (
    <div className="mx-auto max-w-6xl px-8 py-7">
      <header className="mb-5">
        <h1 className="font-display text-2xl font-bold text-ink">Contract Drafting</h1>
        <p className="mt-1 text-sm text-ink-muted">
          Name the person and the job. Everything we already know fills itself in.
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

      {masters && masters.missing.length > 0 && (
        <section className="mb-5 rounded-2xl border border-warning/40 bg-warning/5 p-4">
          <div className="flex items-center gap-2 text-sm font-semibold text-warning">
            <Upload className="h-4 w-4" />
            {masters.missing.length} master{masters.missing.length === 1 ? '' : 's'} still to upload
          </div>
          <div className="mt-3 space-y-2">
            {masters.missing.map((m) => (
              <label
                key={m}
                className="flex cursor-pointer items-center gap-3 rounded-lg border border-hairline bg-surface px-3 py-2 text-xs hover:bg-elevated"
              >
                <FileText className="h-3.5 w-3.5 shrink-0 text-ink-dim" />
                <span className="font-mono text-ink-muted">{m}</span>
                {busy === `upload:${m}` ? (
                  <Loader2 className="ml-auto h-4 w-4 animate-spin text-ink-dim" />
                ) : (
                  <span className="ml-auto text-blurple">choose file</span>
                )}
                <input
                  type="file"
                  accept=".docx"
                  className="hidden"
                  onChange={(e) => {
                    const f = e.target.files?.[0]
                    if (f) upload(m, f)
                  }}
                />
              </label>
            ))}
          </div>
        </section>
      )}

      {/* Who and what */}
      <section className="rounded-2xl border border-hairline bg-surface p-4">
        <div className="grid gap-3 sm:grid-cols-2">
          <div>
            <label className="text-xs font-semibold uppercase tracking-wide text-ink-dim">
              Job
            </label>
            <select
              className="input mt-1 w-full text-sm"
              value={jobId}
              onChange={(e) => setJobId(e.target.value)}
            >
              <option value="">Every job</option>
              {jobs.map((j) => (
                <option key={j.job_pk} value={j.job_pk}>
                  {j.title ?? `Job ${j.job_pk}`}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="text-xs font-semibold uppercase tracking-wide text-ink-dim">
              Person
            </label>
            <select
              className="input mt-1 w-full text-sm"
              value={applicationId}
              onChange={(e) => setApplicationId(e.target.value)}
            >
              <option value="">Choose someone…</option>
              {people.map((p) => (
                <option key={p.application_id} value={p.application_id}>
                  {p.name}
                  {p.has_cnic ? '' : '  (no onboarding form yet)'}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="text-xs font-semibold uppercase tracking-wide text-ink-dim">
              Entity
            </label>
            <select
              className="input mt-1 w-full text-sm"
              value={entity}
              onChange={(e) => setEntity(e.target.value)}
            >
              {options?.entities.map((e) => (
                <option key={e} value={e}>
                  {e}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="text-xs font-semibold uppercase tracking-wide text-ink-dim">
              Engagement
            </label>
            <select
              className="input mt-1 w-full text-sm"
              value={engagement}
              onChange={(e) => setEngagement(e.target.value)}
            >
              {options?.engagements.map((e) => (
                <option key={e.key} value={e.key}>
                  {e.label}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* The legal name is not always the stored name, and the contract
            needs the legal one. */}
        {person?.name_differs && (
          <p className="mt-3 flex gap-2 rounded-lg border border-blurple/30 bg-blurple/5 px-3 py-2 text-xs text-blurple">
            <Info className="mt-0.5 h-3.5 w-3.5 shrink-0" />
            <span>
              Markaz stores them as <strong>{person.markaz_name}</strong>, but on the
              onboarding form they wrote <strong>{person.name}</strong>. The contract
              will use the name they typed.
            </span>
          </p>
        )}
        {person && !person.has_cnic && (
          <p className="mt-3 flex gap-2 rounded-lg border border-warning/40 bg-warning/5 px-3 py-2 text-xs text-warning">
            <AlertTriangle className="mt-0.5 h-3.5 w-3.5 shrink-0" />
            <span>
              They have not submitted the onboarding form, so there is no CNIC and no
              legal name to fill in. You would be typing both.
            </span>
          </p>
        )}

        <button
          type="button"
          className="btn-primary mt-4 text-sm"
          onClick={loadPrefill}
          disabled={!applicationId || busy === 'prefill'}
        >
          {busy === 'prefill' ? (
            <Loader2 className="h-4 w-4 animate-spin" />
          ) : (
            <>
              <Wand2 className="mr-1.5 inline h-3.5 w-3.5" />
              Fill it in
            </>
          )}
        </button>
      </section>

      {plan && (
        <>
          <p className="mt-3 flex gap-2 rounded-xl border border-hairline bg-surface px-4 py-2.5 text-xs text-ink-muted">
            <Info className="mt-0.5 h-3.5 w-3.5 shrink-0 text-ink-dim" />
            <span>
              <strong className="text-ink">{plan.engagement_label}</strong> at {plan.entity}{' '}
              produces {plan.documents.map((d) => d.label).join(' and ')}. {plan.caveat}
            </span>
          </p>

          {[...plan.blockers].map((b) => (
            <p
              key={b}
              className="mt-2 flex gap-2 rounded-xl border border-danger/30 bg-danger/5 px-4 py-2.5 text-xs text-danger"
            >
              <AlertTriangle className="mt-0.5 h-3.5 w-3.5 shrink-0" />
              {b}
            </p>
          ))}

          {/* Anything the offer thread could not settle. The salary is the
              field most likely to be wrong and most expensive to get wrong. */}
          {(plan.offer_warnings ?? []).map((w) => (
            <p
              key={w}
              className="mt-2 flex gap-2 rounded-xl border border-warning/40 bg-warning/5 px-4 py-2.5 text-xs text-warning"
            >
              <AlertTriangle className="mt-0.5 h-3.5 w-3.5 shrink-0" />
              {w}
            </p>
          ))}

          <div className="mt-4 space-y-4">
            {plan.documents.map((doc) => {
              const pf = doc.prefill
              return (
                <section
                  key={doc.doc_type}
                  className="overflow-hidden rounded-2xl border border-hairline bg-surface"
                >
                  <div className="flex items-center gap-2 border-b border-hairline bg-elevated px-4 py-2.5">
                    <FileText className="h-4 w-4 text-ink-dim" />
                    <span className="text-sm font-semibold text-ink">{doc.label}</span>
                    <span className="ml-auto text-xs text-ink-dim">
                      {doc.uploaded && pf
                        ? `${pf.filled} of ${pf.total_fields} filled for you`
                        : 'master not uploaded'}
                    </span>
                  </div>

                  {doc.uploaded ? (
                    <>
                      <div className="grid gap-3 p-4 sm:grid-cols-2">
                        {doc.fields.map((f) => {
                          const source = pf?.sources[f.key]
                          return (
                            <div key={f.key}>
                              <label className="text-xs font-medium text-ink-muted">
                                {f.opaque ? 'Unlabelled field' : f.placeholder}
                              </label>
                              {f.opaque && (
                                <p className="mt-0.5 text-[11px] italic text-ink-dim">
                                  “{f.contexts[0]}”
                                </p>
                              )}
                              {f.spans_contexts && (
                                <p className="mt-0.5 text-[11px] text-warning">
                                  Written into {f.indexes.length} places.
                                </p>
                              )}
                              <input
                                className="input mt-1 w-full text-sm"
                                value={values[doc.doc_type]?.[f.key] ?? ''}
                                onChange={(e) => setValue(doc.doc_type, f.key, e.target.value)}
                              />
                              {/* Where the value came from. A figure with no
                                  source is a figure nobody can check. */}
                              {source && (
                                <p className="mt-0.5 text-[11px] text-ink-dim">from {source}</p>
                              )}
                            </div>
                          )
                        })}
                      </div>
                      <div className="flex items-center gap-3 border-t border-hairline px-4 py-3">
                        <button
                          type="button"
                          className="btn-primary text-sm"
                          disabled={blocked || !person || busy === `build:${doc.doc_type}`}
                          onClick={() => download(doc.doc_type)}
                        >
                          {busy === `build:${doc.doc_type}` ? (
                            <Loader2 className="h-4 w-4 animate-spin" />
                          ) : (
                            <>
                              <Download className="mr-1.5 inline h-3.5 w-3.5" />
                              Build and download
                            </>
                          )}
                        </button>
                        <span className="text-[11px] text-ink-dim">
                          Word file. The email and the pilot are still being built.
                        </span>
                      </div>
                    </>
                  ) : (
                    <p className="px-4 py-4 text-sm text-ink-dim">
                      Upload <span className="font-mono text-xs">{doc.master}</span> above
                      before this can be built.
                    </p>
                  )}
                </section>
              )
            })}
          </div>

          {/* The joining email. Its dates and figure are separate from the
              contract fields because the email words them differently. */}
          <section className="mt-5 rounded-2xl border border-hairline bg-surface">
            <div className="flex items-center gap-2 border-b border-hairline bg-elevated px-4 py-2.5">
              <Mail className="h-4 w-4 text-ink-dim" />
              <span className="text-sm font-semibold text-ink">The joining email</span>
            </div>
            <div className="grid gap-3 p-4 sm:grid-cols-3">
              <div>
                <label className="text-xs font-medium text-ink-muted">Start date</label>
                <input
                  className="input mt-1 w-full text-sm"
                  placeholder="7th September 2026"
                  value={emailStart}
                  onChange={(e) => { setEmailStart(e.target.value); setPilotSent(false) }}
                />
              </div>
              <div>
                <label className="text-xs font-medium text-ink-muted">Contract runs to</label>
                <input
                  className="input mt-1 w-full text-sm"
                  placeholder="31st December 2026"
                  value={emailEnd}
                  onChange={(e) => { setEmailEnd(e.target.value); setPilotSent(false) }}
                />
              </div>
              <div>
                <label className="text-xs font-medium text-ink-muted">Monthly compensation</label>
                <input
                  className="input mt-1 w-full text-sm"
                  placeholder="PKR 108,000"
                  value={emailPay}
                  onChange={(e) => { setEmailPay(e.target.value); setPilotSent(false) }}
                />
              </div>
            </div>
            <p className="px-4 pb-2 text-[11px] text-ink-dim">
              Never name the weekday in a date. Write 7th September 2026.
            </p>

            <div className="flex flex-wrap items-center gap-3 border-t border-hairline px-4 py-3">
              <button
                type="button"
                className="btn btn-secondary text-sm"
                onClick={buildPackage}
                disabled={blocked || !person || busy === 'package'}
              >
                {busy === 'package' ? (
                  <Loader2 className="h-4 w-4 animate-spin" />
                ) : (
                  'Preview the package'
                )}
              </button>
              <button
                type="button"
                className="btn btn-primary text-sm"
                onClick={() => sendPackage(false)}
                disabled={blocked || !person || busy === 'pilot'}
              >
                {busy === 'pilot' ? (
                  <Loader2 className="h-4 w-4 animate-spin" />
                ) : (
                  <>
                    <Send className="mr-1.5 inline h-3.5 w-3.5" />
                    Pilot to Ayesha
                  </>
                )}
              </button>
              {/* 🔴 The live send only appears after a pilot has actually been
                  sent, and any edit withdraws it again. */}
              <button
                type="button"
                className="btn btn-green text-sm"
                onClick={() => sendPackage(true)}
                disabled={!pilotSent || busy === 'live'}
                title={pilotSent ? undefined : 'Send the pilot and look at it first'}
              >
                {busy === 'live' ? (
                  <Loader2 className="h-4 w-4 animate-spin" />
                ) : (
                  'Send to the candidate'
                )}
              </button>
              <span className="text-[11px] text-ink-dim">
                The pilot goes to ayesha.khan@taleemabad.com alone, with no CC, and is
                identical to what the candidate would receive.
              </span>
            </div>

            {pack && (
              <div className="border-t border-hairline p-4">
                <div className="text-xs text-ink-muted">
                  <strong className="text-ink">{pack.subject}</strong>
                  <div className="mt-1">
                    {pack.attachments.map((a) => (
                      <span key={a.filename} className="mr-3 font-mono text-[11px]">
                        {a.filename} ({Math.round(a.size_bytes / 1024)} KB)
                      </span>
                    ))}
                  </div>
                </div>
                {pack.problems.map((pr) => (
                  <p key={pr} className="mt-2 text-xs text-danger">{pr}</p>
                ))}
                <p className="mt-2 text-[11px] text-ink-dim">{pack.caveat}</p>
                {/* Sandboxed: this is email HTML and must not run anything. */}
                <iframe
                  title="Joining email preview"
                  sandbox=""
                  className="mt-3 h-[40rem] w-full rounded-xl border border-hairline bg-white"
                  srcDoc={pack.html}
                />
              </div>
            )}
          </section>
        </>
      )}
    </div>
  )
}
