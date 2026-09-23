import { useQuery } from '@tanstack/react-query'
import type { LucideIcon } from 'lucide-react'
import {
  CalendarCheck,
  CheckSquare,
  ChevronDown,
  ClipboardCheck,
  ClipboardList,
  FileBarChart,
  FileSearch,
  FileText,
  Gauge,
  History,
  Inbox,
  ListChecks,
  LogOut,
  Users,
} from 'lucide-react'
import { useEffect, useState } from 'react'
import { Link, NavLink, Outlet, useLocation } from 'react-router-dom'
import { api } from '../lib/api'
import { fullName, initials } from '../lib/format'
import { MODULES, moduleForPath } from '../lib/modules'

// Sub-pages per live module, keyed by module slug. `built: false` entries are
// real sub-skills that don't have a page yet — rendered as a non-link row
// with the same "soon" pill used at the module level, never as a dead link.
const MODULE_PAGES: Record<string, { to: string; label: string; icon: LucideIcon; end: boolean; built: boolean }[]> = {
  'candidate-communication': [
    { to: '/queue', label: 'Candidates', icon: ClipboardList, end: true, built: true },
    { to: '/review', label: 'Review', icon: Inbox, end: false, built: true },
    { to: '/history', label: 'History', icon: History, end: false, built: true },
  ],
  'candidate-evaluation': [
    { to: '/evaluations', label: 'Technical Screening', icon: FileSearch, end: true, built: true },
    { to: '/cv-screening', label: 'CV Screening', icon: FileText, end: true, built: true },
    { to: '/case-study-tracking', label: 'Case Study Evaluation', icon: ListChecks, end: true, built: true },
    { to: '/case-studies', label: 'Case Study Scoring', icon: ClipboardCheck, end: true, built: true },
    { to: '/kcd-evaluations', label: 'KCD Evaluation', icon: Gauge, end: true, built: true },
    { to: '/values-scorecards', label: 'Values Scorecards', icon: CheckSquare, end: true, built: true },
  ],
  'hiring-operations': [
    { to: '/attendance', label: 'Attendance', icon: CalendarCheck, end: true, built: true },
    { to: '', label: 'Decision Briefs', icon: FileBarChart, end: true, built: false },
    { to: '', label: 'Hiring Decision Brief', icon: ClipboardCheck, end: true, built: false },
  ],
}

export function AppLayout() {
  const { data: me } = useQuery({ queryKey: ['me'], queryFn: api.me, retry: false })
  const isSuperAdmin = me?.app_role === 'super_admin'
  const location = useLocation()
  const [open, setOpen] = useState<string>(() => moduleForPath(location.pathname).slug) // which skill is expanded

  // Keep the sidebar section in sync with whichever module the current route
  // belongs to, so e.g. landing on /evaluations directly (bookmark, reload)
  // doesn't leave candidate-communication expanded and evaluations collapsed.
  useEffect(() => {
    setOpen(moduleForPath(location.pathname).slug)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [location.pathname])

  return (
    <div className="flex h-full bg-canvas">
      <aside className="flex w-64 flex-shrink-0 flex-col border-r border-hairline bg-surface">
        {/* Coco — the agent (click to go Home) */}
        <Link to="/" className="flex items-center gap-2.5 px-5 py-5 transition-colors hover:bg-surface-2">
          <img src="/coco.png" alt="Coco" className="h-10 w-10 rounded-full object-cover" />
          <div>
            <div className="font-display text-base font-bold tracking-tight text-ink">Coco</div>
            <div className="text-[11px] text-ink-dim">Your talent-acquisition agent</div>
          </div>
        </Link>

        {/* Skills (all 6, numbered, click to expand) */}
        <nav className="flex-1 overflow-auto px-3 py-2">
          <div className="px-3 pb-1.5 text-[10px] font-semibold uppercase tracking-wide text-ink-dim">Skills</div>

          {MODULES.map((skill) => {
            const Icon = skill.icon
            const isLive = skill.status === 'live'
            const modulePages = MODULE_PAGES[skill.slug]
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
                    {isLive && modulePages && modulePages.length > 0 ? (
                      modulePages.map(({ to, label, icon: PIcon, end, built }) =>
                        built ? (
                          <NavLink
                            key={label}
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
                        ) : (
                          <div key={label} className="flex items-center gap-2.5 rounded-lg px-3 py-1.5 text-sm font-medium text-ink-dim">
                            <PIcon className="h-3.5 w-3.5" />
                            <span className="flex-1 truncate">{label}</span>
                            <span className="rounded-full bg-surface-2 px-1.5 py-0.5 text-[9px] font-semibold uppercase tracking-wide">soon</span>
                          </div>
                        ),
                      )
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
