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

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.ai.resume.resume_parser import ResumeParser
from app.services.cloudinary_service import upload_resume_to_cloudinary

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/resume", tags=["Resume"])

MAX_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB


@router.post("/parse")
async def parse_resume(file: UploadFile = File(...)):
    """
    Upload a PDF resume to Cloudinary and return AI-parsed structured data.

    Returns:
    ```json
    {
      "cloudinary": { "secure_url": "...", "public_id": "...", "bytes": 0 },
      "parsed_resume": {
        "summary": "...",
        "skills": [...],
        "technologies": [...],
        "experience": [...],
        "projects": [...]
      },
      "mock_test": {
        "topics": [...],
        "max_questions": 8
      }
    }
    ```
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

    return {
        "cloudinary": cloudinary_meta,
        **parsed,         # inlines  parsed_resume  and  mock_test  keys
    }
