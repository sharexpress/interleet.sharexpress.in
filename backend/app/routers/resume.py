"""
/resume — Resume upload + AI parsing endpoint.

Flow:
  1. Receive PDF file via multipart/form-data
  2. Upload raw bytes to Cloudinary (folder: resumes/)
  3. Download the file from the returned Cloudinary URL
  4. Extract text with PyMuPDF
  5. Send text to AI → structured JSON response
  6. Return { cloudinary, parsed_resume, mock_test }
"""

from __future__ import annotations

import logging
import uuid
from datetime import datetime

from fastapi import APIRouter, File, HTTPException, UploadFile, Depends

from app.ai.resume.resume_parser import ResumeParser
from app.services.cloudinary_service import upload_resume_to_cloudinary
from app.middleware.user import Middleware as UserMiddleware
from app.core.db import get_db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/resume", tags=["Resume"])

MAX_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB


@router.post("/parse")
async def parse_resume(
    file: UploadFile = File(...),
    user_auth=Depends(UserMiddleware.me)
):
    """
    Upload a PDF resume to Cloudinary, parse it, save it to database, and return structured data.
    """
    # ── Validate file type ───────────────────────────────────────────────────
    if file.content_type not in ("application/pdf", "application/octet-stream"):
        raise HTTPException(
            status_code=422,
            detail="Only PDF files are supported. Please upload a .pdf resume.",
        )

    # ── Read file bytes ──────────────────────────────────────────────────────
    pdf_bytes = await file.read()

    if len(pdf_bytes) == 0:
        raise HTTPException(status_code=422, detail="Uploaded file is empty.")

    if len(pdf_bytes) > MAX_SIZE_BYTES:
        raise HTTPException(
            status_code=413,
            detail=f"File exceeds the 5 MB size limit ({len(pdf_bytes) // 1024} KB received).",
        )

    # ── Upload to Cloudinary ─────────────────────────────────────────────────
    try:
        cloudinary_meta = await upload_resume_to_cloudinary(
            file_bytes=pdf_bytes,
            original_filename=file.filename or "resume.pdf",
        )
    except RuntimeError as exc:
        logger.error("Cloudinary upload failed: %s", exc)
        raise HTTPException(status_code=502, detail=str(exc))

    # ── AI parse (downloads from Cloudinary URL → PyMuPDF → LLM) ────────────
    parsed = await ResumeParser.parse_from_url(cloudinary_meta["secure_url"])

    # ── Save to Database ─────────────────────────────────────────────────────
    user_doc = user_auth.get("user")
    user_id = str(user_doc["user_id"])
    
    resume_id = str(uuid.uuid4())
    resume_doc = {
        "id": resume_id,
        "user_id": user_id,
        "filename": file.filename or "resume.pdf",
        "cloudinary_url": cloudinary_meta["secure_url"],
        "parsed_resume": parsed.get("parsed_resume", {}),
        "mock_test": parsed.get("mock_test", {}),
        "created_at": datetime.utcnow()
    }
    
    db = get_db()
    await db.resumes.insert_one(resume_doc)

    return {
        "id": resume_id,
        "cloudinary": cloudinary_meta,
        **parsed,  # inlines parsed_resume and mock_test keys
    }


@router.get("/my-resumes")
async def get_my_resumes(user_auth=Depends(UserMiddleware.me)):
    """
    Get all previously uploaded and parsed resumes for the authenticated user.
    """
    user_doc = user_auth.get("user")
    user_id = str(user_doc["user_id"])
    
    db = get_db()
    cursor = db.resumes.find({"user_id": user_id}).sort("created_at", -1)
    resumes = []
    async for doc in cursor:
        resumes.append({
            "id": doc.get("id"),
            "filename": doc.get("filename"),
            "cloudinary_url": doc.get("cloudinary_url"),
            "parsed_resume": doc.get("parsed_resume"),
            "mock_test": doc.get("mock_test"),
            "created_at": str(doc.get("created_at"))
        })
    
    return {"success": True, "resumes": resumes}


@router.delete("/{resume_id}")
async def delete_resume(resume_id: str, user_auth=Depends(UserMiddleware.me)):
    """
    Delete a previously uploaded resume.
    """
    user_doc = user_auth.get("user")
    user_id = str(user_doc["user_id"])
    
    db = get_db()
    res = await db.resumes.delete_one({"id": resume_id, "user_id": user_id})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Resume not found")
        
    return {"success": True, "message": "Resume deleted successfully"}
