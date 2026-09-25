import { useEffect, useState } from 'react'
import { AlertTriangle, BookOpen, ChevronDown, ChevronRight, ExternalLink, Laptop, Zap } from 'lucide-react'
import { Link } from 'react-router-dom'
import { Spinner } from '../components/Spinner'
import { api } from '../lib/api'
import type { SkillLibrary, SkillSubSkill } from '../lib/types'

// Every sub-skill Coco has, read from the files that actually shipped in this
// build. Until 2026-09-25 the image copied 2 of the 7 skill folders, so 29
// sub-skill files did not exist on Railway while all six module tiles read
// "live". This page is what makes that visible rather than silent.

const STATUS: Record<string, { label: string; cls: string; icon: typeof Zap }> = {
  wired: {
    label: 'Running here',
    cls: 'bg-success/10 text-success border-success/30',
    icon: Zap,
  },
  reference: {
    label: 'Reference',
    cls: 'bg-blurple/10 text-blurple border-blurple/30',
    icon: BookOpen,
  },
  claude_code_only: {
    label: 'Claude Code',
    cls: 'bg-ink-dim/10 text-ink-dim border-hairline',
    icon: Laptop,
  },
}

function StatusChip({ status }: { status: string }) {
  const s = STATUS[status] ?? STATUS.reference
  const Icon = s.icon
  return (
    <span
      className={`inline-flex shrink-0 items-center gap-1 rounded-full border px-2 py-0.5 text-[11px] font-semibold ${s.cls}`}
    >
      <Icon className="h-3 w-3" />
      {s.label}
    </span>
  )
}

export function SkillsPage() {
  const [lib, setLib] = useState<SkillLibrary | null>(null)
  const [open, setOpen] = useState<Record<string, boolean>>({})
  const [reading, setReading] = useState<SkillSubSkill | null>(null)
  const [body, setBody] = useState<string>('')
  const [error, setError] = useState<string | null>(null)
  const [loaded, setLoaded] = useState(false)

  useEffect(() => {
    api
      .skills()
      .then((l) => {
        setLib(l)
        // Open everything by default: the whole point is seeing the sub-skills,
        // not a list of seven folders that looks like the old module tiles.
        setOpen(Object.fromEntries(l.skills.map((s) => [s.id, true])))
      })
      .catch(() => setError('Could not load the skill library.'))
      .finally(() => setLoaded(true))
  }, [])

  const openFile = (f: SkillSubSkill) => {
    setReading(f)
    setBody('')
    api
      .skillFile(f.path)
      .then((r) => setBody(r.body))
      .catch(() => setBody('Could not read this file in this build.'))
  }

  if (!loaded) {
    return (
      <div className="mx-auto max-w-6xl px-8 py-7">
        <Spinner label="Reading the skill library…" />
      </div>
    )
  }

  return (
    <div className="mx-auto max-w-6xl px-8 py-7">
      <header className="mb-5">
        <h1 className="font-display text-2xl font-bold text-ink">Skills</h1>
        <p className="mt-1 text-sm text-ink-muted">
          Every skill and sub-skill in this build, read from the files the image
          actually carries.
        </p>
      </header>

      {error && <p className="mb-4 text-sm text-danger">{error}</p>}

      {lib?.error && (
        <p className="mb-4 flex gap-2 rounded-xl border border-danger/30 bg-danger/5 px-4 py-3 text-sm text-danger">
          <AlertTriangle className="mt-0.5 h-4 w-4 shrink-0" />
          {lib.error}
        </p>
      )}

      {lib && !lib.error && (
        <>
          <div className="grid grid-cols-2 gap-3 lg:grid-cols-4">
            {[
              ['Skills', lib.summary.skills],
              ['Sub-skills', lib.summary.sub_skills],
              ['Running here', lib.summary.wired],
              ['Reference', lib.summary.reference + lib.summary.claude_code_only],
            ].map(([label, value]) => (
              <div key={String(label)} className="rounded-2xl border border-hairline bg-surface p-4">
                <div className="text-sm font-medium text-ink-muted">{label}</div>
                <div className="mt-1 text-2xl font-bold tabular-nums text-ink">{value}</div>
              </div>
            ))}
          </div>

          {/* What the three words mean, once, rather than a tooltip nobody
              opens. "Reference" is not a lesser kind of live: the file is in
              the image and served from it. */}
          <div className="mt-3 rounded-xl border border-hairline bg-surface px-4 py-3 text-xs text-ink-muted">
            <p>
              <strong className="text-success">Running here</strong> — a page in this
              app does the work.{' '}
              <strong className="text-blurple">Reference</strong> — the guidance ships
              and is readable here, and Claude Code follows it.{' '}
              <strong className="text-ink-dim">Claude Code</strong> — deliberately not
              on the server; open a file to see why.
            </p>
          </div>

          <div className="mt-5 space-y-3">
            {lib.skills.map((skill) => {
              const isOpen = open[skill.id] ?? false
              return (
                <section
                  key={skill.id}
                  className="overflow-hidden rounded-2xl border border-hairline bg-surface"
                >
                  <button
                    type="button"
                    onClick={() => setOpen({ ...open, [skill.id]: !isOpen })}
                    className="flex w-full items-center gap-3 px-4 py-3 text-left transition-colors hover:bg-elevated"
                  >
                    {isOpen ? (
                      <ChevronDown className="h-4 w-4 shrink-0 text-ink-dim" />
                    ) : (
                      <ChevronRight className="h-4 w-4 shrink-0 text-ink-dim" />
                    )}
                    {skill.number && (
                      <span className="font-mono text-xs text-ink-dim">{skill.number}</span>
                    )}
                    <span className="font-semibold text-ink">{skill.label}</span>
                    <span className="ml-auto text-xs text-ink-dim">
                      {skill.counts.total} file{skill.counts.total === 1 ? '' : 's'}
                      {skill.counts.wired > 0 && (
                        <span className="ml-2 text-success">
                          {skill.counts.wired} running
                        </span>
                      )}
                    </span>
                  </button>

                  {isOpen && (
                    <div className="border-t border-hairline">
                      {skill.summary && (
                        <p className="px-4 py-2.5 text-xs text-ink-muted">{skill.summary}</p>
                      )}
                      <table className="w-full text-sm">
                        <tbody>
                          {[skill.overview, ...skill.sub_skills]
                            .filter(Boolean)
                            .map((f) => f as SkillSubSkill)
                            .map((f) => (
                              <tr
                                key={f.path}
                                className="border-t border-hairline/60 align-top"
                              >
                                <td className="px-4 py-2.5">
                                  <button
                                    type="button"
                                    onClick={() => openFile(f)}
                                    className="text-left font-medium text-ink hover:text-blurple hover:underline"
                                  >
                                    {f.title}
                                    {f.is_overview && (
                                      <span className="ml-2 text-[11px] text-ink-dim">
                                        overview
                                      </span>
                                    )}
                                  </button>
                                  <div className="font-mono text-[11px] text-ink-dim">
                                    {f.filename}
                                  </div>
                                  {f.note && (
                                    <div className="mt-1 max-w-xl text-[11px] text-ink-dim">
                                      {f.note}
                                    </div>
                                  )}
                                </td>
                                <td className="px-4 py-2.5 text-right">
                                  <StatusChip status={f.status} />
                                  {f.route && (
                                    <div className="mt-1">
                                      <Link
                                        to={f.route}
                                        className="text-[11px] text-blurple hover:underline"
                                      >
                                        open <ExternalLink className="inline h-3 w-3" />
                                      </Link>
                                    </div>
                                  )}
                                </td>
                              </tr>
                            ))}
                        </tbody>
                      </table>
                    </div>
                  )}
                </section>
              )
            })}
          </div>
        </>
      )}

      {/* Reading panel */}
      {reading && (
        <div
          className="fixed inset-0 z-50 flex justify-end bg-black/40"
          onClick={() => setReading(null)}
        >
          <div
            className="h-full w-full max-w-3xl overflow-auto bg-surface p-6 shadow-xl"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-start gap-3">
              <div>
                <h2 className="font-display text-lg font-bold text-ink">{reading.title}</h2>
                <p className="font-mono text-xs text-ink-dim">{reading.path}</p>
              </div>
              <button
                type="button"
                className="btn-secondary ml-auto text-xs"
                onClick={() => setReading(null)}
              >
                Close
              </button>
            </div>
            <div className="mt-2">
              <StatusChip status={reading.status} />
            </div>
            {/* Rendered as preformatted text on purpose: this is source
                markdown, and running it through a HTML renderer would be a
                second place for its content to be reinterpreted. */}
            <pre className="mt-4 whitespace-pre-wrap break-words font-mono text-xs leading-relaxed text-ink-muted">
              {body || 'Loading…'}
            </pre>
          </div>
        </div>
      )}
    </div>
  )
}
