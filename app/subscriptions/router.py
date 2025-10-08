from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import User, Subscription
from app.subscriptions.schemas import SubscriptionCreate, SubscriptionResponse, PlanFeatures
from app.auth.dependencies import get_current_user
from typing import List
from datetime import datetime, timedelta

router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])

PLANS = {
    "free": {
        "name": "Free",
        "price": 0.0,
        "currency": "BRL",
        "features": ["30 swipes por dia", "1 boost por dia", "Matches básicos", "Chat básico"],
        "limits": {"swipes_per_day": 30, "boosts_per_day": 1, "wanted_posts": 2, "offers": 1}
    },
    "pro": {
        "name": "Pro",
        "price": 29.90,
        "currency": "BRL",
        "features": ["Swipes ilimitados", "5 boosts por dia", "Filtros avançados", "Análise por IA", "Relatórios detalhados"],
        "limits": {"swipes_per_day": -1, "boosts_per_day": 5, "wanted_posts": -1, "offers": -1}
    },
    "enterprise": {
        "name": "Enterprise",
        "price": 99.90,
        "currency": "BRL",
        "features": ["Tudo do Pro", "Boosts ilimitados", "Destaque no Explorer", "Suporte prioritário", "API access"],
        "limits": {"swipes_per_day": -1, "boosts_per_day": -1, "wanted_posts": -1, "offers": -1}
    }
}

@router.get("/plans")
def get_plans():
    return PLANS

@router.get("/my-subscription", response_model=SubscriptionResponse)
def get_my_subscription(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    subscription = db.query(Subscription).filter(
        Subscription.user_id == current_user.id
    ).first()
    
    if not subscription:
        # Create free subscription if none exists
        subscription = Subscription(
            user_id=current_user.id,
            plan="free",
            status="active"
        )
        db.add(subscription)
        db.commit()
        db.refresh(subscription)
    
    return subscription

@router.post("/upgrade")
def upgrade_subscription(
    subscription_data: SubscriptionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if subscription_data.plan not in PLANS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid plan"
        )
    
    subscription = db.query(Subscription).filter(
        Subscription.user_id == current_user.id
    ).first()
    
    if subscription:
        subscription.plan = subscription_data.plan
        subscription.status = "active"
        subscription.current_period_start = datetime.utcnow()
        subscription.current_period_end = datetime.utcnow() + timedelta(days=30)
    else:
        subscription = Subscription(
            user_id=current_user.id,
            plan=subscription_data.plan,
            status="active",
            current_period_start=datetime.utcnow(),
            current_period_end=datetime.utcnow() + timedelta(days=30)
        )
        db.add(subscription)
    
    # Update user plan enum
    if subscription_data.plan == "pro":
        current_user.plan = "PRO"
    elif subscription_data.plan == "enterprise":
        current_user.plan = "ENTERPRISE"
    else:
        current_user.plan = "FREE"
    
    db.commit()
    
    return {
        "success": True,
        "plan": subscription_data.plan,
        "message": f"Upgraded to {PLANS[subscription_data.plan]['name']} successfully!",
        "features": PLANS[subscription_data.plan]["features"]
    }

@router.post("/cancel")
def cancel_subscription(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    subscription = db.query(Subscription).filter(
        Subscription.user_id == current_user.id
    ).first()
    
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active subscription found"
        )
    
    subscription.status = "cancelled"
    current_user.plan = "free"
    
    db.commit()
    
    return {"message": "Subscription cancelled successfully"}

@router.get("/usage")
def get_usage_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from app.db.models import Swipe, Match
    from datetime import date
    
    # Get today's usage
    today = date.today()
    today_start = datetime.combine(today, datetime.min.time())
    
    swipes_today = db.query(Swipe).filter(
        Swipe.swiper_id == current_user.id,
        Swipe.created_at >= today_start
    ).count()
    
    # Get this month's matches
    month_start = datetime(today.year, today.month, 1)
    matches_this_month = db.query(Match).filter(
        (Match.user_a_id == current_user.id) | (Match.user_b_id == current_user.id),
        Match.created_at >= month_start
    ).count()
    
    user_plan = getattr(current_user, 'plan', 'FREE').lower()
    if user_plan not in PLANS:
        user_plan = 'free'
    
    return {
        "swipes_today": swipes_today,
        "matches_this_month": matches_this_month,
        "current_plan": user_plan,
        "plan_limits": PLANS[user_plan]["limits"],
        "plan_features": PLANS[user_plan]["features"]
    }