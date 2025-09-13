"""creature data models."""

from pydantic import BaseModel


class Creature(BaseModel):
    """creature base model."""

    name: str
    country: str
    area: str
    description: str
    aka: str
