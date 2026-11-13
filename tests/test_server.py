"""Tests for JSONPlaceholder MCP Server tools."""

from unittest.mock import AsyncMock, patch

import pytest
from fastmcp import Client
from fastmcp.exceptions import ToolError

from mcp_jsonplaceholder.api_client import JSONPlaceholderAPIError


@pytest.fixture
def mock_client():
    """Create a mock API client."""
    client = AsyncMock()
    client.list_posts = AsyncMock(
        return_value=[
            {"id": 1, "userId": 1, "title": "Post 1", "body": "Body 1"},
            {"id": 2, "userId": 1, "title": "Post 2", "body": "Body 2"},
        ]
    )
    client.get_post = AsyncMock(
        return_value={"id": 1, "userId": 1, "title": "Post 1", "body": "Body 1"}
    )
    client.create_post = AsyncMock(
        return_value={"id": 101, "userId": 1, "title": "New Post", "body": "New Body"}
    )
    client.update_post = AsyncMock(
        return_value={"id": 1, "userId": 1, "title": "Updated", "body": "Body 1"}
    )
    client.delete_post = AsyncMock(return_value={})
    client.list_comments = AsyncMock(
        return_value=[{"id": 1, "postId": 1, "name": "Comment", "email": "a@b.com", "body": "c"}]
    )
    client.get_post_comments = AsyncMock(
        return_value=[{"id": 1, "postId": 1, "name": "Comment", "email": "a@b.com", "body": "c"}]
    )
    client.list_albums = AsyncMock(return_value=[{"id": 1, "userId": 1, "title": "Album 1"}])
    client.get_album_photos = AsyncMock(
        return_value=[
            {
                "id": 1,
                "albumId": 1,
                "title": "Photo",
                "url": "https://example.com/1",
                "thumbnailUrl": "https://example.com/1/thumb",
            }
        ]
    )
    client.list_photos = AsyncMock(
        return_value=[
            {
                "id": 1,
                "albumId": 1,
                "title": "Photo",
                "url": "https://example.com/1",
                "thumbnailUrl": "https://example.com/1/thumb",
            }
        ]
    )
    client.get_photo = AsyncMock(
        return_value={
            "id": 1,
            "albumId": 1,
            "title": "Photo",
            "url": "https://example.com/1",
            "thumbnailUrl": "https://example.com/1/thumb",
        }
    )
    client.list_todos = AsyncMock(
        return_value=[{"id": 1, "userId": 1, "title": "Todo 1", "completed": False}]
    )
    client.get_todo = AsyncMock(
        return_value={"id": 1, "userId": 1, "title": "Todo 1", "completed": False}
    )
    client.get_user_todos = AsyncMock(
        return_value=[{"id": 1, "userId": 1, "title": "Todo 1", "completed": False}]
    )
    client.list_users = AsyncMock(
        return_value=[{"id": 1, "name": "Leanne Graham", "username": "Bret"}]
    )
    client.get_user = AsyncMock(return_value={"id": 1, "name": "Leanne Graham", "username": "Bret"})
    return client


# ============================================================================
# Posts
# ============================================================================


@pytest.mark.asyncio
async def test_list_posts(mock_client):
    """Test list_posts tool."""
    with patch("mcp_jsonplaceholder.server.get_client", return_value=mock_client):
        from mcp_jsonplaceholder.server import list_posts

        result = await list_posts()
        assert len(result) == 2
        mock_client.list_posts.assert_called_once_with(user_id=None)


@pytest.mark.asyncio
async def test_list_posts_filtered(mock_client):
    """Test list_posts with user_id filter."""
    with patch("mcp_jsonplaceholder.server.get_client", return_value=mock_client):
        from mcp_jsonplaceholder.server import list_posts

        await list_posts(user_id=1)
        mock_client.list_posts.assert_called_once_with(user_id=1)


@pytest.mark.asyncio
async def test_get_post(mock_client):
    """Test get_post tool."""
    with patch("mcp_jsonplaceholder.server.get_client", return_value=mock_client):
        from mcp_jsonplaceholder.server import get_post

        result = await get_post(post_id=1)
        assert result["id"] == 1
        mock_client.get_post.assert_called_once_with(1)


@pytest.mark.asyncio
async def test_create_post(mock_client):
    """Test create_post tool."""
    with patch("mcp_jsonplaceholder.server.get_client", return_value=mock_client):
        from mcp_jsonplaceholder.server import create_post

        result = await create_post(title="New Post", body="New Body", user_id=1)
        assert result["id"] == 101
        mock_client.create_post.assert_called_once_with(
            title="New Post", body="New Body", user_id=1
        )


@pytest.mark.asyncio
async def test_update_post(mock_client):
    """Test update_post tool."""
    with patch("mcp_jsonplaceholder.server.get_client", return_value=mock_client):
        from mcp_jsonplaceholder.server import update_post

        result = await update_post(post_id=1, title="Updated")
        assert result["title"] == "Updated"
        mock_client.update_post.assert_called_once_with(1, title="Updated", body=None, user_id=None)


@pytest.mark.asyncio
async def test_delete_post(mock_client):
    """Test delete_post tool."""
    with patch("mcp_jsonplaceholder.server.get_client", return_value=mock_client):
        from mcp_jsonplaceholder.server import delete_post

        result = await delete_post(post_id=1)
        assert result == {}
        mock_client.delete_post.assert_called_once_with(1)


# ============================================================================
# Comments
# ============================================================================


@pytest.mark.asyncio
async def test_list_comments(mock_client):
    """Test list_comments tool."""
    with patch("mcp_jsonplaceholder.server.get_client", return_value=mock_client):
        from mcp_jsonplaceholder.server import list_comments

        result = await list_comments(post_id=1)
        assert len(result) == 1
        mock_client.list_comments.assert_called_once_with(post_id=1)


@pytest.mark.asyncio
async def test_get_post_comments(mock_client):
    """Test get_post_comments tool."""
    with patch("mcp_jsonplaceholder.server.get_client", return_value=mock_client):
        from mcp_jsonplaceholder.server import get_post_comments

        result = await get_post_comments(post_id=1)
        assert len(result) == 1
        mock_client.get_post_comments.assert_called_once_with(1)


# ============================================================================
# Albums & Photos
# ============================================================================


@pytest.mark.asyncio
async def test_list_albums(mock_client):
    """Test list_albums tool."""
    with patch("mcp_jsonplaceholder.server.get_client", return_value=mock_client):
        from mcp_jsonplaceholder.server import list_albums

        result = await list_albums()
        assert len(result) == 1
        mock_client.list_albums.assert_called_once_with(user_id=None)


@pytest.mark.asyncio
async def test_get_album_photos(mock_client):
    """Test get_album_photos tool."""
    with patch("mcp_jsonplaceholder.server.get_client", return_value=mock_client):
        from mcp_jsonplaceholder.server import get_album_photos

        result = await get_album_photos(album_id=1)
        assert len(result) == 1
        mock_client.get_album_photos.assert_called_once_with(1)


@pytest.mark.asyncio
async def test_list_photos(mock_client):
    """Test list_photos tool."""
    with patch("mcp_jsonplaceholder.server.get_client", return_value=mock_client):
        from mcp_jsonplaceholder.server import list_photos

        result = await list_photos()
        assert len(result) == 1
        mock_client.list_photos.assert_called_once_with(album_id=None)


@pytest.mark.asyncio
async def test_get_photo(mock_client):
    """Test get_photo tool."""
    with patch("mcp_jsonplaceholder.server.get_client", return_value=mock_client):
        from mcp_jsonplaceholder.server import get_photo

        result = await get_photo(photo_id=1)
        assert result["id"] == 1
        mock_client.get_photo.assert_called_once_with(1)


# ============================================================================
# Todos
# ============================================================================


@pytest.mark.asyncio
async def test_list_todos(mock_client):
    """Test list_todos tool."""
    with patch("mcp_jsonplaceholder.server.get_client", return_value=mock_client):
        from mcp_jsonplaceholder.server import list_todos

        result = await list_todos()
        assert len(result) == 1
        mock_client.list_todos.assert_called_once_with(user_id=None, completed=None)


@pytest.mark.asyncio
async def test_get_todo(mock_client):
    """Test get_todo tool."""
    with patch("mcp_jsonplaceholder.server.get_client", return_value=mock_client):
        from mcp_jsonplaceholder.server import get_todo

        result = await get_todo(todo_id=1)
        assert result["id"] == 1
        mock_client.get_todo.assert_called_once_with(1)


@pytest.mark.asyncio
async def test_get_user_todos(mock_client):
    """Test get_user_todos tool."""
    with patch("mcp_jsonplaceholder.server.get_client", return_value=mock_client):
        from mcp_jsonplaceholder.server import get_user_todos

        result = await get_user_todos(user_id=1)
        assert len(result) == 1
        mock_client.get_user_todos.assert_called_once_with(1)


# ============================================================================
# Users
# ============================================================================


@pytest.mark.asyncio
async def test_list_users(mock_client):
    """Test list_users tool."""
    with patch("mcp_jsonplaceholder.server.get_client", return_value=mock_client):
        from mcp_jsonplaceholder.server import list_users

        result = await list_users()
        assert len(result) == 1
        mock_client.list_users.assert_called_once()


@pytest.mark.asyncio
async def test_get_user(mock_client):
    """Test get_user tool."""
    with patch("mcp_jsonplaceholder.server.get_client", return_value=mock_client):
        from mcp_jsonplaceholder.server import get_user

        result = await get_user(user_id=1)
        assert result["id"] == 1
        mock_client.get_user.assert_called_once_with(1)


# ============================================================================
# Error handling
# ============================================================================


@pytest.mark.asyncio
async def test_api_error_is_a_tool_error(mock_client):
    """An API error reaches the caller as a ToolError carrying its message."""
    mock_client.list_posts = AsyncMock(side_effect=JSONPlaceholderAPIError(404, "Not found"))
    with patch("mcp_jsonplaceholder.server.get_client", return_value=mock_client):
        from mcp_jsonplaceholder.server import list_posts

        with pytest.raises(ToolError, match="Not found"):
            await list_posts()


@pytest.mark.asyncio
async def test_api_error_reaches_an_mcp_client_as_an_error_result(mock_client):
    """Through the protocol, the failure is an error result, with no client log message."""
    mock_client.list_posts = AsyncMock(side_effect=JSONPlaceholderAPIError(404, "Not found"))
    with patch("mcp_jsonplaceholder.server.get_client", return_value=mock_client):
        from mcp_jsonplaceholder.server import mcp

        async with Client(mcp) as client:
            with pytest.raises(ToolError, match="Not found"):
                await client.call_tool("list_posts", {})
