import os
from fastapi import FastAPI, Response, status
from typing import Dict, List, Optional
from sqlmodel import Field, SQLModel, select
from sqlalchemy import UniqueConstraint, String
from sqlalchemy import Column
from app.utilities.helpers import hash_password, verify_password, create_jwt_token
from app.utilities.dependencies import get_session
from app.models.database_models import Role, Users


class Driver_Methods:
    def __init__(self):
        self.session = next(get_session())

    def update_location(self, user_data):
        try:
            email = user_data["email"]
            role = user_data["role"]

            query = select(Role.id).where(Role.name == role)

            role_id = self.session.exec(query).first()
            
            statement = select(Users).where(Users.email == email, Users.role_id==role_id)
            results = self.session.exec(statement)
            user =  results.one()
            user.longitude = user_data["longitude"]
            user.latitude = user_data["latitude"]

            self.session.add(user)
            self.session.commit()

            return {
                "error": None,
                "data": user_data,
                "message":"account updated"
            }

        except Exception as e:
            return {
                "status_code": 400,
                "error": e,
                "token": None,
                "message":"failed to create account"
            }
