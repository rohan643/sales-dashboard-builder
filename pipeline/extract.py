"""Source-specific data extractors."""
import requests, os, pandas as pd
from pathlib import Path


def extract_pos(date: str) -> pd.DataFrame:
    resp = requests.get(
        f"{os.environ['POS_API_URL']}/sales",
        params={"date": date},
        headers={"Authorization": f"Bearer {os.environ['POS_API_KEY']}"},
        timeout=30
    )
    resp.raise_for_status()
    return pd.DataFrame(resp.json()["sales"])


def extract_inventory(date: str) -> pd.DataFrame:
    resp = requests.get(
        f"{os.environ['INVENTORY_API_URL']}/snapshot",
        params={"date": date},
        headers={"Authorization": f"Bearer {os.environ['INVENTORY_API_KEY']}"},
        timeout=30
    )
    resp.raise_for_status()
    return pd.DataFrame(resp.json()["inventory"])


def extract_ecommerce(date: str) -> pd.DataFrame:
    import shopify
    shopify.Session.setup(api_key=os.environ["SHOPIFY_API_KEY"], secret=os.environ["SHOPIFY_SECRET"])
    orders = shopify.Order.find(created_at_min=date, status="any", limit=250)
    rows = [{"sku_id": li.sku, "units_sold": li.quantity, "revenue": float(li.price)} for o in orders for li in o.line_items]
    return pd.DataFrame(rows)


def extract_ad_spend(date: str) -> list[dict]:
    # Stub — replace with Meta/Google Ads SDK calls
    return [{"channel": "meta", "spend": 0, "revenue": 0, "date": date}]


def extract_csv_drops(date: str) -> pd.DataFrame:
    drop_dir = Path(os.environ.get("CSV_DROP_DIR", "data/partner_drops"))
    files = list(drop_dir.glob(f"*{date}*.csv"))
    if not files:
        return pd.DataFrame()
    return pd.concat([pd.read_csv(f) for f in files], ignore_index=True)
