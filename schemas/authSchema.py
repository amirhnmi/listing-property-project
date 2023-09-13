from pydantic import EmailStr, BaseModel,validator
from datetime import date
from typing import Optional

class Token(BaseModel):
    token : str

class UserOut(BaseModel):
    id : int
    username : str 
    email : str
    token : int
    dateofbirth : date

class UserRegister(BaseModel):
    email : EmailStr
    username : str
    fullname : str
    password : str
    gender : Optional[str]="not_specified"
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
    
    @validator("gender")
    def validator_gender(cls,value):
        if value.lower() not in ["male","female","not_specified"]:
            raise ValueError("Gender must be male or female") 
        return value
    
    @validator("dateofbirth")
    def validator_dateofbirth(cls,value):
        if str(value) < "1940-01-01":
            raise ValueError("your date of birth must be after than 1940")
        return value

    


class UserLogin(BaseModel):
    username : str
    password : str
