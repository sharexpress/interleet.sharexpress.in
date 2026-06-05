from fastapi import FastAPI, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from dotenv import load_dotenv
from app.core.db import get_db
import uvicorn
from app.routers.user import router as user_router
from app.core.config import SESSION_SECRET_KEY

from starlette.middleware.sessions import SessionMiddleware
from app.routers.interview import router as interview_router

from app.routers.resume import router as resume_router
from app.routers.challenges import router as challenge_router
from fastapi.middleware.cors import CORSMiddleware


load_dotenv()

# INCLUDE ROUTERS


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.add_middleware(
    SessionMiddleware,
    secret_key=SESSION_SECRET_KEY,
    same_site="lax",
    https_only=False,
)


@app.get("/")
async def home(db: AsyncIOMotorDatabase = Depends(get_db)):

    collections = await db.list_collection_names()

    print(collections)

    return {"message": True}


app.include_router(user_router)
app.include_router(resume_router)
app.include_router(interview_router)
app.include_router(challenge_router)


if __name__ == "__main__":
    uvicorn.run(host="127.0.0.1", port=8000, reload=True)
