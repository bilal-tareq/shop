from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.cart import CartItem
from app.models.order import Order, OrderTracking
from app.models.user import User
from app.schemas.order import OrderResponse, OrderTrackingResponse
from app.core.dependencies import get_current_user

router = APIRouter()

@router.post("/checkout", response_model=OrderResponse)
def checkout(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    cart_items = db.query(CartItem).filter(CartItem.user_id == current_user.id).all()
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")
        
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    
    # Create order
    new_order = Order(user_id=current_user.id, total_price=total_price, status="pending")
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    
    # Create initial tracking
    tracking = OrderTracking(order_id=new_order.id, status="pending")
    db.add(tracking)
    
    # Clear cart
    for item in cart_items:
        db.delete(item)
        
    db.commit()
    return new_order

@router.get("/", response_model=List[OrderResponse])
def get_orders(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    orders = db.query(Order).filter(Order.user_id == current_user.id).all()
    return orders

@router.get("/{order_id}/tracking", response_model=List[OrderTrackingResponse])
def get_order_tracking(order_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == current_user.id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
        
    trackings = db.query(OrderTracking).filter(OrderTracking.order_id == order_id).all()
    return trackings
