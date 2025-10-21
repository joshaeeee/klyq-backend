# 🟦 SHARED - ALL background tasks (Celery)
from celery import Celery
from celery.schedules import crontab
from app.services import shopify, meta, ai, trends, analytics
from app.database import get_db
from app.models import Product, Order, Campaign, Ad, Trend
import asyncio

# Initialize Celery
celery = Celery('clique_workers')

# Celery configuration
celery.conf.update(
    broker_url='redis://localhost:6379/0',
    result_backend='redis://localhost:6379/0',
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

# === STORE SETUP TASKS (One-time when store connects) ===
@celery.task
def import_historical_data(store_id: int, shop_url: str, access_token: str):
    """Import 6 months of historical data from Shopify"""
    try:
        # Import products
        products = asyncio.run(shopify.fetch_products(shop_url, access_token))
        asyncio.run(shopify.sync_products_to_db(store_id, products))
        
        # Import orders (last 6 months)
        orders = asyncio.run(shopify.fetch_orders(shop_url, access_token, limit=250))
        asyncio.run(shopify.sync_orders_to_db(store_id, orders))
        
        # Import inventory
        inventory = asyncio.run(shopify.fetch_inventory(shop_url, access_token))
        asyncio.run(shopify.sync_inventory_to_db(store_id, inventory))
        
        return {"status": "completed", "products": len(products), "orders": len(orders)}
    except Exception as e:
        return {"status": "failed", "error": str(e)}


@celery.task
def setup_ai_cold_start(store_id: int, shop_url: str):
    """Setup AI models with cold-start data"""
    try:
        # Get store data
        db = next(get_db())
        products = db.query(Product).filter(Product.store_id == store_id).all()
        
        # Use Meta Ad Library for initial priors
        product_types = list(set(p.product_type for p in products))
        ad_library_data = []
        
        for product_type in product_types:
            trends_data = asyncio.run(trends.fetch_meta_ad_library_trends(product_type))
            ad_library_data.extend(trends_data)
        
        # Train initial attribution model
        model_result = asyncio.run(ai.train_attribution_model(store_id))
        
        return {"status": "completed", "model_accuracy": model_result.get("model_accuracy", 0.0)}
    except Exception as e:
        return {"status": "failed", "error": str(e)}


@celery.task
def create_baseline_metrics(store_id: int):
    """Create baseline performance metrics"""
    try:
        # Calculate baseline metrics
        metrics = asyncio.run(analytics.get_store_metrics(store_id, "30d"))
        
        # Save baseline metrics (simplified)
        baseline_data = {
            "store_id": store_id,
            "rpmo_target": metrics.get("rpmo", 0) * 1.2,  # 20% above current
            "cpa_target": metrics.get("cpa", 0) * 0.8,   # 20% below current
            "aov_target": metrics.get("aov", 0) * 1.1,   # 10% above current
        }
        
        return {"status": "completed", "baseline": baseline_data}
    except Exception as e:
        return {"status": "failed", "error": str(e)}


# === SCHEDULED JOBS (Cron tasks) ===
@celery.task
def detect_trends():
    """Detect viral trends every 15 minutes"""
    try:
        # Get all stores
        db = next(get_db())
        stores = db.query(Product).distinct(Product.store_id).all()
        
        for store in stores:
            # Get store product types
            products = db.query(Product).filter(Product.store_id == store.store_id).all()
            product_types = list(set(p.product_type for p in products))
            
            # Detect trends for each product type
            for product_type in product_types:
                trends_data = asyncio.run(trends.detect_viral_trends(product_type))
                
                # Save trends to database
                for trend in trends_data:
                    asyncio.run(trends.save_trend_to_db(trend, store.store_id))
        
        return {"status": "completed", "trends_detected": len(trends_data)}
    except Exception as e:
        return {"status": "failed", "error": str(e)}


@celery.task
def run_diagnostics():
    """Run diagnostic analysis every 2 hours"""
    try:
        # Get all stores
        db = next(get_db())
        stores = db.query(Product).distinct(Product.store_id).all()
        
        for store in stores:
            # Run AI diagnostics
            suggestions = asyncio.run(ai.generate_suggestions(store.store_id))
            
            # Check for creative fatigue
            ads = db.query(Ad).filter(Ad.store_id == store.store_id).all()
            for ad in ads:
                fatigue_result = asyncio.run(ai.detect_creative_fatigue(ad.shopify_id))
                if fatigue_result.get("fatigue_detected"):
                    # Auto-pause fatigued ads
                    asyncio.run(meta.pause_campaign(ad.shopify_id, store.store_id))
        
        return {"status": "completed", "diagnostics_run": len(stores)}
    except Exception as e:
        return {"status": "failed", "error": str(e)}


@celery.task
def train_ai_models():
    """Train AI models daily"""
    try:
        # Get all stores
        db = next(get_db())
        stores = db.query(Product).distinct(Product.store_id).all()
        
        for store in stores:
            # Retrain attribution model
            asyncio.run(ai.train_attribution_model(store.store_id))
        
        return {"status": "completed", "models_trained": len(stores)}
    except Exception as e:
        return {"status": "failed", "error": str(e)}


@celery.task
def cleanup_old_data():
    """Cleanup old data weekly"""
    try:
        from datetime import datetime, timedelta
        
        # Archive old orders (older than 1 year)
        cutoff_date = datetime.now() - timedelta(days=365)
        db = next(get_db())
        
        old_orders = db.query(Order).filter(Order.created_at < cutoff_date).all()
        for order in old_orders:
            # Archive order (simplified)
            pass
        
        return {"status": "completed", "archived_orders": len(old_orders)}
    except Exception as e:
        return {"status": "failed", "error": str(e)}


# === WEBHOOK PROCESSING (Real-time) ===
@celery.task
def process_shopify_order_webhook(webhook_data: dict):
    """Process Shopify order webhook immediately"""
    try:
        order_id = webhook_data.get("id")
        shop_domain = webhook_data.get("shop_domain")
        
        # Get store
        db = next(get_db())
        store = db.query(ShopifyStore).filter(ShopifyStore.shop_url == shop_domain).first()
        if not store:
            return {"status": "failed", "error": "Store not found"}
        
        # Process order for attribution
        attribution_result = asyncio.run(ai.analyze_attribution([webhook_data], []))
        
        # Update metrics
        asyncio.run(analytics.track_attribution(store.id, str(order_id), ""))
        
        return {"status": "completed", "order_id": order_id}
    except Exception as e:
        return {"status": "failed", "error": str(e)}


@celery.task
def process_meta_ad_webhook(webhook_data: dict):
    """Process Meta ad webhook immediately"""
    try:
        ad_id = webhook_data.get("id")
        ad_account_id = webhook_data.get("ad_account_id")
        
        # Process ad performance update
        # This would update ad performance metrics
        
        return {"status": "completed", "ad_id": ad_id}
    except Exception as e:
        return {"status": "failed", "error": str(e)}


# === USER-TRIGGERED TASKS ===
@celery.task
def sync_data_task(store_id: int):
    """Manual data sync task"""
    try:
        # Get store
        db = next(get_db())
        store = db.query(ShopifyStore).filter(ShopifyStore.id == store_id).first()
        if not store:
            return {"status": "failed", "error": "Store not found"}
        
        # Sync Shopify data
        products = asyncio.run(shopify.fetch_products(store.shop_url, store.access_token))
        asyncio.run(shopify.sync_products_to_db(store_id, products))
        
        orders = asyncio.run(shopify.fetch_orders(store.shop_url, store.access_token))
        asyncio.run(shopify.sync_orders_to_db(store_id, orders))
        
        # Sync Meta data (if connected)
        # This would be implemented by the Ads team
        
        return {"status": "completed", "products_synced": len(products), "orders_synced": len(orders)}
    except Exception as e:
        return {"status": "failed", "error": str(e)}


# === CELERY BEAT SCHEDULE ===
celery.conf.beat_schedule = {
    'detect-trends': {
        'task': 'workers.detect_trends',
        'schedule': crontab(minute='*/15'),  # Every 15 minutes
    },
    'run-diagnostics': {
        'task': 'workers.run_diagnostics',
        'schedule': crontab(minute=0, hour='*/2'),  # Every 2 hours
    },
    'train-ai-models': {
        'task': 'workers.train_ai_models',
        'schedule': crontab(hour=2, minute=0),  # Daily at 2 AM
    },
    'cleanup-old-data': {
        'task': 'workers.cleanup_old_data',
        'schedule': crontab(hour=3, minute=0, day_of_week=0),  # Weekly on Sunday at 3 AM
    },
}
