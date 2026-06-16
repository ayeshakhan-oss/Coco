import type { LucideIcon } from 'lucide-react'

interface StatCardProps {
  label: string
  value: number
  icon: LucideIcon
  tone: 'amber' | 'brand' | 'green' | 'slate'
  active?: boolean
  onClick?: () => void
}

const TONES: Record<StatCardProps['tone'], { ring: string; icon: string; bar: string }> = {
  amber: { ring: 'ring-review/30', icon: 'bg-review-bg text-review', bar: 'bg-review' },
  brand: { ring: 'ring-brand-500/30', icon: 'bg-brand-50 text-brand-600', bar: 'bg-brand-500' },
  green: { ring: 'ring-sent/30', icon: 'bg-sent-bg text-sent', bar: 'bg-sent' },
  slate: { ring: 'ring-slate-300', icon: 'bg-slate-100 text-slate-500', bar: 'bg-slate-400' },
}

export function StatCard({ label, value, icon: Icon, tone, active, onClick }: StatCardProps) {
  const t = TONES[tone]
  return (
    <button
      type="button"
      onClick={onClick}
      className={`group relative flex cursor-pointer items-center gap-4 overflow-hidden rounded-xl border border-slate-200 bg-white p-4 text-left shadow-sm transition-all duration-200 hover:shadow-md ${
        active ? `ring-2 ${t.ring}` : ''
      }`}
    >
      <span className={`absolute left-0 top-0 h-full w-1 ${t.bar}`} />
      <span className={`flex h-11 w-11 items-center justify-center rounded-lg ${t.icon}`}>
        <Icon className="h-5 w-5" />
      </span>
      <span>
        <span className="block text-2xl font-semibold tabular-nums text-slate-900">{value}</span>
        <span className="block text-xs font-medium uppercase tracking-wide text-slate-500">
          {label}
        </span>
      </span>
    </button>
  )
}
