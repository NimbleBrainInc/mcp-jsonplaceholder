"""JSONPlaceholder MCP Server - FastMCP Implementation."""

import logging
import sys

from fastmcp import Context, FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse

from mcp_jsonplaceholder.api_client import JSONPlaceholderAPIError, JSONPlaceholderClient

# Logging setup - all logs to stderr (stdout is reserved for JSON-RPC)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("mcp_jsonplaceholder")

logger.info("JSONPlaceholder server module loading...")

# Create MCP server
mcp = FastMCP("JSONPlaceholder")

# Global client instance (lazy initialization)
_client: JSONPlaceholderClient | None = None


def get_client() -> JSONPlaceholderClient:
    """Get or create the API client instance."""
    global _client
    if _client is None:
        _client = JSONPlaceholderClient()
    return _client


# Health endpoint for HTTP transport
@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> JSONResponse:
    """Health check endpoint for monitoring."""
    return JSONResponse({"status": "healthy", "service": "mcp-jsonplaceholder"})


# ============================================================================
# Posts
# ============================================================================


@mcp.tool()
async def list_posts(
    user_id: int | None = None,
    ctx: Context | None = None,
) -> list[dict]:
    """List posts from JSONPlaceholder, optionally filtered by user ID.

    Args:
        user_id: Filter posts by this user ID
        ctx: MCP context for logging
    """
    client = get_client()
    try:
        return await client.list_posts(user_id=user_id)
    except JSONPlaceholderAPIError as e:
        if ctx:
            await ctx.error(f"API error: {e.message}")
        raise


@mcp.tool()
async def get_post(
    post_id: int,
    ctx: Context | None = None,
) -> dict:
    """Get a single post by ID.

    Args:
        post_id: The post ID (1-100)
        ctx: MCP context for logging
    """
    client = get_client()
    try:
        return await client.get_post(post_id)
    except JSONPlaceholderAPIError as e:
        if ctx:
            await ctx.error(f"API error: {e.message}")
        raise


@mcp.tool()
async def create_post(
    title: str,
    body: str,
    user_id: int,
    ctx: Context | None = None,
) -> dict:
    """Create a new post (simulated - not persisted on server).

    Args:
        title: Post title
        body: Post body content
        user_id: Author user ID
        ctx: MCP context for logging
    """
    client = get_client()
    try:
        return await client.create_post(title=title, body=body, user_id=user_id)
    except JSONPlaceholderAPIError as e:
        if ctx:
            await ctx.error(f"API error: {e.message}")
        raise


@mcp.tool()
async def update_post(
    post_id: int,
    title: str | None = None,
    body: str | None = None,
    user_id: int | None = None,
    ctx: Context | None = None,
) -> dict:
    """Update an existing post (simulated - not persisted on server).

    Args:
        post_id: The post ID to update
        title: New title (optional)
        body: New body content (optional)
        user_id: New author user ID (optional)
        ctx: MCP context for logging
    """
    client = get_client()
    try:
        return await client.update_post(post_id, title=title, body=body, user_id=user_id)
    except JSONPlaceholderAPIError as e:
        if ctx:
            await ctx.error(f"API error: {e.message}")
        raise


@mcp.tool()
async def delete_post(
    post_id: int,
    ctx: Context | None = None,
) -> dict:
    """Delete a post by ID (simulated - not persisted on server).

    Args:
        post_id: The post ID to delete
        ctx: MCP context for logging
    """
    client = get_client()
    try:
        return await client.delete_post(post_id)
    except JSONPlaceholderAPIError as e:
        if ctx:
            await ctx.error(f"API error: {e.message}")
        raise


# ============================================================================
# Comments
# ============================================================================


@mcp.tool()
async def list_comments(
    post_id: int | None = None,
    ctx: Context | None = None,
) -> list[dict]:
    """List comments, optionally filtered by post ID.

    Args:
        post_id: Filter comments by this post ID
        ctx: MCP context for logging
    """
    client = get_client()
    try:
        return await client.list_comments(post_id=post_id)
    except JSONPlaceholderAPIError as e:
        if ctx:
            await ctx.error(f"API error: {e.message}")
        raise


@mcp.tool()
async def get_post_comments(
    post_id: int,
    ctx: Context | None = None,
) -> list[dict]:
    """Get all comments for a specific post.

    Args:
        post_id: The post ID to get comments for
        ctx: MCP context for logging
    """
    client = get_client()
    try:
        return await client.get_post_comments(post_id)
    except JSONPlaceholderAPIError as e:
        if ctx:
            await ctx.error(f"API error: {e.message}")
        raise


# ============================================================================
# Albums
# ============================================================================


@mcp.tool()
async def list_albums(
    user_id: int | None = None,
    ctx: Context | None = None,
) -> list[dict]:
    """List albums, optionally filtered by user ID.

    Args:
        user_id: Filter albums by this user ID
        ctx: MCP context for logging
    """
    client = get_client()
    try:
        return await client.list_albums(user_id=user_id)
    except JSONPlaceholderAPIError as e:
        if ctx:
            await ctx.error(f"API error: {e.message}")
        raise


@mcp.tool()
async def get_album_photos(
    album_id: int,
    ctx: Context | None = None,
) -> list[dict]:
    """Get all photos in a specific album.

    Args:
        album_id: The album ID to get photos for
        ctx: MCP context for logging
    """
    client = get_client()
    try:
        return await client.get_album_photos(album_id)
    except JSONPlaceholderAPIError as e:
        if ctx:
            await ctx.error(f"API error: {e.message}")
        raise


# ============================================================================
# Photos
# ============================================================================


@mcp.tool()
async def list_photos(
    album_id: int | None = None,
    ctx: Context | None = None,
) -> list[dict]:
    """List photos, optionally filtered by album ID.

    Args:
        album_id: Filter photos by this album ID
        ctx: MCP context for logging
    """
    client = get_client()
    try:
        return await client.list_photos(album_id=album_id)
    except JSONPlaceholderAPIError as e:
        if ctx:
            await ctx.error(f"API error: {e.message}")
        raise


@mcp.tool()
async def get_photo(
    photo_id: int,
    ctx: Context | None = None,
) -> dict:
    """Get a single photo by ID.

    Args:
        photo_id: The photo ID
        ctx: MCP context for logging
    """
    client = get_client()
    try:
        return await client.get_photo(photo_id)
    except JSONPlaceholderAPIError as e:
        if ctx:
            await ctx.error(f"API error: {e.message}")
        raise


# ============================================================================
# Todos
# ============================================================================


@mcp.tool()
async def list_todos(
    user_id: int | None = None,
    completed: bool | None = None,
    ctx: Context | None = None,
) -> list[dict]:
    """List todos, optionally filtered by user ID and/or completion status.

    Args:
        user_id: Filter todos by this user ID
        completed: Filter by completion status (true/false)
        ctx: MCP context for logging
    """
    client = get_client()
    try:
        return await client.list_todos(user_id=user_id, completed=completed)
    except JSONPlaceholderAPIError as e:
        if ctx:
            await ctx.error(f"API error: {e.message}")
        raise


@mcp.tool()
async def get_todo(
    todo_id: int,
    ctx: Context | None = None,
) -> dict:
    """Get a single todo by ID.

    Args:
        todo_id: The todo ID
        ctx: MCP context for logging
    """
    client = get_client()
    try:
        return await client.get_todo(todo_id)
    except JSONPlaceholderAPIError as e:
        if ctx:
            await ctx.error(f"API error: {e.message}")
        raise


@mcp.tool()
async def get_user_todos(
    user_id: int,
    ctx: Context | None = None,
) -> list[dict]:
    """Get all todos for a specific user.

    Args:
        user_id: The user ID to get todos for
        ctx: MCP context for logging
    """
    client = get_client()
    try:
        return await client.get_user_todos(user_id)
    except JSONPlaceholderAPIError as e:
        if ctx:
            await ctx.error(f"API error: {e.message}")
        raise


# ============================================================================
# Users
# ============================================================================


@mcp.tool()
async def list_users(
    ctx: Context | None = None,
) -> list[dict]:
    """List all users.

    Args:
        ctx: MCP context for logging
    """
    client = get_client()
    try:
        return await client.list_users()
    except JSONPlaceholderAPIError as e:
        if ctx:
            await ctx.error(f"API error: {e.message}")
        raise


@mcp.tool()
async def get_user(
    user_id: int,
    ctx: Context | None = None,
) -> dict:
    """Get a single user by ID.

    Args:
        user_id: The user ID (1-10)
        ctx: MCP context for logging
    """
    client = get_client()
    try:
        return await client.get_user(user_id)
    except JSONPlaceholderAPIError as e:
        if ctx:
            await ctx.error(f"API error: {e.message}")
        raise


# ============================================================================
# Entrypoints
# ============================================================================

# ASGI app for HTTP deployment (uvicorn mcp_jsonplaceholder.server:app)
app = mcp.http_app()

# Stdio entrypoint for Claude Desktop / mpak
if __name__ == "__main__":
    logger.info("Running in stdio mode")
    mcp.run()
