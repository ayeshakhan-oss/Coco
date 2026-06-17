import { AlertTriangle, CheckCircle2, Loader2, XCircle } from 'lucide-react'
import type { EvalResult } from '../lib/types'

export function QualityPanel({ result, busy }: { result: EvalResult | null; busy?: boolean }) {
  const hard = result?.violations.filter((v) => v.severity === 'HARD_BLOCK') ?? []
  const warn = result?.violations.filter((v) => v.severity === 'WARNING') ?? []
  const words = result?.word_count ?? 0
  const wordsOk = words >= 800

  return (
    <div className="border-t border-slate-200 bg-white">
      <div className="flex items-center gap-3 px-4 py-2.5 text-sm">
        {busy ? (
          <span className="flex items-center gap-1.5 text-slate-500"><Loader2 className="h-4 w-4 animate-spin" /> checking…</span>
        ) : hard.length ? (
          <span className="flex items-center gap-1.5 font-medium text-block"><XCircle className="h-4 w-4" /> {hard.length} hard block{hard.length > 1 ? 's' : ''}</span>
        ) : (
          <span className="flex items-center gap-1.5 font-medium text-sent"><CheckCircle2 className="h-4 w-4" /> Passes checks</span>
        )}
        {warn.length > 0 && (
          <span className="flex items-center gap-1.5 text-review"><AlertTriangle className="h-4 w-4" /> {warn.length} warning{warn.length > 1 ? 's' : ''}</span>
        )}
        <span className={`ml-auto rounded-md px-2 py-0.5 text-xs font-semibold tabular-nums ${wordsOk ? 'bg-sent-bg text-sent' : 'bg-review-bg text-review'}`}>
          {words} / 800 words
        </span>
      </div>
      {(hard.length > 0 || warn.length > 0) && (
        <ul className="max-h-44 space-y-1.5 overflow-auto px-4 pb-3 text-xs">
          {hard.map((v, i) => (
            <li key={`h${i}`} className="rounded-md bg-block-bg px-2.5 py-1.5 text-block">
              <span className="font-semibold">{v.rule}</span> — <span className="text-block/80">{v.detail}</span>
            </li>
          ))}
          {warn.map((v, i) => (
            <li key={`w${i}`} className="rounded-md bg-review-bg px-2.5 py-1.5 text-review">
              <span className="font-semibold">{v.rule}</span> — <span className="opacity-80">{v.detail}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
