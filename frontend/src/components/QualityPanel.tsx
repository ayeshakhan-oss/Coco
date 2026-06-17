import { AlertTriangle, CheckCircle2, Loader2, XCircle } from 'lucide-react'
import type { EvalResult } from '../lib/types'

export function QualityPanel({ result, busy }: { result: EvalResult | null; busy?: boolean }) {
  const hard = result?.violations.filter((v) => v.severity === 'HARD_BLOCK') ?? []
  const warn = result?.violations.filter((v) => v.severity === 'WARNING') ?? []
  const words = result?.word_count ?? 0
  const wordsOk = words >= 800

  return (
    <div className="border-t border-hairline bg-surface">
      <div className="flex items-center gap-3 px-4 py-2.5 text-sm">
        {busy ? (
          <span className="flex items-center gap-1.5 text-ink-dim"><Loader2 className="h-4 w-4 animate-spin" /> checking…</span>
        ) : hard.length ? (
          <span className="flex items-center gap-1.5 font-medium text-danger"><XCircle className="h-4 w-4" /> {hard.length} hard block{hard.length > 1 ? 's' : ''}</span>
        ) : (
          <span className="flex items-center gap-1.5 font-medium text-green"><CheckCircle2 className="h-4 w-4" /> Passes checks</span>
        )}
        {warn.length > 0 && (
          <span className="flex items-center gap-1.5 text-[#f0b232]"><AlertTriangle className="h-4 w-4" /> {warn.length} warning{warn.length > 1 ? 's' : ''}</span>
        )}
        <span className={`ml-auto rounded-md px-2 py-0.5 text-xs font-semibold tabular-nums ${wordsOk ? 'bg-green/15 text-green' : 'bg-[#f0b232]/15 text-[#f0b232]'}`}>
          {words} / 800 words
        </span>
      </div>
      {(hard.length > 0 || warn.length > 0) && (
        <ul className="max-h-44 space-y-1.5 overflow-auto px-4 pb-3 text-xs">
          {hard.map((v, i) => (
            <li key={`h${i}`} className="rounded-lg bg-danger/15 px-2.5 py-1.5 text-danger">
              <span className="font-semibold">{v.rule}</span> — {v.detail}
            </li>
          ))}
          {warn.map((v, i) => (
            <li key={`w${i}`} className="rounded-lg bg-[#f0b232]/12 px-2.5 py-1.5 text-[#f0b232]">
              <span className="font-semibold">{v.rule}</span> — {v.detail}
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
