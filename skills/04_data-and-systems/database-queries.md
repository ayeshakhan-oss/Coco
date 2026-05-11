---
name: database-queries
description: Database queries via MCP (never direct psycopg2). Audit logging mandatory. Result verification required. Query templates for common operations.
compatibility: Requires MCP neon-postgres, audit logging, RULES.md Integration Rules
---

# Database Queries

Execute database queries via MCP only (never direct connection). Mandatory audit logging. Verify results against ground truth.

---

## When to Use This Skill

Trigger this skill when:
- User asks for "database query" or "data from Markaz"
- Need candidate data, staging data, leave requests
- Query must use MCP (never direct psycopg2)
- Audit logging required

---

## Related SOP

**Location:** `SOPs/04_Data_and_Systems/database_queries.md`

---

## Universal Rules

**Connection Method (Non-Negotiable):**
- ALWAYS use MCP (`mcp__neon-postgres__query()`)
- NEVER use direct psycopg2
- NEVER use custom connections

**Audit Logging (Mandatory):**
- Every query logged: `log_db_query(description, row_count)`
- Timestamp, user, query text, rows returned
- Log file: `logs/db_query_audit.log`

**Result Verification:**
- Small result sets (<5 rows) require manual verification
- Cross-reference with other sources
- Flag suspicious results

**Common Queries:**
- Candidate data from candidates table
- Leave requests from leave_requests table
- Application status from applications table
- Staging data from any relevant table

---

## Execution Discipline

1. Read the MCP documentation
2. Construct query (SELECT with proper WHERE)
3. Execute via MCP (`mcp__neon-postgres__query()`)
4. Log result: `log_db_query(description, row_count)`
5. Verify result (small set? cross-check)
6. Return data

---

## Success Criteria

✅ Used MCP (not direct DB)  
✅ Audit logging in place  
✅ Results verified (ground truth)  
✅ No hardcoded queries  

**Status:** ✅ PRODUCTION READY
