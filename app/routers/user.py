from fastapi import FastAPI, Response, Depends, HTTPException, status, APIRouter
from .. import models, schemas, utils
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..database import get_db

router = APIRouter(prefix="/users", tags=["Users"])


# ✅ Create a user
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # hashing the password in user_password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.model_dump())
    db.add(new_user)

    try:
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError as e:
        db.rollback()
        if "users_email_key" in str(e.orig):
            # Proper HTTP 409 Conflict for existing account
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Account with this email already exists.",
            )
        # fallback for other DB errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred.",
        )


# ✅Get a user by ID
@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id: {id} was not found",
        )
    return user
