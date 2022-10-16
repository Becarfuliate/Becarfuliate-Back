import pytest
from crud.UserSERvices import search_user
import string
import random



user = str(random.choice(string.ascii_letters + string.digits) for _ in range(8))
passwordd=str(random.choice(string.ascii_letters + string.digits) for _ in range(8))
emaild = str(random.choice(string.ascii_letters + string.digits) for _ in range(8))


def test_search_user(userID=user):
    assert search_user(userID).username == user