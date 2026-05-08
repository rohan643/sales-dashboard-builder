"""ETL orchestrator — extract, transform, load to PostgreSQL."""
import logging
from concurrent.futures import ThreadPoolExecutor
from pipeline.extract import (
    extract_pos, extract_inventory, extract_ecommerce,
    extract_ad_spend, extract_csv_drops
)
from sqlalchemy import create_engine
import pandas as pd, os

log = logging.getLogger(__name__)
ENGINE = create_engine(os.environ["POSTGRES_URL"])


def run_etl(date: str):
    log.info(f"ETL started for {date}")

    # Extract in parallel
    with ThreadPoolExecutor(max_workers=5) as ex:
        futures = {
            "pos":        ex.submit(extract_pos, date),
            "inventory":  ex.submit(extract_inventory, date),
            "ecommerce":  ex.submit(extract_ecommerce, date),
            "ad_spend":   ex.submit(extract_ad_spend, date),
            "partner":    ex.submit(extract_csv_drops, date),
        }
        raw = {k: f.result() for k, f in futures.items()}

    # Transform
    sku_df = transform_sku_data(raw["pos"], raw["inventory"], raw["ecommerce"])
    marketing_df = transform_marketing(raw["ad_spend"])

    # Load
    sku_df.to_sql("sku_daily", ENGINE, if_exists="append", index=False)
    marketing_df.to_sql("marketing_daily", ENGINE, if_exists="append", index=False)
    log.info(f"Loaded {len(sku_df)} SKU rows, {len(marketing_df)} marketing rows")


def transform_sku_data(pos, inventory, ecommerce) -> pd.DataFrame:
    df = pd.merge(pos, inventory, on="sku_id", how="left")
    df = pd.merge(df, ecommerce, on="sku_id", how="left")
    df["sell_through_rate"] = df["units_sold"] / df["units_available"].replace(0, 1)
    df["days_of_supply"] = df["units_available"] / df["avg_daily_velocity"].replace(0, 1)
    return df


def transform_marketing(ad_spend) -> pd.DataFrame:
    df = pd.DataFrame(ad_spend)
    df["roas"] = df["revenue"] / df["spend"].replace(0, 1)
    return df


if __name__ == "__main__":
    from datetime import date
    run_etl(str(date.today()))
