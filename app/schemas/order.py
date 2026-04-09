from pydantic import BaseModel
from typing import List, Optional

class OrderTrackingBase(BaseModel):
    status: str

class OrderTrackingResponse(OrderTrackingBase):
    id: int
    order_id: int

    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    total_price: float
    status: str = "pending"

class OrderResponse(OrderBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
