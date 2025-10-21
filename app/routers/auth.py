from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, ShopifyStore
from ..services.shopify import exchange_shopify_token, validate_shopify_hmac
from ..config import settings
import uuid

router = APIRouter()


@router.get("/shopify")
async def initiate_shopify_oauth(shop: str, request: Request):
    """Initiate Shopify OAuth flow"""
    if not shop.endswith('.myshopify.com'):
        raise HTTPException(status_code=400, detail="Invalid shop URL")
    
    scopes = "read_products,read_orders,read_inventory"
    redirect_uri = f"{settings.frontend_url}/auth/shopify/callback"
    
    install_url = f"https://{shop}/admin/oauth/authorize?client_id={settings.shopify_api_key}&scope={scopes}&redirect_uri={redirect_uri}&state=random_state"
    
    return {"install_url": install_url}


@router.get("/shopify/callback")
async def shopify_oauth_callback(
    shop: str,
    code: str,
    hmac: str,
    state: str,
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):
    """Handle Shopify OAuth callback"""
    # Validate HMAC
    params = dict(request.query_params)
    if not validate_shopify_hmac(params):
        raise HTTPException(status_code=400, detail="Invalid HMAC")
    
    # Exchange code for access token
    token_data = await exchange_shopify_token(shop, code)
    if not token_data:
        raise HTTPException(status_code=400, detail="Failed to exchange token")
    
    # Create or get user (simplified for demo)
    user = db.query(User).filter(User.email == "demo@example.com").first()
    if not user:
        user = User(email="demo@example.com")
        db.add(user)
        db.commit()
        db.refresh(user)
    
    # Create or update Shopify store
    store = db.query(ShopifyStore).filter(ShopifyStore.shop_url == shop).first()
    if store:
        store.access_token = token_data["access_token"]
        store.scopes = token_data["scope"]
    else:
        store = ShopifyStore(
            user_id=user.id,
            shop_url=shop,
            access_token=token_data["access_token"],
            scopes=token_data["scope"]
        )
        db.add(store)
    
    db.commit()
    
    # Redirect to frontend dashboard
    response.headers["Location"] = f"{settings.frontend_url}/dashboard?store_id={store.id}"
    return {"message": "Successfully connected to Shopify", "redirect_url": f"{settings.frontend_url}/dashboard"}


@router.get("/meta")
async def initiate_meta_oauth(ad_account_id: str):
    """Initiate Meta OAuth flow"""
    # Meta OAuth implementation
    return {"message": "Meta OAuth not implemented yet"}


@router.get("/meta/callback")
async def meta_oauth_callback(
    code: str,
    state: str,
    db: Session = Depends(get_db)
):
    """Handle Meta OAuth callback"""
    # Meta OAuth callback implementation
    return {"message": "Meta OAuth callback not implemented yet"}


@router.post("/logout")
async def logout(response: Response):
    """Logout user"""
    response.delete_cookie("session")
    return {"message": "Logged out successfully"}