from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import Product, Order, ShopifyStore
from ..services.data_fetcher import fetch_products, fetch_orders, fetch_inventory, sync_products_to_database, sync_orders_to_database
from pydantic import BaseModel

router = APIRouter()


class ProductResponse(BaseModel):
    id: int
    shopify_id: str
    title: str
    handle: str
    description: str
    vendor: str
    product_type: str
    status: str
    price: float
    compare_at_price: float = None
    sku: str
    inventory_quantity: int
    weight: float
    created_at: str
    updated_at: str = None

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: int
    shopify_id: str
    order_number: str
    email: str
    total_price: float
    subtotal_price: float
    total_tax: float
    currency: str
    financial_status: str
    fulfillment_status: str
    processed_at: str = None
    created_at: str
    updated_at: str = None

    class Config:
        from_attributes = True


@router.get("/products", response_model=List[ProductResponse])
async def get_products(db: Session = Depends(get_db)):
    """Get all products from connected store"""
    # For demo purposes, get the first store
    store = db.query(ShopifyStore).first()
    if not store:
        raise HTTPException(status_code=404, detail="No Shopify store connected")
    
    products = db.query(Product).filter(Product.store_id == store.id).all()
    return products


@router.get("/orders", response_model=List[OrderResponse])
async def get_orders(db: Session = Depends(get_db)):
    """Get all orders from connected store"""
    # For demo purposes, get the first store
    store = db.query(ShopifyStore).first()
    if not store:
        raise HTTPException(status_code=404, detail="No Shopify store connected")
    
    orders = db.query(Order).filter(Order.store_id == store.id).all()
    return orders


@router.get("/inventory")
async def get_inventory(db: Session = Depends(get_db)):
    """Get inventory levels from connected store"""
    # For demo purposes, get the first store
    store = db.query(ShopifyStore).first()
    if not store:
        raise HTTPException(status_code=404, detail="No Shopify store connected")
    
    inventory_data = await fetch_inventory(store.shop_url, store.access_token)
    return {"inventory_levels": inventory_data}


@router.post("/sync")
async def sync_data(db: Session = Depends(get_db)):
    """Trigger manual sync of all data from Shopify"""
    # For demo purposes, get the first store
    store = db.query(ShopifyStore).first()
    if not store:
        raise HTTPException(status_code=404, detail="No Shopify store connected")
    
    try:
        # Fetch data from Shopify
        products_data = await fetch_products(store.shop_url, store.access_token)
        orders_data = await fetch_orders(store.shop_url, store.access_token)
        
        # Sync to database
        sync_products_to_database(store.id, products_data, db)
        sync_orders_to_database(store.id, orders_data, db)
        
        return {
            "message": "Data synced successfully",
            "products_synced": len(products_data),
            "orders_synced": len(orders_data)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sync failed: {str(e)}")


@router.get("/store-info")
async def get_store_info(db: Session = Depends(get_db)):
    """Get connected store information"""
    store = db.query(ShopifyStore).first()
    if not store:
        raise HTTPException(status_code=404, detail="No Shopify store connected")
    
    return {
        "shop_url": store.shop_url,
        "scopes": store.scopes,
        "created_at": store.created_at,
        "products_count": db.query(Product).filter(Product.store_id == store.id).count(),
        "orders_count": db.query(Order).filter(Order.store_id == store.id).count()
    }
