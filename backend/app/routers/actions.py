from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import BundleCreateRequest, PriceUpdateRequest, AdVariantRequest
from ..services.shopify import create_bundle, update_pricing
from ..services.meta import pause_campaign, create_ad_variant
from ..workers import sync_data_task

router = APIRouter()


# === SHOPIFY ACTIONS (🟦 SHOPIFY TEAM) ===
@router.post("/create-bundle")
async def create_product_bundle(
    bundle_data: BundleCreateRequest,
    store_id: int = Depends(get_current_store)
):
    """Create a new product bundle"""
    try:
        result = await create_bundle(
            store_id=store_id,
            title=bundle_data.title,
            product_ids=bundle_data.product_ids,
            price=bundle_data.price,
            description=bundle_data.description
        )
        return {"status": "success", "bundle_id": result["id"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create bundle: {str(e)}")


@router.post("/update-pricing")
async def update_product_pricing(
    price_data: PriceUpdateRequest,
    store_id: int = Depends(get_current_store)
):
    """Update product pricing"""
    try:
        result = await update_pricing(
            store_id=store_id,
            product_id=price_data.product_id,
            new_price=price_data.new_price
        )
        return {"status": "success", "updated": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update pricing: {str(e)}")


# === META ACTIONS (🟨 ADS TEAM) ===
@router.post("/pause-ad")
async def pause_ad_campaign(ad_id: str, store_id: int = Depends(get_current_store)):
    """Pause a specific ad campaign"""
    try:
        result = await pause_campaign(ad_id=ad_id, store_id=store_id)
        return {"status": "success", "paused": True, "ad_id": ad_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to pause ad: {str(e)}")


@router.post("/create-ad-variant")
async def create_ad_variant_endpoint(
    variant_data: AdVariantRequest,
    store_id: int = Depends(get_current_store)
):
    """Create a new ad variant"""
    try:
        result = await create_ad_variant(
            campaign_id=variant_data.campaign_id,
            creative_data=variant_data.creative_data,
            targeting=variant_data.targeting,
            store_id=store_id
        )
        return {"status": "success", "variant_id": result["id"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create ad variant: {str(e)}")


# === SHARED ACTIONS ===
@router.post("/sync-data")
async def sync_data(store_id: int = Depends(get_current_store)):
    """Trigger manual data sync"""
    try:
        # Queue background sync task
        sync_data_task.delay(store_id)
        return {"status": "accepted", "message": "Data sync started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start sync: {str(e)}")


@router.post("/launch-campaign")
async def launch_campaign(
    campaign_data: dict,
    store_id: int = Depends(get_current_store)
):
    """Launch a new campaign (1-click action)"""
    try:
        # This will be implemented by the Ads team
        return {"status": "success", "message": "Campaign launch - to be implemented by Ads team"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to launch campaign: {str(e)}")


@router.post("/generate-bundle-suggestion")
async def generate_bundle_suggestion(store_id: int = Depends(get_current_store)):
    """Generate AI-powered bundle suggestion"""
    try:
        # This will be implemented by the AI team
        return {"status": "success", "message": "Bundle suggestion - to be implemented by AI team"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate suggestion: {str(e)}")


@router.post("/replicate-trend")
async def replicate_trend(
    trend_id: int,
    store_id: int = Depends(get_current_store)
):
    """Replicate a viral trend for the store"""
    try:
        # This will be implemented by the Ads team
        return {"status": "success", "message": "Trend replication - to be implemented by Ads team"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to replicate trend: {str(e)}")


def get_current_store(db: Session = Depends(get_db)) -> int:
    """Get current store ID (simplified for demo)"""
    from ..models import ShopifyStore
    store = db.query(ShopifyStore).first()
    if not store:
        raise HTTPException(status_code=404, detail="No store connected")
    return store.id
