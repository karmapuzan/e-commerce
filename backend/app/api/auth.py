from datetime import timedelta
from sqlalchemy.orm import Session
from typing import Annotated

from fastapi import Depends, HTTPException, APIRouter, status
from fastapi.security import OAuth2PasswordRequestForm

from backend.app.auth.auth import authenticate_user, create_access_token
from backend.app.models.users import User as UserModel
from backend.app.schemas.users import Token
from backend.app.database.database import get_db
from backend.app.utils.config import settings

from backend.app.models.users import User as UserModel
from backend.app.schemas.users import UserCreate
from backend.app.auth.security import hash_password

router = APIRouter(prefix="", tags=["auth"])


@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    user = authenticate_user(
        email=form_data.username,
        password=form_data.password,
        db=db,
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={"sub": user.id},
        expires_delta=access_token_expires,
    )
    refresh_token = create_access_token(
        data={"sub": user.id},
        expires_delta=refresh_token_expires,
    )

    user.refresh_token = refresh_token  # type: ignore
    db.commit()
    db.refresh(user)

    return Token(
        msg="User has logged in",
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post("/register")
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.email == user_data.email).first()

    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="user already exist"
        )
    new_user = UserModel(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        email=user_data.email,
        phone=user_data.phone,
        password_hash=hash_password(user_data.password),
    )
    print("data", new_user)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully", "user": new_user}
