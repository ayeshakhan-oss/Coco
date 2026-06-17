import { Loader2, Send } from 'lucide-react'
import type { Communication } from '../lib/types'

type Action = 'submit' | 'approve' | 'request_changes' | 'send'

export function ApprovalBar({
  comm,
  isApprover,
  mode,
  onModeChange,
  passed,
  busy,
  onAction,
}: {
  comm: Communication
  isApprover: boolean
  mode: 'pilot' | 'live'
  onModeChange: (m: 'pilot' | 'live') => void
  passed: boolean
  busy: boolean
  onAction: (a: Action) => void
}) {
  const status = comm.status
  const recipients = mode === 'pilot' ? 'ayesha.khan@taleemabad.com (pilot only)' : 'candidate + hiring@ + Ayesha'
  const canLive = isApprover && status === 'approved'
  const sendDisabled = busy || !passed || (mode === 'live' && !canLive)

  return (
    <div className="flex flex-wrap items-center gap-3 border-t border-hairline bg-surface px-4 py-3">
      <StatusChip status={status} />

      <div className="flex overflow-hidden rounded-xl border border-hairline text-sm">
        {(['pilot', 'live'] as const).map((m) => (
          <button
            key={m}
            type="button"
            onClick={() => onModeChange(m)}
            className={`px-3 py-1.5 capitalize ${mode === m ? 'bg-blurple text-white' : 'bg-surface-2 text-ink-muted hover:text-ink'}`}
          >
            {m}
          </button>
        ))}
      </div>
      <span className="text-xs text-ink-dim">→ {recipients}</span>

      <div className="ml-auto flex items-center gap-2">
        {busy && <Loader2 className="h-4 w-4 animate-spin text-ink-dim" />}
        {status === 'draft' && (
          <button type="button" disabled={busy || !passed} onClick={() => onAction('submit')} className="btn btn-ghost">
            Submit for review
          </button>
        )}
        {status === 'in_review' && isApprover && (
          <>
            <button type="button" disabled={busy} onClick={() => onAction('request_changes')} className="btn btn-ghost">
              Request changes
            </button>
            <button type="button" disabled={busy || !passed} onClick={() => onAction('approve')} className="btn btn-primary">
              Approve
            </button>
          </>
        )}
        {status !== 'sent' && (
          <button
            type="button"
            disabled={sendDisabled}
            title={mode === 'live' && !canLive ? 'Live send needs an approver and an approved draft' : undefined}
            onClick={() => onAction('send')}
            className={`btn ${mode === 'live' ? 'btn-green' : 'btn-primary'}`}
          >
            <Send className="h-4 w-4" /> Send {mode}
          </button>
        )}
        {status === 'sent' && <span className="text-sm font-medium text-green">Sent ✓</span>}
      </div>
    </div>
  )
}

function StatusChip({ status }: { status: string }) {
  const map: Record<string, string> = {
    draft: 'bg-elevated text-ink-muted',
    in_review: 'bg-[#b7791f]/15 text-[#b7791f]',
    approved: 'bg-blurple/20 text-[#4752c4]',
    sent: 'bg-green/15 text-green',
    failed: 'bg-danger/15 text-danger',
  }
  return <span className={`chip capitalize ${map[status] || 'bg-elevated text-ink-muted'}`}>{status.replace('_', ' ')}</span>
}
