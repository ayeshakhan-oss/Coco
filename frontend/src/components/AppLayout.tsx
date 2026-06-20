import { useQuery } from '@tanstack/react-query'
import { ChevronDown, ClipboardList, History, Inbox, LogOut, Sparkles, Users } from 'lucide-react'
import { useState } from 'react'
import { Link, NavLink, Outlet } from 'react-router-dom'
import { api } from '../lib/api'
import { fullName, initials } from '../lib/format'
import { ACTIVE_MODULE, MODULES } from '../lib/modules'

export function AppLayout() {
  const { data: me } = useQuery({ queryKey: ['me'], queryFn: api.me, retry: false })
  const isSuperAdmin = me?.app_role === 'super_admin'
  const [open, setOpen] = useState<string>(ACTIVE_MODULE) // which skill is expanded

  // Pages that belong to the live skill (Candidate Communication).
  const pages = [
    { to: '/', label: 'Candidates', icon: ClipboardList, end: true },
    { to: '/review', label: 'Review', icon: Inbox, end: false },
    { to: '/history', label: 'History', icon: History, end: false },
  ]

  return (
    <div className="flex h-full bg-canvas">
      <aside className="flex w-64 flex-shrink-0 flex-col border-r border-hairline bg-surface">
        {/* Coco — the agent */}
        <div className="flex items-center gap-2.5 px-5 py-5">
          <span className="flex h-9 w-9 items-center justify-center rounded-xl bg-blurple text-white">
            <Sparkles className="h-5 w-5" />
          </span>
          <div>
            <div className="font-display text-base font-bold tracking-tight text-ink">Coco</div>
            <div className="text-[11px] text-ink-dim">Your talent-acquisition agent</div>
          </div>
        </div>

        {/* Skills (all 6, numbered, click to expand) */}
        <nav className="flex-1 overflow-auto px-3 py-2">
          <div className="px-3 pb-1.5 text-[10px] font-semibold uppercase tracking-wide text-ink-dim">Skills</div>

          {MODULES.map((skill) => {
            const Icon = skill.icon
            const isLive = skill.slug === ACTIVE_MODULE
            const isOpen = open === skill.slug
            return (
              <div key={skill.slug} className="mb-0.5">
                <button
                  type="button"
                  onClick={() => setOpen(isOpen ? '' : skill.slug)}
                  className={`flex w-full items-center gap-2.5 rounded-xl px-3 py-2 text-sm transition-colors ${
                    isLive ? 'font-semibold text-ink hover:bg-elevated' : 'text-ink-dim hover:bg-surface-2 hover:text-ink-muted'
                  }`}
                >
                  <Icon className={`h-4 w-4 ${isLive ? 'text-blurple' : ''}`} />
                  <span className="flex-1 truncate text-left">{skill.label}</span>
                  {isLive ? (
                    <span className="h-1.5 w-1.5 rounded-full bg-green" title="Live" />
                  ) : (
                    <span className="rounded-full bg-surface-2 px-1.5 py-0.5 text-[9px] font-semibold uppercase tracking-wide">soon</span>
                  )}
                  <ChevronDown className={`h-3.5 w-3.5 text-ink-dim transition-transform ${isOpen ? 'rotate-180' : ''}`} />
                </button>

                {isOpen && (
                  <div className="mb-1 mt-0.5 space-y-0.5 pl-8">
                    {isLive ? (
                      pages.map(({ to, label, icon: PIcon, end }) => (
                        <NavLink
                          key={to}
                          to={to}
                          end={end}
                          className={({ isActive }) =>
                            `flex items-center gap-2.5 rounded-lg px-3 py-1.5 text-sm font-medium transition-colors ${
                              isActive ? 'bg-blurple text-white' : 'text-ink-muted hover:bg-elevated hover:text-ink'
                            }`
                          }
                        >
                          <PIcon className="h-3.5 w-3.5" />
                          {label}
                        </NavLink>
                      ))
                    ) : (
                      <Link
                        to={`/modules/${skill.slug}`}
                        className="block rounded-lg px-3 py-1.5 text-xs leading-snug text-ink-dim hover:bg-surface-2 hover:text-ink-muted"
                      >
                        {skill.blurb} <span className="font-medium text-blurple">Learn more →</span>
                      </Link>
                    )}
                  </div>
                )}
              </div>
            )
          })}
        </nav>

        {/* Users — admin, sits just above the account block */}
        {isSuperAdmin && (
          <div className="border-t border-hairline px-3 py-2">
            <NavLink
              to="/users"
              className={({ isActive }) =>
                `flex items-center gap-3 rounded-xl px-3 py-2 text-sm font-medium transition-colors ${
                  isActive ? 'bg-blurple text-white' : 'text-ink-muted hover:bg-elevated hover:text-ink'
                }`
              }
            >
              <Users className="h-4 w-4" />
              Users
            </NavLink>
          </div>
        )}

        <div className="border-t border-hairline p-3">
          <div className="flex items-center gap-3 rounded-xl px-2 py-2">
            <span className="flex h-9 w-9 items-center justify-center rounded-full bg-elevated text-xs font-semibold text-ink">
              {me ? initials(me) : '··'}
            </span>
            <div className="min-w-0 flex-1">
              <div className="truncate text-sm font-medium text-ink">{me ? fullName(me) : 'Loading…'}</div>
              <div className="truncate text-[11px] capitalize text-ink-dim">{me?.app_role?.replace('_', ' ') ?? '—'}</div>
            </div>
            <a href="/auth/logout" title="Sign out" className="rounded-lg p-1.5 text-ink-dim transition-colors hover:bg-elevated hover:text-ink">
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
