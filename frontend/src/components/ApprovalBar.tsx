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
  const recipients = mode === 'pilot' ? 'ayesha.khan@taleemabad.com (pilot only)' : 'candidate + hiring@taleemabad.com + Ayesha'
  const canLive = isApprover && status === 'approved'
  const sendDisabled = busy || !passed || (mode === 'live' && !canLive)

  const btn = 'inline-flex items-center gap-1.5 rounded-lg px-3.5 py-2 text-sm font-medium transition-colors disabled:cursor-not-allowed disabled:opacity-50'

  return (
    <div className="flex flex-wrap items-center gap-3 border-t border-slate-200 bg-white px-4 py-3">
      <StatusChip status={status} />

      {/* Pilot / Live toggle */}
      <div className="flex overflow-hidden rounded-lg border border-slate-200 text-sm">
        {(['pilot', 'live'] as const).map((m) => (
          <button
            key={m}
            type="button"
            onClick={() => onModeChange(m)}
            className={`px-3 py-1.5 capitalize ${mode === m ? 'bg-brand-500 text-white' : 'bg-white text-slate-600 hover:bg-slate-50'}`}
          >
            {m}
          </button>
        ))}
      </div>
      <span className="text-xs text-slate-500">→ {recipients}</span>

      <div className="ml-auto flex items-center gap-2">
        {busy && <Loader2 className="h-4 w-4 animate-spin text-slate-400" />}
        {status === 'draft' && (
          <button type="button" disabled={busy || !passed} onClick={() => onAction('submit')} className={`${btn} bg-slate-100 text-slate-700 hover:bg-slate-200`}>
            Submit for review
          </button>
        )}
        {status === 'in_review' && isApprover && (
          <>
            <button type="button" disabled={busy} onClick={() => onAction('request_changes')} className={`${btn} bg-slate-100 text-slate-700 hover:bg-slate-200`}>
              Request changes
            </button>
            <button type="button" disabled={busy || !passed} onClick={() => onAction('approve')} className={`${btn} bg-brand-50 text-brand-700 hover:bg-brand-100`}>
              Approve
            </button>
          </>
        )}
        {status !== 'sent' && (
          <button
            type="button"
            disabled={sendDisabled}
            title={mode === 'live' && !canLive ? 'Live send requires an approver and an approved draft' : undefined}
            onClick={() => onAction('send')}
            className={`${btn} bg-brand-500 text-white hover:bg-brand-600`}
          >
            <Send className="h-4 w-4" /> Send {mode}
          </button>
        )}
        {status === 'sent' && <span className="text-sm font-medium text-sent">Sent ✓</span>}
      </div>
    </div>
  )
}

function StatusChip({ status }: { status: string }) {
  const map: Record<string, string> = {
    draft: 'bg-slate-100 text-slate-600',
    in_review: 'bg-review-bg text-review',
    approved: 'bg-brand-50 text-brand-700',
    sent: 'bg-sent-bg text-sent',
    failed: 'bg-block-bg text-block',
  }
  return <span className={`rounded-full px-2.5 py-1 text-xs font-medium capitalize ${map[status] || 'bg-slate-100'}`}>{status.replace('_', ' ')}</span>
}
