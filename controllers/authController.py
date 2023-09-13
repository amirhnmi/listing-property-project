from fastapi import HTTPException,Depends
from sqlalchemy.orm import Session
from models import listingModel
from datetime import datetime,timedelta
from dependencies.hash import Hash
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime,timedelta
from jose import jwt, JWTError
from dependencies.hash import Hash
from dependencies.get_db import get_db
import random

hash = Hash()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login")

SECRET_KEY = "a4ccf8e58dcc5ebc6ce1637d362c2ced20f4dcc030a3e985c97d7f9dfbe29616"  # openssl rand -hex 32
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

active_tokens = {}

def create_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



def register(request,db):
    email_exist = db.query(listingModel.User).filter(listingModel.User.email == request.email).first()
    username_exist = db.query(listingModel.User).filter(listingModel.User.username == request.username).first()

    if email_exist:
        raise HTTPException(detail="Email already exist", status_code=400)
    if username_exist:
        raise HTTPException(detail="Username already exist", status_code=400)

    user = listingModel.User(
        email=request.email,
        username=request.username,
        fullname=request.fullname,
        gender=request.gender, 
        password=hash.bcrypt(request.password),
        dateOfBirth=request.dateofbirth,
        createAt=datetime.now(),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user



def login(request,db):
    user = db.query(listingModel.User).filter(listingModel.User.username == request.username).first()

    if not user or not hash.verify(user.password, request.password):
        raise HTTPException(detail="Invalid username or password", status_code=status.HTTP_404_NOT_FOUND)
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    dbtoken = random.randint(1,1000)

    token = create_token(data={"sub":request.username,"token": dbtoken}, expires_delta=access_token_expires)
    _dict = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    dbtoken = _dict.get("token")
    user.token = dbtoken
    db.commit()

    return {
        "access_token": token,
        "type_token": "bearer",
        "user_id": user.id,
        "username": user.username
    }


def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(get_db)):
    error_credential = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="invalid credential",
    headers={"WWW-authenticate":"bearer"})
    try:
        _dict = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username = _dict.get("sub")
        dbtoken = _dict.get("token")
        if not username:
            raise error_credential
    except JWTError:
        raise error_credential
        
    user_and_token_exist = db.query(listingModel.User).filter(listingModel.User.username == username).filter(listingModel.User.token == dbtoken).first()

    # if user_and_token_exist.token == dbtoken:
    #     raise HTTPException(detail="User already loggedin", status_code=status.HTTP_409_CONFLICT)
    
    if user_and_token_exist is None:
        raise HTTPException(detail="User not found with this username", status_code=status.HTTP_404_NOT_FOUND)
    
    return user_and_token_exist



