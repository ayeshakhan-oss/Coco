import { useCallback, useState } from 'react'
import type { ApiError } from './api'

/** Progress state for a bulk operation that runs one item at a time. */
export type BulkState = {
  running: boolean
  done: number
  total: number
  failed: { item: string; error: string }[]
}

const IDLE: BulkState = { running: false, done: 0, total: 0, failed: [] }

/** Runs an async action over a list of items SEQUENTIALLY, tracking progress and
 *  collecting per-item errors (one failure never aborts the rest). This is how
 *  bulk draft / approve / pilot-send work: the client drives the existing
 *  per-item endpoints in a loop, so every item still passes the same quality
 *  gate and there is no risky new bulk backend path. */
export function useBulk() {
  const [state, setState] = useState<BulkState>(IDLE)

  const run = useCallback(
    async <T,>(items: T[], fn: (item: T) => Promise<unknown>, label?: (item: T) => string) => {
      setState({ running: true, done: 0, total: items.length, failed: [] })
      const failed: { item: string; error: string }[] = []
      for (let i = 0; i < items.length; i++) {
        try {
          await fn(items[i])
        } catch (e) {
          failed.push({
            item: label ? label(items[i]) : String(items[i]),
            error: (e as ApiError)?.message || String(e),
          })
        }
        setState((s) => ({ ...s, done: i + 1, failed: [...failed] }))
      }
      setState((s) => ({ ...s, running: false }))
      return { failed }
    },
    [],
  )

  const reset = useCallback(() => setState(IDLE), [])
  return { ...state, run, reset }
}
