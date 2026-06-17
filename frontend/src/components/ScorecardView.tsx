import type { GwcScorecard, ValuesScorecard } from '../lib/types'

const RATING_TONE: Record<string, string> = {
  '+': 'bg-green/15 text-green',
  '+/-': 'bg-[#f0b232]/15 text-[#f0b232]',
  '-': 'bg-danger/15 text-danger',
}

/** Read-only scorecard reference (the evidence the email must be grounded in). */
export function ScorecardView({ values, gwc }: { values: ValuesScorecard | null; gwc: GwcScorecard | null }) {
  if (!values && !gwc) {
    return <p className="text-sm text-ink-dim">No interview scorecard on file.</p>
  }
  return (
    <div className="space-y-4 text-sm">
      {values && (
        <div>
          <div className="mb-2 flex flex-wrap gap-x-4 gap-y-1 text-xs text-ink-dim">
            {values.host && <span>Host: <b className="text-ink-muted">{values.host}</b></span>}
            {values.date && <span>{values.date}</span>}
            {values.proceed_to_right_seat && <span>Proceed: <b className="text-ink-muted">{values.proceed_to_right_seat}</b></span>}
          </div>
          <ul className="space-y-2">
            {values.values.map((v, i) => (
              <li key={i} className="rounded-lg border border-hairline p-2">
                <div className="flex items-center justify-between gap-2">
                  <span className="text-[13px] font-medium text-ink">{v.name}</span>
                  {v.rating && (
                    <span className={`rounded px-1.5 py-0.5 text-[11px] font-semibold ${RATING_TONE[v.rating] || 'bg-elevated text-ink-muted'}`}>{v.rating}</span>
                  )}
                </div>
                {(v.deep_dive || v.curve_ball || v.micro_case) && (
                  <div className="mt-1 space-y-0.5 text-[12px] text-ink-muted">
                    {v.deep_dive && <p><span className="text-ink-dim">Deep dive: </span>{v.deep_dive}</p>}
                    {v.curve_ball && <p><span className="text-ink-dim">Curveball: </span>{v.curve_ball}</p>}
                    {v.micro_case && <p><span className="text-ink-dim">Micro-case: </span>{v.micro_case}</p>}
                  </div>
                )}
              </li>
            ))}
          </ul>
          {values.final_comments && (
            <div className="mt-2 rounded-lg bg-blurple/10 p-2 text-[12px] text-ink-muted">
              <span className="font-medium text-[#aab2ff]">Final comments: </span>{values.final_comments}
            </div>
          )}
        </div>
      )}
      {gwc && (
        <div>
          <div className="mb-2 text-xs text-ink-dim">{gwc.hiring_manager && <span>Hiring manager: <b className="text-ink-muted">{gwc.hiring_manager}</b></span>}</div>
          <div className="grid grid-cols-3 gap-2">
            {gwc.competencies.map((c, i) => (
              <div key={i} className="rounded-lg border border-hairline p-2 text-center">
                <div className="text-[11px] text-ink-dim">{c.name}</div>
                <div className="text-base font-semibold text-ink">{c.score ?? '—'}</div>
              </div>
            ))}
          </div>
          {gwc.additional_comments && (
            <div className="mt-2 rounded-lg bg-blurple/10 p-2 text-[12px] text-ink-muted">
              <span className="font-medium text-[#aab2ff]">Comments: </span>{gwc.additional_comments}
            </div>
          )}
        </div>
      )}
    </div>
  )
}
