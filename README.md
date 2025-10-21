# Clique AI CMO - Backend

An AI-powered Chief Marketing Officer tool for Shopify stores that provides real-time insights, automated diagnostics, and one-click marketing actions.

## 🎯 What We're Building

**Clique** is an AI CMO that connects Shopify stores with Meta ads to provide:
- **Real-time Attribution** - See which ads drive which sales
- **AI Diagnostics** - Understand why ads aren't working
- **Smart Suggestions** - Get AI recommendations for promotions
- **Trend Detection** - Capitalize on viral trends automatically
- **1-Click Actions** - Execute marketing changes instantly

## 🏗️ Repository Structure

```
backend/
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py              # Environment configuration
│   ├── database.py            # Database connection & session management
│   ├── models.py              # SQLAlchemy database models
│   ├── schemas.py             # Pydantic request/response schemas
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py           # OAuth & authentication endpoints
│   │   ├── webhooks.py       # Webhook handlers (Shopify & Meta)
│   │   ├── data.py            # Data endpoints (products, orders, ads)
│   │   ├── actions.py        # User-triggered actions (1-click features)
│   │   └── admin.py          # Admin endpoints (reports, settings)
│   ├── services/
│   │   ├── __init__.py
│   │   ├── shopify.py        # 🟦 SHOPIFY TEAM - Shopify API integration functions
│   │   ├── meta.py           # 🟨 ADS TEAM - Meta/Facebook ads API integration
│   │   ├── ai.py             # 🟦 SHARED - AI/ML processing functions
│   │   ├── trends.py         # 🟨 ADS TEAM - Trend detection & analysis
│   │   └── analytics.py      # 🟦 SHARED - Analytics & reporting functions
│   └── utils/
│       ├── __init__.py
│       ├── validators.py     # Data validation utilities
│       └── helpers.py         # Common helper functions
├── workers.py                # 🟦 SHARED - ALL background tasks (Celery)
├── celery_app.py            # Celery configuration
├── requirements.txt         # Python dependencies
├── alembic/                 # Database migrations
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
├── feature_matrix.csv       # Complete feature categorization
└── README.md               # This file
```

## 👥 Team Separation

### **🟦 Shopify Team (Your Co-founder)**
- **`services/shopify.py`** - All Shopify API integration
- **Shopify models** in `models.py` (Product, Order, Inventory, ShopifyStore)
- **Shopify schemas** in `schemas.py` (ProductResponse, OrderResponse, etc.)
- **Shopify webhooks** in `routers/webhooks.py` (orders/create, products/update, etc.)

### **🟨 Ads Team (You)**
- **`services/meta.py`** - All Meta/Facebook ads API integration
- **`services/trends.py`** - Trend detection and analysis
- **Ads models** in `models.py` (Campaign, Ad, AdSet, MetaAccount)
- **Ads schemas** in `schemas.py` (CampaignResponse, AdResponse, etc.)
- **Meta webhooks** in `routers/webhooks.py` (ads_insights, campaigns, etc.)

### **🟦 Shared (Both Teams)**
- **`services/ai.py`** - AI/ML processing and analysis
- **`services/analytics.py`** - Analytics and reporting
- **`workers.py`** - All background tasks
- **`routers/auth.py`** - OAuth for both platforms
- **`routers/data.py`** - Combined data endpoints
- **`routers/actions.py`** - 1-click actions for both platforms

## 📁 File Descriptions

### **Core Application Files**

#### **`app/main.py`**
- **Purpose**: FastAPI application entry point
- **What it does**: 
  - Initializes FastAPI app with CORS middleware
  - Includes all router modules
  - Defines health check endpoints
- **Key endpoints**: `/`, `/health`, `/docs`

#### **`app/config.py`**
- **Purpose**: Environment configuration management
- **What it does**:
  - Loads environment variables from `.env`
  - Provides settings for database, APIs, frontend URL
  - Centralized configuration for all services

#### **`app/database.py`**
- **Purpose**: Database connection and session management
- **What it does**:
  - Creates SQLAlchemy engine and session factory
  - Provides database dependency injection
  - Handles connection pooling

#### **`app/models.py`**
- **Purpose**: SQLAlchemy database models
- **What it does**:
  - Defines all database tables (Users, Stores, Products, Orders, Ads, etc.)
  - Establishes relationships between entities
  - Handles data persistence layer

#### **`app/schemas.py`**
- **Purpose**: Pydantic request/response schemas
- **What it does**:
  - Validates incoming API requests
  - Serializes outgoing API responses
  - Type safety for API contracts

### **API Endpoints (`app/routers/`)**

#### **`routers/auth.py`**
- **Purpose**: OAuth authentication for Shopify and Meta
- **What it does**:
  - Handles Shopify OAuth flow (`/auth/shopify`)
  - Handles Meta OAuth flow (`/auth/meta`)
  - Manages token exchange and storage
  - Redirects to frontend after successful auth

#### **`routers/webhooks.py`**
- **Purpose**: Real-time webhook processing
- **What it does**:
  - Receives Shopify webhooks (orders, products, inventory)
  - Receives Meta webhooks (ads, campaigns, performance)
  - Validates webhook signatures for security
  - Queues webhook data for background processing

#### **`routers/data.py`**
- **Purpose**: Data retrieval endpoints
- **What it does**:
  - Serves products, orders, ads data to frontend
  - Handles data filtering and pagination
  - Provides real-time data sync status
  - Exposes store information and metrics

#### **`routers/actions.py`**
- **Purpose**: User-triggered actions (1-click features)
- **What it does**:
  - Launches campaigns (`/actions/launch-campaign`)
  - Pauses ads (`/actions/pause-ad`)
  - Creates bundles (`/actions/create-bundle`)
  - Updates pricing (`/actions/update-pricing`)
  - Manual data sync (`/actions/sync-data`)

#### **`routers/admin.py`**
- **Purpose**: Admin and reporting endpoints
- **What it does**:
  - Generates performance reports
  - Manages user settings and preferences
  - Provides system health and metrics
  - Handles bulk operations

### **Business Logic (`app/services/`)**

#### **`services/shopify.py`** 🟦 **SHOPIFY TEAM**
- **Purpose**: All Shopify API integration
- **What it does**:
  - Fetches products, orders, inventory from Shopify
  - Creates/updates products and bundles
  - Handles Shopify webhook processing
  - Manages store connection and tokens
- **Key functions**:
  - `fetch_products(store_id, access_token)`
  - `create_bundle(store_id, product_ids)`
  - `update_pricing(store_id, product_id, new_price)`
  - `sync_products_to_db(store_id, products_data)`

#### **`services/meta.py`** 🟨 **ADS TEAM**
- **Purpose**: All Meta/Facebook ads API integration
- **What it does**:
  - Fetches campaigns, ads, performance data from Meta
  - Creates/pauses ads and campaigns
  - Handles Meta webhook processing
  - Manages ad account connections
- **Key functions**:
  - `fetch_campaigns(ad_account_id, access_token)`
  - `pause_campaign(campaign_id, access_token)`
  - `create_ad_variant(campaign_id, creative_data)`
  - `sync_ads_to_db(store_id, ads_data)`

#### **`services/ai.py`** 🟦 **SHARED (Both Teams)**
- **Purpose**: AI/ML processing and analysis
- **What it does**:
  - Analyzes ad-to-order attribution
  - Generates AI suggestions and recommendations
  - Detects creative fatigue and performance issues
  - Trains and updates ML models
- **Key functions**:
  - `analyze_attribution(orders, ads)`
  - `generate_suggestions(store_id)`
  - `detect_creative_fatigue(ad_id)`
  - `train_attribution_model(store_id)`

#### **`services/trends.py`** 🟨 **ADS TEAM**
- **Purpose**: Trend detection and analysis
- **What it does**:
  - Monitors Meta Ad Library for viral trends
  - Tracks TikTok and X for social trends
  - Analyzes trend relevance to store categories
  - Generates trend-based creative suggestions
- **Key functions**:
  - `detect_viral_trends(category)`
  - `analyze_trend_relevance(store_products, trend)`
  - `generate_trend_creatives(trend_data)`

#### **`services/analytics.py`** 🟦 **SHARED (Both Teams)**
- **Purpose**: Analytics and reporting
- **What it does**:
  - Calculates RPMo, CPA, CTR metrics
  - Generates performance reports
  - Tracks attribution and conversion data
  - Provides insights and recommendations
- **Key functions**:
  - `calculate_rpmo(orders, impressions)`
  - `calculate_cpa(spend, conversions)`
  - `generate_performance_report(store_id)`

### **Background Processing**

#### **`workers.py`**
- **Purpose**: ALL background tasks in one file
- **What it does**:
  - Handles one-time setup tasks (when store connects)
  - Processes scheduled cron jobs
  - Manages webhook processing
  - Runs AI model training
- **Task categories**:
  - **Store Setup**: `import_historical_data()`, `setup_ai_cold_start()`
  - **Scheduled Jobs**: `detect_trends()`, `run_diagnostics()`
  - **Webhook Processing**: `process_order_webhook()`, `process_ad_webhook()`
  - **AI Training**: `train_attribution_models()`, `update_ai_models()`

#### **`celery_app.py`**
- **Purpose**: Celery configuration and setup
- **What it does**:
  - Configures Celery with Redis broker
  - Sets up task routing and queues
  - Defines scheduled jobs (cron tasks)
  - Manages worker processes

### **Utilities**

#### **`utils/validators.py`**
- **Purpose**: Data validation utilities
- **What it does**:
  - Validates webhook signatures
  - Checks API response formats
  - Ensures data integrity

#### **`utils/helpers.py`**
- **Purpose**: Common helper functions
- **What it does**:
  - Date/time formatting
  - Data transformation utilities
  - Common calculations and conversions

## 🔄 Execution Patterns

### **1. Webhook-Driven (Real-time)**
- **Shopify**: `orders/create`, `products/update`, `inventory_levels/update`
- **Meta**: `ads_insights`, `campaigns`, `ad_sets`
- **Processing**: Immediate attribution analysis, performance updates

### **2. User-Triggered (On-demand)**
- **Actions**: 1-click campaign launches, ad pauses, bundle creation
- **Processing**: Direct API calls to Shopify/Meta, immediate responses

### **3. Scheduled Jobs (Cron)**
- **High Frequency**: Trend detection (15 min), creative fatigue (30 min)
- **Medium Frequency**: Diagnostics (2 hrs), performance analysis (4 hrs)
- **Low Frequency**: AI training (daily), data cleanup (weekly)

### **4. One-Time Setup**
- **Store Connection**: Historical data import, AI cold-start, baseline metrics
- **Configuration**: Webhook registration, user preferences, store settings

## 🚀 Development Workflow

### **Team Separation**
- **🟦 Shopify Team**: `services/shopify.py`, Shopify models, Shopify webhooks
- **🟨 Ads Team**: `services/meta.py`, `services/trends.py`, Ads models, Meta webhooks
- **🟦 Shared**: `services/ai.py`, `services/analytics.py`, `workers.py`

### **Git Strategy**
```bash
main                    # Production-ready code
├── develop            # Integration branch
├── feature/shopify-*  # Shopify team features
└── feature/ads-*      # Ads team features
```

### **Deployment**
```bash
# Development
uvicorn app.main:app --reload

# Production
celery -A workers worker --loglevel=info
celery -A workers beat --loglevel=info
```

## 📊 Data Flow

1. **Store Connection** → OAuth → Webhook Registration → Historical Import
2. **Real-time Updates** → Webhooks → Background Processing → Database Updates
3. **User Actions** → API Endpoints → Direct API Calls → Immediate Response
4. **Scheduled Analysis** → Cron Jobs → AI Processing → Insights Generation
5. **Dashboard Display** → Data Endpoints → Frontend → User Interface

## 🔧 Key Features

- **Real-time Attribution**: See which ads drive sales instantly
- **AI Diagnostics**: Understand why ads fail with actionable insights
- **Smart Suggestions**: Get AI recommendations for promotions and bundles
- **Trend Detection**: Capitalize on viral trends automatically
- **1-Click Actions**: Execute marketing changes in seconds
- **Performance Analytics**: Track RPMo, CPA, and conversion metrics
- **Automated Optimization**: AI-powered campaign management

This backend provides the foundation for a complete AI CMO that transforms how Shopify stores manage their marketing and advertising.

## 📊 Feature Matrix Reference

The complete feature categorization is available in `backend/feature_matrix.csv` which provides a comprehensive breakdown of all 30+ features by execution pattern and data sources.

### **Feature Categories Overview**

| Execution Pattern | Count | Examples |
|------------------|-------|----------|
| **Webhook-driven** | 4 | Order Attribution, Product Sync, Inventory Updates, Ad Performance Monitoring |
| **Cron (15-30 min)** | 3 | Creative Fatigue Detection, Budget Waste Detection, Trend Detection |
| **Cron (1-4 hrs)** | 4 | Diagnostics, SKU Performance Analysis, Competitor Monitoring, Market Events |
| **Cron (Daily)** | 2 | AI Model Training, Co-purchase Analysis |
| **Cron (Weekly)** | 1 | Data Cleanup |
| **User-triggered** | 10 | Suggestions, Trend Replication, 1-Click Actions, Manual Sync, etc. |
| **One-time setup** | 5 | OAuth Setup, Historical Data Import, AI Cold-Start, Baseline Metrics, Webhook Registration |

| Data Sources | Count | Examples |
|-------------|-------|----------|
| **Only Shopify** | 8 | Product Sync, Inventory Updates, SKU Performance Analysis, Bundle Creation, etc. |
| **Only Ads** | 6 | Ad Performance Monitoring, Creative Fatigue Detection, Budget Waste Detection, etc. |
| **Both Shopify + Ads** | 8 | Order Attribution, Diagnostics, Suggestions, 1-Click Actions, etc. |
| **Other APIs** | 6 | OAuth Setup, Trend Detection, Settings Management, etc. |
| **Mix (Multiple)** | 3 | AI Cold-Start, Data Cleanup, Trend Replication |

### **Key Insights from Feature Matrix**

1. **Real-time Focus**: 4 webhook-driven features provide instant data processing
2. **AI-Powered**: 8 features require both Shopify and Ads data for intelligent analysis
3. **User Control**: 10 user-triggered features give merchants direct control over actions
4. **Automated Intelligence**: 10 scheduled jobs provide continuous monitoring and optimization
5. **One-time Setup**: 5 initialization features ensure smooth onboarding

### **Team Distribution by Data Sources**

- **🟦 Shopify Team**: 8 features (Only Shopify data)
- **🟨 Ads Team**: 6 features (Only Ads data) + 3 features (Trend detection)
- **🟦 Shared**: 8 features (Both Shopify + Ads data) + 3 features (Mixed data sources)

This matrix serves as the single source of truth for feature planning, development prioritization, and team coordination.# klyq-backend
