"""user model."""

import uuid

from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from database import BASE


class User(BASE):
    """User model."""

    __tablename__ = "user"
    id = Column(
        UUID, primary_key=True, nullable=False, default=lambda: str(uuid.uuid4())
    )
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"


class UserSession(BASE):
    __tablename__ = "user_session"
    id = Column(UUID, primary_key=True, nullable=False, default=lambda: str(uuid.uuid4()))
    jti = Column(String(36), primary_key=True, nullable=False)
    user_id = Column(UUID, ForeignKey("user.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    revoked = Column(Boolean, default=False, nullable=False)
