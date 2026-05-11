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
