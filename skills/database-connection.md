# Skill: Database Connection via MCP

## Purpose
Connect the AI agent to an external database using Model Context Protocol (MCP),
enabling direct queries without engineering support.

## Prerequisites
- Database credentials (host, port, database name, username, password)
- Cursor or VS Code with Claude Code extension installed
- Read-only database access (never use write credentials for analysis)

## What is MCP?
MCP (Model Context Protocol) is the standard way for AI agents to connect to
external tools. Think of it as a plugin system. Once set up, the agent can
query your database directly using natural language or SQL.

## Setup Instructions

### Step 1: Get Your Database Credentials
You need:
- Host (e.g., db.example.com or an IP address)
- Port (e.g., 5432 for PostgreSQL, 3306 for MySQL)
- Database name
- Username (use a READ-ONLY account)
- Password

Store credentials in a secure location (password manager or Notion).
NEVER commit credentials to a file in this project folder.

### Step 2: Tell the Agent to Set Up MCP
Use this exact prompt:
> "Can you please set up an MCP for me? We will need to do some data analysis
> on [your database/product name]. Please read documentation online on how to
> do this and let me know when you're done."

The agent will:
1. Research the correct MCP server for your database type
2. Create an `.mcp.json` configuration file
3. Ask you to paste in your credentials
4. Test the connection

### Step 3: Paste Credentials When Asked
The agent will prompt you for each credential value. Paste them one at a time.

### Step 4: Accept Connection Prompts
Cursor/VS Code will ask permission to allow the MCP connection. Click Allow.

### Step 5: Test the Connection
Ask: "Can you list the tables in the database?"
If it returns table names — you're connected.

### Step 6: Save the Schema
Once connected, ask:
> "Please read the full database schema and save it to docs/schema.md"

## Security Rules
- ALWAYS use read-only credentials for analysis work
- NEVER share write access unless explicitly authorized
- If credentials are compromised, rotate them immediately
- Treat credentials like a physical key — don't leave them in plain text files

## Common MCP Servers by Database Type

| Database | MCP Server Package |
|----------|-------------------|
| PostgreSQL | @modelcontextprotocol/server-postgres |
| MySQL | Use PostgreSQL-compatible server or custom |
| SQLite | @modelcontextprotocol/server-sqlite |
| Google Sheets | @modelcontextprotocol/server-google-sheets |

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Connection refused" | Check host/port; verify database is running |
| "Authentication failed" | Double-check username/password |
| "Permission denied" | Confirm the user has SELECT privileges |
| MCP server not found | Ask agent to re-read Anthropic MCP documentation |
| Queries return nothing | Check if you need to specify schema (e.g., public.tablename) |

## After Successful Connection
Document in memory.md:
- Database type and any quirks
- Any syntax differences from standard SQL
- Which tables are most useful for your work
- Any columns that are confusingly named (and what they actually mean)
