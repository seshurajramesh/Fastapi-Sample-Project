from fastapi import FastAPI
from db import get_db,engine
from db import init_db
from contextlib import asynccontextmanager
import asyncio
from fastapi.middleware.cors import CORSMiddleware

from routers import posts,users,auth,votes


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
##"Shutting down app and close the connections to DB
    await engine.dispose()



app = FastAPI(lifespan=lifespan)

origins =['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)



@app.get("/")
def root():
    return {"Hello": "World"}






