from pydantic import BaseModel,EmailStr,validator
from datetime import date


class UserUpdate(BaseModel):
    email : EmailStr
    username : str
    fullname : str
    password : str
    dateofbirth : date

    @validator("password")
    def Validator_password(cls,value):
        if not any(character.islower() for character in value):
            raise ValueError("Password must contain at least one lowercase character")
        
        if not any(character.isupper() for character in value):
            raise ValueError("Password must contain at least one uppercase character")
        
        if len(value) < 8:
            raise ValueError("Password must contain at least 8 characters")
        return value
    

class UserOut(BaseModel):
    id : int
    username : str 
    email : str
    fullname : str
    dateofbirth : date

    class config:
        orm_mode = True