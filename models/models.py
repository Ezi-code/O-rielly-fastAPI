from datetime import datetime
from pydantic import BaseModel


class TagIn(BaseModel):
    tag: str


class Tag(BaseModel):
    tag: str
    created: datetime
    secrete: str


class TagOut(BaseModel):
    tag: str
    created: datetime


def create(tag):
    tag: Tag = Tag(tag=tag.tag, created=datetime.now(), secrete="secret")
    return tag


def get(tag):
    tag_out: TagOut = TagOut(tag=tag, created=datetime.now())
    return tag_out


class Creature(BaseModel):
    name: str
    country: str
    area: str
    description: str
    aka: str
