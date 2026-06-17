import { useQuery } from '@tanstack/react-query'
import { History } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { Spinner } from '../components/Spinner'
import { api } from '../lib/api'
import { formatDate } from '../lib/format'

export function HistoryPage() {
  const navigate = useNavigate()
  const q = useQuery({ queryKey: ['comms', 'sent'], queryFn: () => api.listCommunications({ status: 'sent' }) })

  return (
    <div className="mx-auto max-w-5xl px-8 py-7">
      <h1 className="text-xl font-semibold text-slate-900">History</h1>
      <p className="mt-1 text-sm text-slate-500">Communications that have been sent.</p>

      <div className="mt-6 overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm">
        {q.isLoading ? (
          <Spinner label="Loading…" />
        ) : !q.data?.length ? (
          <div className="flex flex-col items-center py-16 text-center text-sm text-slate-500">
            <History className="mb-2 h-7 w-7 text-slate-400" />
            No communications sent yet.
          </div>
        ) : (
          <table className="w-full text-left text-sm">
            <thead className="border-b border-slate-200 bg-slate-50 text-xs uppercase tracking-wide text-slate-500">
              <tr>
                <th className="px-5 py-3 font-medium">Subject</th>
                <th className="px-5 py-3 font-medium">Role</th>
                <th className="px-5 py-3 font-medium">Type</th>
                <th className="px-5 py-3 font-medium">Sent</th>
                <th className="px-5 py-3 font-medium">Mode</th>
                <th className="px-5 py-3" />
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {q.data.map((c) => (
                <tr key={c.id} onClick={() => navigate(`/drafts/${c.id}`)} className="cursor-pointer transition-colors hover:bg-slate-50">
                  <td className="px-5 py-3 font-medium text-slate-900">{c.title_line || '(untitled)'}</td>
                  <td className="px-5 py-3 text-slate-600">{c.role_title}</td>
                  <td className="px-5 py-3 text-slate-500">{c.email_type.replace('_', ' ')}</td>
                  <td className="px-5 py-3 text-slate-500">{formatDate(c.sent_at)}</td>
                  <td className="px-5 py-3"><span className="rounded-md bg-sent-bg px-2 py-0.5 text-xs font-medium text-sent">{c.mode || 'live'}</span></td>
                  <td className="px-5 py-3 text-right text-sm font-medium text-brand-600">View →</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}
