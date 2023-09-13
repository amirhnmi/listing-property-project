from fastapi import APIRouter
from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session
from schemas import userSchema
from dependencies.get_db import get_db
from controllers import userController
from controllers.authController import get_current_user
from schemas import authSchema

router = APIRouter(prefix="/api")

@router.get("/user")
def get_all_user(): 
    return userController.get_all_user()

@router.get("/user/{user_id}")
def get_one_user(user_id:int, db:Session = Depends(get_db),current_user:authSchema.UserOut=Depends(get_current_user)): 
    return userController.get_one_user(user_id,db,current_user)

@router.put("/user/{user_id}")
def update_user(user_id:int,user:userSchema.UserUpdate, db:Session = Depends(get_db),current_user:authSchema.UserOut=Depends(get_current_user)):
    return userController.update_user(user_id,user,db,current_user)

@router.delete("/user/{user_id}")
def delete_user(user_id:int, db:Session = Depends(get_db),current_user:authSchema.UserOut=Depends(get_current_user)):
    return userController.delete_user(user_id,db,current_user)