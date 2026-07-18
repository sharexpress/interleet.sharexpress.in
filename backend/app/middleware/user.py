# Copyright 2026 Sharexpress Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
                auth_header = request.headers.get("Authorization")
                if auth_header and auth_header.lower().startswith("bearer "):
                    token = auth_header[7:].strip()
            
            if not token:
                raise HTTPException(status_code=401, detail="Unauthorized")
            payload = verify_token(token)
            if not payload:
                raise HTTPException(status_code=401, detail="Invalid token")
            user_id = payload.get("sub")
            user = await db.users.find_one({"user_id": user_id}, {"_id": 0})
            user["is_premium"] = True
            user["plan"] = "Pro"
            return {"success": True, "user": user}
        except HTTPException:
            raise
        except Exception:
            logger.exception("Fetch current user failed")
            raise HTTPException(status_code=500, detail="Internal server error")
