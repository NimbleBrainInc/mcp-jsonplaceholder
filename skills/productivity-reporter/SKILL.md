---
name: productivity-reporter
description: >
  Generates a productivity report across all JSONPlaceholder users showing todo completion rates,
  rankings, and pending work. Use when you need to compare productivity across users or identify
  who has the most incomplete tasks.
compatibility: Requires @nimblebraininc/jsonplaceholder MCP server
metadata:
  tags:
    - report
    - productivity
    - jsonplaceholder
  category: data
  triggers:
    - "productivity report"
    - "todo completion rates"
    - "who has the most incomplete todos"
    - "compare user productivity"
  keywords:
    - productivity
    - todos
    - completion
    - report
    - ranking
    - status
  version: "0.1.0"
  surfaces:
    - claude-code
    - claude-ai
  author:
    name: NimbleBrain Inc
  examples:
    - prompt: "Generate a productivity report for all users"
    - prompt: "Who has the best todo completion rate?"
---

# Productivity Reporter

Generate a cross-user productivity report based on todo completion data.

## Steps

1. **Fetch all users** using `list_users`
2. **For each user**, fetch their todos using `get_user_todos`
3. **Calculate metrics** for each user:
   - Total todos
   - Completed count
   - Completion rate (percentage)
   - List of pending items
4. **Rank users** by completion rate (highest first)
5. **Present the report** in the output format below

## Output Format

```markdown
# Productivity Report

## Rankings

| Rank | User | Completed | Total | Rate |
|------|------|-----------|-------|------|
| 1 | {name} | {done} | {total} | {rate}% |
| ... | ... | ... | ... | ... |

## Overall Stats
- Total todos across all users: {total}
- Overall completion rate: {rate}%
- Most productive: {top_user}
- Needs attention: {bottom_user}

## Pending Items by User
### {user.name} ({pending_count} pending)
- {todo_title_1}
- {todo_title_2}
...
```

## Notes

- JSONPlaceholder has exactly 10 users with 20 todos each (200 total)
- Todo completion status is static — the same report is generated each time
- Useful for demonstrating report-generation workflows
