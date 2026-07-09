import { EMAIL_TYPES } from './types'
import type { QueueRow } from './types'

export function fullName(p: {
  first_name?: string | null
  last_name?: string | null
}): string {
  return [p.first_name, p.last_name].filter(Boolean).join(' ').trim() || 'Unknown'
}

export function initials(p: {
  first_name?: string | null
  last_name?: string | null
}): string {
  const f = (p.first_name || '').trim()[0] || ''
  const l = (p.last_name || '').trim()[0] || ''
  return (f + l).toUpperCase() || '?'
}

export function formatDate(value?: string | null): string {
  if (!value) return '—'
  const d = new Date(value)
  if (isNaN(d.getTime())) return '—'
  return d.toLocaleDateString(undefined, {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  })
}

export function scorecardLabel(row: QueueRow): string {
  const parts: string[] = []
  if (row.values_filled) parts.push('Values')
  if (row.gwc_filled) parts.push('GWC')
  return parts.length ? parts.join(' + ') : '—'
}

export function relativeTime(value?: string | null): string {
  if (!value) return 'never'
  const then = new Date(value).getTime()
  if (isNaN(then)) return '—'
  const secs = Math.max(0, Math.round((Date.now() - then) / 1000))
  if (secs < 60) return 'just now'
  const mins = Math.round(secs / 60)
  if (mins < 60) return `${mins}m ago`
  const hrs = Math.round(mins / 60)
  if (hrs < 24) return `${hrs}h ago`
  const days = Math.round(hrs / 24)
  return `${days}d ago`
}

export function emailTypeLabel(value?: string | null): string {
  if (!value) return '—'
  return EMAIL_TYPES.find((t) => t.value === value)?.label ?? value
}

/** The one-line "what to do next" for a candidate row. */
export function suggestedAction(row: QueueRow): string {
  switch (row.display_status) {
    case 'high_priority':
    case 'needs_comms':
      return `Draft ${emailTypeLabel(row.required_email_type).toLowerCase()}`
    case 'in_progress':
      return 'Continue draft'
    case 'sent':
      return 'View'
    case 'needs_review':
      return 'Verify Gmail match'
    case 'ignored':
      return 'Ignored'
    case 'shortlisted':
      return 'Shortlisted · awaiting decision'
    case 'interview_scheduled':
      return 'Interview scheduled'
    case 'case_study':
      return 'Case study sent'
    case 'awaiting_scorecard':
      return 'Awaiting decision'
    default:
      return 'Review'
  }
}
