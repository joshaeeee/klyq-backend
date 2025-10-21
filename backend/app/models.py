from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    shopify_stores = relationship("ShopifyStore", back_populates="user")


class ShopifyStore(Base):
    __tablename__ = "shopify_stores"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    shop_url = Column(String, unique=True, index=True)
    access_token = Column(Text)
    scopes = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="shopify_stores")
    products = relationship("Product", back_populates="store")
    orders = relationship("Order", back_populates="store")


class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer, ForeignKey("shopify_stores.id"))
    shopify_id = Column(String, index=True)
    title = Column(String)
    handle = Column(String)
    description = Column(Text)
    vendor = Column(String)
    product_type = Column(String)
    status = Column(String)
    price = Column(Float)
    compare_at_price = Column(Float)
    sku = Column(String)
    inventory_quantity = Column(Integer)
    weight = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    store = relationship("ShopifyStore", back_populates="products")


class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer, ForeignKey("shopify_stores.id"))
    shopify_id = Column(String, index=True)
    order_number = Column(String)
    email = Column(String)
    total_price = Column(Float)
    subtotal_price = Column(Float)
    total_tax = Column(Float)
    currency = Column(String)
    financial_status = Column(String)
    fulfillment_status = Column(String)
    processed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    store = relationship("ShopifyStore", back_populates="orders")


# === ADS MODELS (🟨 ADS TEAM) ===
class MetaAccount(Base):
    __tablename__ = "meta_accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer, ForeignKey("shopify_stores.id"))
    ad_account_id = Column(String, unique=True, index=True)
    access_token = Column(Text)
    scopes = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    store = relationship("ShopifyStore")
    campaigns = relationship("Campaign", back_populates="meta_account")


class Campaign(Base):
    __tablename__ = "campaigns"
    
    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer, ForeignKey("shopify_stores.id"))
    meta_account_id = Column(Integer, ForeignKey("meta_accounts.id"))
    shopify_id = Column(String, index=True)
    name = Column(String)
    status = Column(String)
    objective = Column(String)
    daily_budget = Column(Float)
    currency = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    store = relationship("ShopifyStore")
    meta_account = relationship("MetaAccount", back_populates="campaigns")
    ads = relationship("Ad", back_populates="campaign")


class Ad(Base):
    __tablename__ = "ads"
    
    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer, ForeignKey("shopify_stores.id"))
    campaign_id = Column(Integer, ForeignKey("campaigns.id"))
    shopify_id = Column(String, index=True)
    name = Column(String)
    status = Column(String)
    creative_id = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    store = relationship("ShopifyStore")
    campaign = relationship("Campaign", back_populates="ads")


# === AI MODELS (🟦 SHARED) ===
class Attribution(Base):
    __tablename__ = "attributions"
    
    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer, ForeignKey("shopify_stores.id"))
    order_id = Column(String, index=True)
    ad_id = Column(String, index=True)
    attribution_score = Column(Float)
    revenue_lift = Column(Float)
    confidence = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    store = relationship("ShopifyStore")


class Suggestion(Base):
    __tablename__ = "suggestions"
    
    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer, ForeignKey("shopify_stores.id"))
    type = Column(String)  # promote, pause, create_bundle, update_price
    title = Column(String)
    description = Column(Text)
    reasoning = Column(Text)
    expected_impact = Column(String)
    action_data = Column(Text)  # JSON
    priority = Column(Integer)
    status = Column(String, default="pending")  # pending, applied, dismissed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    store = relationship("ShopifyStore")


# === TREND MODELS (🟨 ADS TEAM) ===
class Trend(Base):
    __tablename__ = "trends"
    
    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer, ForeignKey("shopify_stores.id"))
    platform = Column(String)  # meta, tiktok, x
    category = Column(String)
    content = Column(Text)
    engagement_score = Column(Float)
    relevance_score = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    store = relationship("ShopifyStore")
