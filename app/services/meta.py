# 🟨 ADS TEAM - All Meta/Facebook ads API integration functions
import httpx
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from ..models import Campaign, Ad, MetaAccount
from ..database import get_db


async def fetch_campaigns(ad_account_id: str, access_token: str) -> List[Dict]:
    """Fetch campaigns from Meta ad account"""
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://graph.facebook.com/v18.0/{ad_account_id}/campaigns",
            headers=headers,
            params={"fields": "id,name,status,objective,daily_budget,created_time"}
        )
        
        if response.status_code == 200:
            data = response.json()
            return data.get("data", [])
        return []


async def fetch_ads(campaign_id: str, access_token: str) -> List[Dict]:
    """Fetch ads from Meta campaign"""
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://graph.facebook.com/v18.0/{campaign_id}/ads",
            headers=headers,
            params={"fields": "id,name,status,creative,created_time"}
        )
        
        if response.status_code == 200:
            data = response.json()
            return data.get("data", [])
        return []


async def fetch_ad_insights(ad_id: str, access_token: str) -> Dict:
    """Fetch ad performance insights"""
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://graph.facebook.com/v18.0/{ad_id}/insights",
            headers=headers,
            params={
                "fields": "impressions,clicks,spend,conversions,ctr,cpc,cpa",
                "date_preset": "last_30d"
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            return data.get("data", [{}])[0] if data.get("data") else {}
        return {}


async def pause_campaign(ad_id: str, store_id: int) -> Dict:
    """Pause a specific ad campaign"""
    # Get store's Meta access token
    store = get_meta_account_by_store_id(store_id)
    if not store:
        raise Exception("Meta account not found")
    
    headers = {
        "Authorization": f"Bearer {store.access_token}",
        "Content-Type": "application/json"
    }
    
    data = {"status": "PAUSED"}
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://graph.facebook.com/v18.0/{ad_id}",
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to pause ad: {response.text}")


async def create_ad_variant(
    campaign_id: str,
    creative_data: Dict,
    targeting: Optional[Dict] = None,
    store_id: int = None
) -> Dict:
    """Create a new ad variant"""
    store = get_meta_account_by_store_id(store_id)
    if not store:
        raise Exception("Meta account not found")
    
    headers = {
        "Authorization": f"Bearer {store.access_token}",
        "Content-Type": "application/json"
    }
    
    ad_data = {
        "name": creative_data.get("name", "New Ad Variant"),
        "campaign_id": campaign_id,
        "creative": creative_data,
        "status": "ACTIVE"
    }
    
    if targeting:
        ad_data["targeting"] = targeting
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://graph.facebook.com/v18.0/act_{store.ad_account_id}/ads",
            headers=headers,
            json=ad_data
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to create ad variant: {response.text}")


async def sync_campaigns_to_db(store_id: int, campaigns_data: List[Dict]) -> None:
    """Sync campaigns data to database"""
    db = next(get_db())
    
    for campaign_data in campaigns_data:
        # Check if campaign already exists
        existing_campaign = db.query(Campaign).filter(
            Campaign.store_id == store_id,
            Campaign.shopify_id == str(campaign_data["id"])
        ).first()
        
        if existing_campaign:
            # Update existing campaign
            existing_campaign.name = campaign_data.get("name", "")
            existing_campaign.status = campaign_data.get("status", "")
            existing_campaign.objective = campaign_data.get("objective", "")
            existing_campaign.daily_budget = float(campaign_data.get("daily_budget", 0))
        else:
            # Create new campaign
            new_campaign = Campaign(
                store_id=store_id,
                shopify_id=str(campaign_data["id"]),
                name=campaign_data.get("name", ""),
                status=campaign_data.get("status", ""),
                objective=campaign_data.get("objective", ""),
                daily_budget=float(campaign_data.get("daily_budget", 0)),
                currency="USD"
            )
            db.add(new_campaign)
    
    db.commit()


async def sync_ads_to_db(store_id: int, ads_data: List[Dict]) -> None:
    """Sync ads data to database"""
    db = next(get_db())
    
    for ad_data in ads_data:
        # Check if ad already exists
        existing_ad = db.query(Ad).filter(
            Ad.store_id == store_id,
            Ad.shopify_id == str(ad_data["id"])
        ).first()
        
        if existing_ad:
            # Update existing ad
            existing_ad.name = ad_data.get("name", "")
            existing_ad.status = ad_data.get("status", "")
        else:
            # Create new ad
            new_ad = Ad(
                store_id=store_id,
                shopify_id=str(ad_data["id"]),
                name=ad_data.get("name", ""),
                status=ad_data.get("status", ""),
                campaign_id=ad_data.get("campaign_id", ""),
                creative_id=ad_data.get("creative", {}).get("id", "")
            )
            db.add(new_ad)
    
    db.commit()


def get_meta_account_by_store_id(store_id: int) -> Optional[MetaAccount]:
    """Get Meta account by store ID"""
    db = next(get_db())
    return db.query(MetaAccount).filter(MetaAccount.store_id == store_id).first()


async def detect_creative_fatigue(ad_id: str, access_token: str) -> Dict:
    """Detect if ad has creative fatigue"""
    insights = await fetch_ad_insights(ad_id, access_token)
    
    # Simple fatigue detection based on CTR drop
    ctr = insights.get("ctr", 0)
    impressions = insights.get("impressions", 0)
    
    fatigue_score = 0
    if ctr < 0.01:  # Low CTR
        fatigue_score += 0.5
    if impressions > 10000 and ctr < 0.02:  # High impressions, low CTR
        fatigue_score += 0.3
    
    return {
        "ad_id": ad_id,
        "fatigue_score": fatigue_score,
        "is_fatigued": fatigue_score > 0.5,
        "recommendation": "pause" if fatigue_score > 0.7 else "monitor"
    }
