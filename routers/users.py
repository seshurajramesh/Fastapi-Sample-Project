import asyncio
from fastapi import APIRouter,Depends,status,Response,HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from models import User
from schemas import UserBase,UserResponse
from utils import Hash
from db import get_db



router = APIRouter(
    prefix="/users",
    tags=["Users"]
)



@router.post("/",status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(user: UserBase,db: AsyncSession = Depends(get_db)):
    user.password = Hash.hashed_password(user.password)
    new_user = User(**user.dict())
    db.add(new_user)
    try:
        await db.commit()
        await db.refresh(new_user)
        return new_user
    except IntegrityError:
        await db.rollback()

@router.get("/{id}",status_code=status.HTTP_200_OK,response_model=UserResponse)
async def get_user(id: int,db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "User not found")
    return user
