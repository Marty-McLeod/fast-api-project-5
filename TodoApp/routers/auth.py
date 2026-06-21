from datetime import timedelta, datetime, timezone
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import JWTError, jwt
from ..database import SessionLocal
from ..models import Users
from fastapi.templating import Jinja2Templates


# Instantiate router with oauth for each endpoint
router = APIRouter(
    prefix = "/auth",
    tags = ["auth"]
)

# Define the secret key and type of encryption for JWT authentication
SECRET_KEY = "2280cf342386bac32c6c8399e2169edb6a05a88da71df09d8afcf10fcf5f3dee"
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# Verified the token as a dependency in our request
# - changed from "token" to "auth/token" for endpoing where we need dependency
# injection
oauth2_bearer = OAuth2PasswordBearer(tokenUrl = "auth/token")

# 
class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str
    phone_number: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    

# -- Initiate / open DB interface session
# 
def get_db():
    db = SessionLocal()
    try: # Execute commands/functions
        yield db
    finally:  # After DB response, close connection
        db.close()
        

db_dependency = Annotated[Session, Depends(get_db)]

templates = Jinja2Templates(directory="TodoApp/templates")

### Pages ###

@router.get("/login-page")
def render_login_page(request: Request):
    return templates.TemplateResponse(name="login.html", 
                                      request=request,
                                        context={"request": request} )


@router.get("/register-page")
def render_login_page(request: Request):
    return templates.TemplateResponse(name="register.html", 
                                      request=request,
                                        context={"request": request} )





### Endpoints ###
def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    # Authentication succeeded, so return True
    return user
    
    
def create_access_token(username: str, user_id: int, role: str,
                        expires_delta: timedelta):
    encode = { "sub": username, "id": user_id, "role": role }
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({ "exp": expires })
    
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    

# Checks token
async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        user_role: str = payload.get("role")
        
        # Test for decrypted data to match the user data
        if username is None or user_id is None:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                                detail="Could not validate user.")
        
        return { "username": username, "id": user_id, "user_role": user_role }
    except JWTError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate user.")        
    
    
# Creates user records in table "users"
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency,
                      create_user_request: CreateUserRequest):
    create_user_model = Users(
        username = create_user_request.username,
        email = create_user_request.email,
        first_name = create_user_request.first_name,
        last_name = create_user_request.last_name,
        role = create_user_request.role,
        hashed_password = bcrypt_context.hash(create_user_request.password),
        is_active = True,
        phone_number = create_user_request.phone_number
    )
    
    db.add(create_user_model)
    db.commit()
    
@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, 
    Depends()], db: db_dependency):
    
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate user.")
    
    token = create_access_token(user.username, user.id, user.role,
                                timedelta(minutes=20))
    return { "access_token": token, "token_type": "bearer" }




# Gets all user records from table "users"
@router.get("/users", status_code=status.HTTP_200_OK)
async def get_users(db: db_dependency):
    return db.query(Users).all()
    