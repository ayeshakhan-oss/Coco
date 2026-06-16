import type { ReactNode } from 'react'
import type { Bucket } from '../lib/types'

const BUCKET_STYLES: Record<Bucket, { label: string; cls: string }> = {
  needs_comms: { label: 'Needs comms', cls: 'bg-review-bg text-review' },
  in_progress: { label: 'In progress', cls: 'bg-brand-50 text-brand-700' },
  sent: { label: 'Sent', cls: 'bg-sent-bg text-sent' },
  awaiting_scorecard: { label: 'No scorecard', cls: 'bg-slate-100 text-slate-600' },
}

export function StatusBadge({ bucket }: { bucket: Bucket }) {
  const s = BUCKET_STYLES[bucket]
  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-xs font-medium ${s.cls}`}
    >
      <span className="h-1.5 w-1.5 rounded-full bg-current opacity-70" />
      {s.label}
    </span>
  )
}

export function Pill({ children, tone = 'slate' }: { children: ReactNode; tone?: 'slate' | 'green' | 'red' | 'brand' }) {
  const tones: Record<string, string> = {
    slate: 'bg-slate-100 text-slate-700',
    green: 'bg-sent-bg text-sent',
    red: 'bg-block-bg text-block',
    brand: 'bg-brand-50 text-brand-700',
  }
  return (
    <span className={`inline-flex items-center rounded-md px-2 py-0.5 text-xs font-medium ${tones[tone]}`}>
      {children}
    </span>
  )
}
