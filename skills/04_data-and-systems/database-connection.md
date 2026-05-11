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

## Detailed Procedure

**Prerequisites:**
- Obtain database credentials: host, port, database name, username (read-only), password
- Store securely (password manager or Notion, NOT in project files)
- Have VS Code or Cursor with Claude Code extension

**Step 1: Set Up MCP (One-Time Setup)**
- MCP = Model Context Protocol (plugin system for external tools)
- User provides prompt: "Set up an MCP for [database type]"
- Agent will:
  1. Research correct MCP server for your database (e.g., @modelcontextprotocol/server-postgres)
  2. Create `.mcp.json` configuration file with connection details
  3. Ask you to paste credentials one at a time
  4. Test connection with `SELECT COUNT(*) FROM information_schema.tables`

**Step 2: Accept Connection Permissions**
- VS Code/Cursor will ask permission to allow MCP connection
- Click "Allow"
- Connection established

**Step 3: Test Connection**
- Ask agent: "Can you list the tables in the database?"
- Expected response: list of table names from information_schema
- If successful: connection is ready

**Step 4: Generate Schema Documentation**
- Ask agent: "Please read the full database schema and save it to docs/schema.md"
- Agent will query `information_schema` and document:
  - All table names
  - All column names and data types
  - Primary/foreign keys
  - Constraints

**Step 5: Token Management (Ongoing)**
- Before each session: check token expiry with `scripts/utils/check_token_expiry.py`
- If expiring: run token refresh script (provided by agent)
- Store tokens in `.claude/config/` (NOT root directory)
- Include in `.gitignore` to prevent accidental commits

**Step 6: Connection Pooling & Reuse**
- Reuse connections across multiple queries (don't create new connection per query)
- Close connections after batch of queries completes
- Monitor pool size (document in memory)
- Alert if pool becomes exhausted (too many open connections)

**Step 7: Error Handling & Retry Logic**
```python
import time
from mcp__neon-postgres__query import query

def execute_with_retry(sql, max_retries=3, backoff=2):
    for attempt in range(max_retries):
        try:
            result = query(sql=sql)
            return result
        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = backoff ** attempt
                print(f"Retry in {wait_time}s...")
                time.sleep(wait_time)
            else:
                print(f"Failed after {max_retries} attempts: {e}")
                raise
```

**Step 8: Health Monitoring & Incident Logging**
- Check response time for each query (flag if >5 seconds)
- Log any connection failures with timestamp + error message
- Document incident in `logs/connection_incidents.log`
- Notify user if slowness persists across multiple queries

**Common MCP Servers by Database Type:**
- PostgreSQL: `@modelcontextprotocol/server-postgres` (Neon serverless)
- MySQL: Use PostgreSQL-compatible server or custom
- SQLite: `@modelcontextprotocol/server-sqlite`
- Google Sheets: `@modelcontextprotocol/server-google-sheets`

**Troubleshooting Common Issues:**
- "Connection refused" → Check host/port, verify database is running
- "Authentication failed" → Double-check username/password
- "Permission denied" → Confirm user has SELECT privileges
- "MCP server not found" → Agent needs to re-read MCP documentation
- "Queries return nothing" → Check if schema name needed (e.g., `public.tablename`)

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
