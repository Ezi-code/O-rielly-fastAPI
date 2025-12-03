from fastapi import APIRouter, Depends, HTTPException, status, Response

from users.models import User
from users.resources import save_session, revoke_session
from users.schemas import UserCreate, UserOut, LoginRequest, Token, LoginResponse
from database import get_db
from sqlalchemy.orm import Session
from users.security import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user_payload,
)

router = APIRouter(tags=["users"], prefix="/users")


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate, db: Session = Depends(get_db)):
    user = User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=hash_password(user_in.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
async def login(body: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == body.username).first()
    print(user.username)
    if not user or not verify_password(body.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token, jti, exp = create_access_token(data={"sub": str(user.id)})
    save_session(db, jti=jti, user_id=user.id, expires_at=exp)

    token = Token(access_token=access_token)
    user_out = UserOut.model_validate(user)
    return LoginResponse(token=token, user=user_out)


@router.post("/token", response_model=Token, status_code=status.HTTP_200_OK)
async def login_for_access_token(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request.username).first()

    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token, _, _ = create_access_token(data={"sub": user.username})

    return Token(access_token=access_token)


@router.get("/me", status_code=status.HTTP_200_OK)
async def me(payload=Depends(get_current_user_payload)):
    return {"sub": payload["sub"], "jti": payload["jti"]}


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout_refresh(
    request=Depends(get_current_user_payload), db: Session = Depends(get_db)
):
    jti = request.get("jti")
    if not jti:
        raise HTTPException(status_code=400, detail="JTI required")
    revoke_session(db, jti=jti)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
