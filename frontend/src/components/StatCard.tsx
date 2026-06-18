import type { LucideIcon } from 'lucide-react'

interface StatCardProps {
  label: string
  value: number
  icon: LucideIcon
  tone: 'amber' | 'brand' | 'green' | 'slate' | 'danger' | 'cyan'
  active?: boolean
  onClick?: () => void
}

const TONES: Record<StatCardProps['tone'], { icon: string; bar: string; ring: string }> = {
  amber: { icon: 'bg-magenta/15 text-magenta', bar: 'bg-magenta', ring: 'ring-magenta/50' },
  brand: { icon: 'bg-blurple/20 text-[#4752c4]', bar: 'bg-blurple', ring: 'ring-blurple/60' },
  green: { icon: 'bg-green/15 text-green', bar: 'bg-green', ring: 'ring-green/50' },
  slate: { icon: 'bg-elevated text-ink-dim', bar: 'bg-ink-dim', ring: 'ring-ink-dim/50' },
  danger: { icon: 'bg-danger/15 text-danger', bar: 'bg-danger', ring: 'ring-danger/50' },
  cyan: { icon: 'bg-cyan/15 text-cyan', bar: 'bg-cyan', ring: 'ring-cyan/50' },
}

export function StatCard({ label, value, icon: Icon, tone, active, onClick }: StatCardProps) {
  const t = TONES[tone]
  const cls = `relative flex items-center gap-4 overflow-hidden rounded-2xl border border-hairline bg-surface p-4 text-left shadow-sm ${
    onClick ? 'cursor-pointer transition-all duration-200 hover:bg-elevated' : ''
  } ${active ? `ring-2 ${t.ring}` : ''}`
  const inner = (
    <>
      <span className={`absolute left-0 top-0 h-full w-1 ${t.bar}`} />
      <span className={`flex h-11 w-11 items-center justify-center rounded-xl ${t.icon}`}>
        <Icon className="h-5 w-5" />
      </span>
      <span>
        <span className="block font-display text-2xl font-bold tabular-nums text-ink">{value}</span>
        <span className="block text-xs font-medium uppercase tracking-wide text-ink-dim">{label}</span>
      </span>
    </>
  )
  return onClick ? (
    <button type="button" onClick={onClick} className={cls}>{inner}</button>
  ) : (
    <div className={cls}>{inner}</div>
  )
}
