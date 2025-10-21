# 🟦 SHOPIFY TEAM - All Shopify API integration functions
import httpx
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from ..models import Product, Order, ShopifyStore
from ..database import get_db


async def fetch_products(shop_url: str, access_token: str) -> List[Dict]:
    """Fetch products from Shopify store"""
    headers = {
        "X-Shopify-Access-Token": access_token,
        "Content-Type": "application/json"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://{shop_url}/admin/api/2023-10/products.json",
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            return data.get("products", [])
        return []


async def fetch_orders(shop_url: str, access_token: str, limit: int = 50) -> List[Dict]:
    """Fetch orders from Shopify store"""
    headers = {
        "X-Shopify-Access-Token": access_token,
        "Content-Type": "application/json"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://{shop_url}/admin/api/2023-10/orders.json?limit={limit}",
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            return data.get("orders", [])
        return []


async def fetch_inventory(shop_url: str, access_token: str) -> List[Dict]:
    """Fetch inventory levels from Shopify store"""
    headers = {
        "X-Shopify-Access-Token": access_token,
        "Content-Type": "application/json"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://{shop_url}/admin/api/2023-10/inventory_levels.json",
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            return data.get("inventory_levels", [])
        return []


async def create_bundle(
    store_id: int,
    title: str,
    product_ids: List[int],
    price: float,
    description: Optional[str] = None
) -> Dict:
    """Create a product bundle in Shopify"""
    # Get store access token
    store = get_store_by_id(store_id)
    if not store:
        raise Exception("Store not found")
    
    # Create bundle product in Shopify
    bundle_data = {
        "product": {
            "title": title,
            "body_html": description or "",
            "vendor": "Clique AI",
            "product_type": "Bundle",
            "variants": [{
                "price": str(price),
                "inventory_management": "shopify"
            }]
        }
    }
    
    headers = {
        "X-Shopify-Access-Token": store.access_token,
        "Content-Type": "application/json"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://{store.shop_url}/admin/api/2023-10/products.json",
            headers=headers,
            json=bundle_data
        )
        
        if response.status_code == 201:
            return response.json()["product"]
        else:
            raise Exception(f"Failed to create bundle: {response.text}")


async def update_pricing(store_id: int, product_id: str, new_price: float) -> Dict:
    """Update product pricing in Shopify"""
    store = get_store_by_id(store_id)
    if not store:
        raise Exception("Store not found")
    
    # Update product variant price
    variant_data = {
        "variant": {
            "id": product_id,
            "price": str(new_price)
        }
    }
    
    headers = {
        "X-Shopify-Access-Token": store.access_token,
        "Content-Type": "application/json"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"https://{store.shop_url}/admin/api/2023-10/variants/{product_id}.json",
            headers=headers,
            json=variant_data
        )
        
        if response.status_code == 200:
            return response.json()["variant"]
        else:
            raise Exception(f"Failed to update pricing: {response.text}")


async def sync_products_to_db(store_id: int, products_data: List[Dict]) -> None:
    """Sync products data to database"""
    db = next(get_db())
    
    for product_data in products_data:
        # Check if product already exists
        existing_product = db.query(Product).filter(
            Product.store_id == store_id,
            Product.shopify_id == str(product_data["id"])
        ).first()
        
        if existing_product:
            # Update existing product
            existing_product.title = product_data.get("title", "")
            existing_product.handle = product_data.get("handle", "")
            existing_product.description = product_data.get("body_html", "")
            existing_product.vendor = product_data.get("vendor", "")
            existing_product.product_type = product_data.get("product_type", "")
            existing_product.status = product_data.get("status", "")
        else:
            # Create new product
            variants = product_data.get("variants", [])
            price = 0
            if variants:
                price = float(variants[0].get("price", 0))
            
            new_product = Product(
                store_id=store_id,
                shopify_id=str(product_data["id"]),
                title=product_data.get("title", ""),
                handle=product_data.get("handle", ""),
                description=product_data.get("body_html", ""),
                vendor=product_data.get("vendor", ""),
                product_type=product_data.get("product_type", ""),
                status=product_data.get("status", ""),
                price=price
            )
            db.add(new_product)
    
    db.commit()


async def fetch_products_from_db(store_id: int) -> List[Product]:
    """Fetch products from database"""
    db = next(get_db())
    return db.query(Product).filter(Product.store_id == store_id).all()


async def fetch_orders_from_db(store_id: int) -> List[Order]:
    """Fetch orders from database"""
    db = next(get_db())
    return db.query(Order).filter(Order.store_id == store_id).all()


async def fetch_inventory_from_db(store_id: int) -> List[Dict]:
    """Fetch inventory from database (simplified)"""
    # This would typically query inventory levels
    return []


def get_store_by_id(store_id: int) -> Optional[ShopifyStore]:
    """Get store by ID"""
    db = next(get_db())
    return db.query(ShopifyStore).filter(ShopifyStore.id == store_id).first()


async def exchange_shopify_token(shop_url: str, code: str) -> Optional[Dict]:
    """Exchange authorization code for access token"""
    from ..config import settings
    
    data = {
        "client_id": settings.shopify_api_key,
        "client_secret": settings.shopify_api_secret,
        "code": code
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://{shop_url}/admin/oauth/access_token",
            data=data
        )
        
        if response.status_code == 200:
            return response.json()
        return None


def validate_shopify_hmac(params: Dict) -> bool:
    """Validate Shopify HMAC signature"""
    # Simplified for demo - implement proper HMAC validation
    return True
