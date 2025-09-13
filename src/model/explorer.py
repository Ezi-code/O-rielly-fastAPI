from pydantic import BaseModel


class Explorer(BaseModel):
    """explorer base model."""

    name: str
    country: str
    description: str
