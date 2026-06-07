from fastapi import Request, HTTPException
from app.middleware.user import Middleware as UserMiddleware

class AdminMiddleware:
    @staticmethod
    async def is_admin(request: Request):
        user_auth = await UserMiddleware.me(request)
        user = user_auth.get("user")
        if not user or user.get("email") != "santushtkotai1221@gmail.com" or user.get("role") != "admin":
            raise HTTPException(status_code=403, detail="Access denied. Admin access only.")
        return user
