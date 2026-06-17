import type { ReactNode } from 'react'
import type { DraftContent } from '../lib/types'

/** Edits the structured draft content. Headings are fixed labels (the backend
 *  applies the canonical heading), so a typo can't break the required-heading
 *  rule. Paragraphs are edited as text blocks separated by a blank line. */
export function SectionEditor({
  title,
  content,
  onTitleChange,
  onContentChange,
  disabled,
}: {
  title: string
  content: DraftContent
  onTitleChange: (v: string) => void
  onContentChange: (c: DraftContent) => void
  disabled?: boolean
}) {
  const sections = content.sections ?? []

  function setSectionParas(i: number, text: string) {
    const next = sections.map((s, idx) =>
      idx === i ? { ...s, paragraphs: text.split(/\n\s*\n/).map((p) => p.trim()).filter(Boolean) } : s,
    )
    onContentChange({ ...content, sections: next })
  }
  function setSubhead(i: number, v: string) {
    const next = sections.map((s, idx) => (idx === i ? { ...s, subhead: v || null } : s))
    onContentChange({ ...content, sections: next })
  }

  const ta =
    'w-full resize-y rounded-lg border border-slate-200 bg-white p-3 text-sm leading-relaxed text-slate-800 outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20 disabled:bg-slate-50'

  return (
    <div className="space-y-5">
      <div>
        <label className="mb-1 block text-xs font-semibold uppercase tracking-wide text-slate-500">Subject line</label>
        <input
          value={title}
          disabled={disabled}
          onChange={(e) => onTitleChange(e.target.value)}
          className="w-full rounded-lg border border-slate-200 bg-white px-3 py-2 text-sm font-medium text-slate-900 outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20 disabled:bg-slate-50"
        />
      </div>

      <Field label="Greeting">
        <input
          value={content.greeting ?? ''}
          disabled={disabled}
          onChange={(e) => onContentChange({ ...content, greeting: e.target.value })}
          className="w-full rounded-lg border border-slate-200 bg-white px-3 py-2 text-sm text-slate-800 outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20 disabled:bg-slate-50"
        />
      </Field>

      <Field label="Opening" hint="One or two paragraphs. Separate paragraphs with a blank line.">
        <textarea
          rows={3}
          disabled={disabled}
          value={(content.opening ?? []).join('\n\n')}
          onChange={(e) => onContentChange({ ...content, opening: e.target.value.split(/\n\s*\n/).map((p) => p.trim()).filter(Boolean) })}
          className={ta}
        />
      </Field>

      {sections.map((s, i) => (
        <div key={i} className="rounded-lg border border-slate-100 bg-slate-50/60 p-3">
          <div className="mb-2 text-sm font-semibold text-brand-700">{s.heading ?? `Section ${i + 1}`}</div>
          <input
            placeholder="Optional sub-heading"
            value={s.subhead ?? ''}
            disabled={disabled}
            onChange={(e) => setSubhead(i, e.target.value)}
            className="mb-2 w-full rounded-md border border-slate-200 bg-white px-2.5 py-1.5 text-xs text-slate-700 outline-none focus:border-brand-500 disabled:bg-slate-50"
          />
          <textarea
            rows={5}
            disabled={disabled}
            value={(s.paragraphs ?? []).join('\n\n')}
            onChange={(e) => setSectionParas(i, e.target.value)}
            className={ta}
          />
        </div>
      ))}

      <Field label="P.S.">
        <textarea
          rows={2}
          disabled={disabled}
          value={content.ps ?? ''}
          onChange={(e) => onContentChange({ ...content, ps: e.target.value })}
          className={ta}
        />
      </Field>
    </div>
  )
}

function Field({ label, hint, children }: { label: string; hint?: string; children: ReactNode }) {
  return (
    <div>
      <label className="mb-1 block text-xs font-semibold uppercase tracking-wide text-slate-500">{label}</label>
      {children}
      {hint && <p className="mt-1 text-[11px] text-slate-400">{hint}</p>}
    </div>
  )
}
