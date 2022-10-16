from typing_extensions import Required
from pydantic import BaseModel, validator 
from typing import Optional


class User_base(BaseModel):
    username: str
    password: str
    avatar: Optional[str] = None
    email: str


class User_create(User_base):
    class Config:
        orm_mode = True


@validator("password")
def username_length(cls, password):
    if len(password) < 7:
        raise ValueError("La longitud mínima  es de 4 caracteres.")
    if len(password) > 40:
        raise ValueError("La longitud máxima es de 50 caracteres.")
    return password


class user_login_schema(BaseModel):
    username: str
    email : str
    password: str
