from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import Response, Request, HTTPException
from pathlib import Path
from typing import Optional
from app.core.config import (
    PROJECT_ENVIRONMENT,
    JWT_EXPIRES,
    JWT_ALGORITHM,
)


is_prod = PROJECT_ENVIRONMENT == "PRODUCTION"

BASE_DIR = Path(__file__).resolve().parent
try:
    SECURITY_DIR = BASE_DIR.parent / "core" / "security"
    PRIVATE_KEY = (SECURITY_DIR / "private.pem").read_text()
    PUBLIC_KEY = (SECURITY_DIR / "public.pem").read_text()
except FileNotFoundError as e:
    raise RuntimeError(f"JWT key files not found: {e}")


def generate_token(user_id: str, response: Response) -> bool:
    try:
        payload = {
            "sub": user_id,
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(days=JWT_EXPIRES),
        }
        token = jwt.encode(
            payload,
            PRIVATE_KEY,
            algorithm=JWT_ALGORITHM,
        )
        response.set_cookie(
            key="user",
            value=token,
            httponly=True,
            secure=is_prod,
            samesite="lax" if not is_prod else "none",
            path="/",
        )
        return True
    except Exception as e:
        print(f"JWT generation error: {e}")
        return False


def verify_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(
            token,
            PUBLIC_KEY,
            algorithms=[JWT_ALGORITHM],
        )
        return payload
    except JWTError as e:
        print(f"JWT verification failed: {e}")
        return None


async def check_token(request: Request):
    token = request.cookies.get("user")

    if not token:
        return

    try:
        jwt.decode(token, PUBLIC_KEY, algorithms=[JWT_ALGORITHM])
        raise HTTPException(status_code=400, detail="You are already logged in")

    except JWTError:
        return
