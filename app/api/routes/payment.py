from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class PaymentRequest(BaseModel):
    amount: float
    currency: str = "usd"

@router.post("/stripe/checkout")
def create_checkout_session(request: PaymentRequest):
    # Mock checkout session
    return {
        "checkout_url": f"https://checkout.stripe.com/mock/{request.amount}"
    }

@router.post("/paymob/iframe")
def get_paymob_iframe(request: PaymentRequest):
    # Mock paymob iframe
    return {
        "iframe_url": "https://accept.paymob.com/api/acceptance/iframes/123456"
    }
