---
name: security
description: Manage OAuth tokens, credentials, git secrets scanning. Credential management. Audit trail maintenance.
compatibility: Requires .env, .gitignore, GitHub push protection, token files in .claude/config/
---

# Security

Manage OAuth tokens and credentials securely. Maintain audit trails. Enforce git secrets scanning.

---

## When to Use This Skill

Trigger this skill when:
- User asks to "set up credentials" or "manage tokens"
- Tokens need refresh
- Credentials exposure suspected
- Git secrets scanning needed

---

## Related SOP

**Location:** `SOPs/04_Data_and_Systems/security.md`

---

## Universal Rules

**Credential Storage (Non-Negotiable):**
- NEVER commit credentials (.env, tokens) to git
- Store in `.env` (gitignored)
- Store tokens in `.claude/config/` (gitignored)
- Check .gitignore before every push

**Token Management:**
- OAuth tokens in `.claude/config/token*.json`
- Refresh before expiry
- Rotate periodically
- Log token operations

**Git Security:**
- Enforce .gitignore (no credentials)
- Enable GitHub push protection
- Scan for secrets before push
- Remove from history if exposed

**Audit Logging (Mandatory):**
- Log all credential access
- Log token operations
- Log security incidents
- Maintain searchable audit trail

**Incident Response:**
- If credentials exposed: rotate immediately
- If token leaked: revoke and refresh
- If git compromise: rewrite history (filter-repo)
- Document incident and lessons

---

## Detailed Procedure

**Step 1: Credential Storage Setup (One-Time)**
- Create `.env` file in project root with email/API credentials
- Store OAuth tokens in `.claude/config/token_*.json` (e.g., token_gmail.json, token_drive.json)
- Never store credentials in: code files, .md files, git-tracked files
- Add to `.gitignore`:
  ```
  .env
  .env.local
  .env.*.local
  .claude/config/token_*.json
  .claude/config/*.json
  ```
- Verify .gitignore is committed to git (credentials files are NOT)

**Step 2: Before Every Git Push (Mandatory Checklist)**
1. Run: `git status` → verify NO `.env` or `.claude/config/` files are staged
2. Run: `git diff --cached` → inspect what's about to be committed
3. If credentials appear: `git reset [filename]` to unstage them
4. Run: `git log --oneline -5` → spot-check recent commits have no secrets
5. Enable GitHub push protection: Settings → Code and security → Protected branches
6. Only push after confirming step 1-4

**Step 3: Token Refresh & Expiry Management**
- Check token expiry: `python scripts/utils/check_token_expiry.py`
- Schedule refresh before expiry (store expiry dates in memory.md)
- Refresh script: `python scripts/utils/refresh_oauth_tokens.py`
- After refresh: verify new tokens work with test query
- Log token operations: timestamp + operation (refresh/rotate) in `logs/token_operations.log`

**Step 4: Git Secrets Scanning (Before Push)**
- Install git secrets: `git secrets --install`
- Run scan: `git secrets --scan`
- Fix any issues (remove credentials) before pushing

**Step 5: Audit Logging (Every Credential Access)**
```python
from scripts.utils.audit_log import log_credential_access

log_credential_access(
    action="token_refresh",
    credential_type="OAuth Gmail",
    status="success",
    timestamp=datetime.now(),
    context="Refreshed before meeting scheduled 2026-05-13"
)
```

**Step 6: Incident Response (If Exposed)**
1. **Credentials Exposed:**
   - Stop all work immediately
   - Notify user
   - Rotate credentials (generate new API keys)
   - Update `.env` and `.claude/config/` with new credentials
   - Log incident: `logs/security_incidents.log`
   - Document in memory: what was exposed, when detected, remediation

2. **Token Leaked (Visible in Git History):**
   - Use git-filter-repo to remove from entire history:
     ```bash
     git-filter-repo --paths token_*.json --invert-paths
     ```
   - Force push: `git push --force-with-lease`
   - Revoke token in provider (Gmail, Google Drive, etc.)
   - Generate new token
   - Document incident + lessons

3. **Unnoticed Breach (Detected Later):**
   - Assess exposure window (when committed vs. detected)
   - Rotate ALL credentials (not just exposed one)
   - Check provider logs for unauthorized access
   - Enable 2FA on all provider accounts
   - Update incident log with assessment findings

**Step 7: Regular Security Audit (Weekly)**
- Review `.gitignore` for completeness
- Check `.env` and `.claude/config/` are properly protected
- Run git secrets scan
- Verify no credentials in logs or output files
- Check expiry dates of all tokens
- Document findings in memory

**Common Security Mistakes to Avoid:**
- Committing `.env` or token files to git (even once)
- Using shared/weak passwords for API keys
- Hardcoding credentials in Python scripts
- Leaving tokens in plain text in emails or Slack
- Not rotating credentials after employee changes
- Assuming git history is private (it's not if pushed to public repo)
- Forgetting 2FA on provider accounts (Gmail, GCP, etc.)

**Reference Scripts & Tools:**
- Check expiry: `scripts/utils/check_token_expiry.py`
- Refresh tokens: `scripts/utils/refresh_oauth_tokens.py`
- Git secrets: `git secrets --scan` (install once, run before every push)
- Audit trail: `logs/token_operations.log`, `logs/security_incidents.log`
- GCP audit: `scripts/utils/audit_gmail_scopes.py` (verify permissions)

---

## Execution Discipline

1. Check .gitignore (credentials excluded)
2. Verify tokens in `.claude/config/`
3. Check token expiry
4. Refresh if needed
5. Enable GitHub push protection
6. Scan for secrets before push
7. Log all operations
8. Document any incidents

---

## Success Criteria

✅ Credentials not in git (.gitignore enforced)  
✅ Tokens in `.claude/config/` (not root)  
✅ GitHub push protection enabled  
✅ Audit logging in place  
✅ No exposed credentials  

**Status:** ✅ PRODUCTION READY
