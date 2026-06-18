import type { LucideIcon } from 'lucide-react'
import { Building2, Database, FileSearch, Mail, Search, Send } from 'lucide-react'

export interface ModuleDef {
  slug: string
  label: string
  icon: LucideIcon
  status: 'live' | 'soon'
  blurb: string
}

export const ACTIVE_MODULE = 'candidate-communication'

export const MODULES: ModuleDef[] = [
  { slug: 'candidate-communication', label: 'Candidate Communication', icon: Mail, status: 'live', blurb: 'Draft, review, approve and send candidate rejection and feedback emails.' },
  { slug: 'candidate-evaluation', label: 'Candidate Evaluation', icon: FileSearch, status: 'soon', blurb: 'Screen CVs, score case studies and interview scorecards.' },
  { slug: 'hiring-operations', label: 'Hiring Operations', icon: Building2, status: 'soon', blurb: 'Attendance reports, decision briefs and weekly pipeline monitoring.' },
  { slug: 'talent-sourcing', label: 'Talent Sourcing', icon: Search, status: 'soon', blurb: 'Find and track passive candidates across sources.' },
  { slug: 'candidate-invites', label: 'Candidate Invites', icon: Send, status: 'soon', blurb: 'Send interview and opportunity invites for every stage.' },
  { slug: 'data-systems', label: 'Data & Systems', icon: Database, status: 'soon', blurb: 'Reports, integrations and system infrastructure.' },
]

export const activeModule = () => MODULES.find((m) => m.slug === ACTIVE_MODULE)!
export const comingSoonModules = () => MODULES.filter((m) => m.status === 'soon')
export const moduleBySlug = (slug?: string) => MODULES.find((m) => m.slug === slug)
