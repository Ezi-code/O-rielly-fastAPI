"""bllog api models."""

from datetime import datetime

from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from database import BASE
import uuid


class Post(BASE):
    __tablename__ = "post"
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    content = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self) -> str:
        return f"<Post: {self.title}>"
