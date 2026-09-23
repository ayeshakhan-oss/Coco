import type { LucideIcon } from 'lucide-react'
import { Building2, Database, FileSearch, Mail, Search, Send } from 'lucide-react'

export interface ModuleDef {
  slug: string
  label: string
  icon: LucideIcon
  status: 'live' | 'soon'
  blurb: string
  route?: string
}

export const ACTIVE_MODULE = 'candidate-communication'

export const MODULES: ModuleDef[] = [
  { slug: 'candidate-communication', label: 'Candidate Communication', icon: Mail, status: 'live', route: '/queue', blurb: 'Draft, review, approve and send candidate rejection and feedback emails.' },
  { slug: 'candidate-evaluation', label: 'Candidate Evaluation', icon: FileSearch, status: 'live', route: '/evaluations', blurb: 'Screen CVs, track and score case studies, run values scorecards, evaluate on KCD and read technical screening.' },
  { slug: 'hiring-operations', label: 'Hiring Operations', icon: Building2, status: 'live', route: '/attendance', blurb: 'Daily attendance and decision briefs, from Markaz. The hiring decision brief is on the way.' },
  { slug: 'data-systems', label: 'Data & Systems', icon: Database, status: 'soon', blurb: 'Reports, integrations and system infrastructure.' },
  { slug: 'talent-sourcing', label: 'Talent Sourcing', icon: Search, status: 'soon', blurb: 'Find and track passive candidates across sources.' },
  { slug: 'candidate-invites', label: 'Candidate Invites', icon: Send, status: 'soon', blurb: 'Send interview and opportunity invites for every stage.' },
]

export const activeModule = () => MODULES.find((m) => m.slug === ACTIVE_MODULE)!
export const liveModules = () => MODULES.filter((m) => m.status === 'live')
export const comingSoonModules = () => MODULES.filter((m) => m.status === 'soon')
export const moduleBySlug = (slug?: string) => MODULES.find((m) => m.slug === slug)

// Every URL prefix a live module owns, including detail/child routes that
// aren't in its own top-level `route` field (e.g. candidate-communication
// also owns /applications/:id and /drafts/:commId, reached by drilling into
// /queue or /review). Longest prefix wins so more specific routes never lose
// to a shorter one. Falls back to ACTIVE_MODULE for routes no module claims
// (home, /users).
const ROUTE_OWNERS: { prefix: string; slug: string }[] = [
  { prefix: '/queue', slug: 'candidate-communication' },
  { prefix: '/review', slug: 'candidate-communication' },
  { prefix: '/history', slug: 'candidate-communication' },
  { prefix: '/applications', slug: 'candidate-communication' },
  { prefix: '/drafts', slug: 'candidate-communication' },
  { prefix: '/evaluations', slug: 'candidate-evaluation' },
  { prefix: '/cv-screening', slug: 'candidate-evaluation' },
  { prefix: '/case-study-tracking', slug: 'candidate-evaluation' },
  { prefix: '/kcd-evaluations', slug: 'candidate-evaluation' },
  { prefix: '/attendance', slug: 'hiring-operations' },
  { prefix: '/decision-brief', slug: 'hiring-operations' },
  { prefix: '/values-scorecards', slug: 'candidate-evaluation' },
  { prefix: '/case-studies', slug: 'candidate-evaluation' },
]

export const moduleForPath = (pathname: string): ModuleDef => {
  const matches = ROUTE_OWNERS.filter((o) => pathname.startsWith(o.prefix))
  if (matches.length === 0) return activeModule()
  const best = matches.reduce((a, b) => (b.prefix.length > a.prefix.length ? b : a))
  return moduleBySlug(best.slug) ?? activeModule()
}
