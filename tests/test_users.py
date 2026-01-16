from fastapi import HTTPException,status
from httpx import AsyncClient
from schemas import UserResponse,Token
import pytest
from oauthen2 import verify_token





# @pytest.mark.asyncio
# async def test_read_main(client):
#     response = await client.get("/")
#     assert response.status_code == 200
#     assert response.json() == {"Hello": "World"}


@pytest.mark.asyncio
async def test_create_user(client):
    response = await client.post("/users/", json={"email": "anusha@gmail.com", "password": "1234"}) # Must use await
    
    assert response.status_code == 201
    new_user = UserResponse(**response.json())
    assert new_user.email == "anusha@gmail.com"




@pytest.mark.asyncio
async def test_login_user(client,test_user):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"})


    response = await client.post("/login", data={"username":test_user["email"] , "password": test_user["password"] })
    assert response.status_code == 200
    print(response.json())


    token_resp = Token(**response.json())
    token_data = await verify_token(token_resp.access_token,credentials_exception)
    assert token_data.email == test_user["email"]
    assert token_data.user_id == test_user["id"]

@pytest.mark.asyncio
async def test_login_user_wrong_email(client,test_user):
    response = await client.post("/login", data={"username":"abc", "password": test_user["password"] })
    assert response.status_code == 403
    assert response.json()["detail"] == "Invalid Credentials"


@pytest.mark.asyncio
async def test_login_user_wrong_password(client,test_user):
    response = await client.post("/login", data={"username":test_user["email"] , "password": "abc" })
    assert response.status_code == 403
    assert response.json()["detail"] == "Invalid Credentials"

    


