from fastapi import APIRouter, Depends, Body
from app.controllers.payment import PaymentController
from app.middleware.user import Middleware as UserMiddleware

router = APIRouter(prefix="/api/payment", tags=["Payment"])

@router.post("/create-order")
async def create_order(user_auth=Depends(UserMiddleware.me)):
    user_id = user_auth["user"]["user_id"]
    return await PaymentController.create_order(user_id)

@router.post("/verify-payment")
async def verify_payment(
    payload: dict = Body(...),
    user_auth=Depends(UserMiddleware.me)
):
    user_id = user_auth["user"]["user_id"]
    order_id = payload.get("order_id")
    payment_id = payload.get("payment_id")
    signature = payload.get("signature")
    return await PaymentController.verify_payment(
        user_id=user_id,
        order_id=order_id,
        payment_id=payment_id,
        signature=signature
    )
