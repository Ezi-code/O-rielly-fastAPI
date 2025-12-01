import uuid

from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from users.resources import is_session_active

pwd_conext = CryptContext(schemes=["argon2"], deprecated="auto")

ACCESS_TOKEN_EXPIRE_MINUTES = 30
ALGORITHM = "HS256"
SECRET_KEY = "randomesecrete"


def hash_password(password):
    return pwd_conext.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_conext.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    jti = str(uuid.uuid4())
    now = datetime.now()
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update(
        {
            "iat": now,
            "nbf": now,
            "exp": expire,
            "jti": jti,
        }
    )
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt, jti, expire


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token/")


def decode_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


def get_current_user_payload(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> dict:
    try:
        payload = decode_token(token)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    jti = payload.get("jti")
    if not jti or not is_session_active(db, jti):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is revoked or inactive",
        )
    return payload  # you can also look up the user h
