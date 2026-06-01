from fastapi import HTTPException, Response, Request
from datetime import datetime
from uuid import uuid4
import logging
import hashlib
import secrets
from app.models.users import UserModel as User
from app.models.users import OTPverify as OTP
from app.core.db import get_db
from app.core.config import PROJECT_ENVIRONMENT
from app.utils.OTP import (
    sendOTP,
    VerifyOTPbyUtils,
)
from app.utils.JWT import (
    generate_token,
)
from app.lib.generateOTP import generateOTP
from app.core.oauth import oauth
from authlib.integrations.base_client.errors import OAuthError


from fastapi.responses import RedirectResponse


logger = logging.getLogger(__name__)
is_prod = PROJECT_ENVIRONMENT == "PRODUCTION"


db = get_db()


class UserController:
    @staticmethod
    def _hash_password(password: str, salt: str | None = None) -> tuple[str, str]:
        salt = salt or secrets.token_hex(16)
        digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 120000)
        return salt, digest.hex()

    @staticmethod
    def _public_user(user: dict) -> dict:
        public = dict(user)
        public.pop("_id", None)
        public.pop("password_hash", None)
        public.pop("password_salt", None)
        return public

    @staticmethod
    async def register(payload, response: Response):
        existing = await db.users.find_one({"email": payload.email})
        if existing:
            raise HTTPException(status_code=409, detail="Email is already registered")

        user_id = str(uuid4())
        salt, password_hash = UserController._hash_password(payload.password)
        full_name = " ".join(
            part for part in [payload.first_name, payload.last_name] if part
        ).strip() or None
        username = payload.username or payload.email.split("@")[0]
        new_user = {
            "user_id": user_id,
            "email": payload.email,
            "username": username,
            "full_name": full_name,
            "role": "user",
            "auth_provider": "password",
            "password_salt": salt,
            "password_hash": password_hash,
            "frontend_rating": 0,
            "backend_rating": 0,
            "fullstack_rating": 0,
            "devops_rating": 0,
            "overall_rating": 1200,
            "solved_problems": [],
            "badges": [],
            "streak_count": 0,
            "is_verified": True,
            "is_active": True,
            "is_locked": False,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "last_login": datetime.utcnow(),
        }
        await db.users.insert_one(new_user)
        generate_token(user_id, response)
        return {"success": True, "user": UserController._public_user(new_user)}

    @staticmethod
    async def login(payload, response: Response):
        existing_user = await db.users.find_one({"email": payload.email})
        if not existing_user:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        salt = existing_user.get("password_salt")
        expected = existing_user.get("password_hash")
        if not salt or not expected:
            raise HTTPException(status_code=400, detail="Use your original sign-in provider")
        _, actual = UserController._hash_password(payload.password, salt)
        if not secrets.compare_digest(actual, expected):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        if existing_user.get("is_locked"):
            raise HTTPException(status_code=403, detail="Account is locked")
        if not existing_user.get("is_active", True):
            raise HTTPException(status_code=403, detail="Account is inactive")

        await db.users.update_one(
            {"email": payload.email},
            {"$set": {"updated_at": datetime.utcnow(), "last_login": datetime.utcnow()}},
        )
        generate_token(existing_user["user_id"], response)
        return {"success": True, "user": UserController._public_user(existing_user)}

    @staticmethod
    async def send_otp(user: User):
        try:
            if not user.email:
                raise HTTPException(status_code=400, detail="Email is required")

            otp_code = generateOTP()

            otp_response = await sendOTP(user.email, otp_code)

            if not otp_response.get("success"):
                raise HTTPException(status_code=400, detail="Failed to send OTP")

            return {
                "success": True,
                "message": f"OTP sent to {user.email}",
                "transactionID": otp_response.get("transactionID"),
            }

        except HTTPException:
            raise
        except Exception as e:
            logger.exception(f"Send OTP failed: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

    @staticmethod
    async def verify_otp(payload: OTP, response: Response, request: Request):
        try:
            verify_result = await VerifyOTPbyUtils(payload.transactionID, payload.OTP)

            if not verify_result.get("valid"):
                raise HTTPException(
                    status_code=400, detail=verify_result.get("reason", "Invalid OTP")
                )

            user_email = verify_result.get("email")
            if not user_email:
                raise HTTPException(status_code=400, detail="Email not found")

            existing_user = await db.users.find_one({"email": user_email})

            if not existing_user:
                user_id = str(uuid4())
                new_user = {
                    "user_id": user_id,
                    "email": user_email,
                    "role": "user",
                    "auth_provider": "OTP",
                    "frontend_rating": 0,
                    "backend_rating": 0,
                    "fullstack_rating": 0,
                    "devops_rating": 0,
                    "overall_rating": 0,
                    "solved_problems": [],
                    "badges": [],
                    "streak_count": 0,
                    "is_verified": True,
                    "is_active": True,
                    "is_locked": False,
                    "created_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow(),
                    "last_login": datetime.utcnow(),
                }
                await db.users.insert_one(new_user)
                generate_token(user_id, response)

                if request.cookies.get("guest_session"):
                    response.delete_cookie(
                        key="guest_session",
                        httponly=True,
                        samesite="lax",
                        secure=is_prod,
                    )
                return {"success": True, "message": "User created successfully"}

            if existing_user.get("is_locked"):
                raise HTTPException(status_code=403, detail="Account is locked")
            if not existing_user.get("is_active", True):
                raise HTTPException(status_code=403, detail="Account is inactive")

            await db.users.update_one(
                {"email": user_email},
                {
                    "$set": {
                        "is_verified": True,
                        "updated_at": datetime.utcnow(),
                        "last_login": datetime.utcnow(),
                    }
                },
            )

            generate_token(existing_user["user_id"], response)

            if request.cookies.get("guest_session"):
                response.delete_cookie(
                    key="guest_session",
                    httponly=True,
                    samesite="lax",
                    secure=is_prod,
                )
            return {"success": True, "message": "Login successful"}
        except HTTPException:
            raise
        except Exception as e:
            logger.exception(f"Verify OTP failed: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

    @staticmethod
    async def google_login(request: Request):
        try:
            redirect_uri = "http://localhost:8000/auth/google/callback"
            return await oauth.google.authorize_redirect(
                request,
                redirect_uri,
                prompt="select_account consent",
                access_type="offline",
            )

        except HTTPException:
            raise
        except Exception as e:
            print(f"Error in redirect_to_uri: {e}")
            raise HTTPException(
                status_code=500, detail="Failed to initiate Google login"
            )

    @staticmethod
    async def google_callback(request: Request):
        try:
            token = await oauth.google.authorize_access_token(request)
            user_info = token.get("userinfo")
            if not user_info:
                raise HTTPException(
                    status_code=400, detail="Google authentication failed"
                )

            email = user_info.get("email")
            avatar = user_info.get("picture")
            google_sub = user_info.get("sub")
            if not email:
                raise HTTPException(
                    status_code=400, detail="Email not provided by Google"
                )

            existing_user = await db.users.find_one(
                {
                    "$or": [
                        {"email": email},
                        {"google_sub": google_sub},
                    ]
                }
            )

            if not existing_user:
                user_id = str(uuid4())
                new_user = {
                    "user_id": user_id,
                    "email": email,
                    "username": None,
                    "full_name": None,
                    "avatar": avatar,
                    "google_sub": google_sub,
                    "auth_provider": "google",
                    "onboarding_completed": False,
                    "role": "user",
                    "frontend_rating": 0,
                    "backend_rating": 0,
                    "fullstack_rating": 0,
                    "devops_rating": 0,
                    "overall_rating": 0,
                    "solved_problems": [],
                    "badges": [],
                    "streak_count": 0,
                    "is_verified": True,
                    "is_active": True,
                    "is_locked": False,
                    "created_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow(),
                    "last_login": datetime.utcnow(),
                }
                await db.users.insert_one(new_user)
                response = RedirectResponse(url="http://localhost:5173/onboarding")
                generate_token(user_id, response)
                return response

            if existing_user.get("is_locked"):
                raise HTTPException(status_code=403, detail="Account is locked")
            if not existing_user.get("is_active", True):
                raise HTTPException(status_code=403, detail="Account is inactive")

            await db.users.update_one(
                {"email": email},
                {
                    "$set": {
                        "updated_at": datetime.utcnow(),
                        "last_login": datetime.utcnow(),
                        "avatar": avatar,
                    }
                },
            )

            redirect_url = "http://localhost:5173"
            if not existing_user.get("onboarding_completed"):
                redirect_url = "http://localhost:5173/onboarding"
            response = RedirectResponse(url=redirect_url)
            generate_token(existing_user["user_id"], response)
            return response
        except OAuthError:
            raise HTTPException(status_code=400, detail="Google OAuth failed")
        except Exception as e:
            logger.exception(f"Google callback failed: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

    @staticmethod
    async def github_login(request: Request):
        try:
            redirect_uri = "http://localhost:8000/auth/github/callback"
            return await oauth.github.authorize_redirect(request, redirect_uri)
        except Exception:
            logger.exception("GitHub login failed")
            raise HTTPException(
                status_code=500, detail="Failed to initiate GitHub login"
            )

    @staticmethod
    async def github_callback(request: Request):
        try:
            token = await oauth.github.authorize_access_token(request)

            response = await oauth.github.get("user", token=token)
            github_user = response.json()
            github_id = str(github_user.get("id"))
            github_username = github_user.get("login")
            avatar = github_user.get("avatar_url")
            full_name = github_user.get("name")

            email_response = await oauth.github.get("user/emails", token=token)
            emails = email_response.json()
            primary_email = None
            for email_data in emails:
                if email_data.get("primary") and email_data.get("verified"):
                    primary_email = email_data.get("email")
                    break
            if not primary_email:
                raise HTTPException(status_code=400, detail="GitHub email not found")

            existing_user = await db.users.find_one(
                {"$or": [{"email": primary_email}, {"github_id": github_id}]}
            )

            if not existing_user:
                user_id = str(uuid4())
                new_user = {
                    "user_id": user_id,
                    "email": primary_email,
                    "username": None,
                    "full_name": full_name,
                    "avatar": avatar,
                    "github_id": github_id,
                    "github_username": github_username,
                    "auth_provider": "github",
                    "onboarding_completed": False,
                    "role": "user",
                    "frontend_rating": 0,
                    "backend_rating": 0,
                    "fullstack_rating": 0,
                    "devops_rating": 0,
                    "overall_rating": 0,
                    "solved_problems": [],
                    "badges": [],
                    "streak_count": 0,
                    "is_verified": True,
                    "is_active": True,
                    "is_locked": False,
                    "created_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow(),
                    "last_login": datetime.utcnow(),
                }
                await db.users.insert_one(new_user)
                redirect_response = RedirectResponse(
                    url="http://localhost:5173/onboarding"
                )
                generate_token(user_id, redirect_response)
                return redirect_response

            if existing_user.get("is_locked"):
                raise HTTPException(status_code=403, detail="Account is locked")
            if not existing_user.get("is_active", True):
                raise HTTPException(status_code=403, detail="Account is inactive")

            await db.users.update_one(
                {"_id": existing_user["_id"]},
                {
                    "$set": {
                        "github_id": github_id,
                        "github_username": github_username,
                        "avatar": avatar,
                        "updated_at": datetime.utcnow(),
                        "last_login": datetime.utcnow(),
                    }
                },
            )
            redirect_url = "http://localhost:5173"
            if not existing_user.get("onboarding_completed"):
                redirect_url = "http://localhost:5173/onboarding"
            redirect_response = RedirectResponse(url=redirect_url)
            generate_token(existing_user["user_id"], redirect_response)
            return redirect_response
        except OAuthError as e:
            print("GITHUB OAUTH ERROR =", e)
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            print("FULL GITHUB ERROR =", repr(e))
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def logout(response: Response):
        try:
            response.delete_cookie(
                key="user",
                httponly=True,
                secure=is_prod,
                samesite="none" if is_prod else "lax",
                path="/",
            )

            response.delete_cookie(
                key="guest_session",
                httponly=True,
                secure=is_prod,
                samesite="none" if is_prod else "lax",
                path="/",
            )
            return {"success": True, "message": "Logged out successfully"}
        except Exception:
            logger.exception("Logout failed")
            raise HTTPException(status_code=500, detail="Internal server error")
