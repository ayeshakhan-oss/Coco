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
  { slug: 'hiring-operations', label: 'Hiring Operations', icon: Building2, status: 'live', route: '/attendance', blurb: 'Daily attendance, decision briefs and the hiring funnel, from Markaz and the mailbox.' },
  { slug: 'data-systems', label: 'Data & Systems', icon: Database, status: 'live', route: '/system', blurb: 'What is configured, what exists in the database, and what is known to be broken.' },
  { slug: 'talent-sourcing', label: 'Talent Sourcing', icon: Search, status: 'live', route: '/sourcing', blurb: 'The passive candidate pool and who has been approached. Searching still runs in Claude Code.' },
  { slug: 'candidate-invites', label: 'Candidate Invites', icon: Send, status: 'live', route: '/invites', blurb: 'Send interview and opportunity invites for every stage, in the locked design.' },
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
  { prefix: '/hiring-brief', slug: 'hiring-operations' },
  { prefix: '/sourcing', slug: 'talent-sourcing' },
  { prefix: '/invites', slug: 'candidate-invites' },
  { prefix: '/system', slug: 'data-systems' },
  { prefix: '/values-scorecards', slug: 'candidate-evaluation' },
  { prefix: '/case-studies', slug: 'candidate-evaluation' },
]

export const moduleForPath = (pathname: string): ModuleDef => {
  const matches = ROUTE_OWNERS.filter((o) => pathname.startsWith(o.prefix))
  if (matches.length === 0) return activeModule()
  const best = matches.reduce((a, b) => (b.prefix.length > a.prefix.length ? b : a))
  return moduleBySlug(best.slug) ?? activeModule()
}

// Which skill folder backs each module, so a card can say what sits behind it
// rather than only its title. The live counts come from /api/skills; this is
// just the label, and `/skills` is where the files themselves are listed.
export const MODULE_SKILL_DIR: Record<string, string> = {
  'candidate-communication': '01_candidate-communication',
  'candidate-evaluation': '02_candidate-evaluation',
  'hiring-operations': '03_operations',
  'data-systems': '04_data-and-systems',
  'talent-sourcing': '05_talent-sourcing',
  'candidate-invites': '06_candidate-invites',
}

export const SKILL_FOR_MODULE: Record<string, string> = {
  'candidate-communication': '8 letter types',
  'candidate-evaluation': '6 evaluation skills',
  'hiring-operations': '5 operations skills',
  'data-systems': '6 systems skills',
  'talent-sourcing': 'sourcing workflow',
  'candidate-invites': '7 invite types',
}
