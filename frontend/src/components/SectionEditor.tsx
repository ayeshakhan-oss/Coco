import type { ReactNode } from 'react'
import type { DraftContent } from '../lib/types'

/** Edits the structured draft content. Headings are fixed labels (the backend
 *  applies the canonical heading). Paragraphs are edited as text blocks
 *  separated by a blank line. */
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

  return (
    <div className="space-y-5">
      <Field label="Subject line">
        <input value={title} disabled={disabled} onChange={(e) => onTitleChange(e.target.value)} className="input font-medium" />
      </Field>

      <Field label="Greeting">
        <input value={content.greeting ?? ''} disabled={disabled} onChange={(e) => onContentChange({ ...content, greeting: e.target.value })} className="input" />
      </Field>

      <Field label="Opening" hint="One or two paragraphs. Separate paragraphs with a blank line.">
        <textarea
          rows={3}
          disabled={disabled}
          value={(content.opening ?? []).join('\n\n')}
          onChange={(e) => onContentChange({ ...content, opening: e.target.value.split(/\n\s*\n/).map((p) => p.trim()).filter(Boolean) })}
          className="input resize-y leading-relaxed"
        />
      </Field>

      {sections.map((s, i) => (
        <div key={i} className="rounded-xl border border-hairline bg-surface-2/60 p-3">
          <div className="mb-2 text-sm font-semibold text-[#4752c4]">{s.heading ?? `Section ${i + 1}`}</div>
          <input placeholder="Optional sub-heading" value={s.subhead ?? ''} disabled={disabled} onChange={(e) => setSubhead(i, e.target.value)} className="input mb-2 text-xs" />
          <textarea
            rows={5}
            disabled={disabled}
            value={(s.paragraphs ?? []).join('\n\n')}
            onChange={(e) => setSectionParas(i, e.target.value)}
            className="input resize-y leading-relaxed"
          />
        </div>
      ))}

      <Field label="P.S.">
        <textarea rows={2} disabled={disabled} value={content.ps ?? ''} onChange={(e) => onContentChange({ ...content, ps: e.target.value })} className="input resize-y leading-relaxed" />
      </Field>
    </div>
  )
}

function Field({ label, hint, children }: { label: string; hint?: string; children: ReactNode }) {
  return (
    <div>
      <label className="mb-1 block text-xs font-semibold uppercase tracking-wide text-ink-dim">{label}</label>
      {children}
      {hint && <p className="mt-1 text-[11px] text-ink-dim">{hint}</p>}
    </div>
  )
}
