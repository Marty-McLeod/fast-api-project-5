from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, Path, Query
from pydantic import BaseModel, Field
from passlib.context import CryptContext
from ..models import Users
from ..database import SessionLocal
from .auth import get_current_user, bcrypt_context

router = APIRouter(
    prefix="/user",
    tags = ["user"]
)


# -- Initiate / open DB interface session
# 
def get_db():
    db = SessionLocal()
    try: # Execute commands/functions
        yield db
    finally:  # After DB response, close connection
        db.close()
        

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)


# ==== GET endpoings ====
# ASSIGNMENT WORK: get the current session's user's info
@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed.")
    
    # return db.query(Users).filter(Users.id == user.get("id")).first()
    return db.query(Users).filter(Users.id == user.get("id")).first()

    
# ==== PUT endpoints ====
@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency,\
    user_verification: UserVerification):
    
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed.")
    
    user_model = db.query(Users).filter(Users.id == user.get("id")).first()
    
    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail="Error on password change")
    # Hash the new password and update the current user record
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    
    db.add(user_model)
    db.commit()
    
    
@router.put("/phonenumber/{phone_number}", status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(user: user_dependency, db: db_dependency,\
    phone_number: str = Path(min_length=7)):
    
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed.")
    
    user_model = db.query(Users).filter(Users.id == user.get("id")).first()
    user_model.phone_number = phone_number
    db.add(user_model)
    db.commit()
    