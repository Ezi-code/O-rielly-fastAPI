"""user resources."""

from sqlalchemy.orm import Session
from datetime import datetime, timezone
from users.models import UserSession


class AuthManager:
    """user authentication manager."""

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password


def save_session(db: Session, *, jti: str, user_id: str, expires_at: datetime) -> None:
    db.add(UserSession(jti=jti, user_id=user_id, expires_at=expires_at))
    db.commit()


def revoke_session(db: Session, jti: str) -> None:
    row = db.query(UserSession).filter(UserSession.jti == jti).first()
    if row and not row.revoked:
        row.revoked = True
        db.add(row)
        db.commit()


def is_session_active(db: Session, jti: str) -> bool:
    row = db.query(UserSession).filter(UserSession.jti == jti).first()
    if not row:
        return False
    if row.expires_at < datetime.now(timezone.utc):
        return False
    return not row.revoked
