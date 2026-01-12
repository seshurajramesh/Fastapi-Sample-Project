import asyncio
from fastapi import APIRouter,Depends,status,Response,HTTPException

from sqlalchemy import select,func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from models import Post,Votes
from schemas import PostBase,PostCreate,TokenData,PostNestedUser,PostNestedUserVotes
from db import get_db
from sqlalchemy.orm import selectinload


from oauthen2 import get_current_user

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


async def get_post(id: int, db, user_id: int):
    result = await db.execute(
        select(Post).where(
            Post.id == id,
            Post.owner_id == user_id
        ).options(selectinload(Post.owner)
    ))
    post = result.scalars().first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized or post not found"
        )

    return post

    
    

@router.get("/",status_code=status.HTTP_200_OK,response_model=list[PostNestedUserVotes])
async def get_posts(db: AsyncSession = Depends(get_db),user_identity: TokenData = Depends(get_current_user),
limit: int = 10, skip: int = 0, search: str = ""):
    query = (
        select(Post, func.count(Votes.post_id).label("votes"))
        .outerjoin(Votes, Post.id == Votes.post_id)
        .where(Post.owner_id == user_identity.user_id)
        .group_by(Post.id).options(selectinload(Post.owner)).limit(limit).offset(skip).filter(Post.content.contains(search))
    )
    result = await db.execute(query)
    posts = result.mappings().all()
    return posts
    
    


@router.post("/",status_code=status.HTTP_201_CREATED, response_model=PostCreate)
async def create_post(post: PostBase,db: AsyncSession = Depends(get_db), user_identity: TokenData = Depends(get_current_user) ):
    new_post = Post(**post.dict(),owner_id=user_identity.user_id)
    db.add(new_post)
    try:
        await db.commit()
        await db.refresh(new_post)
        return new_post
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST ,detail = "Posts already exists")


# @router.get("/posts/{id}",status_code=status.HTTP_200_OK,response_model=PostCreate)
# async def get_post(id: int,db: AsyncSession = Depends(get_db)):
#     result = await db.execute(select(Post).where(Post.id == id))
#     post = result.scalars().first()
#     if not post:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail = "Post not found")
#     return post

@router.get("/{id}",status_code=status.HTTP_200_OK,response_model=PostNestedUser)
async def get_post_id(id: int,db: AsyncSession = Depends(get_db),user_identity: TokenData = Depends(get_current_user)):
    post = await get_post(id,db,user_identity.user_id)
    return post


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int,db: AsyncSession = Depends(get_db),user_identity: TokenData = Depends(get_current_user)):
    post = await get_post(id,db,user_identity.user_id)
    await db.delete(post)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}",status_code=status.HTTP_202_ACCEPTED,response_model=PostNestedUser)
async def update_post(id: int,post: PostBase,db: AsyncSession = Depends(get_db),user_identity: TokenData = Depends(get_current_user)):
    post_query = await get_post(id,db,user_identity.user_id)
    for key,value in post.dict().items():
        setattr(post_query,key,value)
    await db.commit()
    await db.refresh(post_query)
    return post_query
