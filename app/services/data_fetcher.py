import httpx
from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from ..models import Product, Order, ShopifyStore


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


def sync_products_to_database(store_id: int, products_data: List[Dict], db: Session):
    """Sync products data to database"""
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
            
            # Get price from first variant
            variants = product_data.get("variants", [])
            if variants:
                variant = variants[0]
                existing_product.price = float(variant.get("price", 0))
                existing_product.compare_at_price = float(variant.get("compare_at_price", 0)) if variant.get("compare_at_price") else None
                existing_product.sku = variant.get("sku", "")
                existing_product.inventory_quantity = variant.get("inventory_quantity", 0)
                existing_product.weight = float(variant.get("weight", 0))
        else:
            # Create new product
            variants = product_data.get("variants", [])
            price = 0
            compare_at_price = None
            sku = ""
            inventory_quantity = 0
            weight = 0
            
            if variants:
                variant = variants[0]
                price = float(variant.get("price", 0))
                compare_at_price = float(variant.get("compare_at_price", 0)) if variant.get("compare_at_price") else None
                sku = variant.get("sku", "")
                inventory_quantity = variant.get("inventory_quantity", 0)
                weight = float(variant.get("weight", 0))
            
            new_product = Product(
                store_id=store_id,
                shopify_id=str(product_data["id"]),
                title=product_data.get("title", ""),
                handle=product_data.get("handle", ""),
                description=product_data.get("body_html", ""),
                vendor=product_data.get("vendor", ""),
                product_type=product_data.get("product_type", ""),
                status=product_data.get("status", ""),
                price=price,
                compare_at_price=compare_at_price,
                sku=sku,
                inventory_quantity=inventory_quantity,
                weight=weight
            )
            db.add(new_product)
    
    db.commit()


def sync_orders_to_database(store_id: int, orders_data: List[Dict], db: Session):
    """Sync orders data to database"""
    for order_data in orders_data:
        # Check if order already exists
        existing_order = db.query(Order).filter(
            Order.store_id == store_id,
            Order.shopify_id == str(order_data["id"])
        ).first()
        
        if not existing_order:
            # Create new order
            new_order = Order(
                store_id=store_id,
                shopify_id=str(order_data["id"]),
                order_number=str(order_data.get("order_number", "")),
                email=order_data.get("email", ""),
                total_price=float(order_data.get("total_price", 0)),
                subtotal_price=float(order_data.get("subtotal_price", 0)),
                total_tax=float(order_data.get("total_tax", 0)),
                currency=order_data.get("currency", ""),
                financial_status=order_data.get("financial_status", ""),
                fulfillment_status=order_data.get("fulfillment_status", ""),
                processed_at=order_data.get("processed_at")
            )
            db.add(new_order)
    
    db.commit()
