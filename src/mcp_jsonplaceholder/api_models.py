"""Pydantic models for JSONPlaceholder API responses."""

from pydantic import BaseModel, Field

# ============================================================================
# Resource Models
# ============================================================================


class Post(BaseModel):
    """A blog post."""

    id: int = Field(..., description="Post ID")
    user_id: int = Field(..., alias="userId", description="Author user ID")
    title: str = Field(..., description="Post title")
    body: str = Field(..., description="Post body")


class Comment(BaseModel):
    """A comment on a post."""

    id: int = Field(..., description="Comment ID")
    post_id: int = Field(..., alias="postId", description="Parent post ID")
    name: str = Field(..., description="Comment name/subject")
    email: str = Field(..., description="Commenter email")
    body: str = Field(..., description="Comment body")


class Album(BaseModel):
    """A photo album."""

    id: int = Field(..., description="Album ID")
    user_id: int = Field(..., alias="userId", description="Owner user ID")
    title: str = Field(..., description="Album title")


class Photo(BaseModel):
    """A photo in an album."""

    id: int = Field(..., description="Photo ID")
    album_id: int = Field(..., alias="albumId", description="Parent album ID")
    title: str = Field(..., description="Photo title")
    url: str = Field(..., description="Full-size photo URL")
    thumbnail_url: str = Field(..., alias="thumbnailUrl", description="Thumbnail URL")


class Todo(BaseModel):
    """A todo item."""

    id: int = Field(..., description="Todo ID")
    user_id: int = Field(..., alias="userId", description="Owner user ID")
    title: str = Field(..., description="Todo title")
    completed: bool = Field(..., description="Whether the todo is completed")


class Geo(BaseModel):
    """Geographic coordinates."""

    lat: str = Field(..., description="Latitude")
    lng: str = Field(..., description="Longitude")


class Address(BaseModel):
    """A user's address."""

    street: str = Field(..., description="Street name")
    suite: str = Field(..., description="Suite/apartment")
    city: str = Field(..., description="City")
    zipcode: str = Field(..., description="Zip code")
    geo: Geo = Field(..., description="Geographic coordinates")


class Company(BaseModel):
    """A user's company."""

    name: str = Field(..., description="Company name")
    catch_phrase: str = Field(..., alias="catchPhrase", description="Company catch phrase")
    bs: str = Field(..., description="Company business description")


class User(BaseModel):
    """A user."""

    id: int = Field(..., description="User ID")
    name: str = Field(..., description="Full name")
    username: str = Field(..., description="Username")
    email: str = Field(..., description="Email address")
    address: Address = Field(..., description="Address")
    phone: str = Field(..., description="Phone number")
    website: str = Field(..., description="Website URL")
    company: Company = Field(..., description="Company info")
