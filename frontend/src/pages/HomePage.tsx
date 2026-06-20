import { useQuery } from '@tanstack/react-query'
import { ArrowRight, Briefcase, CheckCircle2, ClipboardList, Inbox, Search } from 'lucide-react'
import { useState } from 'react'
import type { FormEvent } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { StatCard } from '../components/StatCard'
import { api } from '../lib/api'
import { ACTIVE_MODULE, MODULES } from '../lib/modules'

export function HomePage() {
  const navigate = useNavigate()
  const meQ = useQuery({ queryKey: ['me'], queryFn: api.me, retry: false })
  const statsQ = useQuery({ queryKey: ['stats'], queryFn: api.stats })
  const s = statsQ.data
  const [q, setQ] = useState('')
  const liveCount = MODULES.filter((m) => m.status === 'live').length

  function onSearch(e: FormEvent) {
    e.preventDefault()
    const term = q.trim()
    navigate(term ? `/queue?status=relevant&q=${encodeURIComponent(term)}` : '/queue')
  }

  return (
    <div className="mx-auto max-w-5xl px-8 py-12">
      {/* Hero */}
      <div className="text-center">
        <img src="/coco.png" alt="Coco" className="mx-auto h-24 w-24 rounded-full object-cover shadow-sm" />
        <h1 className="mt-4 font-display text-3xl font-bold tracking-tight text-ink">
          {meQ.data?.first_name ? `Hi ${meQ.data.first_name} — meet Coco` : 'Meet Coco'}
        </h1>
        <p className="mx-auto mt-2 max-w-xl text-sm leading-relaxed text-ink-muted">
          Your AI talent-acquisition agent for Taleemabad. Coco helps you screen, evaluate, communicate with,
          and keep track of every candidate — across the whole hiring journey, in one place.
        </p>
      </div>

      {/* Search */}
      <form
        onSubmit={onSearch}
        className="mx-auto mt-7 flex max-w-xl items-center gap-2 rounded-2xl border border-hairline bg-surface p-2 shadow-sm transition focus-within:ring-2 focus-within:ring-blurple/40"
      >
        <Search className="ml-2 h-5 w-5 text-ink-dim" />
        <input
          value={q}
          onChange={(e) => setQ(e.target.value)}
          placeholder="Search a candidate by name or email…"
          className="flex-1 bg-transparent px-1 text-sm text-ink outline-none placeholder:text-ink-dim"
        />
        <button type="submit" className="btn btn-primary">
          Search <ArrowRight className="h-4 w-4" />
        </button>
      </form>

      {/* At-a-glance overview */}
      <div className="mt-10 grid grid-cols-2 gap-4 sm:grid-cols-4">
        <StatCard label="Applications received" value={s?.total_applications ?? 0} icon={Inbox} tone="brand" />
        <StatCard label="Open positions" value={s?.open_positions ?? 0} icon={Briefcase} tone="violet" />
        <StatCard label="Needs comms" value={s?.needs_comms ?? 0} icon={ClipboardList} tone="amber" onClick={() => navigate('/queue?status=needs_comms')} />
        <StatCard label="Sent" value={s?.sent ?? 0} icon={CheckCircle2} tone="green" onClick={() => navigate('/queue?status=already_sent')} />
      </div>

      {/* Skills */}
      <div className="mt-12">
        <div className="mb-3 flex items-baseline justify-between">
          <h2 className="font-display text-lg font-bold text-ink">Coco&rsquo;s skills</h2>
          <span className="text-sm text-ink-dim">{liveCount} of {MODULES.length} live</span>
        </div>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {MODULES.map((skill) => {
            const Icon = skill.icon
            const isLive = skill.slug === ACTIVE_MODULE
            return (
              <Link
                key={skill.slug}
                to={isLive ? '/queue' : `/modules/${skill.slug}`}
                className="card flex flex-col p-5 transition-colors hover:bg-elevated"
              >
                <div className="flex items-center gap-3">
                  <span className={`flex h-10 w-10 items-center justify-center rounded-xl ${isLive ? 'bg-blurple/15 text-blurple' : 'bg-surface-2 text-ink-dim'}`}>
                    <Icon className="h-5 w-5" />
                  </span>
                  <span className="font-semibold text-ink">{skill.label}</span>
                  {isLive ? (
                    <span className="chip ml-auto bg-green/15 text-green">Live</span>
                  ) : (
                    <span className="chip ml-auto bg-surface-2 text-ink-dim">Soon</span>
                  )}
                </div>
                <p className="mt-3 text-sm leading-snug text-ink-muted">{skill.blurb}</p>
              </Link>
            )
          })}
        </div>
      </div>
    </div>
  )
}
