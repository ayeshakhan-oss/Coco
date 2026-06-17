import { useQuery } from '@tanstack/react-query'
import { ClipboardList, History, Inbox, LogOut, Mail, Users } from 'lucide-react'
import { NavLink, Outlet } from 'react-router-dom'
import { api } from '../lib/api'
import { fullName, initials } from '../lib/format'

export function AppLayout() {
  const { data: me } = useQuery({ queryKey: ['me'], queryFn: api.me, retry: false })
  const isSuperAdmin = me?.app_role === 'super_admin'

  const nav = [
    { to: '/', label: 'Queue', icon: ClipboardList, end: true },
    { to: '/review', label: 'Review', icon: Inbox, end: false },
    { to: '/history', label: 'History', icon: History, end: false },
    ...(isSuperAdmin ? [{ to: '/users', label: 'Users', icon: Users, end: false }] : []),
  ]

  return (
    <div className="flex h-full bg-canvas">
      <aside className="flex w-60 flex-shrink-0 flex-col border-r border-hairline bg-surface">
        <div className="flex items-center gap-2.5 px-5 py-5">
          <span className="flex h-9 w-9 items-center justify-center rounded-xl bg-blurple text-white">
            <Mail className="h-5 w-5" />
          </span>
          <div>
            <div className="font-display text-base font-bold tracking-tight text-ink">Coco</div>
            <div className="text-[11px] text-ink-dim">Candidate Comms</div>
          </div>
        </div>

        <nav className="flex-1 space-y-1 px-3 py-2">
          {nav.map(({ to, label, icon: Icon, end }) => (
            <NavLink
              key={to}
              to={to}
              end={end}
              className={({ isActive }) =>
                `flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition-colors ${
                  isActive ? 'bg-blurple text-white' : 'text-ink-muted hover:bg-elevated hover:text-ink'
                }`
              }
            >
              <Icon className="h-4 w-4" />
              {label}
            </NavLink>
          ))}
        </nav>

        <div className="border-t border-hairline p-3">
          <div className="flex items-center gap-3 rounded-xl px-2 py-2">
            <span className="flex h-9 w-9 items-center justify-center rounded-full bg-elevated text-xs font-semibold text-ink">
              {me ? initials(me) : '··'}
            </span>
            <div className="min-w-0 flex-1">
              <div className="truncate text-sm font-medium text-ink">{me ? fullName(me) : 'Loading…'}</div>
              <div className="truncate text-[11px] capitalize text-ink-dim">{me?.app_role?.replace('_', ' ') ?? '—'}</div>
            </div>
            <a
              href="/auth/logout"
              title="Sign out"
              className="rounded-lg p-1.5 text-ink-dim transition-colors hover:bg-elevated hover:text-ink"
            >
              <LogOut className="h-4 w-4" />
            </a>
          </div>
        </div>
      </aside>

      <div className="flex min-w-0 flex-1 flex-col overflow-hidden">
        <main className="flex-1 overflow-auto">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
