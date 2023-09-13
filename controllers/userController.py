from fastapi import HTTPException,status
from models import listingModel
from dependencies.hash import Hash
from fastapi.responses import JSONResponse
from datetime import datetime
from dependencies.database import sessionLocal
hash = Hash()



def get_all_user():
    db=sessionLocal()
    try:
        users = db.query(listingModel.User).all()
        return {
            "message":"ok",
            "users":users
        }
    finally:
        db.close()


def get_one_user(user_id,db,current_user): 
    user = db.query(listingModel.User).filter(listingModel.User.id == user_id).first()
    if user is None:
        raise HTTPException(detail="User not found with this id", status_code=404)
    if user.id == current_user.id:
        return {
            "message":"ok",
            "user":user
        }
    return HTTPException(detail="You can not get this user", status_code=status.HTTP_403_FORBIDDEN)
    

def update_user(user_id,request,db,current_user):
    user = db.query(listingModel.User).filter(listingModel.User.id == user_id).first()
    if user is None:
        raise HTTPException(detail="User not found with this id", status_code=404)
    user_data = {
        listingModel.User.email: request.email,
        listingModel.User.username: request.username,
        listingModel.User.fullname: request.fullname,
        listingModel.User.password: hash.bcrypt(request.password),
        listingModel.User.dateOfBirth:request.dateofbirth,
        listingModel.User.updateAt:datetime.now(),
    }
    if user.id == current_user.id :
        db.query(listingModel.User).filter(listingModel.User.id == user_id).update(user_data)
        db.commit()
        return JSONResponse(content="user successfully updated")
    return HTTPException(detail="You can not update this user", status_code=status.HTTP_403_FORBIDDEN)


def delete_user(user_id,db,current_user):
    user = db.query(listingModel.User).filter(listingModel.User.id == user_id).first()
    if user is None:
        raise HTTPException(detail="User not found with this id", status_code=404)
    if user.id == current_user.id :
        db.delete(user)
        db.commit()
        return JSONResponse(content="User successfully deleted")
    return HTTPException(detail="You can not delete this user", status_code=status.HTTP_403_FORBIDDEN)