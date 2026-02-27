"""Async HTTP client for JSONPlaceholder API."""

from typing import Any

import aiohttp
from aiohttp import ClientError


class JSONPlaceholderAPIError(Exception):
    """Exception raised for JSONPlaceholder API errors."""

    def __init__(self, status: int, message: str) -> None:
        self.status = status
        self.message = message
        super().__init__(f"JSONPlaceholder API Error {status}: {message}")


class JSONPlaceholderClient:
    """Async client for JSONPlaceholder API."""

    BASE_URL = "https://jsonplaceholder.typicode.com"

    def __init__(self, timeout: float = 30.0) -> None:
        self.timeout = timeout
        self._session: aiohttp.ClientSession | None = None

    async def __aenter__(self) -> "JSONPlaceholderClient":
        await self._ensure_session()
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        await self.close()

    async def _ensure_session(self) -> None:
        if not self._session:
            headers = {
                "User-Agent": "mcp-server-jsonplaceholder/0.1.0",
                "Accept": "application/json",
                "Content-Type": "application/json; charset=UTF-8",
            }
            self._session = aiohttp.ClientSession(
                headers=headers, timeout=aiohttp.ClientTimeout(total=self.timeout)
            )

    async def close(self) -> None:
        """Close the HTTP session."""
        if self._session:
            await self._session.close()
            self._session = None

    async def _request(
        self,
        method: str,
        path: str,
        params: dict[str, Any] | None = None,
        json_data: Any | None = None,
    ) -> Any:
        """Make an HTTP request to the JSONPlaceholder API."""
        await self._ensure_session()
        url = f"{self.BASE_URL}{path}"

        if params:
            params = {k: v for k, v in params.items() if v is not None}

        try:
            if not self._session:
                raise RuntimeError("Session not initialized")

            kwargs: dict[str, Any] = {}
            if json_data is not None:
                kwargs["json"] = json_data
            if params:
                kwargs["params"] = params

            async with self._session.request(method, url, **kwargs) as response:
                result = await response.json()

                if response.status >= 400:
                    error_msg = "Unknown error"
                    if isinstance(result, dict) and "message" in result:
                        error_msg = result["message"]
                    raise JSONPlaceholderAPIError(response.status, error_msg)

                return result

        except ClientError as e:
            raise JSONPlaceholderAPIError(500, f"Network error: {e!s}") from e

    # ========================================================================
    # Posts
    # ========================================================================

    async def list_posts(self, user_id: int | None = None) -> list[dict[str, Any]]:
        """List posts, optionally filtered by user ID."""
        params = {"userId": user_id} if user_id else None
        return await self._request("GET", "/posts", params=params)

    async def get_post(self, post_id: int) -> dict[str, Any]:
        """Get a single post by ID."""
        return await self._request("GET", f"/posts/{post_id}")

    async def create_post(self, title: str, body: str, user_id: int) -> dict[str, Any]:
        """Create a new post."""
        return await self._request(
            "POST", "/posts", json_data={"title": title, "body": body, "userId": user_id}
        )

    async def update_post(
        self,
        post_id: int,
        title: str | None = None,
        body: str | None = None,
        user_id: int | None = None,
    ) -> dict[str, Any]:
        """Update an existing post (partial update)."""
        data: dict[str, Any] = {}
        if title is not None:
            data["title"] = title
        if body is not None:
            data["body"] = body
        if user_id is not None:
            data["userId"] = user_id
        return await self._request("PATCH", f"/posts/{post_id}", json_data=data)

    async def delete_post(self, post_id: int) -> dict[str, Any]:
        """Delete a post by ID."""
        return await self._request("DELETE", f"/posts/{post_id}")

    # ========================================================================
    # Comments
    # ========================================================================

    async def list_comments(self, post_id: int | None = None) -> list[dict[str, Any]]:
        """List comments, optionally filtered by post ID."""
        params = {"postId": post_id} if post_id else None
        return await self._request("GET", "/comments", params=params)

    async def get_post_comments(self, post_id: int) -> list[dict[str, Any]]:
        """Get all comments for a specific post (nested route)."""
        return await self._request("GET", f"/posts/{post_id}/comments")

    # ========================================================================
    # Albums
    # ========================================================================

    async def list_albums(self, user_id: int | None = None) -> list[dict[str, Any]]:
        """List albums, optionally filtered by user ID."""
        params = {"userId": user_id} if user_id else None
        return await self._request("GET", "/albums", params=params)

    async def get_album_photos(self, album_id: int) -> list[dict[str, Any]]:
        """Get all photos in a specific album (nested route)."""
        return await self._request("GET", f"/albums/{album_id}/photos")

    # ========================================================================
    # Photos
    # ========================================================================

    async def list_photos(self, album_id: int | None = None) -> list[dict[str, Any]]:
        """List photos, optionally filtered by album ID."""
        params = {"albumId": album_id} if album_id else None
        return await self._request("GET", "/photos", params=params)

    async def get_photo(self, photo_id: int) -> dict[str, Any]:
        """Get a single photo by ID."""
        return await self._request("GET", f"/photos/{photo_id}")

    # ========================================================================
    # Todos
    # ========================================================================

    async def list_todos(
        self,
        user_id: int | None = None,
        completed: bool | None = None,
    ) -> list[dict[str, Any]]:
        """List todos, optionally filtered by user ID and/or completion status."""
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        if completed is not None:
            params["completed"] = str(completed).lower()
        return await self._request("GET", "/todos", params=params or None)

    async def get_todo(self, todo_id: int) -> dict[str, Any]:
        """Get a single todo by ID."""
        return await self._request("GET", f"/todos/{todo_id}")

    async def get_user_todos(self, user_id: int) -> list[dict[str, Any]]:
        """Get all todos for a specific user (nested route)."""
        return await self._request("GET", f"/users/{user_id}/todos")

    # ========================================================================
    # Users
    # ========================================================================

    async def list_users(self) -> list[dict[str, Any]]:
        """List all users."""
        return await self._request("GET", "/users")

    async def get_user(self, user_id: int) -> dict[str, Any]:
        """Get a single user by ID."""
        return await self._request("GET", f"/users/{user_id}")
