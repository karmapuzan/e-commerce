from fastapi import APIRouter, Depends, HTTPException, status
from backend.app.auth.security import hash_password, oauth2_scheme


router = APIRouter(
    prefix="/user", tags=["user login"], dependencies=[Depends(oauth2_scheme)]
)
