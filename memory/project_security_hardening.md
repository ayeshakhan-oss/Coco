---
name: Security Hardening — 2026-03-31
description: What was built, why, and current security rating after Noah benchmark comparison
type: project
---

Security hardening completed 2026-03-31 after benchmarking against Noah (Jawwad's agent).

**Why:** Noah email audit revealed gaps in Coco's security posture. User asked to fix all gaps except bulk send rate limiting.

## What was built

### Send-layer bouncer (scripts/utils/safe_send.py)
All 35 send scripts patched via patch_safe_send.py to use safe_sendmail() instead of raw smtplib.sendmail(). Raises SecurityError + logs to logs/email_audit.log if any unapproved recipient detected. ALLOWED_DOMAINS = {taleemabad.com, niete.edu.pk}. External candidate addresses must be explicitly whitelisted via allow_candidate_addresses([...]) before sending.

### Read-layer audit (scripts/utils/audit_log.py)
Logs every Gmail read and DB query to logs/read_audit.log. Wired into:
- scripts/jobs/job36/fetch_job36_rejection_replies.py
- scripts/jobs/job36/check_job36_case_study_submissions.py
- scripts/gmail/gmail_scan_inbox.py

### Token expiry monitor (scripts/utils/check_token_expiry.py)
Checks all 4 OAuth token files (token.json, token_gmail.json, token_gmail_labels.json, token_sheets.json) for expiry/revocation. Warns if expiring within 3 days. Called at startup in all Gmail read scripts and send_job36_debrief_invite_pilot.py.

### Gmail scope auditor (scripts/utils/audit_gmail_scopes.py)
Flags tokens with overly broad scopes. Run manually: python scripts/utils/audit_gmail_scopes.py

### Candidate data out of git
- git rm --cached removed: output/, data/, nain_tara_cv.pdf, job36_rejection_replies.json, job36_case_study_gmail_check.json, job32_invite_check.txt, job36_invite_check.txt
- .gitignore updated: output/, data/, *.pdf, *.txt, candidate JSON files excluded permanently

### Security rules (skills/security.md)
6 rules: prompt injection defense, credential protection, fail-safe behavior, data leakage prevention, untrusted external content, scope boundaries.

## Current security rating: 8.5/10
**Remaining gap:** Git history still contains candidate files from commit 4f3dffd. Needs git filter-repo to fully scrub — requires user approval (destructive/force-push).
**Excluded by user:** Bulk send rate limiting.

**How to apply:** Before building any new send or read script, use safe_sendmail() and log_gmail_read()/log_db_query() from the start. Don't add raw smtplib.sendmail() calls anywhere.
