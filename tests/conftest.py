import os
import pytest
import pytest_asyncio
from dotenv import load_dotenv
from httpx import ASGITransport, AsyncClient # Use AsyncClient for async tests
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from oauthen2 import create_access_token
from main import app
from db import get_db, Base
from schemas import UserResponse
from models import Post
from sqlalchemy import select

load_dotenv()

DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_PORT = os.getenv("DATABASE_PORT")


DATABASE_URL = f"postgresql+asyncpg://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"


engine = create_async_engine(DATABASE_URL, echo=True, future=True)

AsyncTestingSessionLocal = async_sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine, 
    class_=AsyncSession
)


async def override_get_db():
    async with AsyncTestingSessionLocal() as db:
        yield db

app.dependency_overrides[get_db] = override_get_db


@pytest.fixture()
async def setup_temp_database():
    async with engine.begin() as conn:
        # run_sync is required for metadata commands on an async engine
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


@pytest.fixture()
async def client(setup_temp_database):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac






@pytest.fixture()
async def test_user(client):
    user_data = {"email": "seshu@gmail.com", "password": "1234"}
    response = await client.post("/users/", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture()
async def token_header(test_user):
    access_token = await create_access_token(data={"sub": test_user["email"],"id": test_user["id"]})
    return access_token



@pytest.fixture()
async def authorized_client(client,token_header):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token_header}"
    }
    return client

@pytest.fixture()
async def test_posts(test_user):
    posts = [
        {"title": "first title", "content": "first content", "owner_id": test_user["id"]},
        {"title": "2nd title", "content": "2nd content", "owner_id": test_user["id"]},
        {"title": "3rd title", "content": "3rd content", "owner_id": test_user["id"]},
    ]
    
    def create_post_model(post):
        return Post(**post)

    post_map = map(create_post_model, posts)
    posts = list(post_map)

    async with AsyncTestingSessionLocal() as db:
        db.add_all(posts)
        await db.commit()
        await db.refresh(posts[0])
        await db.refresh(posts[1])
        await db.refresh(posts[2])

        all_posts = await db.execute(select(Post))
        all_posts = all_posts.scalars().all()
        return all_posts
     
    
    


