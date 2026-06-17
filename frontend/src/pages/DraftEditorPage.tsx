import { useQuery } from '@tanstack/react-query'
import { ArrowLeft } from 'lucide-react'
import { useEffect, useRef, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { ApprovalBar } from '../components/ApprovalBar'
import { EmailPreview } from '../components/EmailPreview'
import { QualityPanel } from '../components/QualityPanel'
import { ScorecardView } from '../components/ScorecardView'
import { SectionEditor } from '../components/SectionEditor'
import { Spinner } from '../components/Spinner'
import { ApiError, api } from '../lib/api'
import { canApprove, canEdit } from '../lib/roles'
import type { DraftContent, EvalResult } from '../lib/types'

export function DraftEditorPage() {
  const { commId } = useParams()
  const meQ = useQuery({ queryKey: ['me'], queryFn: api.me, retry: false })
  const commQ = useQuery({ queryKey: ['comm', commId], queryFn: () => api.communication(commId!), enabled: !!commId })
  const comm = commQ.data
  const appId = comm?.application_id ?? undefined
  const scoreQ = useQuery({ queryKey: ['scorecard', appId], queryFn: () => api.scorecard(appId!), enabled: !!appId })

  const [title, setTitle] = useState('')
  const [content, setContent] = useState<DraftContent>({})
  const [evalResult, setEvalResult] = useState<EvalResult | null>(null)
  const [mode, setMode] = useState<'pilot' | 'live'>('pilot')
  const [reloadKey, setReloadKey] = useState(0)
  const [saving, setSaving] = useState(false)
  const [acting, setActing] = useState(false)
  const [loadedId, setLoadedId] = useState<string | null>(null)
  const [msg, setMsg] = useState<{ text: string; kind: 'ok' | 'err' } | null>(null)
  const dirty = useRef(false)

  const role = meQ.data?.app_role
  const editable = comm ? (comm.status === 'draft' || comm.status === 'in_review') && canEdit(role) : false
  const isApprover = canApprove(role)
  const passed = evalResult ? evalResult.passed : false

  useEffect(() => {
    if (comm && comm.id !== loadedId) {
      setTitle(comm.title_line ?? '')
      setContent(comm.draft_content ?? {})
      setEvalResult(comm.eval_result ?? null)
      setMode(comm.status === 'approved' ? 'live' : 'pilot')
      setLoadedId(comm.id)
      dirty.current = false
    }
  }, [comm, loadedId])

  async function save() {
    if (!commId) return
    setSaving(true)
    try {
      const res = await api.updateDraft(commId, { title_line: title, role_title: comm?.role_title ?? null, content })
      setEvalResult(res.eval)
      setReloadKey((k) => k + 1)
      dirty.current = false
    } catch (e) {
      setMsg({ text: `Save failed: ${(e as ApiError).message}`, kind: 'err' })
    } finally {
      setSaving(false)
    }
  }

  useEffect(() => {
    if (!editable || !dirty.current) return
    const t = setTimeout(save, 800)
    return () => clearTimeout(t)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [title, content])

  async function doAction(a: 'submit' | 'approve' | 'request_changes' | 'send') {
    if (!commId) return
    setActing(true)
    setMsg(null)
    try {
      if (dirty.current) await save()
      if (a === 'submit') await api.submit(commId)
      else if (a === 'approve') await api.approve(commId)
      else if (a === 'request_changes') await api.requestChanges(commId)
      else if (a === 'send') {
        const r = await api.send(commId, mode)
        setMsg({ text: `${mode === 'pilot' ? 'Pilot' : 'Live'} email sent to: ${r.recipients.join(', ')}`, kind: 'ok' })
      }
      await commQ.refetch()
    } catch (e) {
      setMsg({ text: `Could not ${a.replace('_', ' ')}: ${(e as ApiError).message}`, kind: 'err' })
    } finally {
      setActing(false)
    }
  }

  if (commQ.isLoading) return <Spinner label="Loading draft…" />
  if (commQ.isError || !comm) return <div className="p-8 text-sm text-danger">Could not load this draft.</div>

  return (
    <div className="flex h-full flex-col">
      <div className="flex items-center gap-3 border-b border-hairline bg-surface px-6 py-3">
        <Link to={appId ? `/applications/${appId}` : '/'} className="inline-flex items-center gap-1.5 text-sm text-ink-dim hover:text-ink">
          <ArrowLeft className="h-4 w-4" /> Back
        </Link>
        <div className="text-sm font-medium text-ink">{comm.role_title} · {comm.email_type.replace('_', ' ')}</div>
        {!editable && <span className="rounded-md bg-elevated px-2 py-0.5 text-xs text-ink-dim">read-only ({comm.status.replace('_', ' ')})</span>}
      </div>

      {msg && (
        <div className={`px-6 py-2 text-sm ${msg.kind === 'ok' ? 'bg-green/15 text-green' : 'bg-danger/15 text-danger'}`}>{msg.text}</div>
      )}

      <div className="grid min-h-0 flex-1 grid-cols-1 lg:grid-cols-[320px_minmax(0,1fr)_minmax(0,1fr)]">
        <aside className="min-h-0 overflow-auto border-r border-hairline bg-surface p-4">
          <h3 className="mb-3 text-xs font-semibold uppercase tracking-wide text-ink-dim">Scorecard reference</h3>
          {scoreQ.isLoading ? <Spinner /> : <ScorecardView values={scoreQ.data?.values ?? null} gwc={scoreQ.data?.gwc ?? null} />}
        </aside>

        <section className="min-h-0 overflow-auto border-r border-hairline bg-canvas p-5">
          <SectionEditor
            title={title}
            content={content}
            disabled={!editable || acting}
            onTitleChange={(v) => { dirty.current = true; setTitle(v) }}
            onContentChange={(c) => { dirty.current = true; setContent(c) }}
          />
        </section>

        <section className="min-h-0 overflow-hidden bg-surface">
          <EmailPreview src={api.previewUrl(comm.id)} reloadKey={reloadKey} busy={saving} />
        </section>
      </div>

      <QualityPanel result={evalResult} busy={saving} />
      <ApprovalBar comm={comm} isApprover={isApprover} mode={mode} onModeChange={setMode} passed={passed} busy={acting} onAction={doAction} />
    </div>
  )
}
