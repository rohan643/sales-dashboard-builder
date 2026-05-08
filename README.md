# 📊 Sales Dashboard Builder

Automated ETL pipelines + live Looker Studio dashboards for product placement and sales strategy decisions.

---

### What It Replaces

Manual spreadsheet consolidation across 5 platforms. Used to take 3–4 hours per week. Now runs nightly at 2 AM automatically.

---

### Data Sources

```
POS / Retail Sales API ──────────────────┐
Inventory Management System ─────────────┤
E-commerce Platform (Shopify) ───────────┤──► PostgreSQL DW ──► Looker Studio
Marketing Ad Spend (Meta, Google Ads) ───┤                  ──► Daily Email Digest
Partner CSV Drops ───────────────────────┘
```

---

### Files

```
sales-dashboard-builder/
├── pipeline/
│   ├── etl.py              # Main ETL orchestrator
│   └── extract.py          # Source-specific extractors
├── dags/
│   └── daily_pipeline.py   # Airflow DAG
├── sql/
│   └── sku_performance.sql # Key analytical query
└── requirements.txt
```

---

### Metrics Tracked

- Revenue by SKU, store, region, channel
- Sell-through rate and days of supply
- Placement vs. performance correlation
- Ad spend efficiency (ROAS by channel)
- Forecast vs. actual variance

---

### Run

```bash
# One-time
python pipeline/etl.py

# Scheduled (via Airflow)
airflow dags trigger daily_sales_pipeline
```

---

<sub>[@rohan643](https://github.com/rohan643)</sub>
