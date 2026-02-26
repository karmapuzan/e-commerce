from datetime import timedelta
from sqlalchemy.orm import Session
from typing import Annotated

from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from backend.app.auth.auth import authenticate_user, create_access_token
from backend.app.models.users import User as UserModel
from backend.app.schemas.users import Token
from backend.app.database.database import get_db
from backend.app.utils.config import settings

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
