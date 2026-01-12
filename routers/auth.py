import asyncio
from fastapi import APIRouter,Depends,status,Response,HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from models import User
from utils import Hash
from db import get_db
from oauthen2 import create_access_token
from schemas import Token





router = APIRouter(
    tags=["Authentication"]
)


@router.post("/login",status_code=status.HTTP_200_OK, response_model=Token)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends() ,db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user_credentials.username))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Invalid Credentials")
    
    if not Hash.verify_password(user.password,user_credentials.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Invalid Credentials")
    
    token = await create_access_token(data={"sub": user.email,"id": user.id})
    
    return {"access_token": token , "token_type": "bearer"}