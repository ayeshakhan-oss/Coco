---
name: data-analysis
description: Analyze data with verification. Query data, cross-reference sources. Generate insights and trends. Document methodology.
compatibility: Requires MCP database access, verified sources, analysis frameworks
---

# Data Analysis

Analyze data with cross-source verification, generate insights and trends, and document methodology clearly.

---

## When to Use This Skill

Trigger this skill when:
- User asks to "analyze data" or "find trends"
- User needs "insights" from candidate data
- Multiple data sources available
- Analysis requires cross-reference verification

---

## Related SOP

**Location:** `SOPs/04_Data_and_Systems/data-analysis.md`

---

## Universal Rules

**Data Verification (Non-Negotiable):**
- Query verified data (MCP only)
- Cross-reference multiple sources
- No assumptions (flag uncertain data)
- No fabrication (use only verified sources)

**Analysis Process:**
1. Query data (via MCP)
2. Cross-reference with other sources
3. Identify patterns (trends, anomalies)
4. Generate insights (what does it mean?)
5. Document methodology (how did we get here?)
6. Flag limitations (what we don't know)

**Insights Quality:**
- Grounded in specific data
- Not generic conclusions
- Evidence-based (cite source)
- Actionable (clear next steps)

**Documentation (Mandatory):**
- State queries used
- Note sources cross-checked
- Document methodology
- Flag any uncertainties

---

## Detailed Procedure

**Step 1: Read Schema First (MANDATORY)**
- Open `docs/schema.md`
- Understand table names, column names, data types
- Never assume column meanings — read documentation
- Ask: "Does this column name mean what I think it means?"

**Step 2: Explore Before Analyzing**
```sql
-- List all tables
SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';

-- Inspect table columns
SELECT column_name, data_type FROM information_schema.columns
WHERE table_name = 'your_table';

-- Check row counts and date ranges
SELECT COUNT(*), MIN(created_at), MAX(created_at) FROM your_table;
```

**Step 3: Write Analysis Query**
- Use explicit column names (never `SELECT *`)
- Filter out deleted/inactive records if applicable
- Include date range filters (document in report)
- For retention: cohort by signup week, not calendar week
- For performance: add LIMIT 10000 during exploration, remove for final analysis

**Step 4: Execute via MCP & Process Data**
```python
from mcp__neon-postgres__query import query

results = query(sql=your_query_string)

import pandas as pd
df = pd.DataFrame(results)

# Inspect before analyzing
print(df.head())           # First 5 rows
print(df.dtypes)           # Column types
print(df.isnull().sum())   # Missing values
```

**Step 5: Generate Visualizations (If Needed)**
```python
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Non-interactive mode

fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(df['category'], df['value'])
ax.set_title('Chart Title')
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
plt.tight_layout()  # Always call this to prevent label cutoff
plt.savefig('output/chart_name.png', dpi=150, bbox_inches='tight')
plt.close()
```

**Step 6: Save Outputs**
- Save charts to `output/chart_name.png`
- Save written report to `output/YYYY-MM-DD-analysis-name.md`
- Name files with date prefix
- Include raw data (CSV or table) if applicable

**Step 7: Document Methodology**
- State which queries were used (include SQL)
- Note sources cross-checked
- Document date ranges and filters
- Flag any uncertainties or data quality issues
- Example: "Data source: candidates table, filtered for active status (is_active=true), date range 2026-01-01 to 2026-05-12"

**Step 8: Generate Insights**
- Grounded in specific data (not generic conclusions)
- Evidence-based (cite source table/column)
- Actionable (clear next steps or recommendations)
- Flag limitations (what we don't know, what we didn't analyze)

**Common Mistakes to Avoid:**
- Guessing column names without reading schema
- Missing plt.tight_layout() → labels cut off in charts
- Not filtering deleted records (soft deletes with deleted_at column)
- Using wrong date grouping (DATE_TRUNC vs EXTRACT)
- Forgetting data source/date range in report
- Making generic conclusions without evidence

---

## Execution Discipline

1. Define analysis question
2. Query verified data (MCP)
3. Cross-check with other sources
4. Extract patterns
5. Generate insights
6. Document methodology
7. Flag limitations
8. Present findings

---

## Success Criteria

✅ Data verified (multiple sources)  
✅ Queries documented  
✅ Methodology clear  
✅ Insights grounded in data  
✅ Limitations flagged  

**Status:** ✅ PRODUCTION READY
