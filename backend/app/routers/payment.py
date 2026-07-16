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

from fastapi import APIRouter, Depends, Body, HTTPException
from app.controllers.payment import PaymentController
from app.middleware.user import Middleware as UserMiddleware

router = APIRouter(prefix="/api/payment", tags=["Payment"])

@router.post("/create-order")
async def create_order(
    payload: dict = Body(default={}),
    user_auth=Depends(UserMiddleware.me)
):
    user_id = user_auth["user"]["user_id"]
    amount_paise = payload.get("amount", 14900)
    return await PaymentController.create_order(user_id, amount_paise=amount_paise)

@router.post("/verify-payment")
async def verify_payment(
    payload: dict = Body(...),
    user_auth=Depends(UserMiddleware.me)
):
    user_id = user_auth["user"]["user_id"]
    order_id = payload.get("order_id")
    payment_id = payload.get("payment_id")
    signature = payload.get("signature")

    if not order_id or not payment_id or not signature:
        raise HTTPException(
            status_code=400,
            detail="Missing required fields: order_id, payment_id, and signature are all required."
        )

    return await PaymentController.verify_payment(
        user_id=user_id,
        order_id=order_id,
        payment_id=payment_id,
        signature=signature
    )

@router.get("/orders")
async def get_orders(
    user_auth=Depends(UserMiddleware.me)
):
    user_id = user_auth["user"]["user_id"]
    return await PaymentController.get_orders(user_id)

