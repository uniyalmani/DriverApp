import os
from fastapi import FastAPI, Response, status
from typing import Dict, List, Optional
from sqlmodel import Field, SQLModel, select
from sqlalchemy import UniqueConstraint, String
from sqlalchemy import Column
from app.utilities.helpers import hash_password, verify_password, create_jwt_token
from app.utilities.dependencies import get_session
from app.models.database_models import Role, Users


class Authentication:
    def __init__(self):
        self.session = next(get_session())

    def create_user(self, user_data):
        try:
            hashed_password = hash_password(user_data["password"])
            role = user_data["role"].lower().strip()

            query = select(Role.id).where(Role.name == role)
            role_id = self.session.exec(query).first()
            user = Users(name=user_data["name"].lower().strip(),
                        email=user_data["email"].lower().strip(),
                        hashed_password=hashed_password,
                        longitude=user_data["longitude"],
                        latitude=user_data["latitude"],
                        mobile_number=user_data["mobile_number"],
                        rating=user_data["rating"],
                        role_id=role_id,)
            
            self.session.add(user)
            self.session.flush()
            self.session.commit()
            data = {"email": user_data["email"].lower().strip(), "role": role, "is_varified": user.is_varified}
            time = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
            token = create_jwt_token(data, time)

            return {
                "error": None,
                "status_code": 200,
                "token": token,
                "message":"account created"
            }

        except Exception as e:
            return {
                "status_code": 400,
                "error": e,
                "token": None,
                "message":"failed to create account"
            }
    def authenticate_user(self, user_data):
        try:
            print("]]]]]]]]]]]]]]]", user_data)
            email, password, role = user_data["email"], user_data["password"], user_data["role"]
            email = email.lower().strip()
            print(role, "[[[[[[[[[[-----------------")
            query = select(Role.id).where(Role.name == role)
            role_id = self.session.exec(query).first()
            print("----------------", email, role)
            query = select(Users).where(Users.email == email, Users.role_id == role_id)
            user = self.session.exec(query).first()
            print(user)
            if verify_password(password, user.hashed_password):
                data = {"email": email, "role": role, "is_varified": user.is_varified}
                time = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
                token = create_jwt_token(data, time)
                return {
                    "error":None,
                    "token":token,
                    "message": "sucessfully login"
                }
            else:
                return {
                    "error": "wrong email or pass word",
                    "token":None,
                    "status_code": 401,
                    "message": "failed login"
                }
        except Exception as e:
            return {
                "status_code": 400,
                "error": e,
                "token": None,
                "message":"failed to log account"
            }