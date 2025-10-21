from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


# === SHARED SCHEMAS ===
class UserResponse(BaseModel):
    id: int
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


class StoreInfoResponse(BaseModel):
    shop_url: str
    scopes: str
    created_at: datetime
    products_count: int
    orders_count: int


# === SHOPIFY SCHEMAS (🟦 SHOPIFY TEAM) ===
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
    compare_at_price: Optional[float] = None
    sku: str
    inventory_quantity: int
    weight: float
    created_at: datetime
    updated_at: Optional[datetime] = None

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
    processed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class InventoryResponse(BaseModel):
    inventory_item_id: str
    location_id: str
    available: int
    updated_at: datetime


class BundleCreateRequest(BaseModel):
    title: str
    product_ids: List[int]
    price: float
    description: Optional[str] = None


class PriceUpdateRequest(BaseModel):
    product_id: str
    new_price: float


# === ADS SCHEMAS (🟨 ADS TEAM) ===
class CampaignResponse(BaseModel):
    id: int
    shopify_id: str
    name: str
    status: str
    objective: str
    daily_budget: float
    currency: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class AdResponse(BaseModel):
    id: int
    shopify_id: str
    name: str
    status: str
    campaign_id: str
    creative_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class PerformanceResponse(BaseModel):
    campaign_id: str
    impressions: int
    clicks: int
    spend: float
    conversions: int
    ctr: float
    cpc: float
    cpa: float
    date: datetime


class AdVariantRequest(BaseModel):
    campaign_id: str
    creative_data: dict
    targeting: Optional[dict] = None


# === AI SCHEMAS (🟦 SHARED) ===
class AttributionResponse(BaseModel):
    ad_id: str
    order_id: str
    attribution_score: float
    revenue_lift: float
    confidence: float
    created_at: datetime


class SuggestionResponse(BaseModel):
    id: int
    type: str  # "promote", "pause", "create_bundle", "update_price"
    title: str
    description: str
    reasoning: str
    expected_impact: str
    action_data: dict
    priority: int
    created_at: datetime

    class Config:
        from_attributes = True


class DiagnosticResponse(BaseModel):
    issue_type: str
    severity: str
    description: str
    affected_ads: List[str]
    recommendations: List[str]
    created_at: datetime


# === TREND SCHEMAS (🟨 ADS TEAM) ===
class TrendResponse(BaseModel):
    id: int
    platform: str
    category: str
    content: str
    engagement_score: float
    relevance_score: float
    created_at: datetime

    class Config:
        from_attributes = True


class TrendCreativeRequest(BaseModel):
    trend_id: int
    store_category: str
    brand_style: Optional[str] = None


# === ANALYTICS SCHEMAS (🟦 SHARED) ===
class MetricsResponse(BaseModel):
    rpmo: float
    cpa: float
    ctr: float
    aov: float
    conversion_rate: float
    period: str
    date: datetime


class ReportRequest(BaseModel):
    store_id: int
    start_date: datetime
    end_date: datetime
    report_type: str  # "performance", "attribution", "trends"


# === WEBHOOK SCHEMAS ===
class ShopifyWebhookData(BaseModel):
    id: int
    shop_domain: str
    created_at: str
    data: dict


class MetaWebhookData(BaseModel):
    id: str
    ad_account_id: str
    created_time: str
    data: dict
