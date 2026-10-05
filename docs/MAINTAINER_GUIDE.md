# Coco Maintainer Guide

**For:** Aymen Abid and Jawwad Ali, who can review, push and deploy anything in this repo.
Everyone else follows `CONTRIBUTING.md`, and their changes come to one of you (or Ayesha) for review.

**The one thing to remember:** anything that lands on `main` goes live on Railway within a few
minutes. Coco is used by the whole P&C team and sends real emails to real candidates.

---

## Part 1: One-time setup (about 30 minutes)

### Step 1. Accept your invitations
Check your Taleemabad inbox for two emails and accept both:
- **GitHub**: the invitation to the Coco repository.
- **Railway**: the invitation to the "Ayesha Coco" project. This is what lets you see and
  roll back deploys.

### Step 2. Install the tools (skip anything you already have)
1. **Git**: https://git-scm.com/downloads, then click Next through the installer.
2. **Python 3.13**: https://www.python.org/downloads/, and tick **"Add Python to PATH"**.
3. **Node.js 22 LTS**: https://nodejs.org (needed only if you change the web app's pages).
4. **VS Code**: https://code.visualstudio.com, then install the **Claude Code** extension and
   sign in with your own Claude account.

### Step 3. Get the repository (clone it, don't download the ZIP)
1. In VS Code press **Ctrl+Shift+P**, type **Git: Clone**, and press Enter.
2. Paste the repository URL Ayesha sends you, and press Enter.
3. Choose a folder (for example `C:\Coco`), then click **Open** when VS Code asks.
4. If VS Code asks you to sign in to GitHub, do so.

> Why not the ZIP? A downloaded folder is not connected to GitHub, so nothing you
> improve can be sent back. A clone can.

### Step 4. Set up Python (once)
Open the terminal in VS Code (**Ctrl+`**) and run, one line at a time:

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt -r webapp/requirements.txt
```

### Step 5. Your own settings file
1. Copy `.env.example` and rename the copy to `.env`.
2. Fill in **your own** values. Ayesha will send you **your own** database connection
   string (`DATABASE_URL`) privately.
3. 🔴 Never paste a password, token or `.env` contents into Claude, Slack, WhatsApp or email.
   `.env` is ignored by git, so it never leaves your laptop.

### Step 6. Your own Google access (Gmail, Drive, Sheets)
Run these in **your own terminal window**, not by asking Claude, because they print a secret
token on screen:

```
python scripts/setup/setup_sheets_token.py
python scripts/auth/setup_gmail_sync_token.py
```

Sign in with **your own** Taleemabad account when the browser opens. The tokens are saved in
`.claude/config/`, which git ignores.

### Step 7. Check everything works
```
python -m pytest webapp/tests -q
```
You should see "passed" at the end. Then type any question to Coco in the Claude Code panel.
It should answer with Taleemabad context, which means CLAUDE.md and the skills loaded.

---

## Part 2: Making a change

1. **Start fresh.** In the terminal: `git pull`
2. **Make a branch** for anything bigger than a typo: `git checkout -b aymen/warm-bench-tone`
3. **Ask Coco to do the work**, in plain words. Coco knows the rules in `CLAUDE.md`.
4. **Run the tests:** `python -m pytest webapp/tests -q`
5. **Check exactly what you are about to commit** (two people's sessions have mixed up files before):
   `git diff --cached --name-only`. Read the list.
6. **Send it:**
   - Small, safe change: you may push straight to `main`.
   - Anything that changes how letters are written, checked or sent: open a pull request, and
     ask the other of you two (or Ayesha) to look. Trusted does not mean unreviewed.

You can ask Coco to do steps 2, 5 and 6 for you: *"put this on a branch and open a pull request."*

---

## Part 3: Reviewing someone else's pull request

On GitHub, open **Pull requests**, then click the PR and the **Files changed** tab. Before approving:

- [ ] The automatic tests passed (green tick).
- [ ] No password, token, `.env`, CV or candidate email address is in the change.
- [ ] Locked rules are untouched unless Ayesha agreed: the tone master file, `v8_template.py`,
      `scripts/evals/`, `CLAUDE.md`.
- [ ] CV Screening and Technical Screening are still separate (CLAUDE.md Rule 33).
- [ ] A new file the web app uses is actually in the PR, not only on the author's laptop
      (Rule 32: this once took the site down for 29 minutes).
- [ ] If it changes what letters say, read one generated letter yourself.

Then click **Review changes → Approve → Merge**.

---

## Part 4: After a merge (it goes live)

1. Railway deploys automatically. Wait 3 to 5 minutes.
2. Open `https://coco-production-bcc8.up.railway.app/healthz`. The `commit` value should
   match the first characters of your commit on GitHub.
3. This only proves the app started. Open the page you changed and use it once.
4. **If something is broken:** in Railway open the service, then **Deployments**, then click
   **Redeploy** on the last good one. Then tell Ayesha.

> Database changes (new tables) do not run on deploy. Ask before merging anything in `alembic/`.

---

## Part 5: Never

- Never send a live candidate email without a pilot first. Pilots go to ayesha.khan@taleemabad.com only (CLAUDE.md Rule 4).
- Never put `[PILOT – ]` in a live subject line.
- Never commit `.env`, tokens, CVs or files with candidate emails. Personal working files go in `data/`, which git ignores.
- Never force-push to `main`.
- Never share your database string or tokens with anyone, including teammates. Each person has their own, so access can be switched off for one person without affecting the others.
