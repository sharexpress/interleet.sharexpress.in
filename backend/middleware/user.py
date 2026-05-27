from fastapi import Request, HTTPException
import logging
from app.core.db import get_db
from app.utils.JWT import verify_token

db = get_db()


logger = logging.getLogger(__name__)


class Middleware:
    @staticmethod
    async def me(request: Request):
        try:
            token = request.cookies.get("user")
            if not token:
                raise HTTPException(status_code=401, detail="Unauthorized")
            payload = verify_token(token)
            if not payload:
                raise HTTPException(status_code=401, detail="Invalid token")
            user_id = payload.get("sub")
            user = await db.users.find_one({"user_id": user_id}, {"_id": 0})
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return {"success": True, "user": user}
        except HTTPException:
            raise
        except Exception:
            logger.exception("Fetch current user failed")
            raise HTTPException(status_code=500, detail="Internal server error")
