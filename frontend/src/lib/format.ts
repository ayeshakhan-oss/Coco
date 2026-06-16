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
