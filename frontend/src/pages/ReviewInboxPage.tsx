import { useQuery, useQueryClient } from '@tanstack/react-query'
import { CheckCircle2, Inbox, Loader2, Send, XCircle } from 'lucide-react'
import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Spinner } from '../components/Spinner'
import { api } from '../lib/api'
import { useBulk } from '../lib/bulk'
import { formatDate } from '../lib/format'
import { canApprove, canEdit } from '../lib/roles'

export function ReviewInboxPage() {
  const navigate = useNavigate()
  const qc = useQueryClient()
  const meQ = useQuery({ queryKey: ['me'], queryFn: api.me, retry: false })
  const role = meQ.data?.app_role
  const q = useQuery({ queryKey: ['comms', 'in_review'], queryFn: () => api.listCommunications({ status: 'in_review' }) })
  const rows = q.data ?? []

  const [selected, setSelected] = useState<Set<string>>(new Set())
  const [banner, setBanner] = useState<string | null>(null)
  const bulk = useBulk()

  function toggle(id: string) {
    setSelected((prev) => {
      const next = new Set(prev)
      if (next.has(id)) next.delete(id)
      else next.add(id)
      return next
    })
  }
  const allSelected = rows.length > 0 && rows.every((c) => selected.has(c.id))
  function toggleAll() {
    setSelected(allSelected ? new Set() : new Set(rows.map((c) => c.id)))
  }

  // Bulk approve / bulk pilot-send drive the existing per-item endpoints in a
  // loop (each still passes the server-side quality gate). Live send stays 1:1.
  async function runBulk(kind: 'approve' | 'pilot') {
    setBanner(null)
    const ids = [...selected]
    const { failed } = await bulk.run(
      ids,
      (id) => (kind === 'approve' ? api.approve(id) : api.send(id, 'pilot')),
      (id) => id,
    )
    const ok = ids.length - failed.length
    const verb = kind === 'approve' ? 'Approved' : 'Sent a pilot to you for'
    setBanner(`${verb} ${ok} of ${ids.length}${failed.length ? `, ${failed.length} failed (open individually)` : ''}.`)
    setSelected(new Set())
    qc.invalidateQueries({ queryKey: ['comms'] })
    q.refetch()
  }

  return (
    <div className="mx-auto max-w-5xl px-8 py-7">
      <h1 className="font-display text-2xl font-bold text-ink">Review</h1>
      <p className="mt-1 text-sm text-ink-muted">
        Drafts submitted for approval. Select several to approve or pilot the whole batch, or open one to review, edit, approve, and send live.
      </p>

      {banner && (
        <div className="mt-4 flex items-center gap-3 rounded-xl border border-green/30 bg-green/10 px-4 py-2.5 text-sm text-ink">
          <CheckCircle2 className="h-4 w-4 flex-shrink-0 text-green" />
          <span>{banner}</span>
          <button type="button" onClick={() => setBanner(null)} className="ml-auto text-ink-dim hover:text-ink" aria-label="Dismiss">
            <XCircle className="h-4 w-4" />
          </button>
        </div>
      )}

      {selected.size > 0 && (
        <div className="mt-4 flex flex-wrap items-center gap-3 rounded-xl border border-blurple/40 bg-blurple/5 px-4 py-2.5">
          <span className="text-sm font-semibold text-ink">{selected.size} selected</span>
          {canApprove(role) && (
            <button type="button" disabled={bulk.running} onClick={() => runBulk('approve')} className="btn btn-green h-8 text-sm">
              {bulk.running ? <Loader2 className="h-4 w-4 animate-spin" /> : <CheckCircle2 className="h-4 w-4" />}
              Approve selected
            </button>
          )}
          {canEdit(role) && (
            <button type="button" disabled={bulk.running} onClick={() => runBulk('pilot')} className="btn btn-ghost h-8 text-sm">
              {bulk.running ? <Loader2 className="h-4 w-4 animate-spin" /> : <Send className="h-4 w-4" />}
              Send pilot to me
            </button>
          )}
          {bulk.running && <span className="text-sm text-ink-muted">Working {bulk.done}/{bulk.total}…</span>}
          <button type="button" onClick={() => setSelected(new Set())} className="ml-auto text-sm text-ink-dim hover:text-ink">
            Clear
          </button>
        </div>
      )}

      <div className="card mt-6 overflow-hidden">
        {q.isLoading ? (
          <Spinner label="Loading…" />
        ) : !rows.length ? (
          <div className="mx-auto flex max-w-sm flex-col items-center py-16 text-center text-sm text-ink-dim">
            <Inbox className="mb-2 h-7 w-7 text-ink-dim" />
            <p className="font-medium text-ink-muted">Nothing waiting for approval</p>
            <p className="mt-1">When you draft candidate emails and submit them for review, they&rsquo;ll appear here to approve and send.</p>
          </div>
        ) : (
          <table className="w-full text-left text-sm">
            <thead className="border-b border-hairline bg-surface-2 text-xs uppercase tracking-wide text-ink-dim">
              <tr>
                <th className="w-10 px-3 py-3">
                  <input type="checkbox" checked={allSelected} onChange={toggleAll} aria-label="Select all" className="h-4 w-4 cursor-pointer" />
                </th>
                <th className="px-5 py-3 font-medium">Subject</th>
                <th className="px-5 py-3 font-medium">Role</th>
                <th className="px-5 py-3 font-medium">Type</th>
                <th className="px-5 py-3 font-medium">Updated</th>
                <th className="px-5 py-3" />
              </tr>
            </thead>
            <tbody className="divide-y divide-hairline">
              {rows.map((c) => (
                <tr key={c.id} onClick={() => navigate(`/drafts/${c.id}`)} className="cursor-pointer transition-colors hover:bg-elevated">
                  <td className="px-3 py-3" onClick={(e) => e.stopPropagation()}>
                    <input
                      type="checkbox"
                      checked={selected.has(c.id)}
                      onChange={() => toggle(c.id)}
                      aria-label={`Select ${c.title_line || 'draft'}`}
                      className="h-4 w-4 cursor-pointer"
                    />
                  </td>
                  <td className="px-5 py-3 font-medium text-ink">{c.title_line || '(untitled)'}</td>
                  <td className="px-5 py-3 text-ink-muted">{c.role_title}</td>
                  <td className="px-5 py-3 text-ink-dim">{c.email_type.replace('_', ' ')}</td>
                  <td className="px-5 py-3 text-ink-dim">{formatDate(c.updated_at)}</td>
                  <td className="px-5 py-3 text-right text-sm font-medium text-blurple-600">Review →</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}
