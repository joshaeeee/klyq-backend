# Clique AI CMO - Backend Feature Matrix

## Master Feature Matrix

| Category | OAuth Setup | Order Attribution | Product Sync | Inventory Updates | Ad Performance Monitoring | Creative Fatigue Detection | Budget Waste Detection | Diagnostics (Why Ads Fail) | SKU Performance Analysis | Suggestions (What to Promote) | Trend Detection | Trend Replication | 1-Click Campaign Launch | 1-Click Ad Pause | Bundle Creation | Price Updates | Manual Data Sync | A/B Test Creation | Dashboard Views | Report Export | Settings Management | Historical Data Import | AI Model Training | AI Cold-Start | Baseline Metrics | Data Cleanup | Co-purchase Analysis | Competitor Monitoring | Market Events | Webhook Registration |
|----------|-------------|-------------------|--------------|------------------|---------------------------|----------------------------|----------------------|----------------------------|-------------------------|--------------------------------|----------------|------------------|----------------------|------------------|----------------|---------------|-----------------|------------------|----------------|--------------|-------------------|----------------------|-----------------|-------------|----------------|------------|-------------------|----------------------|--------------|-------------------|
| **EXECUTION PATTERN** | One-time setup | Webhook-driven | Webhook-driven | Webhook-driven | Webhook-driven | Cron (15-30 min) | Cron (15-30 min) | Cron (1-4 hrs) | Cron (1-4 hrs) | User-triggered | Cron (15-30 min) | User-triggered | User-triggered | User-triggered | User-triggered | User-triggered | User-triggered | User-triggered | User-triggered | User-triggered | User-triggered | One-time setup | Cron (Daily) | One-time setup | One-time setup | Cron (Weekly) | Cron (Daily) | Cron (1-4 hrs) | Cron (1-4 hrs) | One-time setup |
| **Details** | Initial OAuth flow | `orders/create`, `orders/paid` | `products/create`, `products/update` | `inventory_levels/update` | `ads_insights`, `campaigns` | Performance drop analysis | Budget threshold monitoring | Scheduled analysis | MoM trend analysis | On-demand API call | Meta Ad Library, TikTok, X polling | Gen-AI creative generation | Direct Meta API call | Direct Meta API call | Shopify API call | Shopify API call | Force refresh button | Meta API variant creation | Real-time data display | PDF/CSV generation | User preference updates | Historical data import | ML model retraining | Meta Ad Library priors | Performance benchmarks | Data archiving | Purchase pattern analysis | Price/strategy tracking | Holiday/event detection | Webhook endpoint setup |
| **DATA SOURCES** | Other (API creds) | Only Shopify | Only Shopify | Only Shopify | Only Ads | Only Ads | Only Ads | Both Shopify + Ads | Only Shopify | Both Shopify + Ads | Other (Meta Ad Library, TikTok, X) | Mix (Shopify + Ads + Other) | Both Shopify + Ads | Only Ads | Only Shopify | Only Shopify | Both Shopify + Ads | Only Ads | Both Shopify + Ads | Both Shopify + Ads | Other (user prefs) | Both Shopify + Ads | Both Shopify + Ads | Mix (Shopify + Ads + Other) | Both Shopify + Ads | Mix (Shopify + Ads + Other) | Only Shopify | Other (competitor APIs) | Other (market APIs) | Other (webhook configs) |
| **APIs Required** | Shopify OAuth | Shopify Admin API (read_orders) | Shopify Admin API (read_products) | Shopify Admin API (read_inventory) | Meta Marketing API (ads_read) | Meta Marketing API (ads_read) | Meta Marketing API (ads_read) | Shopify + Meta APIs | Shopify Admin API (read_products) | Shopify + Meta APIs | Meta Ad Library, TikTok, X APIs | Shopify + Meta + Gen-AI APIs | Shopify + Meta APIs | Meta Marketing API (ads_management) | Shopify Admin API (write_products) | Shopify Admin API (write_products) | Shopify + Meta APIs | Meta Marketing API (ads_management) | Shopify + Meta APIs | Shopify + Meta APIs | User settings API | Shopify + Meta APIs | Shopify + Meta APIs | Shopify + Meta + Meta Ad Library APIs | Shopify + Meta APIs | Shopify + Meta + External APIs | Shopify Admin API (read_orders) | Competitor APIs | Market data APIs | Webhook management APIs |

## Legend

### Execution Patterns
- **Webhook-driven**: Real-time events from Shopify/Meta webhooks
- **Cron (15-30 min)**: High-frequency scheduled background jobs
- **Cron (1-4 hrs)**: Medium-frequency scheduled background jobs  
- **Cron (Daily)**: Daily scheduled background jobs
- **Cron (Weekly)**: Weekly scheduled background jobs
- **User-triggered**: On-demand actions triggered by user interaction
- **One-time setup**: Setup/initialization tasks run once

### Data Sources
- **Only Shopify**: Requires only Shopify API data
- **Only Ads**: Requires only Meta/ads API data
- **Both Shopify + Ads**: Requires both Shopify and Ads data
- **Other**: External APIs (trends, competitors, market data)
- **Mix**: Combination of multiple data sources

## Infrastructure Requirements

### Webhook-driven Features
- **Infrastructure**: FastAPI endpoints + Redis queue + Celery workers
- **Database**: Real-time updates to PostgreSQL
- **Monitoring**: Webhook delivery status, retry logic
- **Security**: HMAC validation, rate limiting

### Cron Jobs
- **Infrastructure**: Celery + Redis + APScheduler
- **Database**: Batch processing, data aggregation
- **Monitoring**: Job status, failure alerts
- **Scaling**: Horizontal scaling for heavy processing

### User-triggered Features
- **Infrastructure**: FastAPI endpoints + direct API calls
- **Database**: Immediate updates, transaction handling
- **Monitoring**: Response times, error rates
- **Security**: Authentication, authorization

### One-time Setup
- **Infrastructure**: Async tasks + progress tracking
- **Database**: Bulk imports, schema migrations
- **Monitoring**: Progress indicators, completion status
- **Error Handling**: Rollback capabilities

## Implementation Priority

### Phase 1 (MVP) - Core Data & Auth
1. OAuth Setup
2. Product Sync
3. Order Attribution
4. Inventory Updates
5. Dashboard Views
6. Manual Data Sync

### Phase 2 (Real-time) - Webhooks & Monitoring
7. Ad Performance Monitoring
8. Webhook Registration
9. Historical Data Import
10. Baseline Metrics

### Phase 3 (AI Features) - Intelligence & Automation
11. Diagnostics (Why Ads Fail)
12. Suggestions (What to Promote)
13. AI Model Training
14. AI Cold-Start

### Phase 4 (Advanced) - Trends & Actions
15. Trend Detection
16. Trend Replication
17. 1-Click Campaign Launch
18. 1-Click Ad Pause
19. Bundle Creation
20. Price Updates

### Phase 5 (Optimization) - Analysis & Reports
21. Creative Fatigue Detection
22. Budget Waste Detection
23. SKU Performance Analysis
24. Co-purchase Analysis
25. Report Export
26. A/B Test Creation

### Phase 6 (Enterprise) - External & Advanced
27. Competitor Monitoring
28. Market Events
29. Settings Management
30. Data Cleanup

## API Scopes Required

### Shopify Admin API
- `read_products` - Product data access
- `read_orders` - Order data access
- `read_inventory` - Inventory level access
- `write_products` - Product modifications
- `read_customers` - Customer data access

### Meta Marketing API
- `ads_read` - Ad performance data
- `ads_management` - Ad creation/modification
- `business_management` - Account management
- `pages_read_engagement` - Page insights

### External APIs
- Meta Ad Library API - Trend detection
- TikTok API - Social trends
- X (Twitter) API - Social trends
- OpenAI API - AI generation
- Competitor APIs - Price monitoring
- Market data APIs - Event detection

## Database Schema Requirements

### Core Tables
- `users` - User accounts
- `shopify_stores` - Connected stores
- `products` - Product data cache
- `orders` - Order data cache
- `ads` - Ad performance cache
- `campaigns` - Campaign data cache

### Analysis Tables
- `attributions` - Ad-to-order mappings
- `diagnostics` - Performance analysis results
- `suggestions` - AI-generated recommendations
- `trends` - Detected trends cache
- `reports` - Generated reports

### Configuration Tables
- `webhook_subscriptions` - Webhook registrations
- `user_settings` - User preferences
- `ai_models` - Model training data
- `sync_logs` - Data sync history
