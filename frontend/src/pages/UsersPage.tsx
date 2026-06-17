import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { ShieldAlert, UserPlus } from 'lucide-react'
import { useState } from 'react'
import { Spinner } from '../components/Spinner'
import { ApiError, api } from '../lib/api'
import { formatDate } from '../lib/format'
import { ROLE_LABELS, isSuperAdmin } from '../lib/roles'

export function UsersPage() {
  const qc = useQueryClient()
  const meQ = useQuery({ queryKey: ['me'], queryFn: api.me, retry: false })
  const usersQ = useQuery({ queryKey: ['users'], queryFn: api.listUsers, enabled: isSuperAdmin(meQ.data?.app_role) })

  const [email, setEmail] = useState('')
  const [role, setRole] = useState('viewer')
  const [err, setErr] = useState<string | null>(null)

  const onErr = (e: unknown) => setErr((e as ApiError).message)
  const done = () => { setErr(null); qc.invalidateQueries({ queryKey: ['users'] }) }

  const createM = useMutation({
    mutationFn: () => api.createUser({ email: email.trim(), app_role: role }),
    onSuccess: () => { setEmail(''); setRole('viewer'); done() },
    onError: onErr,
  })
  const updateM = useMutation({
    mutationFn: (v: { id: string; app_role?: string; active?: boolean }) => api.updateUser(v.id, { app_role: v.app_role, active: v.active }),
    onSuccess: done,
    onError: onErr,
  })

  if (!isSuperAdmin(meQ.data?.app_role)) {
    return (
      <div className="mx-auto max-w-2xl px-8 py-16 text-center text-ink-muted">
        <ShieldAlert className="mx-auto mb-3 h-8 w-8 text-ink-dim" />
        Only a Super Admin can manage users.
      </div>
    )
  }

  return (
    <div className="mx-auto max-w-4xl px-8 py-7">
      <h1 className="font-display text-2xl font-bold text-ink">Users</h1>
      <p className="mt-1 text-sm text-ink-muted">Only people listed here can sign in. Set each person's role.</p>

      {/* Add user */}
      <form
        className="card mt-6 flex flex-wrap items-end gap-3 p-4"
        onSubmit={(e) => { e.preventDefault(); if (email.trim()) createM.mutate() }}
      >
        <div className="flex-1">
          <label className="mb-1 block text-xs font-semibold uppercase tracking-wide text-ink-dim">Add by email</label>
          <input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="name@taleemabad.com" className="input" />
        </div>
        <div>
          <label className="mb-1 block text-xs font-semibold uppercase tracking-wide text-ink-dim">Role</label>
          <select value={role} onChange={(e) => setRole(e.target.value)} className="input w-auto">
            {ROLE_LABELS.map((r) => (<option key={r.value} value={r.value}>{r.label}</option>))}
          </select>
        </div>
        <button type="submit" disabled={createM.isPending || !email.trim()} className="btn btn-primary">
          <UserPlus className="h-4 w-4" /> Add user
        </button>
      </form>

      {err && <div className="mt-3 rounded-xl bg-danger/15 px-3 py-2 text-sm text-danger">{err}</div>}

      <div className="card mt-6 overflow-hidden">
        {usersQ.isLoading ? (
          <Spinner label="Loading users…" />
        ) : (
          <table className="w-full text-left text-sm">
            <thead className="border-b border-hairline bg-surface-2 text-xs uppercase tracking-wide text-ink-dim">
              <tr>
                <th className="px-5 py-3 font-medium">User</th>
                <th className="px-5 py-3 font-medium">Role</th>
                <th className="px-5 py-3 font-medium">Last login</th>
                <th className="px-5 py-3 font-medium">Status</th>
                <th className="px-5 py-3" />
              </tr>
            </thead>
            <tbody className="divide-y divide-hairline">
              {usersQ.data?.map((u) => {
                const isMe = u.id === meQ.data?.id
                return (
                  <tr key={u.id} className={u.active ? '' : 'opacity-50'}>
                    <td className="px-5 py-3">
                      <div className="font-medium text-ink">{[u.first_name, u.last_name].filter(Boolean).join(' ') || u.email}</div>
                      <div className="text-xs text-ink-dim">{u.email}{isMe && ' · you'}</div>
                    </td>
                    <td className="px-5 py-3">
                      <select
                        value={u.app_role}
                        onChange={(e) => updateM.mutate({ id: u.id, app_role: e.target.value })}
                        className="input w-auto py-1.5 text-xs"
                      >
                        {ROLE_LABELS.map((r) => (<option key={r.value} value={r.value}>{r.label}</option>))}
                      </select>
                    </td>
                    <td className="px-5 py-3 text-ink-dim">{u.last_login_at ? formatDate(u.last_login_at) : 'never'}</td>
                    <td className="px-5 py-3">
                      <span className={`chip ${u.active ? 'bg-green/15 text-green' : 'bg-elevated text-ink-dim'}`}>{u.active ? 'active' : 'inactive'}</span>
                    </td>
                    <td className="px-5 py-3 text-right">
                      {!isMe && (
                        <button
                          type="button"
                          onClick={() => updateM.mutate({ id: u.id, active: !u.active })}
                          className="text-sm font-medium text-[#aab2ff] hover:underline"
                        >
                          {u.active ? 'Deactivate' : 'Activate'}
                        </button>
                      )}
                    </td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}
