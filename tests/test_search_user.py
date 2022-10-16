import pytest
from crud.UserSERvices import add_user, search_user
import string
import random
from models.Users import User
from pony.orm import db_session


user = str(random.choice(string.ascii_letters + string.digits) for _ in range(8))
passwordd=str(random.choice(string.ascii_letters + string.digits) for _ in range(8))
emaild = str(random.choice(string.ascii_letters + string.digits) for _ in range(8))

user_create = {
  "username": user,
  "password": passwordd,
  "avatar": "",
  "email": emaild}
add_user(user_create)

def test_search_user(userID=user):
    assert search_user(userID).username == user