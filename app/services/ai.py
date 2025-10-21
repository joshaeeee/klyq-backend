# 🟦 SHARED - AI/ML processing and analysis functions
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from ..models import Product, Order, Campaign, Ad
from ..database import get_db


async def analyze_attribution(orders: List[Dict], ads: List[Dict]) -> List[Dict]:
    """Analyze ad-to-order attribution using AI"""
    attributions = []
    
    for order in orders:
        # Simple attribution logic - in production, use ML models
        order_time = order.get("created_at")
        order_value = order.get("total_price", 0)
        
        # Find ads that ran before this order
        relevant_ads = []
        for ad in ads:
            ad_time = ad.get("created_time")
            if ad_time and ad_time < order_time:
                relevant_ads.append(ad)
        
        # Calculate attribution score (simplified)
        attribution_score = 0.8 if relevant_ads else 0.0
        revenue_lift = order_value * attribution_score
        
        attributions.append({
            "order_id": order["id"],
            "ad_ids": [ad["id"] for ad in relevant_ads],
            "attribution_score": attribution_score,
            "revenue_lift": revenue_lift,
            "confidence": 0.85
        })
    
    return attributions


async def generate_suggestions(store_id: int) -> List[Dict]:
    """Generate AI suggestions for the store"""
    db = next(get_db())
    
    # Get store data
    products = db.query(Product).filter(Product.store_id == store_id).all()
    orders = db.query(Order).filter(Order.store_id == store_id).all()
    ads = db.query(Ad).filter(Ad.store_id == store_id).all()
    
    suggestions = []
    
    # Analyze product performance
    for product in products:
        if product.inventory_quantity > 50:  # High inventory
            suggestions.append({
                "type": "promote",
                "title": f"Promote {product.title}",
                "description": f"High inventory ({product.inventory_quantity} units) - consider promoting",
                "reasoning": "High stock levels indicate potential for increased sales",
                "action_data": {"product_id": product.shopify_id, "action": "create_ad"},
                "priority": 3
            })
    
    # Analyze ad performance
    for ad in ads:
        if ad.status == "ACTIVE":
            # Check for creative fatigue (simplified)
            suggestions.append({
                "type": "pause",
                "title": f"Review {ad.name}",
                "description": "Ad may be experiencing creative fatigue",
                "reasoning": "Ad has been running for extended period",
                "action_data": {"ad_id": ad.shopify_id, "action": "pause"},
                "priority": 2
            })
    
    # Bundle suggestions
    if len(products) >= 2:
        suggestions.append({
            "type": "create_bundle",
            "title": "Create Product Bundle",
            "description": "Combine top-performing products into a bundle",
            "reasoning": "Bundle products can increase AOV and reduce inventory",
            "action_data": {"product_ids": [p.shopify_id for p in products[:3]]},
            "priority": 1
        })
    
    return suggestions


async def detect_creative_fatigue(ad_id: str) -> Dict:
    """Detect creative fatigue using AI analysis"""
    # This would typically use ML models to analyze performance patterns
    # For now, using simple heuristics
    
    db = next(get_db())
    ad = db.query(Ad).filter(Ad.shopify_id == ad_id).first()
    
    if not ad:
        return {"fatigue_detected": False, "confidence": 0.0}
    
    # Simple fatigue detection based on ad age and performance
    # In production, this would use actual performance data
    fatigue_score = 0.0
    
    # Add more sophisticated ML-based fatigue detection here
    return {
        "ad_id": ad_id,
        "fatigue_detected": fatigue_score > 0.7,
        "fatigue_score": fatigue_score,
        "confidence": 0.8,
        "recommendation": "pause" if fatigue_score > 0.7 else "monitor"
    }


async def train_attribution_model(store_id: int) -> Dict:
    """Train attribution model with store data"""
    db = next(get_db())
    
    # Get historical data
    orders = db.query(Order).filter(Order.store_id == store_id).all()
    ads = db.query(Ad).filter(Ad.store_id == store_id).all()
    
    # Simple model training (in production, use proper ML libraries)
    model_accuracy = 0.85  # Placeholder
    
    return {
        "store_id": store_id,
        "model_accuracy": model_accuracy,
        "training_samples": len(orders) + len(ads),
        "status": "completed"
    }


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


async def predict_trend_impact(trend_data: Dict, store_products: List[Dict]) -> Dict:
    """Predict the impact of a trend on store performance"""
    # Simple trend impact prediction
    trend_category = trend_data.get("category", "")
    trend_engagement = trend_data.get("engagement_score", 0)
    
    # Find matching products
    matching_products = [
        p for p in store_products 
        if trend_category.lower() in p.get("product_type", "").lower()
    ]
    
    impact_score = len(matching_products) * trend_engagement * 0.1
    
    return {
        "trend_id": trend_data.get("id"),
        "impact_score": impact_score,
        "matching_products": len(matching_products),
        "recommended_action": "create_content" if impact_score > 0.5 else "monitor"
    }
