import { Loader2, RefreshCw } from 'lucide-react'

/** Renders the locked v8 email in a sandboxed iframe. Reflects the last SAVED
 *  state (the backend renders the preview), so we reload it after each save. */
export function EmailPreview({ src, reloadKey, busy }: { src: string; reloadKey: number; busy?: boolean }) {
  return (
    <div className="flex h-full flex-col">
      <div className="flex items-center gap-2 border-b border-hairline bg-surface px-3 py-2 text-xs text-ink-dim">
        <span className="font-semibold uppercase tracking-wide text-ink-muted">Live preview</span>
        {busy && <Loader2 className="h-3.5 w-3.5 animate-spin" />}
        <span className="ml-auto flex items-center gap-1"><RefreshCw className="h-3 w-3" /> updates on save</span>
      </div>
      <iframe
        key={reloadKey}
        title="Email preview"
        src={src}
        sandbox="allow-same-origin"
        className="h-full w-full flex-1 bg-[#f0f4f0]"
      />
    </div>
  )
}
