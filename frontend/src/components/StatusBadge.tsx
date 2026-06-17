import type { ReactNode } from 'react'
import type { Bucket } from '../lib/types'

const BUCKET_STYLES: Record<Bucket, { label: string; cls: string }> = {
  needs_comms: { label: 'Needs comms', cls: 'bg-magenta/15 text-magenta' },
  in_progress: { label: 'In progress', cls: 'bg-blurple/20 text-[#aab2ff]' },
  sent: { label: 'Sent', cls: 'bg-green/15 text-green' },
  awaiting_scorecard: { label: 'No scorecard', cls: 'bg-elevated text-ink-dim' },
}

export function StatusBadge({ bucket }: { bucket: Bucket }) {
  const s = BUCKET_STYLES[bucket]
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
    brand: 'bg-blurple/20 text-[#aab2ff]',
  }
  return <span className={`inline-flex items-center rounded-md px-2 py-0.5 text-xs font-medium ${tones[tone]}`}>{children}</span>
}
