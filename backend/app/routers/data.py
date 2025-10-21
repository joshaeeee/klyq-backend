from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import Product, Order, ShopifyStore
from ..schemas import ProductResponse, OrderResponse, InventoryResponse, StoreInfoResponse
from ..services.shopify import fetch_products_from_db, fetch_orders_from_db, fetch_inventory_from_db

router = APIRouter()


def get_current_store(db: Session = Depends(get_db)) -> int:
    """Get current store ID (simplified for demo)"""
    store = db.query(ShopifyStore).first()
    if not store:
        raise HTTPException(status_code=404, detail="No store connected")
    return store.id


@router.get("/products", response_model=List[ProductResponse])
async def get_products(store_id: int = Depends(get_current_store)):
    """Get all products for the current store"""
    products = await fetch_products_from_db(store_id)
    return products


@router.get("/orders", response_model=List[OrderResponse])
async def get_orders(store_id: int = Depends(get_current_store)):
    """Get all orders for the current store"""
    orders = await fetch_orders_from_db(store_id)
    return orders


@router.get("/inventory", response_model=List[InventoryResponse])
async def get_inventory(store_id: int = Depends(get_current_store)):
    """Get inventory levels for the current store"""
    inventory = await fetch_inventory_from_db(store_id)
    return inventory


@router.get("/store-info", response_model=StoreInfoResponse)
async def get_store_info(store_id: int = Depends(get_current_store), db: Session = Depends(get_db)):
    """Get store information and metrics"""
    store = db.query(ShopifyStore).filter(ShopifyStore.id == store_id).first()
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    
    products_count = db.query(Product).filter(Product.store_id == store_id).count()
    orders_count = db.query(Order).filter(Order.store_id == store_id).count()
    
    return StoreInfoResponse(
        shop_url=store.shop_url,
        scopes=store.scopes,
        created_at=store.created_at,
        products_count=products_count,
        orders_count=orders_count
    )


@router.get("/campaigns")
async def get_campaigns(store_id: int = Depends(get_current_store)):
    """Get campaigns for the current store"""
    # This will be implemented by the Ads team
    return {"message": "Campaigns endpoint - to be implemented by Ads team"}


@router.get("/ads")
async def get_ads(store_id: int = Depends(get_current_store)):
    """Get ads for the current store"""
    # This will be implemented by the Ads team
    return {"message": "Ads endpoint - to be implemented by Ads team"}


@router.get("/performance")
async def get_performance(store_id: int = Depends(get_current_store)):
    """Get performance metrics for the current store"""
    # This will be implemented by the Analytics team
    return {"message": "Performance endpoint - to be implemented by Analytics team"}


@router.get("/suggestions")
async def get_suggestions(store_id: int = Depends(get_current_store)):
    """Get AI suggestions for the current store"""
    # This will be implemented by the AI team
    return {"message": "Suggestions endpoint - to be implemented by AI team"}


@router.get("/trends")
async def get_trends(store_id: int = Depends(get_current_store)):
    """Get trending content for the current store"""
    # This will be implemented by the Ads team
    return {"message": "Trends endpoint - to be implemented by Ads team"}
