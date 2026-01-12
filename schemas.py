from pydantic import BaseModel, EmailStr, conint
from typing import Optional
from datetime import datetime


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    class Config:
        from_attributes = True


class UserBase(BaseModel):
    email: EmailStr 
    password: str

class UserResponse(BaseModel):
    email: EmailStr
    id: int
    created_at: datetime
    

class TokenData(BaseModel):
    email: Optional[EmailStr] = None
    user_id: int = None
    class Config:
        from_attributes = True
    

class Token(BaseModel):
    access_token: str
    token_type: str
    class Config:
        from_attributes = True

class PostNestedUser(PostCreate):
    owner: UserResponse
    class Config:
        from_attributes = True


class VotesCreate(BaseModel):
    post_id: int
    dir: conint(le=1)

class PostNestedUserVotes(BaseModel):
    Post : PostNestedUser

    votes: int
    class Config:
        from_attributes = True