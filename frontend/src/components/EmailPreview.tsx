import { useCallback, useEffect, useRef, useState } from 'react'
import { Loader2, RefreshCw } from 'lucide-react'

/** Renders the locked v8 email in a sandboxed iframe, scaled to FIT the width of
 *  the preview panel (like "Fit width" in Figma / a PDF viewer): the whole email
 *  is visible with only vertical scrolling — never a horizontal scrollbar.
 *
 *  The email itself is NEVER modified. We render the iframe at the email's
 *  natural pixel width, then apply a CSS `transform: scale()` so it fits the
 *  container. The scale is recomputed whenever the panel/sidebar/window resizes
 *  or the email content reflows. Scaling down keeps text crisp (it's vector, not
 *  raster); we never scale ABOVE 1:1, so nothing is blurred. */
export function EmailPreview({ src, reloadKey, busy }: { src: string; reloadKey: number; busy?: boolean }) {
  const containerRef = useRef<HTMLDivElement>(null)
  const iframeRef = useRef<HTMLIFrameElement>(null)
  const bodyObs = useRef<ResizeObserver | null>(null)
  const [w, setW] = useState(640) // natural email width  (px)
  const [h, setH] = useState(600) // natural email height (px)
  const [scale, setScale] = useState(1)

  const measure = useCallback(() => {
    const iframe = iframeRef.current
    const container = containerRef.current
    if (!iframe || !container) return
    let doc: Document | null = null
    try {
      doc = iframe.contentDocument
    } catch {
      return // cross-origin (shouldn't happen: preview is same-origin) — leave as-is
    }
    if (!doc || !doc.body) return
    const natW = Math.max(doc.documentElement.scrollWidth, doc.body.scrollWidth, 320)
    const natH = Math.max(doc.documentElement.scrollHeight, doc.body.scrollHeight, 1)
    const avail = container.clientWidth
    const s = Math.min(1, avail / natW) // fit width; never upscale past 1:1
    // Only update on a real change, so we don't thrash / loop with the observers.
    setW((p) => (Math.abs(p - natW) > 1 ? natW : p))
    setH((p) => (Math.abs(p - natH) > 1 ? natH : p))
    setScale((p) => (Math.abs(p - s) > 0.001 ? s : p))
  }, [])

  // Re-fit when the panel / sidebar / window changes size.
  useEffect(() => {
    const container = containerRef.current
    if (!container || !('ResizeObserver' in window)) return
    const ro = new ResizeObserver(() => measure())
    ro.observe(container)
    return () => ro.disconnect()
  }, [measure])

  // Measure once the iframe document is loaded, again after images/fonts settle,
  // and keep watching the email body for any late reflow.
  const onLoad = useCallback(() => {
    measure()
    window.setTimeout(measure, 250)
    window.setTimeout(measure, 900)
    let doc: Document | null = null
    try {
      doc = iframeRef.current?.contentDocument ?? null
    } catch {
      doc = null
    }
    bodyObs.current?.disconnect()
    if (doc?.body && 'ResizeObserver' in window) {
      bodyObs.current = new ResizeObserver(() => measure())
      bodyObs.current.observe(doc.body)
    }
  }, [measure])

  useEffect(() => () => bodyObs.current?.disconnect(), [])

  return (
    <div className="flex h-full flex-col">
      <div className="flex items-center gap-2 border-b border-hairline bg-surface px-3 py-2 text-xs text-ink-dim">
        <span className="font-semibold uppercase tracking-wide text-ink-muted">Live preview</span>
        {busy && <Loader2 className="h-3.5 w-3.5 animate-spin" />}
        <span className="ml-auto flex items-center gap-1"><RefreshCw className="h-3 w-3" /> updates on save</span>
      </div>
      {/* Scroll container: vertical only. overflow-x-hidden guarantees no
          horizontal scrollbar even for a frame before the first measure. */}
      <div ref={containerRef} className="min-h-0 flex-1 overflow-y-auto overflow-x-hidden bg-[#f0f4f0]">
        {/* Reserves the SCALED footprint so vertical scrolling is correct and the
            email is centred when the panel is wider than the email. */}
        <div style={{ width: w * scale, height: h * scale, margin: '0 auto' }}>
          <iframe
            key={reloadKey}
            ref={iframeRef}
            title="Email preview"
            src={src}
            sandbox="allow-same-origin"
            scrolling="no"
            onLoad={onLoad}
            style={{
              width: w,
              height: h,
              border: 0,
              display: 'block',
              transform: `scale(${scale})`,
              transformOrigin: 'top left',
            }}
          />
        </div>
      </div>
    </div>
  )
}
