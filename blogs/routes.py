"""blog routes."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import ValidationError
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from users.security import get_current_user_payload
from .schemas import Post, PostCreate
from fastapi import status
from database import get_db
from blogs import models

router = APIRouter(tags=["blogs"], prefix="/blogs")


@router.get(
    "/posts",
    response_model=List[Post],
    status_code=status.HTTP_200_OK,
)
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@router.post(
    "/posts",
    status_code=status.HTTP_201_CREATED,
    response_model=Post,
    dependencies=[Depends(get_current_user_payload)],
)
async def create_post(post: PostCreate, db: Session = Depends(get_db)):
    """create post."""
    try:
        db_post = models.Post(title=post.title, content=post.content)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


@router.get("/posts/{id}", response_model=Post, status_code=status.HTTP_200_OK)
async def get_post(id: int, db: Session = Depends(get_db)):
    try:
        post = db.query(models.Post).filter(models.Post.id == id).first()
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return post


@router.patch(
    "/posts/{id}",
    dependencies=[Depends(get_db), Depends(get_current_user_payload)],
    response_model=Post,
    status_code=status.HTTP_200_OK,
)
async def update_post(id: int, post: PostCreate, db: Session = Depends(get_db)):
    """update post."""
    try:
        updated_post = db.query(models.Post).filter(models.Post.id == id).first()
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    try:
        updated_post.title = post.title
        updated_post.content = post.content
        db.add(updated_post)
        db.commit()
    except ValidationError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    db.refresh(updated_post)
    return updated_post


@router.delete(
    "/posts/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_user_payload)],
)
async def delete_post(id: int, db: Session = Depends(get_db)):
    """delete post."""
    try:
        db.query(models.Post).filter(models.Post.id == id).delete()
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
