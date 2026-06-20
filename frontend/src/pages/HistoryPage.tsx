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
      <h1 className="font-display text-2xl font-bold text-ink">History</h1>
      <p className="mt-1 text-sm text-ink-muted">Emails sent through Coco. (Emails sent via Gmail or Markaz show on each candidate&rsquo;s timeline.)</p>

      <div className="card mt-6 overflow-hidden">
        {q.isLoading ? (
          <Spinner label="Loading…" />
        ) : !q.data?.length ? (
          <div className="mx-auto flex max-w-sm flex-col items-center py-16 text-center text-sm text-ink-dim">
            <History className="mb-2 h-7 w-7 text-ink-dim" />
            <p className="font-medium text-ink-muted">Nothing sent through Coco yet</p>
            <p className="mt-1">Emails you draft, approve and send here will be logged in this history. Emails already sent via Gmail or Markaz appear on each candidate&rsquo;s timeline instead.</p>
          </div>
        ) : (
          <table className="w-full text-left text-sm">
            <thead className="border-b border-hairline bg-surface-2 text-xs uppercase tracking-wide text-ink-dim">
              <tr>
                <th className="px-5 py-3 font-medium">Subject</th>
                <th className="px-5 py-3 font-medium">Role</th>
                <th className="px-5 py-3 font-medium">Type</th>
                <th className="px-5 py-3 font-medium">Sent</th>
                <th className="px-5 py-3 font-medium">Mode</th>
                <th className="px-5 py-3" />
              </tr>
            </thead>
            <tbody className="divide-y divide-hairline">
              {q.data.map((c) => (
                <tr key={c.id} onClick={() => navigate(`/drafts/${c.id}`)} className="cursor-pointer transition-colors hover:bg-elevated">
                  <td className="px-5 py-3 font-medium text-ink">{c.title_line || '(untitled)'}</td>
                  <td className="px-5 py-3 text-ink-muted">{c.role_title}</td>
                  <td className="px-5 py-3 text-ink-dim">{c.email_type.replace('_', ' ')}</td>
                  <td className="px-5 py-3 text-ink-dim">{formatDate(c.sent_at)}</td>
                  <td className="px-5 py-3"><span className="chip bg-green/15 text-green">{c.mode || 'live'}</span></td>
                  <td className="px-5 py-3 text-right text-sm font-medium text-[#4752c4]">View →</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}
