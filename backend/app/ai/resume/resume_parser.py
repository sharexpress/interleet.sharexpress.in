"""
ResumeParser — downloads a PDF from a URL (Cloudinary), extracts text
via PyMuPDF, then sends it to the AI to produce a structured response
with both `parsed_resume` and `mock_test` sections.
"""
from __future__ import annotations

import json
import logging
import re

import fitz          # PyMuPDF
import httpx

logger = logging.getLogger(__name__)

# ── Prompt template ──────────────────────────────────────────────────────────
SYSTEM_PROMPT = (
    "You are a precise technical resume parser. "
    "You return ONLY valid JSON — no markdown fences, no explanations."
)

USER_PROMPT_TEMPLATE = """
Parse the following resume and return JSON matching this exact schema:

{{
  "parsed_resume": {{
    "summary": "<2–4 sentence professional summary>",
    "skills": ["skill1", "skill2"],
    "technologies": ["tech1", "tech2"],
    "experience": [
      {{
        "company": "Company Name",
        "role": "Job Title",
        "duration": "Jan 2022 – Present",
        "highlights": ["achievement 1", "achievement 2"]
      }}
    ],
    "projects": [
      {{
        "name": "Project Name",
        "description": "Short description",
        "technologies": ["React", "Node.js"]
      }}
    ]
  }},
  "mock_test": {{
    "topics": ["topic1", "topic2", "topic3", "topic4", "topic5"],
    "max_questions": 8
  }}
}}

Rules:
- skills: ALL technical + soft skills mentioned
- technologies: only named tools / frameworks / languages
- mock_test.topics: 5 interview focus areas derived from the candidate's strongest background
- mock_test.max_questions: always 8
- Empty list [] for any missing field; never omit keys

RESUME TEXT:
{resume_text}
"""


class ResumeParser:
    # ── Public entry points ──────────────────────────────────────────────────

    @staticmethod
    async def parse_from_url(pdf_url: str) -> dict:
        """Download PDF from URL → extract text → AI parse."""
        try:
            text = await ResumeParser._text_from_url(pdf_url)
        except Exception as exc:
            logger.error("Failed to download/extract PDF from URL: %s", exc)
            return ResumeParser._fallback()
        return await ResumeParser._ai_parse(text)

    @staticmethod
    async def parse_from_bytes(pdf_bytes: bytes) -> dict:
        """Parse from raw bytes — used when file is already in memory."""
        try:
            text = await ResumeParser._text_from_bytes(pdf_bytes)
        except Exception as exc:
            logger.error("Failed to extract PDF bytes: %s", exc)
            return ResumeParser._fallback()
        return await ResumeParser._ai_parse(text)

    # Backwards-compat shim (old route used a local file path)
    @staticmethod
    async def parse_resume(file_path: str) -> dict:
        from pathlib import Path
        path = Path(file_path)
        if path.suffix.lower() == ".pdf":
            return await ResumeParser.parse_from_bytes(path.read_bytes())
        text = path.read_text(encoding="utf-8", errors="ignore")
        return await ResumeParser._ai_parse(text)

    # ── Internal helpers ─────────────────────────────────────────────────────

    @staticmethod
    async def _text_from_url(url: str) -> str:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.get(url)
            resp.raise_for_status()
        return await ResumeParser._text_from_bytes(resp.content)

    @staticmethod
    async def _text_from_bytes(pdf_bytes: bytes) -> str:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        pages = [page.get_text("text") for page in doc]
        doc.close()
        return "\n".join(pages).strip()

    @staticmethod
    async def _ai_parse(resume_text: str) -> dict:
        # Import here to avoid circular import at module load time
        from app.ai.services.ai_client import ai_client

        # Truncate to ~4 000 chars to stay within token budget
        truncated = resume_text[:4000]
        user_msg = USER_PROMPT_TEMPLATE.format(resume_text=truncated)

        try:
            raw = await ai_client.generate_text(
                system=SYSTEM_PROMPT,
                user=user_msg,
                temperature=0.1,
            )
            # Strip any accidental markdown fences the model added
            clean = re.sub(r"```(?:json)?", "", raw).strip().strip("`")
            # Grab the outermost JSON object
            start = clean.find("{")
            end = clean.rfind("}")
            if start == -1 or end == -1:
                raise ValueError("No JSON object found in AI response")
            data = json.loads(clean[start : end + 1])
            return data
        except json.JSONDecodeError as exc:
            logger.error("AI returned non-JSON: %s", exc)
            return ResumeParser._fallback()
        except Exception as exc:
            logger.error("AI parse error: %s", exc)
            return ResumeParser._fallback()

    @staticmethod
    def _fallback() -> dict:
        return {
            "parsed_resume": {
                "summary": "Resume could not be parsed automatically.",
                "skills": [],
                "technologies": [],
                "experience": [],
                "projects": [],
            },
            "mock_test": {
                "topics": [
                    "General problem-solving",
                    "Data structures",
                    "System design basics",
                    "Coding best practices",
                    "Behavioral questions",
                ],
                "max_questions": 8,
            },
        }
