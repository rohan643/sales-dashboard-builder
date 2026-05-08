<div align="center">

# 📊 Sales Dashboard Builder

**Automated data pipelines + live dashboards for product placement and sales strategy decisions**

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Looker Studio](https://img.shields.io/badge/Looker_Studio-Dashboards-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://lookerstudio.google.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Data_Warehouse-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)
[![Airflow](https://img.shields.io/badge/Airflow-Pipelines-017CEE?style=for-the-badge&logo=apacheairflow&logoColor=white)](https://airflow.apache.org)

</div>

---

## Overview

Manual reporting is a time sink and always one step behind. This system replaces spreadsheet-based reporting with automated ETL pipelines that pull from every data source, transform it into decision-ready metrics, and push it to a live Looker Studio dashboard — updated daily, zero human effort.

Built for teams making product placement and sales strategy decisions at scale across thousands of SKUs and retail locations.

---

## Architecture

```
Data Sources (multi-channel)
    │
    ├── POS / Retail Sales API
    ├── Inventory Management System
    ├── E-commerce Platform (Shopify/custom)
    ├── Marketing Ad Spend (Meta, Google)
    └── Manual uploads (CSV drops from partners)
    │
    ▼
┌────────────────────────────────┐
│  ETL Pipeline (Python/Airflow) │  ← Runs daily at 2 AM
│                                │    Extract → Validate → Transform → Load
│  • Data quality checks         │
│  • Deduplication               │
│  • Schema normalization        │
│  • Anomaly flagging            │
└───────────────┬────────────────┘
                │
                ▼
┌────────────────────────────────┐
│  Data Warehouse (PostgreSQL)   │  ← Single source of truth
│                                │    Partitioned by date + region
│  • sku_performance             │
│  • store_metrics               │
│  • placement_analysis          │
│  • competitor_pricing          │
│  • forecast_vs_actual          │
└───────────────┬────────────────┘
                │
        ┌───────┴────────┐
        ▼                ▼
┌───────────────┐  ┌──────────────────────┐
│ Looker Studio │  │  Daily Email Digest  │
│  Dashboard    │  │  (Leadership team)   │
│               │  │                      │
│  Live, auto-  │  │  Top 10 SKUs         │
│  refreshed    │  │  Underperformers      │
│  drill-down   │  │  Placement rec's     │
└───────────────┘  └──────────────────────┘
```

---

## Dashboard Panels

### Executive View
```
┌──────────────────────────────────────────────────────────┐
│  SALES PERFORMANCE — Week of May 5, 2026                 │
├────────────────┬────────────────┬────────────────────────┤
│  Total Revenue │  Units Sold    │  vs. Prior Week        │
│  $4.2M         │  87,341        │  ▲ 12.4%               │
├────────────────┴────────────────┴────────────────────────┤
│  TOP PERFORMING SKUs (by revenue)                        │
│  1. SKU-08821  │ $412K  │ ▲ 34%  │ Placement: Endcap     │
│  2. SKU-03341  │ $389K  │ ▲ 8%   │ Placement: Aisle 4    │
│  3. SKU-09912  │ $301K  │ ▼ 2%   │ Placement: Eye-level  │
├──────────────────────────────────────────────────────────┤
│  UNDERPERFORMERS (placement review recommended)          │
│  • SKU-04421 — Down 18% WoW, currently on bottom shelf  │
│  • SKU-07731 — Down 22% WoW, low foot traffic section   │
└──────────────────────────────────────────────────────────┘
```

### Placement Optimization View
Cross-references physical shelf placement data against sales velocity to surface placement change recommendations automatically.

```python
# Placement scoring logic
def placement_score(sku: str, location: str) -> float:
    revenue_per_sqft = get_revenue(sku) / get_shelf_space(sku, location)
    foot_traffic_index = get_foot_traffic(location) / avg_foot_traffic
    cannibalization_risk = check_adjacent_skus(sku, location)
    return (revenue_per_sqft * 0.6) + (foot_traffic_index * 0.3) - (cannibalization_risk * 0.1)
```

---

## ETL Pipeline

### Extract
```python
# Parallel extraction from all sources
with ThreadPoolExecutor(max_workers=5) as executor:
    futures = {
        executor.submit(extract_pos_data, date_range): "pos",
        executor.submit(extract_inventory, date_range): "inventory",
        executor.submit(extract_ecommerce, date_range): "ecommerce",
        executor.submit(extract_ad_spend, date_range): "marketing",
        executor.submit(extract_csv_drops, date_range): "partner",
    }
```

### Transform
- Normalize SKU codes across systems (different naming conventions per source)
- Currency standardization
- Region and store hierarchy mapping
- Calculated metrics: sell-through rate, days of supply, velocity

### Load
- Upsert into PostgreSQL with conflict resolution
- Partition pruning for fast query performance
- Materialized views for dashboard queries (sub-second response)

---

## Daily Email Digest

Sent at 7 AM every morning to the leadership distribution list:

```
Subject: Sales Digest — May 7, 2026 | ▲ 12.4% WoW

Good morning,

Yesterday's highlights:
• Total revenue: $4.2M (+12.4% vs. last Wednesday)
• Best performer: SKU-08821 on endcap — $412K (+34%)
• Action needed: SKU-04421 down 18% — placement review recommended

Full dashboard: [link]

3 SKUs flagged for placement optimization review this week.
```

---

## Setup

### Requirements
```
python >= 3.11
apache-airflow
psycopg2-binary
pandas
sqlalchemy
google-api-python-client   # Looker Studio / Sheets
requests
python-dotenv
```

### Install
```bash
git clone https://github.com/rohan643/sales-dashboard-builder.git
cd sales-dashboard-builder
pip install -r requirements.txt
cp .env.example .env
# Configure data source credentials

# Initialize Airflow
airflow db init
airflow webserver --port 8080 &
airflow scheduler &
```

### Environment Variables
```env
POSTGRES_URL=postgresql://user:pass@host:5432/sales_dw
POS_API_KEY=...
INVENTORY_API_KEY=...
SHOPIFY_API_KEY=...
GOOGLE_SERVICE_ACCOUNT_JSON=path/to/service-account.json
SMTP_HOST=...
DIGEST_RECIPIENTS=team@company.com,ceo@company.com
```

---

## Performance

```
Data sources connected:    5
SKUs tracked:              12,000+
Stores covered:            400+
Pipeline run time:         ~18 minutes (nightly)
Dashboard query speed:     < 800ms (materialized views)
Data freshness:            Daily by 3 AM
```

---

<div align="center">

**Built by [Rohan Mukherjee](https://github.com/rohan643)**

</div>
