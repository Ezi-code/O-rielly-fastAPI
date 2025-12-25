from datetime import datetime

from pydantic import BaseModel, UUID4, Field


class BasePost(BaseModel):
    """Base post model."""

    title: str = Field(max_length=100)
    content: str


class Post(BasePost):
    """Post model."""

    id: UUID4
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    model_config = {"from_attributes": True}


class PostCreate(BasePost):
    """Post create model."""
