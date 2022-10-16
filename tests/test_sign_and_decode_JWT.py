import pytest
from crud.UserSERvices import sign_JWT, decode_JWT,get_payload
import string
import random

random_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))
token = sign_JWT(random_str)
payload = get_payload(random_str)
decoded_token = decode_JWT(token)


def test_sign_and_decode_JWT(r=random_str):
    assert payload['userID'] == decoded_token['userID']
