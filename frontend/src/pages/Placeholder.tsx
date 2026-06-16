import { Construction } from 'lucide-react'

export function Placeholder({ title, note }: { title: string; note: string }) {
  return (
    <div className="mx-auto max-w-7xl px-8 py-7">
      <h1 className="text-xl font-semibold text-slate-900">{title}</h1>
      <div className="mt-6 flex flex-col items-center justify-center rounded-xl border border-dashed border-slate-300 bg-white py-20 text-center">
        <Construction className="mb-3 h-8 w-8 text-slate-400" />
        <p className="text-sm text-slate-500">{note}</p>
      </div>
    </div>
  )
}
