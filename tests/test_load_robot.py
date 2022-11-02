# import pytest
# from fastapi.testclient import TestClient
# import main
# from crud.user_services import *


# client = TestClient(main.app)

# # Funciones auxiliares para los test
# def client_post_register(username, password, email):
#     return client.post(
#         "/register",
#         json={
#             "username": username,
#             "password": password,
#             "email": email
#             }
#     )

# @db_session
# def client_fast_confirmation(username: str):
#     with db_session:
#         User[username].confirmation_mail = True


# def test_load_robot():
#     client_post_register(
#         "anonymous",
#         "Asd23asdasdasdasd@",
#         "anonymous@hotmail.com"
#         )
#     client_fast_confirmation("anonymous")
#     response = client.post(
#         "/login",
#         json={
#             "username": "anonymous",
#             "email": "anonymous@hotmail.com",
#             "password": "Asd23asdasdasdasd@"
#         },
#     )
#     usr_tkn = response.json()['token']
#     files_up = [("config", open("tests/test_files/robot1.py", "rb")),
#              ("avatar", open("tests/test_files/tortuga.jpg", "rb"))]
#     response = client.post(
#         "/upload/robot",
#         data={
#             "name": "robot1",
#             "tkn": usr_tkn,
#             "username": "anonymous"
#         },
#         files=files_up,
#         headers={
#             'Accept': 'application/json',
#             'Content-Type': 'multipart/form-data'
#         }
#     )
#     assert response.json() == "response"

# # eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySUQiOiJMaXNhbmRybyIsImV4cGlyeSI6IjIwMjItMTEtMDMgMTY6NDE6MTkuNjI1Njk5In0.PUbPjfs6I51Ba1CJWw8yjSQxsANMW1HBaenZ_Bajz64