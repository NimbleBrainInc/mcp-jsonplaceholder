---
name: user-activity-digest
description: >
  Generates a comprehensive activity digest for a JSONPlaceholder user by aggregating their posts,
  comments, and todo status. Use when you need a summary of what a specific user has been doing,
  including their content output and task completion rate.
compatibility: Requires @nimblebraininc/jsonplaceholder MCP server
metadata:
  tags:
    - digest
    - summary
    - jsonplaceholder
  category: data
  triggers:
    - "summarize user activity"
    - "user digest"
    - "what has user X been doing"
    - "activity report for user"
  keywords:
    - user
    - activity
    - digest
    - summary
    - posts
    - todos
  version: "0.1.0"
  surfaces:
    - claude-code
    - claude-ai
  author:
    name: NimbleBrain Inc
  examples:
    - prompt: "Give me an activity digest for user 1"
    - prompt: "Summarize what user 5 has been up to"
---

# User Activity Digest

Generate a comprehensive activity summary for a JSONPlaceholder user.

## Steps

1. **Fetch user profile** using `get_user` with the specified user ID
2. **Fetch user's posts** using `list_posts` filtered by user ID
3. **Fetch user's todos** using `get_user_todos` with the user ID
4. **For each post**, fetch comments using `get_post_comments`
5. **Compile the digest** with the following sections:

## Output Format

```markdown
# Activity Digest: {user.name} (@{user.username})

## Profile
- Email: {email}
- Company: {company.name}
- Website: {website}

## Posts ({count})
For each post:
- **{title}** — {comment_count} comments

## Todos
- Completed: {completed_count}/{total_count} ({percentage}%)
- Pending items: {list of incomplete todo titles}

## Summary
Brief narrative summary of the user's activity level.
```

## Notes

- JSONPlaceholder has 10 users (IDs 1-10)
- Each user has ~10 posts and ~20 todos
- All data is static/fake — useful for testing and demos
