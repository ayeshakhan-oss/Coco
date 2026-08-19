---
name: Audio Monitoring Officer — 15-Day Re-Engagement Confirmation (LIVE 2026-08-19)
description: In-thread contract-extension confirmation sent live to 6 Audio Monitoring Officers. Establishes the "Project Extension / Re-Engagement Confirmation" email pattern, Ayesha's reusable signature HTML, and three verified traps (mailbox-specific thread IDs, typo'd recipient addresses, "go live" CC inheritance).
type: project
---

# Audio Monitoring Officer (Assessments) — 15-Day Re-Engagement — LIVE 2026-08-19

**Sent:** 19 Aug 2026 06:31 UTC · 6 emails · from `ayesha.khan@taleemabad.com`
**Engagement:** 20 Aug 2026 (Thu) → 3 Sep 2026 (Thu) = **15 days inclusive** · **PKR 50,000** each
**Script:** `scripts/jobs/audio_monitoring/send_audio_monitoring_extension_pilot.py`
**Precedent:** Ayesha's 15 Jul 2026 extension (16–30 Jul run), message-id
`CAE4XdQOZrGkg2RKCEaYQQW8upQHaj4RynbrcpJpfMeTZagkAxQ@mail.gmail.com`

---

## The 6 recipients

| Person | Candidate address (CC) | Thread (Ayesha's mailbox) |
|---|---|---|
| Fareeda Sanam | shaikhfareeda8@gmail.com | 19e0746e31476689 |
| Kainat (Syeda Kaynat Bukhari) | kaynatsyeda4@gmail.com **+ kainatsyeda628@gmail.com** | 19e07432b94fa276 |
| Laraib Bukhari | laraibsyed1999@gmail.com | 19e07448e7176fd8 |
| Gul Rukh | gulrukhdinal@gmail.com | 19e074595e7f9b22 |
| Arshad Khan | arshadkhan285981@gmail.com | 19e0746c39852e4c |
| Muddasir Zaman | **zamanmuddasir44@gmail.com** (corrected) | 19e07423efadb014 |

**Recipient shape (inherited from the thread, per Ayesha 2026-08-18):**
`To: ayat@niete.edu.pk` · `Cc: candidate + accounts.query@ + hr@ + hiring@ +
muzzammil.patel@ + salman.iqbal@ + ahwaz.akhtar@ + sabeena.abbasi@`

Only Fareeda and Kainat had received the 15 Jul extension; the other four had
nothing on their thread since 8 May.

---

## 🔴 TRAP 1 — Gmail thread IDs are MAILBOX-SPECIFIC; Message-IDs are global

The claude.ai Gmail MCP connector is authed as **jawwad.ali@**. The local
`.claude/config/token_gmail.json` is **ayesha.khan@** (readonly + send) — the
account we actually send from. Passing an MCP-derived `threadId` to the local
Gmail API returns **404 "Requested entity was not found."** — it is not a
permissions problem, the ID simply does not exist in that mailbox.

**Rule:** resolve threads in the SAME mailbox you will send from. RFC822
`Message-ID` headers are globally stable and are what `In-Reply-To`/`References`
need — get them with
`threads().get(..., format="metadata", metadataHeaders=["Message-ID", ...])`.

**Second trap inside this:** searching `subject:"..." <address>` also matches
calendar-invite threads where the address appears in an attendee list. Filter to
the thread whose FIRST message is the one you mean.

## 🔴 TRAP 2 — A three-month-old thread can be addressed to a typo

Muddasir's 8 May welcome went to `Zamanmuddasir44@**gamil**.com` and never
landed — no reply, and he alone never got the 9 May credentials email. Nobody
noticed for three months because the thread *looked* normal from the inside.
His real address (`zamanmuddasir44@gmail.com`) was recoverable from his own
calendar RSVP in Ayesha's mailbox.

**Rule:** before threading onto an old conversation, read the `To:` of the
original and sanity-check the domain. Inheriting a thread's recipients must not
mean inheriting its delivery failure. A thread with zero candidate replies is a
signal, not a coincidence.

## 🔴 TRAP 3 — `newer_than:1h` is unreliable for send verification

Gmail's `newer_than:` is day-granular in practice; a `1h` query returned 0
immediately after a confirmed send. Verify with `newer_than:2d` and separate
pilots from live sends by a real discriminator — here, **presence of a `Cc`
header** (pilots have none) plus `internalDate`.

---

## The email pattern — "Project Extension / Re-Engagement Confirmation"

Not a candidate-comms decision email and **not** a Design 3 contract email. It
is a short in-thread confirmation to someone already engaged. Properties:

- **Threads into the person's original conversation** (In-Reply-To + References).
- **Subject unchanged**: `Re: Welcome to Taleemabad – Audio Monitoring Officer (Assessments)`.
  A `[PILOT – ]` prefix would BREAK threading — omitted deliberately on pilots,
  which is safe because pilots go to Ayesha alone.
- **~150 words**, plain wording, no "not a yes for now" (nothing is being declined).
- `multipart/alternative` — plain text + HTML.
- **Three bolded elements only**: `15-day Audio Monitoring project`,
  `<START> to <END>`, `PKR <amount>.`
- **No fixed-width wrapper table** → fluid on mobile (CLAUDE.md Rule 16).
- Neither send hook fires on it (avoid `scripts/contracts/send_` and the
  warm_bench/gwc/values/rejection filename patterns) — correct, since there is
  no .docx package and it is not a decision email.

## Ayesha's signature — reusable HTML

Lifted verbatim from her own 15 Jul send so it renders identically to what she
normally sends (green name, blue title/phone, taleemabad.com + LinkedIn links).
Lives as `SIGNATURE_HTML` in the send script. **Copy it rather than re-guessing
colours** — `#6aa84f` name, `#3d85c6` title and phone, `rgb(34,34,34)` body,
LinkedIn `https://www.linkedin.com/in/ayesha-raza-khan-386668177/`.

---

## Open follow-ups

1. **Muddasir was never actually onboarded in May** — both his welcome and his
   credentials email died on the typo'd address. He likely needs the Google
   Workspace + Markaz account setup the other five got on 9 May. Start date was
   the very next day.
2. **Kainat's live address** — the 17 Jul send added `kainatsyeda628@gmail.com`
   but the thread is still carried by `kaynatsyeda4@gmail.com`. Confirm which
   she reads.

## Verified facts (do not re-derive)

- 20 Aug 2026 = Thursday · 3 Sep 2026 = Thursday · 15 days inclusive.
  Matches the previous 16–30 Jul run's Thu→Thu shape exactly.
- PKR 50,000 was the figure in the original 8 May welcome for Fareeda, Arshad,
  Gul Rukh and Muddasir, and in the 15 Jul extension for Fareeda and Kainat.
- No bounces within the hour after the live send.
