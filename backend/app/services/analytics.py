# 🟦 SHARED - Analytics and reporting functions
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from ..models import Product, Order, Campaign, Ad
from ..database import get_db


async def calculate_rpmo(orders: List[Dict], impressions: int) -> float:
    """Calculate Revenue Per Mille Organic impressions"""
    if impressions == 0:
        return 0.0
    
    total_revenue = sum(order.get("total_price", 0) for order in orders)
    return (total_revenue / impressions) * 1000


async def calculate_cpa(spend: float, conversions: int) -> float:
    """Calculate Cost Per Acquisition"""
    if conversions == 0:
        return 0.0
    return spend / conversions


async def calculate_ctr(clicks: int, impressions: int) -> float:
    """Calculate Click-Through Rate"""
    if impressions == 0:
        return 0.0
    return (clicks / impressions) * 100


async def calculate_aov(orders: List[Dict]) -> float:
    """Calculate Average Order Value"""
    if not orders:
        return 0.0
    
    total_revenue = sum(order.get("total_price", 0) for order in orders)
    return total_revenue / len(orders)


async def calculate_conversion_rate(conversions: int, clicks: int) -> float:
    """Calculate Conversion Rate"""
    if clicks == 0:
        return 0.0
    return (conversions / clicks) * 100


async def get_store_metrics(store_id: int, period: str = "30d") -> Dict:
    """Get key performance metrics for a store"""
    db = next(get_db())
    
    # Calculate date range
    end_date = datetime.now()
    if period == "7d":
        start_date = end_date - timedelta(days=7)
    elif period == "30d":
        start_date = end_date - timedelta(days=30)
    elif period == "90d":
        start_date = end_date - timedelta(days=90)
    else:
        start_date = end_date - timedelta(days=30)
    
    # Get orders in period
    orders = db.query(Order).filter(
        Order.store_id == store_id,
        Order.created_at >= start_date,
        Order.created_at <= end_date
    ).all()
    
    # Get ads in period
    ads = db.query(Ad).filter(Ad.store_id == store_id).all()
    
    # Calculate metrics
    total_revenue = sum(order.total_price for order in orders)
    total_orders = len(orders)
    total_impressions = 10000  # Placeholder - would come from ads data
    total_clicks = 1000  # Placeholder - would come from ads data
    total_spend = 5000.0  # Placeholder - would come from ads data
    
    rpmo = await calculate_rpmo([{"total_price": o.total_price} for o in orders], total_impressions)
    cpa = await calculate_cpa(total_spend, total_orders)
    ctr = await calculate_ctr(total_clicks, total_impressions)
    aov = await calculate_aov([{"total_price": o.total_price} for o in orders])
    conversion_rate = await calculate_conversion_rate(total_orders, total_clicks)
    
    return {
        "period": period,
        "total_revenue": total_revenue,
        "total_orders": total_orders,
        "rpmo": round(rpmo, 2),
        "cpa": round(cpa, 2),
        "ctr": round(ctr, 2),
        "aov": round(aov, 2),
        "conversion_rate": round(conversion_rate, 2),
        "total_spend": total_spend,
        "roi": round((total_revenue - total_spend) / total_spend * 100, 2) if total_spend > 0 else 0
    }


async def generate_performance_report(store_id: int, start_date: str = None, end_date: str = None) -> Dict:
    """Generate comprehensive performance report"""
    db = next(get_db())
    
    # Parse dates
    if start_date:
        start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
    else:
        start_dt = datetime.now() - timedelta(days=30)
    
    if end_date:
        end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
    else:
        end_dt = datetime.now()
    
    # Get data
    orders = db.query(Order).filter(
        Order.store_id == store_id,
        Order.created_at >= start_dt,
        Order.created_at <= end_dt
    ).all()
    
    products = db.query(Product).filter(Product.store_id == store_id).all()
    campaigns = db.query(Campaign).filter(Campaign.store_id == store_id).all()
    
    # Calculate metrics
    metrics = await get_store_metrics(store_id, "30d")
    
    # Top performing products
    product_sales = {}
    for order in orders:
        # Simplified - in production, would track individual product sales
        product_sales["top_product"] = product_sales.get("top_product", 0) + 1
    
    # Campaign performance
    campaign_performance = []
    for campaign in campaigns:
        campaign_performance.append({
            "id": campaign.shopify_id,
            "name": campaign.name,
            "status": campaign.status,
            "daily_budget": campaign.daily_budget,
            "performance": "good"  # Placeholder
        })
    
    return {
        "store_id": store_id,
        "period": {
            "start_date": start_dt.isoformat(),
            "end_date": end_dt.isoformat()
        },
        "metrics": metrics,
        "top_products": list(product_sales.keys())[:5],
        "campaign_performance": campaign_performance,
        "recommendations": [
            "Increase budget for top-performing campaigns",
            "Pause underperforming ads",
            "Create bundle for slow-moving products"
        ]
    }


async def track_attribution(store_id: int, order_id: str, ad_id: str) -> Dict:
    """Track attribution between ads and orders"""
    db = next(get_db())
    
    # Get order and ad data
    order = db.query(Order).filter(
        Order.store_id == store_id,
        Order.shopify_id == order_id
    ).first()
    
    ad = db.query(Ad).filter(
        Ad.store_id == store_id,
        Ad.shopify_id == ad_id
    ).first()
    
    if not order or not ad:
        return {"attribution": "not_found"}
    
    # Calculate attribution score (simplified)
    attribution_score = 0.8  # Placeholder - would use ML model
    revenue_lift = order.total_price * attribution_score
    
    return {
        "order_id": order_id,
        "ad_id": ad_id,
        "attribution_score": attribution_score,
        "revenue_lift": revenue_lift,
        "confidence": 0.85
    }


async def get_performance_trends(store_id: int, metric: str, days: int = 30) -> List[Dict]:
    """Get performance trends for a specific metric"""
    db = next(get_db())
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    # Get daily data
    daily_data = []
    for i in range(days):
        date = start_date + timedelta(days=i)
        
        # Get orders for this day
        orders = db.query(Order).filter(
            Order.store_id == store_id,
            Order.created_at >= date,
            Order.created_at < date + timedelta(days=1)
        ).all()
        
        if metric == "revenue":
            value = sum(order.total_price for order in orders)
        elif metric == "orders":
            value = len(orders)
        else:
            value = 0
        
        daily_data.append({
            "date": date.isoformat(),
            "value": value
        })
    
    return daily_data
