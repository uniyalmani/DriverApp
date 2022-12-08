import os
from typing import Dict, List, Optional
from sqlmodel import Field, SQLModel, select
from sqlalchemy import UniqueConstraint, String
from sqlalchemy import Column


class Users(SQLModel, table=True):

    __tablename__ = "users"

    id: int = Field(primary_key=True)
    name: str
    email: str = Field(sa_column=Column("email", String(40), unique=True))
    mobile_number: str
    longitude: float = Field(default=0.0)
    latitude: float = Field(default=0.0)
    hashed_password: str
    is_varified: bool = Field(default=False)
    is_free: bool = Field(default=True)
    rating: int
    role_id: int = Field(default=None, foreign_key="roles.id")


class Role(SQLModel, table=True):

    __tablename__ = "roles"
    id: int = Field(primary_key=True)
    name: str


class Booked(SQLModel, table=True):

    __tablename__ = "booked"

    id: int = Field(primary_key=True)
    driver_id: int = Field(default=None, foreign_key="users.id")
    user_id: int = Field(default=None, foreign_key="users.id")

