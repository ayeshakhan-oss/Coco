export const ROLE_LEVEL: Record<string, number> = {
  viewer: 0,
  editor: 1,
  approver: 2,
  super_admin: 3,
}

export const ROLE_LABELS: { value: string; label: string }[] = [
  { value: 'viewer', label: 'Viewer' },
  { value: 'editor', label: 'Editor' },
  { value: 'approver', label: 'Approver' },
  { value: 'super_admin', label: 'Super Admin' },
]

const level = (r?: string | null) => ROLE_LEVEL[r ?? ''] ?? 0

export const canEdit = (r?: string | null) => level(r) >= ROLE_LEVEL.editor
export const canApprove = (r?: string | null) => level(r) >= ROLE_LEVEL.approver
export const isSuperAdmin = (r?: string | null) => r === 'super_admin'

export function roleLabel(role: string): string {
  return ROLE_LABELS.find((r) => r.value === role)?.label ?? role
}
