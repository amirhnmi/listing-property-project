import aioredis
from fastapi import APIRouter,Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from dependencies.get_db import get_db
from schemas import authSchema
from controllers import authController
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter

router = APIRouter(prefix="/api")

@router.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost", encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(redis)

@router.post("/register")
def register(request:authSchema.UserRegister, db: Session = Depends(get_db)):
    return authController.register(request,db)


@router.post("/login") #,dependencies=[Depends(RateLimiter(times=5, seconds=30))]
async def login(request:OAuth2PasswordRequestForm=Depends(), db:Session=Depends(get_db)):
    return authController.login(request,db)

