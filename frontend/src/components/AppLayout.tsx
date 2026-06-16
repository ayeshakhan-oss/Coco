import { useQuery } from '@tanstack/react-query'
import { ClipboardList, History, Inbox, LogOut, Mail } from 'lucide-react'
import { NavLink, Outlet } from 'react-router-dom'
import { api } from '../lib/api'
import { fullName, initials } from '../lib/format'

const NAV = [
  { to: '/', label: 'Queue', icon: ClipboardList, end: true },
  { to: '/review', label: 'Review', icon: Inbox, end: false },
  { to: '/history', label: 'History', icon: History, end: false },
]

export function AppLayout() {
  const { data: me } = useQuery({ queryKey: ['me'], queryFn: api.me, retry: false })

  return (
    <div className="flex h-full">
      {/* Sidebar */}
      <aside className="flex w-60 flex-shrink-0 flex-col border-r border-slate-200 bg-white">
        <div className="flex items-center gap-2 px-5 py-5">
          <span className="flex h-9 w-9 items-center justify-center rounded-lg bg-brand-500 text-white">
            <Mail className="h-5 w-5" />
          </span>
          <div>
            <div className="text-sm font-semibold text-slate-900">Coco</div>
            <div className="text-[11px] text-slate-500">Candidate Communication</div>
          </div>
        </div>

        <nav className="flex-1 space-y-1 px-3 py-2">
          {NAV.map(({ to, label, icon: Icon, end }) => (
            <NavLink
              key={to}
              to={to}
              end={end}
              className={({ isActive }) =>
                `flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors ${
                  isActive
                    ? 'bg-brand-50 text-brand-700'
                    : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
                }`
              }
            >
              <Icon className="h-4 w-4" />
              {label}
            </NavLink>
          ))}
        </nav>

        {/* Account */}
        <div className="border-t border-slate-200 p-3">
          <div className="flex items-center gap-3 rounded-lg px-2 py-2">
            <span className="flex h-9 w-9 items-center justify-center rounded-full bg-slate-200 text-xs font-semibold text-slate-700">
              {me ? initials(me) : '··'}
            </span>
            <div className="min-w-0 flex-1">
              <div className="truncate text-sm font-medium text-slate-900">
                {me ? fullName(me) : 'Loading…'}
              </div>
              <div className="truncate text-[11px] capitalize text-slate-500">
                {me?.app_role ?? '—'}
              </div>
            </div>
            <a
              href="/auth/logout"
              title="Sign out"
              className="rounded-md p-1.5 text-slate-400 transition-colors hover:bg-slate-100 hover:text-slate-700"
            >
              <LogOut className="h-4 w-4" />
            </a>
          </div>
        </div>
      </aside>

      {/* Main */}
      <div className="flex min-w-0 flex-1 flex-col overflow-hidden">
        <main className="flex-1 overflow-auto">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
