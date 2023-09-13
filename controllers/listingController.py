from fastapi import HTTPException,status
from fastapi.responses import JSONResponse
from models import listingModel
from datetime import datetime
from dependencies.database import sessionLocal


def get_all_list():
    db = sessionLocal()
    try:
        lists = db.query(listingModel.Listing).all()
        return {
            "message":"ok",
            "lists":lists
        }
    finally:
        db.close()


def get_one_list(list_id, db,current_user):
    list = db.query(listingModel.Listing).filter(listingModel.Listing.id == list_id).first()
    if not list:
        raise HTTPException(detail="Property not found with this id", status_code=status.HTTP_404_NOT_FOUND)
    if list.owner_id == current_user.id:
        return {
            "message":"ok",
            "list":list
        }
    return {
            "message":"ok",
            "list":{
                "id" : list.id,
                "type":list.type,
                "availableNow" : list.availableNow,
                'address' : list.address
            }
        } 


def create_list(request, db, current_user):
    list = listingModel.Listing(
        type = request.type,
        availableNow = request.availableNow,
        owner_id = current_user.id,
        address = request.address,
        createAt = datetime.now(),
    )
    db.add(list)
    db.commit()
    db.refresh(list)
    return {
            "message":"ok",
            "list":list
        }


def update_list(list_id, request, db,current_user):
    list = db.query(listingModel.Listing).filter(listingModel.Listing.id == list_id).first()
    if not list:
        raise HTTPException(detail="Property not found whit this id",status_code=status.HTTP_404_NOT_FOUND)
    list_data = {
        listingModel.Listing.type : request.type,
        listingModel.Listing.availableNow : request.availableNow,
        listingModel.Listing.owner_id : current_user.id,
        listingModel.Listing.address : request.address,
        listingModel.Listing.updateAt : datetime.now()
    }
    if list.owner_id == current_user.id :
        db.query(listingModel.Listing).filter(listingModel.Listing.id == list_id).update(list_data)
        db.commit()
        return JSONResponse(content="list successfully updated")
    return HTTPException(detail="You can not update this list", status_code=status.HTTP_403_FORBIDDEN)
    


def delete_list(list_id, db,current_user):
    list = db.query(listingModel.Listing).filter(listingModel.Listing.id == list_id).first()
    if not list:
        raise HTTPException(detail="Property not found whit this id",status_code=status.HTTP_404_NOT_FOUND)
    if list.owner_id == current_user.id :
        db.delete(list)
        db.commit()
        return JSONResponse(content="list successfully deleted")
    return HTTPException(detail="You can not delete this list", status_code=status.HTTP_403_FORBIDDEN)