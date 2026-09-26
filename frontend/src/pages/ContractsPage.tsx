import { useEffect, useState } from 'react'
import { AlertTriangle, Download, FileText, Info, Loader2, Upload } from 'lucide-react'
import { Spinner } from '../components/Spinner'
import { ApiError, api } from '../lib/api'
import type { ContractMasters, ContractOptions, ContractPlan } from '../lib/types'

// 🔴 The two things this page must never let happen:
//    - a volunteer Fellow offered an employment contract (the engagement
//      simply does not produce one, and the server refuses it too)
//    - a document downloaded with a placeholder still printed in it, which is
//      why an unfilled field blocks the build rather than warning about it.
//
// Nothing here can see a page. The checks are structural, so the caveat is
// shown on screen rather than left to memory.

export function ContractsPage() {
  const [options, setOptions] = useState<ContractOptions | null>(null)
  const [masters, setMasters] = useState<ContractMasters | null>(null)
  const [entity, setEntity] = useState('')
  const [engagement, setEngagement] = useState('')
  const [plan, setPlan] = useState<ContractPlan | null>(null)
  const [person, setPerson] = useState('')
  const [values, setValues] = useState<Record<string, Record<string, string>>>({})
  const [busy, setBusy] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [notice, setNotice] = useState<string | null>(null)
  const [loaded, setLoaded] = useState(false)

  useEffect(() => {
    Promise.all([api.contractOptions(), api.contractMasters()])
      .then(([o, m]) => {
        setOptions(o)
        setMasters(m)
        if (o.entities.length) setEntity(o.entities[0])
        if (o.engagements.length) setEngagement(o.engagements[0].key)
      })
      .catch(() => setError('Could not load contract drafting.'))
      .finally(() => setLoaded(true))
  }, [])

  useEffect(() => {
    if (!entity || !engagement) return
    setPlan(null)
    setNotice(null)
    api
      .contractPlan(engagement, entity)
      .then(setPlan)
      .catch((e) =>
        setError(e instanceof ApiError ? e.message.replace(/^\d+:\s*/, '') : 'Could not plan that.'),
      )
  }, [entity, engagement])

  const refreshMasters = () => api.contractMasters().then(setMasters)

  const upload = (relPath: string, file: File) => {
    setBusy(`upload:${relPath}`)
    setError(null)
    api
      .contractUploadMaster(relPath, file)
      .then((r) => {
        setNotice(
          r.warning ??
            `Stored. It has ${r.field_count} fields to fill.`,
        )
        return refreshMasters().then(() =>
          entity && engagement ? api.contractPlan(engagement, entity).then(setPlan) : null,
        )
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
        person_name: person,
        values: values[docType] ?? {},
      })
      .then(() => setNotice('Downloaded. Open it and look at the page before it goes anywhere.'))
      .catch((e) =>
        setError(e instanceof ApiError ? e.message.replace(/^\d+:\s*/, '') : 'Could not build it.'),
      )
      .finally(() => setBusy(null))
  }

  const setValue = (docType: string, key: string, v: string) =>
    setValues((prev) => ({ ...prev, [docType]: { ...(prev[docType] ?? {}), [key]: v } }))

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
          Contracts, NDAs and addendums built from the approved masters.
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

      {/* Masters. Shown first because nothing works until they are here. */}
      {masters && masters.missing.length > 0 && (
        <section className="mb-5 rounded-2xl border border-warning/40 bg-warning/5 p-4">
          <div className="flex items-center gap-2 text-sm font-semibold text-warning">
            <Upload className="h-4 w-4" />
            {masters.missing.length} master{masters.missing.length === 1 ? '' : 's'} still to upload
          </div>
          <p className="mt-1 text-xs text-ink-muted">
            The masters are stored here rather than in the code, so no approved legal
            document ends up in the repository. Upload each one once.
          </p>
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

      {/* What is being issued */}
      <section className="grid gap-3 rounded-2xl border border-hairline bg-surface p-4 sm:grid-cols-3">
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
        <div>
          <label className="text-xs font-semibold uppercase tracking-wide text-ink-dim">
            Name
          </label>
          <input
            className="input mt-1 w-full text-sm"
            placeholder="Full name"
            value={person}
            onChange={(e) => setPerson(e.target.value)}
          />
        </div>
      </section>

      {plan && (
        <>
          <p className="mt-3 flex gap-2 rounded-xl border border-hairline bg-surface px-4 py-2.5 text-xs text-ink-muted">
            <Info className="mt-0.5 h-3.5 w-3.5 shrink-0 text-ink-dim" />
            <span>
              <strong className="text-ink">{plan.engagement_label}</strong> at {plan.entity}{' '}
              produces {plan.documents.map((d) => d.label).join(' and ')}.{' '}
              {plan.caveat}
            </span>
          </p>

          {plan.blockers.map((b) => (
            <p
              key={b}
              className="mt-2 flex gap-2 rounded-xl border border-danger/30 bg-danger/5 px-4 py-2.5 text-xs text-danger"
            >
              <AlertTriangle className="mt-0.5 h-3.5 w-3.5 shrink-0" />
              {b}
            </p>
          ))}

          {/* One card per document, with its own fields */}
          <div className="mt-4 space-y-4">
            {plan.documents.map((doc) => (
              <section
                key={doc.doc_type}
                className="overflow-hidden rounded-2xl border border-hairline bg-surface"
              >
                <div className="flex items-center gap-2 border-b border-hairline bg-elevated px-4 py-2.5">
                  <FileText className="h-4 w-4 text-ink-dim" />
                  <span className="text-sm font-semibold text-ink">{doc.label}</span>
                  <span className="ml-auto text-xs text-ink-dim">
                    {doc.uploaded ? `${doc.fields.length} fields` : 'master not uploaded'}
                  </span>
                </div>

                {doc.uploaded ? (
                  <>
                    <div className="grid gap-3 p-4 sm:grid-cols-2">
                      {doc.fields.map((f) => (
                        <div key={f.key}>
                          <label className="text-xs font-medium text-ink-muted">
                            {f.opaque ? 'Unlabelled field' : f.placeholder}
                          </label>
                          {/* An opaque placeholder says nothing about what
                              belongs in it. The sentence it sits in does. */}
                          {f.opaque && (
                            <p className="mt-0.5 text-[11px] italic text-ink-dim">
                              “{f.contexts[0]}”
                            </p>
                          )}
                          {f.spans_contexts && (
                            <p className="mt-0.5 text-[11px] text-warning">
                              This one value is written into {f.indexes.length} places.
                            </p>
                          )}
                          <input
                            className="input mt-1 w-full text-sm"
                            value={values[doc.doc_type]?.[f.key] ?? ''}
                            onChange={(e) => setValue(doc.doc_type, f.key, e.target.value)}
                          />
                        </div>
                      ))}
                    </div>
                    <div className="flex items-center gap-3 border-t border-hairline px-4 py-3">
                      <button
                        type="button"
                        className="btn-primary text-sm"
                        disabled={blocked || !person.trim() || busy === `build:${doc.doc_type}`}
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
                        Word file. PDF conversion still runs in Claude Code.
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
            ))}
          </div>
        </>
      )}
    </div>
  )
}
