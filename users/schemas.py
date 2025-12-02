from pydantic import BaseModel, UUID4


class UserOut(BaseModel):
    id: UUID4
    username: str
    email: str

    model_config = {
        "from_attributes": True,
    }


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginResponse(BaseModel):
    token: Token
    user: UserOut
