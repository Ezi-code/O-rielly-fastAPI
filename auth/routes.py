from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from auth.oauth import oauth
from users.models import User
from users.schemas import UserOut, Token, LoginResponse
from users.security import create_access_token
from users.resources import save_session

router = APIRouter(tags=["auth"], prefix="/auth")


@router.get("/google/login")
async def google_login(request: Request):
    # state + PKCE handled by Authlib; it stores transient data in session.
    redirect_uri = request.url_for("google_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/google/callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)
        userinfo = token.get("userinfo")
        if not userinfo:
            # For some providers userinfo comes from a separate call
            userinfo = await oauth.google.parse_id_token(request, token)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"OAuth error: {e}")

    # Extract standard OIDC claims
    sub = userinfo.get("sub")
    email = userinfo.get("email")
    name = userinfo.get("name") or (email.split("@")[0] if email else None)
    if not sub or not email:
        raise HTTPException(
            status_code=400, detail="Missing required profile information from provider"
        )

    # Find or create local user (by email or by provider-sub)
    user = db.query(User).filter(User.email == email).first()
    if not user:
        # You may want to extend your User model to store provider + provider_sub
        user = User(
            username=name,
            email=email,
            hashed_password="",  # Not used for OAuth users; or store a random hash.
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    # Issue your app token + session
    access_token, jti, exp = create_access_token(data={"sub": str(user.id)})
    save_session(db, jti=jti, user_id=user.id, expires_at=exp)

    # Option A: return JSON (SPA/mobile)
    token_out = Token(access_token=access_token)
    user_out = UserOut.model_validate(user)
    return LoginResponse(token=token_out, user=user_out)

    # Option B: set HttpOnly cookie and redirect (uncomment and adapt):
    # response = RedirectResponse(url="/")
    # response.set_cookie(
    #     key="access_token",
    #     value=access_token,
    #     httponly=True,
    #     secure=True,
    #     samesite="lax",
    # )
    # return response
