from fastapi import Request
from sqlmodel import Session
from .helpers import is_valid_token
from app.controllers.database_initializer import engine
from fastapi import APIRouter, Depends, Request, Response, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
security = HTTPBearer()

def get_decoded_token_data(credentials):
    """return token data with key valid_token for validation"""

    print("***************")
    auth_token =   credentials.credentials
    print(auth_token, "********************")
    decoded_data = is_valid_token(auth_token)
    return decoded_data


def get_session():
    """creating session for each request"""
    with Session(engine) as session:
        print("-------------------------")
        yield session