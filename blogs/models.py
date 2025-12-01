"""bllog api models."""

from datetime import datetime

from sqlalchemy import Integer, Column, String, DateTime
from database import BASE


class Post(BASE):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    content = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self) -> str:
        return f"<Post: {self.title}>"
