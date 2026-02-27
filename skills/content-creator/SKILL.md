---
name: content-creator
description: >
  Creates a new blog post on JSONPlaceholder and previews it with simulated engagement data.
  Use when you want to draft a post, assign it to an author, and see what the published result
  would look like including the API response.
compatibility: Requires @nimblebraininc/jsonplaceholder MCP server
metadata:
  tags:
    - create
    - content
    - jsonplaceholder
  category: writing
  triggers:
    - "create a blog post"
    - "write a new post"
    - "draft a post for user"
    - "publish content"
  keywords:
    - post
    - create
    - blog
    - content
    - author
    - write
  version: "0.1.0"
  surfaces:
    - claude-code
    - claude-ai
  author:
    name: NimbleBrain Inc
  examples:
    - prompt: "Create a blog post about AI for user 3"
    - prompt: "Write a post titled 'Hello World' and assign it to user 1"
---

# Content Creator

Draft and create a new blog post on JSONPlaceholder.

## Steps

1. **Identify the author**: If a user ID is provided, use `get_user` to fetch their profile. If not, use `list_users` to show available authors and ask the user to pick one.
2. **Draft the post**: Based on the user's topic/instructions, compose a title and body.
3. **Create the post** using `create_post` with the title, body, and user_id.
4. **Fetch the author's other posts** using `list_posts` filtered by user_id for context.
5. **Present the result** in the output format below.

## Output Format

```markdown
# New Post Created

## Post Details
- **ID**: {response.id}
- **Title**: {title}
- **Author**: {user.name} (@{user.username})

## Content
{body}

## Author Context
{user.name} has {post_count} other posts on the platform.

---
*Note: JSONPlaceholder simulates creation — the post is not actually persisted.*
```

## Notes

- JSONPlaceholder returns `id: 101` for all created posts (simulated)
- The post body and title can be anything — no validation constraints
- User IDs 1-10 are valid authors
