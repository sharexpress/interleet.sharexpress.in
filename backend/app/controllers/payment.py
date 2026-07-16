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
    async def create_order(user_id: str, amount_paise: int = 14900):
        # Validate amount must be strictly 14900 paise (149 INR) or 89900 paise (899 INR)
        if amount_paise not in (14900, 89900):
            raise HTTPException(status_code=400, detail="Invalid subscription plan amount.")

        # 1. Determine if real Razorpay keys are configured
        is_mock_mode = not RAZORPAY_KEY_ID or not RAZORPAY_KEY_SECRET or RAZORPAY_KEY_ID.startswith("rzp_test_mock")

        if is_mock_mode:
            import uuid
            mock_order_id = f"order_mock_{uuid.uuid4().hex[:12]}"
            order_doc = {
                "order_id": mock_order_id,
                "user_id": user_id,
                "amount": amount_paise,
                "currency": "INR",
                "status": "created",
                "created_at": datetime.utcnow(),
                "is_mock": True
            }
            await db.orders.insert_one(order_doc)
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
                order_id = order_data["id"]
                order_doc = {
                    "order_id": order_id,
                    "user_id": user_id,
                    "amount": amount_paise,
                    "currency": "INR",
                    "status": "created",
                    "created_at": datetime.utcnow(),
                    "is_mock": False
                }
                await db.orders.insert_one(order_doc)
                return {
                    "success": True,
                    "order_id": order_id,
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
        # 1. Fetch and validate the order from the database
        order = await db.orders.find_one({"order_id": order_id})
        if not order:
            raise HTTPException(status_code=400, detail="Invalid order ID. Order does not exist.")
            
        # 2. Prevent User-Mismatch Attacks: Validate that this order belongs to the requesting user
        if order.get("user_id") != user_id:
            raise HTTPException(status_code=400, detail="Unauthorized payment verification. Mismatched user credentials.")
            
        # 3. Prevent Replay Attacks: Check if order has already been marked paid
        if order.get("status") == "paid":
            raise HTTPException(status_code=400, detail="Replay attack blocked: This order has already been paid for.")
            
        # 4. Check for duplicate payment ID to prevent multiple users verifying the same payment ID
        duplicate_payment = await db.orders.find_one({"payment_id": payment_id})
        if duplicate_payment:
            raise HTTPException(status_code=400, detail="Duplicate payment transaction detected. Verification blocked.")
            
        # 5. A Proper Clock: Enforce strict order expiration timeline (e.g. 30 minutes)
        created_at = order.get("created_at")
        if not created_at:
            raise HTTPException(status_code=400, detail="Order creation time is missing. Verification blocked.")
            
        order_age = datetime.utcnow() - created_at
        if order_age > timedelta(minutes=30):
            raise HTTPException(status_code=400, detail="Payment request expired. Please initiate a new subscription.")
            
        # 6. Signature verification
        is_mock_order = order.get("is_mock", False)
        verified = False

        if is_mock_order:
            # For mock order, signature verify is bypass/mock validation, but still verify that order ID starts with order_mock_
            if order_id.startswith("order_mock_"):
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

        # Update order status to paid
        now = datetime.utcnow()
        await db.orders.update_one(
            {"order_id": order_id},
            {
                "$set": {
                    "status": "paid",
                    "payment_id": payment_id,
                    "signature": signature,
                    "paid_at": now
                }
            }
        )

        # Activate premium subscription in database
        amount = order.get("amount", 14900)
        if amount == 89900:
            ends_at = now + timedelta(days=365)
        else:
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

    @staticmethod
    async def get_orders(user_id: str):
        """Fetch transaction order history for the user from MongoDB."""
        cursor = db.orders.find({"user_id": user_id}).sort("created_at", -1)
        orders_list = []
        async for doc in cursor:
            doc.pop("_id", None)
            created_at = doc.get("created_at")
            if isinstance(created_at, datetime):
                doc["created_at"] = created_at.isoformat()
            paid_at = doc.get("paid_at")
            if isinstance(paid_at, datetime):
                doc["paid_at"] = paid_at.isoformat()
            orders_list.append(doc)
        return {"success": True, "orders": orders_list}
