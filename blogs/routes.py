"""blog routes."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .schemas import Post, PostCreate
from fastapi import status
from database import get_db
from blogs import models

router = APIRouter(tags=["blogs"], prefix="/blogs")

post_list = []


@router.get("/", dependencies=[Depends(get_db)], response_model=List[Post])
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Post)
async def create_post(post: PostCreate, db: Session = Depends(get_db)):
    db_post = models.Post(title=post.title, content=post.content)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


@router.get("/{id}", response_model=Post)
async def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return post


@router.patch("/{id}", dependencies=[Depends(get_db)], response_model=Post)
async def update_post(id: int, post: PostCreate, db: Session = Depends(get_db)):
    _update = db.query(models.Post).filter(models.Post.id == id).first()
    _update.title = post.title
    _update.content = post.content
    db.add(_update)
    db.commit()
    db.refresh(_update)
    return _update
