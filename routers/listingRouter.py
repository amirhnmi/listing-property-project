from fastapi import APIRouter,Depends
from schemas import listingSchema,authSchema
from sqlalchemy.orm import Session
from dependencies.get_db import get_db
from controllers import listingController
from controllers.authController import get_current_user

router = APIRouter(prefix="/api")

@router.get("/listing")
def get_all_list():
    """This endpoint returns a complete list of all properties in the database"""
    return listingController.get_all_list()


@router.get("/listing/{list_id}")
def get_one_list(list_id:int, db:Session=Depends(get_db),current_user:authSchema.UserOut=Depends(get_current_user)):
    """This endpoint return a property by id"""
    return listingController.get_one_list(list_id,db,current_user)


@router.post("/listing")
def create_list(request:listingSchema.ListCreate, db:Session=Depends(get_db),current_user:authSchema.UserOut=Depends(get_current_user)):
    """This endpoint makes the property """
    return listingController.create_list(request,db,current_user)


@router.put("/listing/{list_id}")
def update_list(list_id:int, request:listingSchema.ListCreate, db:Session=Depends(get_db),current_user:authSchema.UserOut=Depends(get_current_user)): # token:str=Depends(oauth2_scheme),current_user:authSchema.UserOut=Depends(get_current_user)
    """This endpoint useed to update the property by id"""
    return listingController.update_list(list_id,request,db,current_user)


@router.delete("/listing/{list_id}")
def delete_list(list_id:int, db:Session=Depends(get_db),current_user:authSchema.UserOut=Depends(get_current_user)):
    """This endpoint recieve id and delete property by id"""
    return listingController.delete_list(list_id,db,current_user)