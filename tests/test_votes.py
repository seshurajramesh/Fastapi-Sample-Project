import pytest
from schemas import VotesCreate
from models import Votes
from .conftest import AsyncTestingSessionLocal



@pytest.fixture()
async def test_vote(test_posts,test_user):
    new_vote = Votes(post_id=test_posts[0].id,user_id=test_user['id'])
    async with AsyncTestingSessionLocal() as db:
        db.add(new_vote)
        await db.commit()
        return new_vote


async def test_vote_on_post(authorized_client,test_posts):
    response = await authorized_client.post("/votes/",json={"post_id":test_posts[0].id,"dir":1})   

async def test_vote_twice_post(authorized_client,test_posts,test_vote):
    response = await authorized_client.post("/votes/",json={"post_id":test_posts[0].id,"dir":1})
    assert response.status_code == 409

async def test_delete_vote(authorized_client,test_posts,test_vote):
    response = await authorized_client.post("/votes/",json={"post_id":test_posts[0].id,"dir":0})
    assert response.status_code == 201

async def test_delete_vote_non_exist(authorized_client,test_posts):
    response = await authorized_client.post("/votes/",json={"post_id":test_posts[0].id,"dir":0})
    assert response.status_code == 404

async def test_vote_post_non_exist(authorized_client,test_posts):
    response = await authorized_client.post("/votes/",json={"post_id":88888,"dir":1})
    assert response.status_code == 404