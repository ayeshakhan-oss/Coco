// The "Screen this whole position" runner.
//
// 🔴 WHY THIS EXISTS AS ITS OWN MODULE, AND WHY IT RETRIES.
//
// Screening a position is a client-side loop: the server does a few candidates
// per request because each CV is a model call of roughly 12 seconds, so 410
// candidates is over an hour and no single HTTP request survives that.
//
// On 2026-09-23 Ayesha ran CPD Coach (job 17, 410 applications). The loop ran
// cleanly for fifty minutes at about five candidates a minute and then stopped
// dead at 19:12:55 UTC with 236 of 410 done. Nothing was wrong with the
// screening. Railway had redeployed: three deploys landed on top of that one
// run (18:46, 19:10 and 19:13 UTC), and the container restart killed the
// request that was in flight. The loop had no retry, so one dead request ended
// a fifty-minute run.
//
// A redeploy is not the only way to lose one request. A phone switching to
// wifi, a laptop sleeping for a moment, a proxy hiccup and a 502 all look
// identical from here, and all of them used to cost the whole run.
//
// So: a transient failure WAITS AND RETRIES, and only a failure that will not
// fix itself stops the run. The retry budget is deliberately about five
// minutes, because that is how long a Railway redeploy takes to come back --
// the 18:46 deploy above put a four-minute hole in the run.
//
// Retrying is safe. The server commits every candidate as it finishes and the
// cursor only advances on success, so a retry re-asks from the last CONFIRMED
// position. Anyone already committed by the request that died carries a
// current screen and is excluded by the server's own query, so nobody is
// screened twice and nobody is skipped.

import { ApiError } from './api'
import type { CVScreenBatch } from './types'

// Waits between consecutive failures, in seconds. Sums to 300s, five minutes,
// which spans a redeploy with room to spare. The run gives up after the last
// one rather than retrying for ever: a server that has been unreachable for
// five minutes needs a person, not another request.
export const RETRY_BACKOFF_SECONDS = [2, 4, 8, 15, 30, 30, 45, 45, 60, 61]

// Statuses that are worth waiting out. 502/503/504 are what Railway's edge
// returns while a container is restarting; 429 is a rate limit; 408 and a
// missing status (a thrown network error) are the request never arriving.
// 500 is here because the batch endpoint already turns a per-candidate failure
// into a `skipped` entry, so a 500 from it is infrastructural rather than
// something this pool of CVs will keep reproducing.
const TRANSIENT_STATUSES = new Set([408, 429, 500, 502, 503, 504])

/** True when waiting is likely to help. A 401, 403, 404 or 422 will not fix
 *  itself: no session, no permission, no job, or a job with no readable
 *  description. Those stop the run and say why. */
export function isTransient(error: unknown): boolean {
  if (error instanceof ApiError) return TRANSIENT_STATUSES.has(error.status)
  // fetch() rejects with a TypeError when the request never completed: DNS,
  // a dropped connection, a container that went away mid-response.
  return error instanceof TypeError
}

export interface ScreenAllProgress {
  /** Candidates screened so far in this run. */
  done: number
  /** Candidates the server could not read: no CV, or a CV that would not
   *  extract. Rule 32: an unreadable CV is a document problem needing a
   *  human, never a weak candidate. Counted and reported, never hidden. */
  skipped: number
  /** Consecutive failures right now, 0 when healthy. Shown to the user so a
   *  five-minute wait reads as "reconnecting", not as a frozen page. */
  retrying: number
  /** Seconds until the next attempt, when retrying. */
  retryInSeconds: number
}

export interface ScreenAllResult {
  done: number
  skipped: number
  /** Set when the run ended on an error rather than finishing or stopping. */
  error: string | null
  /** True when the caller's stop flag ended it. */
  stopped: boolean
}

/** The minimum a batch response must carry for this loop to drive it.
 *
 *  Generic on purpose. Technical screening runs the same shape of loop for the
 *  same reason (a model call per candidate, far longer than one request), and
 *  its `/runs/{id}/work` response was named to match these four fields. The
 *  loop is transport, not judgement: it knows nothing about criteria, tiers or
 *  rubrics, so sharing it does NOT couple the two screening skills, which stay
 *  separate under CLAUDE.md Rule 33. `screened` and `skipped` are `unknown[]`
 *  here precisely so neither side's vocabulary can leak into the other. */
export interface BatchLike {
  screened: unknown[]
  skipped: unknown[]
  last_application_id: number | null
  remaining: number
}

export interface ScreenAllDeps<B extends BatchLike = CVScreenBatch> {
  /** One slice of work. `after` is the cursor; null starts from the top.
   *  Technical screening ignores it: the server claims its own items. */
  runBatch: (after: number | null) => Promise<B>
  /** Called once per successful batch, before progress is reported. */
  onBatch?: (batch: B) => void
  onProgress?: (progress: ScreenAllProgress) => void
  /** The Stop button. Checked before every attempt. */
  shouldStop?: () => boolean
  /** The user navigated to another job: abandon quietly, change nothing. */
  isAbandoned?: () => boolean
  /** Injected so tests do not wait five real minutes. */
  sleep?: (ms: number) => Promise<void>
}

const realSleep = (ms: number) => new Promise<void>((r) => setTimeout(r, ms))

function message(error: unknown): string {
  if (error instanceof ApiError) return error.message.replace(/^\d+:\s*/, '')
  if (error instanceof Error && error.message) return error.message
  return 'The run stopped unexpectedly.'
}

/**
 * Screen every remaining candidate on a job, surviving transient failures.
 *
 * Returns rather than throws: a run that ends badly still reports how many
 * candidates it got through, because those are committed and real.
 */
export async function runScreenAll<B extends BatchLike = CVScreenBatch>(
  deps: ScreenAllDeps<B>,
): Promise<ScreenAllResult> {
  const {
    runBatch,
    onBatch,
    onProgress,
    shouldStop = () => false,
    isAbandoned = () => false,
    sleep = realSleep,
  } = deps

  let after: number | null = null
  let done = 0
  let skipped = 0
  let failures = 0

  const report = (retryInSeconds = 0) =>
    onProgress?.({ done, skipped, retrying: failures, retryInSeconds })

  for (;;) {
    if (isAbandoned()) return { done, skipped, error: null, stopped: true }
    if (shouldStop()) return { done, skipped, error: null, stopped: true }

    let batch: B
    try {
      batch = await runBatch(after)
    } catch (error) {
      if (isAbandoned()) return { done, skipped, error: null, stopped: true }

      // A failure that will not fix itself, or a retry budget spent.
      if (!isTransient(error) || failures >= RETRY_BACKOFF_SECONDS.length) {
        return { done, skipped, error: message(error), stopped: false }
      }

      const wait = RETRY_BACKOFF_SECONDS[failures]
      failures += 1
      report(wait)
      await sleep(wait * 1000)
      // `after` is deliberately NOT advanced. The next attempt re-asks from
      // the last confirmed cursor; anyone the dead request had already
      // committed is excluded by the server's own unscreened query.
      continue
    }

    if (isAbandoned()) return { done, skipped, error: null, stopped: true }

    failures = 0
    done += batch.screened.length
    skipped += batch.skipped.length
    // A batch that returned nothing advances the cursor to where it looked,
    // so the next pass cannot ask the same question again.
    after = batch.last_application_id ?? after
    onBatch?.(batch)
    report()

    if (batch.remaining === 0) break
    // Belt and braces against a server that reports work remaining but hands
    // back nothing to do: without this the loop would spin at full speed.
    if (batch.screened.length === 0 && batch.skipped.length === 0) break
  }

  return { done, skipped, error: null, stopped: false }
}
