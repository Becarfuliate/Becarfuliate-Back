from pydantic import BaseModel, validator
from typing import Optional
import re


special_chars = "~`!@#$%^&*()-_+={}[]\\|/:;\"'<>,.?"


class User_base(BaseModel):
    username: str
    password: str
    avatar: Optional[str] = None
    email: str

    @validator('password')
    def password_validator(cls, password):
        if len(password) < 7:
            raise ValueError('La longitud mínima es de 8 caracteres.')
        if len(password) > 50:
            raise ValueError('La longitud máxima es de 50 caracteres.')
        if (password.islower() or password.isupper()):
            raise ValueError(
                'Debe contener al menos una mayuscula y una minuscula'
                )
        if ' ' in password:
            raise ValueError(
                'No debe contener espacios'
                )
        if not any(c in special_chars for c in password):
            raise ValueError(
                'Debe contener al menos un caracter especial'
                )
        return password

    @validator('email')
    def email_validator(cls, email):
        regex = r"^[a-zA-Z0-9]+[\._]?[a-zA-Z0-9]+[@]\w+[.]\w{2,3}$"
        if not (re.search(regex, email)):
            raise ValueError(
                'Email invalido'
            )
        return email


class User_create(User_base):
    class Config:
        orm_mode = True
