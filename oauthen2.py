import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
import asyncio
from schemas import TokenData
from fastapi import Depends,status,Response,HTTPException
from jwt import InvalidTokenError
import os
from dotenv import load_dotenv


load_dotenv()



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")






SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


async def create_access_token(data: dict):
    expiry = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data.update({"exp": expiry})
    to_encode = data.copy()
    encoded_jwt =jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def verify_token(token: str , CredentialsException):
    print(token)
    print(CredentialsException)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        user_id: int = payload.get("id")
        if email is None or user_id is None:
            raise CredentialsException
        token_data = TokenData(email=email,user_id=user_id)
        return token_data
        
    except InvalidTokenError:
        raise CredentialsException

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return await verify_token(token,credentials_exception)