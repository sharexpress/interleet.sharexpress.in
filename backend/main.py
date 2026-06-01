from fastapi import FastAPI, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from dotenv import load_dotenv
from app.core.db import get_db
import uvicorn
from app.routers.user import router as user_router
from app.core.config import BACKEND_CORS_ORIGINS, SESSION_SECRET_KEY

from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from app.routers.interview import router as interview_router

from app.routers.resume import router as resume_router
from app.routers.platform import router as platform_router
from app.routers.execution import router as execution_router


load_dotenv()

# INCLUDE ROUTERS


app = FastAPI(title="Interleet API", version="0.1.0")


app.add_middleware(
    CORSMiddleware,
    allow_origins=BACKEND_CORS_ORIGINS,
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

    return {"message": True, "collections": collections}


@app.get("/health")
async def health():
    return {"ok": True}


app.include_router(user_router)
app.include_router(resume_router)
app.include_router(interview_router)
app.include_router(platform_router)
app.include_router(execution_router)


if __name__ == "__main__":
    uvicorn.run(host="127.0.0.1", port=8000, reload=True)
