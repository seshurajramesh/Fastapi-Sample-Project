import asyncio
from fastapi import APIRouter,Depends,status,Response,HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from models import Votes,Post
from schemas import VotesCreate,TokenData
from db import get_db


from oauthen2 import get_current_user

router = APIRouter(
    prefix="/votes",
    tags=["Votes"]
)


@router.post("/",status_code=status.HTTP_201_CREATED)
async def vote(vote: VotesCreate,db: AsyncSession = Depends(get_db),user_identity: TokenData = Depends(get_current_user)):
    result = await db.execute(select(Post).where(Post.id == vote.post_id))
    post = result.scalars().first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Post with id: {vote.post_id} was not found")

    vote_query = await db.execute(select(Votes).where(Votes.post_id == vote.post_id,Votes.user_id == user_identity.user_id))
    found_vote = vote_query.scalars().first()

    
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail = f"User {user_identity.user_id} has already voted on post {vote.post_id}")
        else:
            new_vote = Votes(user_id=user_identity.user_id,post_id=vote.post_id)
            db.add(new_vote)
            await db.commit()
            return {"message": "Successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Vote does not exist")

        await db.delete(found_vote)
        await db.commit()
        return {"message": "Successfully deleted vote"}



