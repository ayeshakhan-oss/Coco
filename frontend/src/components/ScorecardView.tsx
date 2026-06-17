import type { GwcScorecard, ValuesScorecard } from '../lib/types'

const RATING_TONE: Record<string, string> = {
  '+': 'bg-sent-bg text-sent',
  '+/-': 'bg-review-bg text-review',
  '-': 'bg-block-bg text-block',
}

/** Read-only scorecard reference (the evidence the email must be grounded in). */
export function ScorecardView({ values, gwc }: { values: ValuesScorecard | null; gwc: GwcScorecard | null }) {
  if (!values && !gwc) {
    return <p className="text-sm text-slate-500">No interview scorecard on file.</p>
  }
  return (
    <div className="space-y-4 text-sm">
      {values && (
        <div>
          <div className="mb-2 flex flex-wrap gap-x-4 gap-y-1 text-xs text-slate-500">
            {values.host && <span>Host: <b className="text-slate-700">{values.host}</b></span>}
            {values.date && <span>{values.date}</span>}
            {values.proceed_to_right_seat && <span>Proceed: <b className="text-slate-700">{values.proceed_to_right_seat}</b></span>}
          </div>
          <ul className="space-y-2">
            {values.values.map((v, i) => (
              <li key={i} className="rounded-md border border-slate-100 p-2">
                <div className="flex items-center justify-between gap-2">
                  <span className="text-[13px] font-medium text-slate-800">{v.name}</span>
                  {v.rating && (
                    <span className={`rounded px-1.5 py-0.5 text-[11px] font-semibold ${RATING_TONE[v.rating] || 'bg-slate-100 text-slate-600'}`}>{v.rating}</span>
                  )}
                </div>
                {(v.deep_dive || v.curve_ball || v.micro_case) && (
                  <div className="mt-1 space-y-0.5 text-[12px] text-slate-600">
                    {v.deep_dive && <p><span className="text-slate-400">Deep dive: </span>{v.deep_dive}</p>}
                    {v.curve_ball && <p><span className="text-slate-400">Curveball: </span>{v.curve_ball}</p>}
                    {v.micro_case && <p><span className="text-slate-400">Micro-case: </span>{v.micro_case}</p>}
                  </div>
                )}
              </li>
            ))}
          </ul>
          {values.final_comments && (
            <div className="mt-2 rounded-md bg-brand-50 p-2 text-[12px] text-slate-700">
              <span className="font-medium text-brand-700">Final comments: </span>{values.final_comments}
            </div>
          )}
        </div>
      )}
      {gwc && (
        <div>
          <div className="mb-2 text-xs text-slate-500">{gwc.hiring_manager && <span>Hiring manager: <b className="text-slate-700">{gwc.hiring_manager}</b></span>}</div>
          <div className="grid grid-cols-3 gap-2">
            {gwc.competencies.map((c, i) => (
              <div key={i} className="rounded-md border border-slate-100 p-2 text-center">
                <div className="text-[11px] text-slate-500">{c.name}</div>
                <div className="text-base font-semibold text-slate-900">{c.score ?? '—'}</div>
              </div>
            ))}
          </div>
          {gwc.additional_comments && (
            <div className="mt-2 rounded-md bg-brand-50 p-2 text-[12px] text-slate-700">
              <span className="font-medium text-brand-700">Comments: </span>{gwc.additional_comments}
            </div>
          )}
        </div>
      )}
    </div>
  )
}
