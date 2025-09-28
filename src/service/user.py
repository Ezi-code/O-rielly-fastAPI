"""user services module."""

from datetime import datetime, timedelta
from jose import jwt
from model.user import User
from passlib.context import CryptContext
from data import user as data

SECRET_KEY = "somerandomekeytokeepthingssafe"
ALGORITHM = "HS456"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain: str, hash: str) -> bool:
    """hash plain and compare it with hash from the database."""

    return pwd_context.verify(plain, hash)


def get_hash(plain: str):
    return pwd_context.hash(plain)


def get_jwt_username(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if not (username := payload.get("sub")):
            return None
    except jwt.JWTError:
        return None
    return username


def get_current_user(token: str):
    """decode an oauth access token and return the user."""

    if not (username := get_jwt_username(token)):
        return None
    if user := lookup_user(username):
        return user
    return None


def lookup_user(username: str):
    """return a matching user from the database."""
    if user := data.get_one(username):
        return user
    return None


def auth_user(name: str, plain: str):
    if not (user := lookup_user(name)):
        return None
    if not verify_password(plain, user.hash):
        return None
    return user


def create_access_token(data: dict, expires: timedelta | None = None):
    """Return a JWT access token"""
    src = data.copy()
    now = datetime.now()
    if not expires:
        expires = timedelta(minutes=15)
    src.update({"exp": now + expires})
    encoded_jwt = jwt.encode(src, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# --- CRUD passthrough stuff


def get_all() -> list[User]:
    return data.get_all()


def get_one(name) -> User:
    return data.get_one(name)


def create(user: User) -> User:
    return data.create(user)


def modify(name: str, user: User) -> User:
    return data.modify(name, user)


def delete(name: str) -> None:
    return data.delete(name)
