# 🟨 ADS TEAM - Trend detection and analysis functions
import httpx
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from ..models import Trend
from ..database import get_db


async def detect_viral_trends(category: str) -> List[Dict]:
    """Detect viral trends from Meta Ad Library, TikTok, X"""
    trends = []
    
    # Meta Ad Library trends
    meta_trends = await fetch_meta_ad_library_trends(category)
    trends.extend(meta_trends)
    
    # TikTok trends
    tiktok_trends = await fetch_tiktok_trends(category)
    trends.extend(tiktok_trends)
    
    # X (Twitter) trends
    x_trends = await fetch_x_trends(category)
    trends.extend(x_trends)
    
    # Sort by engagement score
    trends.sort(key=lambda x: x.get("engagement_score", 0), reverse=True)
    
    return trends[:10]  # Return top 10 trends


async def fetch_meta_ad_library_trends(category: str) -> List[Dict]:
    """Fetch trends from Meta Ad Library"""
    # This would use Meta Ad Library API
    # For demo, returning mock data
    return [
        {
            "id": "meta_1",
            "platform": "meta",
            "category": category,
            "content": f"Viral {category} trend on Meta",
            "engagement_score": 0.85,
            "relevance_score": 0.9,
            "created_at": datetime.now()
        }
    ]


async def fetch_tiktok_trends(category: str) -> List[Dict]:
    """Fetch trends from TikTok"""
    # This would use TikTok API
    # For demo, returning mock data
    return [
        {
            "id": "tiktok_1",
            "platform": "tiktok",
            "category": category,
            "content": f"#{category} trending on TikTok",
            "engagement_score": 0.92,
            "relevance_score": 0.8,
            "created_at": datetime.now()
        }
    ]


async def fetch_x_trends(category: str) -> List[Dict]:
    """Fetch trends from X (Twitter)"""
    # This would use X API
    # For demo, returning mock data
    return [
        {
            "id": "x_1",
            "platform": "x",
            "category": category,
            "content": f"#{category} trending on X",
            "engagement_score": 0.78,
            "relevance_score": 0.7,
            "created_at": datetime.now()
        }
    ]


async def analyze_trend_relevance(store_products: List[Dict], trend: Dict) -> float:
    """Analyze how relevant a trend is to store products"""
    trend_category = trend.get("category", "").lower()
    trend_keywords = trend.get("content", "").lower().split()
    
    relevance_score = 0.0
    
    for product in store_products:
        product_type = product.get("product_type", "").lower()
        product_title = product.get("title", "").lower()
        
        # Check category match
        if trend_category in product_type:
            relevance_score += 0.5
        
        # Check keyword matches
        keyword_matches = sum(1 for keyword in trend_keywords if keyword in product_title)
        relevance_score += keyword_matches * 0.1
    
    return min(relevance_score, 1.0)


async def generate_trend_creatives(trend_data: Dict, store_products: List[Dict]) -> List[Dict]:
    """Generate creative content based on trending topics"""
    creatives = []
    
    trend_content = trend_data.get("content", "")
    trend_category = trend_data.get("category", "")
    
    # Generate different creative types
    creatives.append({
        "type": "image",
        "content": f"Trending {trend_category} - {trend_content}",
        "style": "modern",
        "call_to_action": "Shop Now"
    })
    
    creatives.append({
        "type": "video",
        "content": f"Join the {trend_category} trend",
        "style": "dynamic",
        "call_to_action": "Learn More"
    })
    
    creatives.append({
        "type": "carousel",
        "content": f"Trending {trend_category} products",
        "style": "showcase",
        "call_to_action": "View Collection"
    })
    
    return creatives


async def save_trend_to_db(trend_data: Dict, store_id: int) -> None:
    """Save trend data to database"""
    db = next(get_db())
    
    trend = Trend(
        store_id=store_id,
        platform=trend_data.get("platform", ""),
        category=trend_data.get("category", ""),
        content=trend_data.get("content", ""),
        engagement_score=trend_data.get("engagement_score", 0.0),
        relevance_score=trend_data.get("relevance_score", 0.0)
    )
    
    db.add(trend)
    db.commit()


async def get_trends_for_store(store_id: int, limit: int = 10) -> List[Dict]:
    """Get trends relevant to a specific store"""
    db = next(get_db())
    
    trends = db.query(Trend).filter(
        Trend.store_id == store_id
    ).order_by(Trend.engagement_score.desc()).limit(limit).all()
    
    return [
        {
            "id": trend.id,
            "platform": trend.platform,
            "category": trend.category,
            "content": trend.content,
            "engagement_score": trend.engagement_score,
            "relevance_score": trend.relevance_score,
            "created_at": trend.created_at
        }
        for trend in trends
    ]


async def replicate_trend_for_store(trend_id: int, store_id: int) -> Dict:
    """Replicate a trend for a specific store"""
    db = next(get_db())
    
    trend = db.query(Trend).filter(Trend.id == trend_id).first()
    if not trend:
        raise Exception("Trend not found")
    
    # Get store products
    from ..models import Product
    products = db.query(Product).filter(Product.store_id == store_id).all()
    
    # Generate creatives based on trend
    creatives = await generate_trend_creatives(
        {
            "content": trend.content,
            "category": trend.category
        },
        [{"title": p.title, "product_type": p.product_type} for p in products]
    )
    
    return {
        "trend_id": trend_id,
        "store_id": store_id,
        "creatives": creatives,
        "status": "generated"
    }
