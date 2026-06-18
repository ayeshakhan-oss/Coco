import { ArrowLeft, Sparkles } from 'lucide-react'
import { Link, Navigate, useParams } from 'react-router-dom'
import { activeModule, comingSoonModules, moduleBySlug } from '../lib/modules'

export function ComingSoonPage() {
  const { slug } = useParams()
  const mod = moduleBySlug(slug)

  // Unknown slug or the live module → send back to the working app.
  if (!mod || mod.status === 'live') return <Navigate to="/" replace />

  const Icon = mod.icon
  const current = activeModule()
  const others = comingSoonModules().filter((m) => m.slug !== mod.slug)

  return (
    <div className="mx-auto max-w-3xl px-8 py-16">
      <Link to="/" className="mb-8 inline-flex items-center gap-1.5 text-sm text-ink-dim hover:text-ink">
        <ArrowLeft className="h-4 w-4" /> Back to {current.label}
      </Link>

      <div className="card flex flex-col items-center px-8 py-14 text-center">
        <span className="flex h-16 w-16 items-center justify-center rounded-2xl bg-blurple/12 text-blurple">
          <Icon className="h-8 w-8" />
        </span>
        <span className="mt-6 inline-flex items-center gap-1.5 rounded-full bg-surface-2 px-3 py-1 text-[11px] font-semibold uppercase tracking-wide text-ink-dim">
          <Sparkles className="h-3.5 w-3.5" /> Coming soon
        </span>
        <h1 className="mt-4 font-display text-3xl font-bold text-ink">{mod.label}</h1>
        <p className="mt-3 max-w-md text-sm leading-relaxed text-ink-muted">{mod.blurb}</p>
        <p className="mt-6 max-w-md text-sm leading-relaxed text-ink-dim">
          This Coco module isn&rsquo;t live yet. We&rsquo;ve launched <span className="font-medium text-ink">{current.label}</span> first.
          The rest of Coco&rsquo;s capabilities are being brought online module by module.
        </p>
        <Link to="/" className="btn-primary mt-8">
          Go to {current.label}
        </Link>
      </div>

      {others.length > 0 && (
        <div className="mt-10">
          <div className="mb-3 text-xs font-semibold uppercase tracking-wide text-ink-dim">Also on the roadmap</div>
          <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
            {others.map((m) => {
              const OIcon = m.icon
              return (
                <Link key={m.slug} to={`/modules/${m.slug}`} className="card flex items-start gap-3 p-4 transition-colors hover:bg-elevated">
                  <span className="flex h-9 w-9 flex-shrink-0 items-center justify-center rounded-lg bg-surface-2 text-ink-dim">
                    <OIcon className="h-4 w-4" />
                  </span>
                  <div>
                    <div className="text-sm font-semibold text-ink">{m.label}</div>
                    <div className="mt-0.5 text-xs leading-snug text-ink-dim">{m.blurb}</div>
                  </div>
                </Link>
              )
            })}
          </div>
        </div>
      )}
    </div>
  )
}
