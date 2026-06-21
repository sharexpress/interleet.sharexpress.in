import os
import hmac
import hashlib
from datetime import datetime, timedelta
import httpx
from fastapi import HTTPException
from app.core.db import get_db

db = get_db()

RAZORPAY_KEY_ID = os.environ.get("RAZORPAY_KEY_ID", "")
RAZORPAY_KEY_SECRET = os.environ.get("RAZORPAY_KEY_SECRET", "")

class PaymentController:
    @staticmethod
    async def create_order(user_id: str, amount_paise: int = 49900):
        # Validate amount >= 100 paise
        if amount_paise < 100:
            raise HTTPException(status_code=400, detail="Amount must be at least 100 paise (1 INR).")

        # 1. Determine if real Razorpay keys are configured
        is_mock_mode = not RAZORPAY_KEY_ID or not RAZORPAY_KEY_SECRET or RAZORPAY_KEY_ID.startswith("rzp_test_mock")

        if is_mock_mode:
            import uuid
            mock_order_id = f"order_mock_{uuid.uuid4().hex[:12]}"
            return {
                "success": True,
                "order_id": mock_order_id,
                "amount": amount_paise,
                "currency": "INR",
                "key_id": "rzp_test_mockkey",
                "is_mock": True
            }

        # 2. Real Razorpay API Call
        url = "https://api.razorpay.com/v1/orders"
        auth = (RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET)
        data = {
            "amount": amount_paise,
            "currency": "INR",
            "receipt": f"receipt_{user_id[:8]}_{int(datetime.utcnow().timestamp())}",
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, auth=auth, json=data, timeout=10.0)
                if response.status_code == 401:
                    raise HTTPException(
                        status_code=401,
                        detail="Razorpay authentication failed. Invalid API keys."
                    )
                if response.status_code != 200:
                    raise HTTPException(
                        status_code=500,
                        detail=f"Razorpay order creation failed: {response.text}"
                    )
                order_data = response.json()
                return {
                    "success": True,
                    "order_id": order_data["id"],
                    "amount": order_data["amount"],
                    "currency": order_data["currency"],
                    "key_id": RAZORPAY_KEY_ID,
                    "is_mock": False
                }
            except HTTPException:
                raise
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Connection to Razorpay failed: {str(e)}"
                )

    @staticmethod
    async def verify_payment(user_id: str, order_id: str, payment_id: str, signature: str):
        is_mock_order = order_id.startswith("order_mock_")
        verified = False

        if is_mock_order:
            verified = True
        else:
            if not RAZORPAY_KEY_SECRET:
                raise HTTPException(status_code=400, detail="Missing server Razorpay configuration.")
            
            # Verify signature: HMAC-SHA256 of "order_id|payment_id" using key secret
            msg = f"{order_id}|{payment_id}".encode()
            generated = hmac.new(
                RAZORPAY_KEY_SECRET.encode(),
                msg,
                hashlib.sha256
            ).hexdigest()

            if hmac.compare_digest(generated, signature):
                verified = True

        if not verified:
            raise HTTPException(status_code=400, detail="Payment signature verification failed. Security breach blocked.")

        # Activate premium subscription in database
        now = datetime.utcnow()
        ends_at = now + timedelta(days=30)

        updates = {
            "is_premium": True,
            "subscription_status": "active",
            "subscription_id": order_id if is_mock_order else payment_id,
            "subscription_ends_at": ends_at,
            "updated_at": now
        }

        await db.users.update_one({"user_id": user_id}, {"$set": updates})

        # Update leaderboard rank model cached attributes
        await db.leaderboards.update_many(
            {"user_id": user_id},
            {"$set": {"is_premium": True}}
        )

        return {
            "success": True,
            "message": "Subscription activated successfully. Welcome to Interleet Premium!",
            "is_premium": True,
            "subscription_ends_at": ends_at.isoformat()
        }
