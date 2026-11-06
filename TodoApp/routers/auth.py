from fastapi import APIRouter, Depends, status, HTTPException, Request #it will allow us to route from our main.py file to auth.py file
from pydantic import BaseModel
from ..models import Users
from passlib.context import CryptContext
from ..database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.templating import Jinja2Templates
import os
from dotenv import load_dotenv


#auth.py needs a different port / allow them to run on the same port but be scalable -> router: way of having a main file (root of main app) and different files will sit on top of this
router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


#secret key lives in the .env file (git-ignored) instead of the code, so it never gets uploaded to github
load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is not set. Copy .env.example to .env and put a key in it (generate one with: openssl rand -hex 32)")
ALGORITHM = 'HS256'


bcrypt_context = CryptContext(schemes=['bcrypt'],deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

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

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

templates = Jinja2Templates(directory="TodoApp/templates")


### Pages ###

@router.get("/login-page")
def render_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/register-page")
def render_register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


### Endpoints ###

def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()

    if not user:
        return False

    if not bcrypt_context.verify(password,user.hashed_password):
        return False
    
    return user

#jwt - jsonwebtoken. {header, payload, signature}.  
# #header -> {algorithm for signing, typ} encoded to byte64;
#payload -> data of the user and additional information, it includes claims: registered (iss (issuer),sub (subject (id for the jwt)),exp(expiration time)), public and private. 
#signature -> algorithm is the header to create the signature hashes the encoded header and payload with a secret, the secret is saved on the server but cluent doesn ot have access
def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
    encode = {'sub': username,
              'id': user_id,
              'role' : role}
    
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role: str = payload.get('role')
        if username is None or user_id is None: 
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail= 'Could not validate credentials.')

        return {'username': username, 'id': user_id, 'user_role': user_role}

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail= 'Could not validate credentials.')



@router.post("/",status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    create_user_model = Users(
        email = create_user_request.email,
        username = create_user_request.username,
        first_name = create_user_request.first_name,
        last_name = create_user_request.last_name,
        role = create_user_request.role,
        hashed_password = bcrypt_context.hash(create_user_request.password),
        is_active = True,
        phone_number = create_user_request.phone_number
    )

    db.add(create_user_model)
    db.commit()


@router.post("/token",response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency):

    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                    detail= 'Could not validate credentials.')

    token = create_access_token(user.username,user.id,user.role,timedelta(minutes=20))

    return {'access_token': token, 'token_type':'bearer'}