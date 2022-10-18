import pytest
from fastapi.testclient import TestClient
import main 
from routers.usersController import *

from crud.UserSERvices import *
import string
import random
from datetime import datetime

@db_session
def add_user(in_username,in_password,in_confirmation_mail,in_email):
    with db_session:
        User(
            username=in_username,
            password= in_password,
            avatar = "",
            confirmation_mail = in_confirmation_mail,
            email= in_email
        )


@db_session
def elim_user(username:str):
    with db_session:
        User[username].delete()


add_user("juanka","asd123",1,"juanka@hotmail.com") 
add_user("messi","antonela",0,"messi@hotmail.com")

client = TestClient(main.app)

def test_username_login_invalid_user():
    response = client.post("/login",
        json={"username":"asdsad","email":"aasdasd","password":"asdasdasd"})
    assert response.json() == {"detail":"no existe el usuario"}

def test_email_login_invalid_user():
    response = client.post("/login",
        json={"username":"","email":"aasdasd","password":"asdasdasd"})
    assert response.json() == {"detail":"no existe el usuario"}

def test_user_login_invalid_password():
    response = client.post("/login",
        json={"username":"juanka","email":"","password":"asdasdasd"})
    assert response.json() == {"detail":"contrasenia incorrecta"}

def test_email_login_invalid_password():
    response = client.post("/login",
        json={"username":"","email":"juanka@hotmail.com","password":"asdasdasd"})
    assert response.json() == {"detail":"contrasenia incorrecta"}

def test_user_login_email_not_verificated():
    response = client.post("/login",
        json={"username":"messi","email":"","password":"antonela"})
    assert response.json() == {"detail":"email no verificado"}

def test_email_login_email_not_verificated():
    response = client.post("/login",
        json={"username":"","email":"messi@hotmail.com","password":"antonela"})
    assert response.json() == {"detail":"email no verificado"}

def test_user_login_success():
    response = client.post("/login",
        json={"username":"juanka","email":"","password":"asd123"})
    assert response.json() != {"detail":"email no verificado"} and response.json() != {"detail":"contrasenia incorrecta"} and response.json() !={"detail":"no existe el usuario"}

def test_email_login_success():
    response = client.post("/login",
        json={"username":"","email":"juanka@hotmail.com","password":"asd123"})
    assert response.json() != {"detail":"email no verificado"} and response.json() != {"detail":"contrasenia incorrecta"} and response.json() !={"detail":"no existe el usuario"}


length_of_string = 8
random_str = (
    random.choice(string.ascii_letters + string.digits) for _ in range(length_of_string)
)


def test_get_payload(userID=random_str):
    assert get_payload(userID)["expiry"] <= str(datetime.now() + JWT_EXPIRES)

random_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))
token = sign_JWT(random_str)
payload = get_payload(random_str)
decoded_token = decode_JWT(token)


def test_sign_and_decode_JWT(r=random_str):
    assert payload['userID'] == decoded_token['userID']
    delete_db()

def delete_db():
    elim_user("juanka")
    elim_user("messi")