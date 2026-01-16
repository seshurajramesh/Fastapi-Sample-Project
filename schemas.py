from pydantic import BaseModel, EmailStr, conint,ConfigDict
from typing import Optional
from datetime import datetime


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    owner_id: int
    


class UserBase(BaseModel):
    email: EmailStr 
    password: str

class UserResponse(BaseModel):
    email: EmailStr
    id: int
    created_at: datetime
    

class TokenData(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    email: Optional[EmailStr] = None
    user_id: int = None
    
    

class Token(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    access_token: str
    token_type: str
    

class PostNestedUser(PostCreate):
    model_config = ConfigDict(from_attributes=True)
    owner: UserResponse
    


class VotesCreate(BaseModel):
    post_id: int
    dir: conint(le=1)

class PostNestedUserVotes(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    Post : PostNestedUser

    votes: int
    