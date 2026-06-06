"""
Interleet Judge Engine — Docker Image Pool
Verifies sandbox images exist on startup and provides pull utilities.
"""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass

import docker
import docker.errors

from app.engine.docker.sandbox import get_docker_client
from app.engine.enums import Language

logger = logging.getLogger(__name__)

# Map language → Docker image name
LANGUAGE_IMAGES: dict[Language, str] = {
    Language.PYTHON: "interleet-python:latest",
    Language.JAVASCRIPT: "interleet-node:latest",
    Language.TYPESCRIPT: "interleet-typescript:latest",
    Language.GO: "interleet-go:latest",
    Language.CPP: "interleet-cpp:latest",
    Language.RUST: "interleet-rust:latest",
    Language.JAVA: "interleet-java:latest",
}


@dataclass
class ImageStatus:
    language: str
    image: str
    available: bool
    error: str = ""


async def verify_sandbox_images() -> list[ImageStatus]:
    """
    Check which sandbox images are available locally.
    Called during FastAPI startup.
    """
    loop = asyncio.get_event_loop()
    statuses: list[ImageStatus] = []

    for language, image in LANGUAGE_IMAGES.items():
        status = await loop.run_in_executor(None, _check_image, language, image)
        statuses.append(status)
        if status.available:
            logger.info("✅ Sandbox image ready: %s → %s", language.value, image)
        else:
            logger.warning(
                "⚠️  Sandbox image missing: %s → %s | Run: make build-sandboxes",
                language.value,
                image,
            )

    return statuses


def _check_image(language: Language, image: str) -> ImageStatus:
    try:
        get_docker_client().images.get(image)
        return ImageStatus(language=language.value, image=image, available=True)
    except docker.errors.ImageNotFound:
        return ImageStatus(
            language=language.value,
            image=image,
            available=False,
            error="Image not found locally",
        )
    except Exception as exc:
        return ImageStatus(
            language=language.value,
            image=image,
            available=False,
            error=str(exc),
        )


async def get_available_languages() -> list[str]:
    """Return list of languages with available Docker images."""
    statuses = await verify_sandbox_images()
    return [s.language for s in statuses if s.available]
