"""Cloudinary integration — resume / file upload service."""
from __future__ import annotations

import io
import logging
import cloudinary
import cloudinary.uploader
from app.core.config import (
    CLOUDINARY_CLOUD_NAME,
    CLOUDINARY_API_KEY,
    CLOUDINARY_API_SECRET,
)

logger = logging.getLogger(__name__)

# ── Configure Cloudinary SDK once at import time ────────────────────────────
cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET,
    secure=True,
)


async def upload_resume_to_cloudinary(
    file_bytes: bytes,
    original_filename: str,
) -> dict:
    """
    Upload a resume PDF to Cloudinary under the 'resumes/' folder.

    Returns a dict with:
        - secure_url : str  — HTTPS URL to the uploaded file
        - public_id  : str  — Cloudinary asset identifier
        - bytes      : int  — File size
        - format     : str  — File extension (usually 'pdf')
    """
    try:
        result = cloudinary.uploader.upload(
            io.BytesIO(file_bytes),
            resource_type="raw",          # PDFs must be 'raw', not 'image'
            folder="resumes",
            public_id=original_filename.rsplit(".", 1)[0],  # strip extension
            overwrite=True,
            use_filename=True,
            unique_filename=True,
        )
        logger.info("Cloudinary upload success: %s", result.get("public_id"))
        return {
            "secure_url": result["secure_url"],
            "public_id": result["public_id"],
            "bytes": result.get("bytes", 0),
            "format": result.get("format", "pdf"),
        }
    except Exception as exc:
        logger.error("Cloudinary upload failed: %s", exc)
        raise RuntimeError(f"Cloudinary upload error: {exc}") from exc
