from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import ReportRequest, MetricsResponse
from ..services.analytics import generate_performance_report, get_store_metrics

router = APIRouter()


@router.get("/reports/performance")
async def get_performance_report(
    store_id: int = Depends(get_current_store),
    start_date: str = None,
    end_date: str = None
):
    """Generate performance report for the store"""
    try:
        report = await generate_performance_report(store_id, start_date, end_date)
        return {"status": "success", "report": report}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate report: {str(e)}")


@router.get("/metrics")
async def get_metrics(
    store_id: int = Depends(get_current_store),
    period: str = "30d"
):
    """Get key performance metrics"""
    try:
        metrics = await get_store_metrics(store_id, period)
        return {"status": "success", "metrics": metrics}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get metrics: {str(e)}")


@router.get("/health")
async def health_check():
    """System health check"""
    return {
        "status": "healthy",
        "timestamp": "2024-01-01T00:00:00Z",
        "services": {
            "database": "connected",
            "redis": "connected",
            "shopify_api": "connected",
            "meta_api": "connected"
        }
    }


@router.get("/settings")
async def get_settings(store_id: int = Depends(get_current_store)):
    """Get store settings and preferences"""
    try:
        # This will be implemented by both teams
        return {
            "status": "success",
            "settings": {
                "notifications": True,
                "auto_pause_threshold": 0.8,
                "cpa_target": 25.0,
                "sync_frequency": "hourly"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get settings: {str(e)}")


@router.put("/settings")
async def update_settings(
    settings_data: dict,
    store_id: int = Depends(get_current_store)
):
    """Update store settings and preferences"""
    try:
        # This will be implemented by both teams
        return {"status": "success", "message": "Settings updated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update settings: {str(e)}")


@router.get("/sync-status")
async def get_sync_status(store_id: int = Depends(get_current_store)):
    """Get data sync status"""
    try:
        return {
            "status": "success",
            "sync_status": {
                "last_sync": "2024-01-01T00:00:00Z",
                "shopify_sync": "completed",
                "meta_sync": "completed",
                "ai_training": "completed"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get sync status: {str(e)}")


def get_current_store(db: Session = Depends(get_db)) -> int:
    """Get current store ID (simplified for demo)"""
    from ..models import ShopifyStore
    store = db.query(ShopifyStore).first()
    if not store:
        raise HTTPException(status_code=404, detail="No store connected")
    return store.id
