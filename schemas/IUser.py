from typing_extensions import Required
from pydantic import BaseModel, validator 
from typing import Optional

class user_login_schema(BaseModel):
    username: str
    email : str
    password: str
