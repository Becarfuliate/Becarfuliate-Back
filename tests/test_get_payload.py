import pytest
from crud.UserSERvices import get_payload, JWT_EXPIRES
import string
import random
from datetime import datetime,timedelta  
length_of_string = 8
random_str = (
    random.choice(string.ascii_letters + string.digits) for _ in range(length_of_string)
)


def test_get_payload(userID=random_str):
    assert get_payload(userID)["expiry"] <= str(datetime.now() + JWT_EXPIRES)
