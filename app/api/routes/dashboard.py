from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Dict
from app.db.session import get_db
from app.models.user import User
from app.models.order import Order
from app.models.product import Product
from app.core.dependencies import get_current_admin
from sqlalchemy.sql import func
import redis
import json
from app.core.config import settings

router = APIRouter()

# Simple Redis connection
try:
    r = redis.from_url(settings.REDIS_URL, decode_responses=True)
except Exception:
    r = None

@router.get("/stats")
def get_dashboard_stats(db: Session = Depends(get_db), current_user: User = Depends(get_current_admin)):
    if r:
        try:
            cached_stats = r.get("dashboard_stats")
            if cached_stats:
                return json.loads(cached_stats)
        except redis.ConnectionError:
            pass

    users_count = db.query(User).count()
    orders_count = db.query(Order).count()
    revenue = db.query(func.sum(Order.total_price)).scalar() or 0.0

    stats = {
        "users": users_count,
        "orders": orders_count,
        "revenue": revenue
    }
    
    if r:
        try:
            r.setex("dashboard_stats", 60, json.dumps(stats))
        except redis.ConnectionError:
            pass
        
    return stats
