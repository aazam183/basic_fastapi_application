from pydantic import BaseModel

class UserSchema(BaseModel):
    name : str
    username : str
    password : str
    email : str
    phone : str

class ResponseSchema(BaseModel):
    id : int
    name : str
    username : str
    # password: str
    email : str
    phone : str

class LoginSchema(BaseModel):
    username : str 
    password : str