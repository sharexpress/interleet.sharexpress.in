import os
from pathlib import Path


from dotenv import load_dotenv

load_dotenv()

PROJECT_ENVIRONMENT = os.getenv("PROJECT_ENVIRONMENT", "DEVELOPMENT")

# DATABASE CONFIGURATION
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")


SESSION_SECRET_KEY = os.getenv("SESSION_SECRET_KEY", "interleet-dev-session-secret")


# REDIS CONFIGURATION

REDIS_HOST = os.getenv("REDIS_HOST", None)
REDIS_PORT = os.getenv("REDIS_PORT", None)


# JWT
JWT_SECRET = os.getenv("JWT_SECRET", "interleet-dev-jwt-secret")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRES = int(os.getenv("JWT_EXPIRES", 7))


# FRONTEND / CORS
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
BACKEND_CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "BACKEND_CORS_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173",
    ).split(",")
    if origin.strip()
]


# GOOGLE OAUTH CLIENT
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_CLIENT_URL = os.getenv("")


# GITHUB OAUTH CLIENT

GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")


# AI CONFIGURATION

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

AI_PROVIDER = os.getenv("AI_PROVIDER", "groq")
AI_MODEL = os.getenv("AI_MODEL", "llama-3.3-70b-versatile")
AI_FALLBACK_PROVIDER = os.getenv("AI_FALLBACK_PROVIDER", "")
AI_FALLBACK_MODEL = os.getenv("AI_FALLBACK_MODEL", "")
AI_REQUEST_TIMEOUT_SECONDS = float(os.getenv("AI_REQUEST_TIMEOUT_SECONDS", 30))
AI_MAX_RETRIES = int(os.getenv("AI_MAX_RETRIES", 2))

INTERVIEW_SESSION_TTL_SECONDS = int(os.getenv("INTERVIEW_SESSION_TTL_SECONDS", 60 * 60 * 6))


# CODE EXECUTION / JUDGE0
JUDGE0_API_URL = os.getenv("JUDGE0_API_URL", "https://judge0-ce.p.rapidapi.com")
JUDGE0_API_KEY = os.getenv("JUDGE0_API_KEY", "")
JUDGE0_RAPIDAPI_HOST = os.getenv("JUDGE0_RAPIDAPI_HOST", "judge0-ce.p.rapidapi.com")
JUDGE0_CALLBACK_URL = os.getenv("JUDGE0_CALLBACK_URL", "")
