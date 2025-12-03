from datetime import datetime

from pydantic import BaseModel, UUID4


class BasePost(BaseModel):
    title: str
    content: str


class Post(BasePost):
    """Post model."""

    id: UUID4
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    model_config = {"from_attributes": True}


class PostCreate(BasePost):
    pass
