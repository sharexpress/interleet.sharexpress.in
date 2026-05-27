from fastapi import APIRouter, UploadFile, File
import shutil
from app.ai.resume.resume_parser import ResumeParser

router = APIRouter(prefix="/resume", tags=["Resume"])


@router.post("/parse")
async def parse_resume(file: UploadFile = File(...)):
    file_path = f"temp/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    parsed_resume = await ResumeParser.parse_resume(file_path)
    return parsed_resume
