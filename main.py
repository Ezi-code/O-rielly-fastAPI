"""fastapi main app."""

import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from database import init_db
from contextlib import asynccontextmanager
from blogs import routes as blog_routes
from users import routes as user_routes
from auth import routes as auth_routes
import os

from starlette.middleware.sessions import SessionMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
)
app.add_middleware(
    SessionMiddleware, secret_key=os.environ.get("APP_SECRET_KEY", "change-me")
)


router = APIRouter()
router.include_router(blog_routes.router)
router.include_router(user_routes.router)
app.include_router(router)
app.include_router(auth_routes.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
