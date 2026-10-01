---
name: A React page is only verified by rendering it
description: tsc, vite build and the test suite all pass on a page whose every button is invisible. 15 live button usages carry a class that does not exist. Headless Chrome over CDP is the visual proof, since no Playwright is installed.
metadata:
  type: feedback
---

# Render the page. A green build says nothing about what a person sees.

Building the technical screening wizard (2026-09-25), `tsc -b` was clean, `vite build` was
clean, 769 backend tests and 12 frontend tests passed, and **every button on the page rendered
as bare unstyled text**. Nothing in the toolchain can see that: a class name is a string, and an
undefined one is not an error.

## The defect, which is live and spreading

`frontend/src/index.css` defines exactly four button classes:

    .btn          shape, padding, radius, font-weight, disabled styling
    .btn-primary  colour only
    .btn-green    colour only
    .btn-ghost    colour only

So a button needs **both**: `className="btn btn-primary"`. Two ways to get it wrong, and both
are in the tree:

- **`.btn-secondary` does not exist at all.** 8 usages. Renders as plain text.
- **A colour class without `.btn`.** 7 usages. Colour, no padding, no shape.

Measured 2026-10-01: **15 broken against 44 correct**, across `CaseStudyTrackingPage`,
`ComingSoonPage`, `ContractsPage`, `CVScreeningPage`, `InvitesPage`, `KCDEvaluationPage`,
`SkillsPage`. It **spreads**, because each new page is copied from an existing one; two of those
files did not exist when the defect was first seen. CV Screening's own Screen / Re-screen
buttons are among them.

Fix is mechanical: `className="btn-secondary …"` to `className="btn btn-ghost …"`, and
`className="btn-primary …"` to `className="btn btn-primary …"`. A lint rule or a test asserting
every `className` containing `btn-` also contains a bare `btn` would stop it returning.

## How to actually look at a page here

No Playwright, no Puppeteer, no chromium-cli. **Chrome is installed** and `websockets` is in
`.venv`, which is enough for both a screenshot and real clicking.

A static screenshot, for a page that needs no interaction:

    chrome.exe --headless=new --disable-gpu --no-sandbox --hide-scrollbars \
      --window-size=1700,1000 --virtual-time-budget=15000 \
      --screenshot=out.png http://127.0.0.1:8000/some-route

Then **Read the PNG**. Same principle as the Drive-export-to-PyMuPDF trick for Sheets and decks:
a rendered image is real visual proof and lifts the Rule 14 limitation.

To drive a multi-step page, start Chrome with `--remote-debugging-port=9333
--user-data-dir=<scratch>`, then `GET http://127.0.0.1:9333/json` for the page's
`webSocketDebuggerUrl` and speak CDP over it: `Page.navigate`, `Runtime.evaluate` (click by
visible text with `document.querySelectorAll('button')`), `Page.captureScreenshot`.
`Runtime.evaluate` on `document.body.innerText` also reads the rendered copy back, which is how
the date format below was caught.

🔴 **Poll, never sleep.** A fixed `await asyncio.sleep(3)` fired while the page still said
"Loading the rubric…" and read as a broken page. Wait for the control to exist and be enabled.

## Two more things only rendering caught

- **Dates printed `7/8/2026`.** A bare `toLocaleDateString()` is month-first and half this team
  reads it as 7 August. `frontend/src/lib/format.ts::formatDate` already existed and renders
  `Jul 8, 2026`. **Check `format.ts` before writing a date helper.**
- **The run-step layout** only made sense once the four steps were walked in order.

## The rule

A page that compiles is not a page that works. For any UI change, render it and look at the
image before saying it is done. Structural checks are not visual proof (Rule 14), and that
applies to React exactly as it does to .docx.

See [[nugget_repo_and_web_app_locations_2026_09_25]] · [[screening_skills_never_merge_2026_09_25]]
