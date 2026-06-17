import type { LucideIcon } from 'lucide-react'

interface StatCardProps {
  label: string
  value: number
  icon: LucideIcon
  tone: 'amber' | 'brand' | 'green' | 'slate'
  active?: boolean
  onClick?: () => void
}

const TONES: Record<StatCardProps['tone'], { icon: string; bar: string; ring: string }> = {
  amber: { icon: 'bg-magenta/15 text-magenta', bar: 'bg-magenta', ring: 'ring-magenta/50' },
  brand: { icon: 'bg-blurple/20 text-[#aab2ff]', bar: 'bg-blurple', ring: 'ring-blurple/60' },
  green: { icon: 'bg-green/15 text-green', bar: 'bg-green', ring: 'ring-green/50' },
  slate: { icon: 'bg-elevated text-ink-dim', bar: 'bg-ink-dim', ring: 'ring-ink-dim/50' },
}

export function StatCard({ label, value, icon: Icon, tone, active, onClick }: StatCardProps) {
  const t = TONES[tone]
  return (
    <button
      type="button"
      onClick={onClick}
      className={`group relative flex cursor-pointer items-center gap-4 overflow-hidden rounded-2xl border border-hairline bg-surface p-4 text-left transition-all duration-200 hover:bg-elevated ${
        active ? `ring-2 ${t.ring}` : ''
      }`}
    >
      <span className={`absolute left-0 top-0 h-full w-1 ${t.bar}`} />
      <span className={`flex h-11 w-11 items-center justify-center rounded-xl ${t.icon}`}>
        <Icon className="h-5 w-5" />
      </span>
      <span>
        <span className="block font-display text-2xl font-bold tabular-nums text-ink">{value}</span>
        <span className="block text-xs font-medium uppercase tracking-wide text-ink-dim">{label}</span>
      </span>
    </button>
  )
}
