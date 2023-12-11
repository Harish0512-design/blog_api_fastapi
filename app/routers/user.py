from fastapi import Depends, APIRouter

from sqlalchemy.orm import session
from starlette import status

from app import models
from app.database import get_db
from app.password import get_hashed_password
from app.schemas import User

router = APIRouter(
    prefix='/users',
    tags=['users']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(payload: User, db: session = Depends(get_db)):
    payload.password = get_hashed_password(payload.password)
    new_user = models.User(**payload.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {
        "message": "User created successfully",
        "detail": new_user,
        "success": True
    }


@router.get("/", status_code=status.HTTP_200_OK)
def get_users(db: session = Depends(get_db)):
    users = db.query(models.User).with_entities(models.User.email, models.User.created_on)
    return {
        "message": "Users retrieved successfully",
        "detail": users,
        "success": True
    }


@router.get("/{id}", status_code=status.HTTP_200_OK)
def get_user(id: int, db: session = Depends(get_db)):
    user = db.query(models.User).with_entities(models.User.email, models.User.created_on).filter(
        models.User.id == id).first()
    return {
        "message": "user fetched successfully",
        "detail": user,
        "success": True
    }
