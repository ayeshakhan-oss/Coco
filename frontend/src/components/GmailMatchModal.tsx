import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { CheckCircle2, ExternalLink, Loader2, Mail, X } from 'lucide-react'
import { useState } from 'react'
import { api } from '../lib/api'
import { formatDate } from '../lib/format'
import { canApprove, canEdit } from '../lib/roles'
import type { GmailMatch } from '../lib/types'
import { Spinner } from './Spinner'

const STATUS_TEXT: Record<string, { label: string; cls: string }> = {
  found: { label: 'Evidence found in Gmail', cls: 'text-green' },
  uncertain: { label: 'Needs review — ambiguous', cls: 'text-cyan' },
  none: { label: 'No matching Gmail email found', cls: 'text-ink-muted' },
  not_checked: { label: 'Not checked yet', cls: 'text-ink-dim' },
}

function gmailLink(m: GmailMatch): string | null {
  if (m.matched_message_id) {
    const id = m.matched_message_id.replace(/[<>]/g, '')
    return `https://mail.google.com/mail/u/0/#search/rfc822msgid:${encodeURIComponent(id)}`
  }
  if (m.gmail_thread_id) return `https://mail.google.com/mail/u/0/#all/${m.gmail_thread_id}`
  return null
}

export function GmailMatchModal({
  applicationId,
  candidateName,
  role,
  onClose,
}: {
  applicationId: number
  candidateName: string
  role?: string | null
  onClose: () => void
}) {
  const qc = useQueryClient()
  const [reason, setReason] = useState('')
  const matchQ = useQuery({
    queryKey: ['gmail-match', applicationId],
    queryFn: () => api.gmailMatch(applicationId),
  })

  const invalidate = () => {
    qc.invalidateQueries({ queryKey: ['gmail-match', applicationId] })
    qc.invalidateQueries({ queryKey: ['candidate', applicationId] })
    qc.invalidateQueries({ queryKey: ['candidates'] })
    qc.invalidateQueries({ queryKey: ['stats'] })
    qc.invalidateQueries({ queryKey: ['positions'] })
  }

  const markSent = useMutation({ mutationFn: () => api.markSent(applicationId, reason || undefined), onSuccess: invalidate })
  const clearMark = useMutation({ mutationFn: () => api.clearMark(applicationId), onSuccess: invalidate })
  const toggleIgnore = useMutation({
    mutationFn: (next: boolean) => api.setIgnore(applicationId, next),
    onSuccess: invalidate,
  })

  const m = matchQ.data
  const st = m ? STATUS_TEXT[m.gmail_status] ?? STATUS_TEXT.not_checked : null
  const link = m ? gmailLink(m) : null
  const busy = markSent.isPending || clearMark.isPending || toggleIgnore.isPending

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-ink/40 p-4" onClick={onClose}>
      <div className="card w-full max-w-lg" onClick={(e) => e.stopPropagation()}>
        <div className="flex items-center justify-between border-b border-hairline px-5 py-3">
          <div className="flex items-center gap-2 text-sm font-semibold text-ink">
            <Mail className="h-4 w-4 text-blurple" /> Gmail evidence — {candidateName}
          </div>
          <button type="button" onClick={onClose} className="rounded-lg p-1 text-ink-dim hover:bg-elevated hover:text-ink">
            <X className="h-4 w-4" />
          </button>
        </div>

        <div className="space-y-4 p-5">
          {matchQ.isLoading ? (
            <Spinner label="Loading evidence…" />
          ) : (
            <>
              <div>
                <div className={`text-sm font-semibold ${st?.cls}`}>{st?.label}</div>
                {m?.checked_at && <div className="text-xs text-ink-dim">Last checked {formatDate(m.checked_at)}</div>}
              </div>

              {m?.marked_sent_at && (
                <div className="rounded-lg border border-green/30 bg-green/10 p-3 text-sm">
                  <div className="flex items-center gap-1.5 font-medium text-green">
                    <CheckCircle2 className="h-4 w-4" /> Manually marked as sent
                  </div>
                  <div className="mt-1 text-xs text-ink-muted">
                    {formatDate(m.marked_sent_at)}
                    {m.marked_sent_reason ? ` · ${m.marked_sent_reason}` : ''}
                  </div>
                </div>
              )}

              {m?.uncertain_reason && (
                <div className="rounded-lg border border-cyan/30 bg-cyan/10 p-3 text-sm text-ink-muted">
                  <span className="font-medium text-cyan">Why this needs review:</span> {m.uncertain_reason}
                </div>
              )}

              {(m?.matched_subject || m?.matched_to) && (
                <div className="rounded-lg border border-hairline bg-surface-2 p-3 text-sm">
                  {m?.matched_subject && <div className="font-medium text-ink">{m.matched_subject}</div>}
                  {m?.matched_to && <div className="mt-0.5 text-xs text-ink-dim">To: {m.matched_to}</div>}
                  {m?.internal_date && <div className="text-xs text-ink-dim">{formatDate(m.internal_date)}</div>}
                  {m?.matched_snippet && <div className="mt-2 text-xs italic text-ink-muted">“{m.matched_snippet}”</div>}
                  {link && (
                    <a href={link} target="_blank" rel="noreferrer" className="mt-2 inline-flex items-center gap-1 text-xs font-medium text-[#4752c4] hover:underline">
                      Open in Gmail <ExternalLink className="h-3 w-3" />
                    </a>
                  )}
                </div>
              )}

              {m?.gmail_status === 'none' && !m?.marked_sent_at && (
                <p className="text-sm text-ink-dim">
                  Coco found no email to this candidate in the synced Sent mail. If they were contacted another way, mark it sent below.
                </p>
              )}

              {/* Actions */}
              {(canApprove(role) || canEdit(role)) && (
                <div className="space-y-2 border-t border-hairline pt-4">
                  {canApprove(role) && !m?.marked_sent_at && (
                    <div className="flex items-center gap-2">
                      <input
                        value={reason}
                        onChange={(e) => setReason(e.target.value)}
                        placeholder="Reason (optional) — e.g. sent from personal inbox"
                        className="input h-9 flex-1"
                      />
                      <button type="button" disabled={busy} onClick={() => markSent.mutate()} className="btn btn-green whitespace-nowrap">
                        {markSent.isPending ? <Loader2 className="h-4 w-4 animate-spin" /> : <CheckCircle2 className="h-4 w-4" />}
                        Mark sent
                      </button>
                    </div>
                  )}
                  {canApprove(role) && m?.marked_sent_at && (
                    <button type="button" disabled={busy} onClick={() => clearMark.mutate()} className="btn btn-ghost">
                      {clearMark.isPending ? <Loader2 className="h-4 w-4 animate-spin" /> : null}
                      Undo manual mark
                    </button>
                  )}
                  {canEdit(role) && (
                    <button type="button" disabled={busy} onClick={() => toggleIgnore.mutate(!m?.ignored)} className="btn btn-ghost">
                      {toggleIgnore.isPending ? <Loader2 className="h-4 w-4 animate-spin" /> : null}
                      {m?.ignored ? 'Un-ignore this candidate' : 'Ignore (interview never scheduled)'}
                    </button>
                  )}
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  )
}
