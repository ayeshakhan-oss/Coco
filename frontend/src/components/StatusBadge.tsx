import type { ReactNode } from 'react'
import type { DisplayStatus } from '../lib/types'

const STATUS_STYLES: Record<DisplayStatus, { label: string; cls: string }> = {
  needs_comms: { label: 'Needs comms', cls: 'bg-magenta/15 text-magenta' },
  high_priority: { label: 'High priority', cls: 'bg-danger/15 text-danger' },
  in_progress: { label: 'In progress', cls: 'bg-blurple/20 text-[#4752c4]' },
  sent: { label: 'Sent', cls: 'bg-green/15 text-green' },
  needs_review: { label: 'Needs review', cls: 'bg-cyan/15 text-cyan' },
  awaiting_scorecard: { label: 'Awaiting scorecard', cls: 'bg-elevated text-ink-dim' },
}

export function StatusBadge({ status }: { status?: DisplayStatus | null }) {
  const s = STATUS_STYLES[status ?? 'awaiting_scorecard'] ?? STATUS_STYLES.awaiting_scorecard
  return (
    <span className={`chip ${s.cls}`}>
      <span className="h-1.5 w-1.5 rounded-full bg-current opacity-80" />
      {s.label}
    </span>
  )
}

export function Pill({
  children,
  tone = 'slate',
}: {
  children: ReactNode
  tone?: 'slate' | 'green' | 'red' | 'brand'
}) {
  const tones: Record<string, string> = {
    slate: 'bg-elevated text-ink-muted',
    green: 'bg-green/15 text-green',
    red: 'bg-danger/15 text-danger',
    brand: 'bg-blurple/20 text-[#4752c4]',
  }
  return <span className={`inline-flex items-center rounded-md px-2 py-0.5 text-xs font-medium ${tones[tone]}`}>{children}</span>
}
