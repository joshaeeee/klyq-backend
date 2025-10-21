import hmac
import hashlib
import urllib.parse
from typing import Dict, Optional
from ..config import settings


def install_url(shop_url: str) -> str:
    """Generate Shopify OAuth install URL"""
    scopes = "read_products,read_orders,read_inventory"
    redirect_uri = f"{settings.frontend_url}/auth/shopify/callback"
    
    params = {
        "client_id": settings.shopify_api_key,
        "scope": scopes,
        "redirect_uri": redirect_uri,
        "state": "random_state_string"  # In production, use a proper state parameter
    }
    
    query_string = urllib.parse.urlencode(params)
    return f"https://{shop_url}/admin/oauth/authorize?{query_string}"


def validate_hmac(params: Dict[str, str]) -> bool:
    """Validate Shopify HMAC signature"""
    if "hmac" not in params:
        return False
    
    hmac_value = params.pop("hmac")
    query_string = urllib.parse.urlencode(sorted(params.items()))
    
    calculated_hmac = hmac.new(
        settings.shopify_api_secret.encode(),
        query_string.encode(),
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(calculated_hmac, hmac_value)


async def exchange_token(shop_url: str, code: str) -> Optional[Dict]:
    """Exchange authorization code for access token"""
    import httpx
    
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
