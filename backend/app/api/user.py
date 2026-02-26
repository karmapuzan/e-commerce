from fastapi import APIRouter, Depends, HTTPException, status
from backend.app.auth.security import hash_password, oauth2_scheme
from backend.app.database.database import get_db
from sqlalchemy.orm import Session

from backend.app.models.users import User as UserModel
from backend.app.schemas.users import UserCreate


router = APIRouter(prefix="/user", tags=["user login"])


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
