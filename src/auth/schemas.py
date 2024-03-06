# https://fastapi-users.github.io/fastapi-users/latest/configuration/schemas/

from datetime import datetime

from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    id: int
    name: str
    date: datetime
    status_name: str
    email: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class UserCreate(schemas.BaseUserCreate):
    name: str
    email: str
    password: str


class UserUpdate(schemas.BaseUserUpdate):
    pass
