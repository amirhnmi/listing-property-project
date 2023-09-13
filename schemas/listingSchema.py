from pydantic import BaseModel,validator


class ListCreate(BaseModel):
    type : str    
    availableNow : bool
    address : str

    @validator("type")
    def validator_type(cls,value):
        if value.lower() not in ["house", "apartment"]:
            raise ValueError("Property type must be house or apartment")
        return value


class ListOut(BaseModel):
    id : int
    type : str
    availableNow : bool
    address : str

    class config:
        orm_mode = True