---
name: database-connection
description: Manage database connections. Token refresh procedures. Connection pooling. Error handling and retry logic. Monitor connection health.
compatibility: Requires Neon DB tokens, OAuth setup scripts, error handling framework
---

# Database Connection

Manage database connections with token refresh, connection pooling, error handling, and health monitoring.

---

## When to Use This Skill

Trigger this skill when:
- User asks to "set up database" or "refresh connection"
- OAuth tokens expired or need renewal
- Connection errors occur
- Need to establish fresh Neon DB connection

---

## Related SOP

**Location:** `SOPs/04_Data_and_Systems/database-connection.md`

---

## Universal Rules

**Token Management (Mandatory):**
- Check token expiry before each session
- Refresh before token expires
- Store tokens in `.claude/config/` (not root)
- Use .gitignore to protect tokens

**Connection Pooling:**
- Reuse connections when possible
- Close connections after use
- Monitor pool size
- Alert on pool exhaustion

**Error Handling (Required):**
- Try/except for all DB operations
- Log errors: timestamp, error message, query
- Retry logic with exponential backoff
- Fallback plan if connection fails

**Health Monitoring:**
- Check connection status before queries
- Monitor response times
- Alert on slowness or failures
- Document incidents

---

## Execution Discipline

1. Check token expiry
2. Refresh if needed (run setup script)
3. Test connection (ping query)
4. Set up error handling
5. Execute queries with retry logic
6. Log any issues
7. Monitor health

---

## Success Criteria

✅ Tokens current (not expired)  
✅ Connection established  
✅ Error handling in place  
✅ Retry logic working  
✅ Health monitored  

**Status:** ✅ PRODUCTION READY
