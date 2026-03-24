# Skill: Data Analysis

## Purpose
Analyze data from connected databases and produce actionable insights.

## Prerequisites
- MCP connection to the database must be active (see skills/database-connection.md)
- Database schema must be loaded (see docs/schema.md)
- Python environment with pandas, matplotlib, seaborn installed

## Instructions

### Step 1: Read the Schema First (MANDATORY)
Before writing a single query, read docs/schema.md.
Never assume what a column means. Never guess table names.
Ask: "Does this column name mean what I think it means?"

### Step 2: Explore Before Analyzing
```sql
-- List all tables
SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';

-- Inspect a table's columns
SELECT column_name, data_type FROM information_schema.columns
WHERE table_name = 'your_table';

-- Check row counts and date ranges
SELECT COUNT(*), MIN(created_at), MAX(created_at) FROM your_table;
```

### Step 3: Write the Analysis Query
- Use explicit column names (never SELECT *)
- Always filter out deleted/inactive records if applicable
- Include date range filters and state them in your report
- For retention: cohort by signup week, not calendar week

### Step 4: Process with Python
```python
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Required for non-interactive environments

# Load query results into DataFrame
df = pd.DataFrame(query_results)

# Always inspect before analyzing
print(df.head())
print(df.dtypes)
print(df.isnull().sum())
```

### Step 5: Generate Visualizations
```python
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(df['category'], df['value'])
ax.set_title('Chart Title')
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
plt.tight_layout()  # Always call this to prevent label cut-off
plt.savefig('output/chart_name.png', dpi=150, bbox_inches='tight')
plt.close()
```

### Step 6: Save Output to output/
- Save all charts to output/ folder
- Save the written report to output/ as a .md file
- Name files with date: output/2026-02-26-analysis-name.md

## Example
Input: "What is the week-over-week retention of users who signed up in January?"
Output: A cohort retention table + line graph saved to output/

## Common Mistakes
- **Guessing column names**: Always read schema first. Use information_schema.
- **plt.tight_layout() missing**: Labels and titles get cut off in saved images.
- **Not filtering deleted records**: Many tables have soft deletes (deleted_at column).
- **Wrong date grouping**: Use DATE_TRUNC('week', created_at) for weekly cohorts.
- **Forgetting data source in report**: Always state which table/date range was queried.

## Notes
- For large datasets, add LIMIT 10000 during exploration, remove for final analysis
- Save all intermediate learnings to memory.md
