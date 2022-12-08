from pydantic import BaseModel, validator

from fastapi import APIRouter, Depends
from app.utilities.dependencies import get_session
from app.services import authserv

router = APIRouter()


class UserModel(BaseModel):
    name:str
    email: str
    password:str
    mobile_number:str
    longitude:float
    latitude: float

@router.post('/signup/driver',
        tags=["Common Routes"],
        description="**Route for creating account**")
def create_account(user_info:UserModel, auth: object = Depends(authserv.Authentication)):
    print("---------------------", user_info, auth.session)
    user_info = dict(user_info)
    user_info["rating"] = 0
    user_info["role"] = "drive"
    res = auth.create_user(user_info)   
    return res

@router.post('/signup/user',
        tags=["Common Routes"],
        description="**Route for creating account**")
def create_account(user_info:UserModel, auth: object = Depends(authserv.Authentication)):
    print("---------------------", user_info, auth.session)
    user_info = dict(user_info)
    user_info["rating"] = 0
    user_info["role"] = "user"
    res = auth.create_user(user_info)   
    return res



class LogIn(BaseModel):
    email: str
    password:str
    
    

@router.post('/login/driver',
        tags=["Common Routes"],
        description="**Route for creating account**")
def authenticate_user(user_info:LogIn, auth: object = Depends(authserv.Authentication)):
    print("---------------------", user_info, auth.session)
    user_info = dict(user_info)
    user_info["role"] = "drive"
    print(user_info, "-----------------")
    res = auth.authenticate_user(user_info)   
    return res