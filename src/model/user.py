"""user model."""

from pydantic import BaseModel


class User(BaseModel):
    """user model."""

    name: str
    hash: str
