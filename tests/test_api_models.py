"""Tests for JSONPlaceholder API models."""

from mcp_jsonplaceholder.api_models import (
    Address,
    Album,
    Comment,
    Company,
    Geo,
    Photo,
    Post,
    Todo,
    User,
)


def test_post_model() -> None:
    """Test Post model parsing from API response."""
    data = {"id": 1, "userId": 5, "title": "Test Post", "body": "Post body content"}
    post = Post(**data)
    assert post.id == 1
    assert post.user_id == 5
    assert post.title == "Test Post"
    assert post.body == "Post body content"


def test_comment_model() -> None:
    """Test Comment model parsing."""
    data = {
        "id": 1,
        "postId": 1,
        "name": "Comment subject",
        "email": "user@example.com",
        "body": "Comment body",
    }
    comment = Comment(**data)
    assert comment.id == 1
    assert comment.post_id == 1
    assert comment.email == "user@example.com"


def test_album_model() -> None:
    """Test Album model parsing."""
    data = {"id": 1, "userId": 1, "title": "My Album"}
    album = Album(**data)
    assert album.id == 1
    assert album.user_id == 1
    assert album.title == "My Album"


def test_photo_model() -> None:
    """Test Photo model parsing."""
    data = {
        "id": 1,
        "albumId": 1,
        "title": "Photo title",
        "url": "https://via.placeholder.com/600/92c952",
        "thumbnailUrl": "https://via.placeholder.com/150/92c952",
    }
    photo = Photo(**data)
    assert photo.id == 1
    assert photo.album_id == 1
    assert photo.thumbnail_url == "https://via.placeholder.com/150/92c952"


def test_todo_model() -> None:
    """Test Todo model parsing."""
    data = {"id": 1, "userId": 1, "title": "Buy groceries", "completed": False}
    todo = Todo(**data)
    assert todo.id == 1
    assert todo.user_id == 1
    assert todo.completed is False


def test_user_model() -> None:
    """Test User model parsing with nested Address and Company."""
    data = {
        "id": 1,
        "name": "Leanne Graham",
        "username": "Bret",
        "email": "Sincere@april.biz",
        "address": {
            "street": "Kulas Light",
            "suite": "Apt. 556",
            "city": "Gwenborough",
            "zipcode": "92998-3874",
            "geo": {"lat": "-37.3159", "lng": "81.1496"},
        },
        "phone": "1-770-736-8031 x56442",
        "website": "hildegard.org",
        "company": {
            "name": "Romaguera-Crona",
            "catchPhrase": "Multi-layered client-server neural-net",
            "bs": "harness real-time e-markets",
        },
    }
    user = User(**data)
    assert user.id == 1
    assert user.name == "Leanne Graham"
    assert user.username == "Bret"
    assert isinstance(user.address, Address)
    assert isinstance(user.address.geo, Geo)
    assert user.address.geo.lat == "-37.3159"
    assert isinstance(user.company, Company)
    assert user.company.catch_phrase == "Multi-layered client-server neural-net"
