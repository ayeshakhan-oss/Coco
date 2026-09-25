// Regression tests for the whole-position screening run.
//
// The bug these exist for: on 2026-09-23 a fifty-minute run of CPD Coach
// (job 17) stopped at 236 of 410 because Railway redeployed underneath it and
// the loop treated one dead request as the end of the run. Every test below
// that involves a failure would have passed trivially before the fix by
// ending the run; they assert the opposite, that the run CONTINUES.

import { describe, expect, it, vi } from 'vitest'
import { ApiError } from './api'
import { RETRY_BACKOFF_SECONDS, isTransient, runScreenAll } from './screenAll'
import type { CVScreen, CVScreenBatch } from './types'

/** A batch response. Only the fields the runner reads need to be real.
 *  `failed` is optional on BatchLike (CV screening has no such list), so the
 *  override type admits it explicitly. */
function batch(
  over: Partial<CVScreenBatch> & { failed?: unknown[] } = {},
): CVScreenBatch {
  return {
    job_id: 17,
    screened: [],
    skipped: [],
    last_application_id: null,
    remaining: 0,
    ...over,
  }
}

function screens(ids: number[]): CVScreen[] {
  return ids.map((id) => ({ application_id: id }) as CVScreen)
}

/** A server holding `total` candidates, handing back `perBatch` at a time,
 *  driven by the same cursor rule as the real endpoint: strictly after the
 *  cursor, in id order. */
function fakeServer(total: number, perBatch = 4) {
  const ids = Array.from({ length: total }, (_, i) => i + 1)
  const screened = new Set<number>()
  return {
    screened,
    calls: 0,
    run(after: number | null): CVScreenBatch {
      this.calls += 1
      const cursor = after ?? 0
      const slice = ids.filter((id) => id > cursor && !screened.has(id)).slice(0, perBatch)
      slice.forEach((id) => screened.add(id))
      const last = slice.length ? slice[slice.length - 1] : cursor
      return batch({
        screened: screens(slice),
        last_application_id: last,
        remaining: ids.filter((id) => id > last && !screened.has(id)).length,
      })
    },
  }
}

const noSleep = async () => {}

describe('runScreenAll', () => {
  it('screens every candidate on the position', async () => {
    const server = fakeServer(410)
    const result = await runScreenAll({
      runBatch: async (after) => server.run(after),
      sleep: noSleep,
    })

    expect(result).toEqual({ done: 410, skipped: 0, failed: 0, error: null, stopped: false })
    expect(server.screened.size).toBe(410)
  })

  // 🔴 THE REGRESSION. A container restart mid-run used to end the run.
  it('survives a container restart and finishes the position', async () => {
    const server = fakeServer(410)
    let thrown = 0
    const result = await runScreenAll({
      runBatch: async (after) => {
        // Two consecutive 502s, exactly what Railway's edge returns while a
        // new container is coming up, a third of the way through.
        if (server.screened.size >= 160 && thrown < 2) {
          thrown += 1
          throw new ApiError(502, '502: Application failed to respond')
        }
        return server.run(after)
      },
      sleep: noSleep,
    })

    expect(thrown).toBe(2)
    expect(result.error).toBeNull()
    expect(result.done).toBe(410)
    expect(server.screened.size).toBe(410)
  })

  it('does not rewind the cursor or double-screen after a failure', async () => {
    const server = fakeServer(40)
    let thrown = false
    const seen: number[] = []
    await runScreenAll({
      runBatch: async (after) => {
        if (!thrown && server.screened.size === 12) {
          thrown = true
          throw new TypeError('Failed to fetch')
        }
        const b = server.run(after)
        b.screened.forEach((s) => seen.push(s.application_id))
        return b
      },
      sleep: noSleep,
    })

    expect(seen).toEqual([...seen].sort((a, b) => a - b))
    expect(new Set(seen).size).toBe(seen.length) // nobody screened twice
    expect(seen.length).toBe(40) // nobody skipped over
  })

  it('waits out a redeploy: the backoff budget covers five minutes', async () => {
    const waits: number[] = []
    const server = fakeServer(8)
    let failures = 0
    await runScreenAll({
      runBatch: async (after) => {
        // Down for four minutes, which is what the 18:46 deploy cost.
        if (failures < 6) {
          failures += 1
          throw new ApiError(503, '503: service unavailable')
        }
        return server.run(after)
      },
      sleep: async (ms) => void waits.push(ms),
    })

    expect(waits).toEqual(RETRY_BACKOFF_SECONDS.slice(0, 6).map((s) => s * 1000))
    const total = RETRY_BACKOFF_SECONDS.reduce((a, b) => a + b, 0)
    expect(total).toBeGreaterThanOrEqual(300)
    expect(server.screened.size).toBe(8)
  })

  it('gives up once the retry budget is spent, and says how far it got', async () => {
    const server = fakeServer(400)
    const result = await runScreenAll({
      runBatch: async (after) => {
        if (server.screened.size >= 8) throw new ApiError(502, '502: gone')
        return server.run(after)
      },
      sleep: noSleep,
    })

    expect(result.error).toBe('gone')
    expect(result.done).toBe(8) // the committed work is still reported
  })

  it('stops immediately on a failure that will not fix itself', async () => {
    for (const status of [401, 403, 404, 422]) {
      let calls = 0
      const result = await runScreenAll({
        runBatch: async () => {
          calls += 1
          throw new ApiError(status, `${status}: no`)
        },
        sleep: noSleep,
      })
      expect(calls, `status ${status} must not be retried`).toBe(1)
      expect(result.error).toBe('no')
    }
  })

  it('counts unreadable CVs without treating them as the end of the run', async () => {
    const server = fakeServer(20)
    const result = await runScreenAll({
      runBatch: async (after) => {
        const b = server.run(after)
        // One CV in the batch would not extract. Rule 32: that is a document
        // problem needing a human, and the run carries on.
        if (b.screened.length > 1) {
          const moved = b.screened.pop()!
          b.skipped.push({ application_id: moved.application_id, reason: 'CV did not extract' })
        }
        return b
      },
      sleep: noSleep,
    })

    expect(result.error).toBeNull()
    expect(result.skipped).toBeGreaterThan(0)
    expect(result.done + result.skipped).toBe(20)
  })

  it('honours Stop, and reports the work already committed', async () => {
    const server = fakeServer(400)
    const result = await runScreenAll({
      runBatch: async (after) => server.run(after),
      shouldStop: () => server.screened.size >= 20,
      sleep: noSleep,
    })

    expect(result.stopped).toBe(true)
    expect(result.error).toBeNull()
    expect(result.done).toBe(20)
  })

  it('abandons quietly when the user switches job', async () => {
    const server = fakeServer(400)
    const onBatch = vi.fn()
    const result = await runScreenAll({
      runBatch: async (after) => server.run(after),
      isAbandoned: () => server.screened.size >= 12,
      onBatch,
      sleep: noSleep,
    })

    expect(result.stopped).toBe(true)
    expect(result.error).toBeNull()
    // Two batches applied, not three. The third came back AFTER the user had
    // navigated away, so its rows are deliberately dropped rather than painted
    // onto a page now showing a different job. Those candidates are not lost:
    // the server committed them, and the next run picks them up.
    expect(onBatch).toHaveBeenCalledTimes(2)
    expect(server.screened.size).toBe(12)
  })

  it('terminates when the server reports work left but hands back none', async () => {
    let calls = 0
    const result = await runScreenAll({
      runBatch: async () => {
        calls += 1
        return batch({ remaining: 99, last_application_id: 7 })
      },
      sleep: noSleep,
    })

    expect(calls).toBe(1)
    expect(result.done).toBe(0)
  })

  it('tells a waiting-it-out failure from a permanent one', () => {
    expect(isTransient(new ApiError(502, ''))).toBe(true)
    expect(isTransient(new ApiError(503, ''))).toBe(true)
    expect(isTransient(new TypeError('Failed to fetch'))).toBe(true)
    expect(isTransient(new ApiError(401, ''))).toBe(false)
    expect(isTransient(new ApiError(422, ''))).toBe(false)
  })

  it('reports retry state so a five-minute wait is not a frozen page', async () => {
    const server = fakeServer(4)
    let failed = false
    const retrying: number[] = []
    await runScreenAll({
      runBatch: async (after) => {
        if (!failed) {
          failed = true
          throw new ApiError(502, '502: gone')
        }
        return server.run(after)
      },
      onProgress: (p) => retrying.push(p.retrying),
      sleep: noSleep,
    })

    expect(retrying).toContain(1) // the UI was told a retry was in progress
    expect(retrying[retrying.length - 1]).toBe(0) // and that it recovered
  })

  // 🔴 A screener that broke is NOT a CV that would not open. Technical
  // screening merged the two, so a run where all 20 candidates failed on a
  // schema mismatch reported 20 unreadable CVs that were perfectly readable,
  // and sent Ayesha to chase documents instead of an engineer.
  it('counts a screener failure apart from an unreadable CV', async () => {
    const server = fakeServer(12)
    const result = await runScreenAll({
      runBatch: async (after) => {
        const b = server.run(after) as CVScreenBatch & { failed?: unknown[] }
        const moved = b.screened.pop()!
        b.skipped.push({ application_id: moved.application_id, reason: 'no CV on file' })
        const broke = b.screened.pop()!
        b.failed = [{ application_id: broke.application_id, reason: 'ValueError: bad shape' }]
        return b
      },
      sleep: noSleep,
    })

    expect(result.skipped).toBeGreaterThan(0)
    expect(result.failed).toBeGreaterThan(0)
    expect(result.done + result.skipped + result.failed).toBe(12)
    expect(result.error).toBeNull() // per-candidate failures do not end the run
  })

  it('a batch of nothing but failures still terminates', async () => {
    let calls = 0
    const result = await runScreenAll({
      runBatch: async () => {
        calls += 1
        return batch({
          failed: [{ application_id: 1, reason: 'boom' }],
          remaining: 0,
          last_application_id: 1,
        }) as CVScreenBatch
      },
      sleep: noSleep,
    })
    expect(calls).toBe(1)
    expect(result.failed).toBe(1)
  })
})
