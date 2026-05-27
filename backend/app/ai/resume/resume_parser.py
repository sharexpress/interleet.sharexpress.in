from __future__ import annotations

from pathlib import Path


class ResumeParser:
    @staticmethod
    async def parse_resume(file_path: str) -> dict:
        path = Path(file_path)
        text = ""

        if path.suffix.lower() in {".txt", ".md"}:
            text = path.read_text(encoding="utf-8", errors="ignore")

        return {
            "summary": text[:1200] if text else "",
            "skills": [],
            "projects": [],
            "technologies": [],
            "experience": [],
            "source_file": path.name,
        }
