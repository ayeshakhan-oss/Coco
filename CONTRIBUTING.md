# Improving Coco

Thank you for helping make Coco better. Anything merged here goes live for the whole
People & Culture team, so every change is reviewed by Ayesha, Aymen or Jawwad first.

## First time (about 30 minutes)

Follow **Part 1** of [docs/MAINTAINER_GUIDE.md](docs/MAINTAINER_GUIDE.md): install the tools,
**clone** the repo in VS Code (Ctrl+Shift+P → Git: Clone; don't download the ZIP), set up
Python, and create your own `.env` and Google tokens. Ayesha sends you your own database
connection privately.

## Each change

1. `git pull` to start from the latest version.
2. Tell Coco what you want to improve, in plain words.
3. Run the tests: `python -m pytest webapp/tests -q`
4. Ask Coco: **"put my changes on a branch and open a pull request."**
5. Wait for a review. When it is approved and merged, it is live.

You cannot push to `main` directly. That is on purpose.

## Please don't

- Commit `.env`, tokens, CVs, or files containing candidate names or emails. Keep personal
  working files in `data/`, which git ignores.
- Change the locked rules (tone master file, v8 email layout, `scripts/evals/`, `CLAUDE.md`)
  without talking to Ayesha first.
- Send a live candidate email without a pilot to Ayesha first.
