from fastapi import Depends, HTTPException, APIRouter

from sqlalchemy.orm import session
from starlette import status

from app.database import get_db
from app import models
from app.schemas import PostPatch, Post

router = APIRouter(
    prefix='/posts',
    tags=['posts']
)


@router.get("/", status_code=status.HTTP_200_OK)
def get_posts(db: session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {
        "message": "posts retrieved successfully",
        "detail": posts,
        "success": True
    }


@router.get("/{post_id}", status_code=status.HTTP_200_OK)
def get_post(post_id: int, db: session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {post_id} not found"
        )
    return {
        "message": f"post with id {post_id} retrieved successfully",
        "detail": post,
        "success": True
    }


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_post(payload: Post, db: session = Depends(get_db)):
    new_post = models.Post(
        id=payload.id, title=payload.title, description=payload.description, published=payload.published
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {
        "message": "Post added successfully",
        "detail": new_post,
        "success": True
    }


@router.patch("/{post_id}", status_code=status.HTTP_201_CREATED)
def update_post(post_id: int, payload: PostPatch, db: session = Depends(get_db)):
    existing_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if existing_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {post_id} not found"
        )
    for field, value in payload.model_dump().items():
        if value is not None:
            setattr(existing_post, field, value)
    db.commit()
    db.refresh(existing_post)
    return {
        "message": f"post with id {post_id} is updated successfully",
        "success": True
    }


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {post_id} not found"
        )
    db.delete(post)
    db.commit()

    return {
        "message": f"post with id{post_id} deleted successfully",
        "success": True
    }
