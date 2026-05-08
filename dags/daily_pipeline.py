"""Airflow DAG — daily sales ETL."""
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "rohan643",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "email_on_failure": True,
    "email": ["texanrohan@gmail.com"]
}

with DAG(
    "daily_sales_pipeline",
    default_args=default_args,
    schedule_interval="0 2 * * *",  # 2 AM daily
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["sales", "etl"]
) as dag:

    def run_etl(**context):
        from pipeline.etl import run_etl
        run_etl(context["ds"])  # Airflow passes execution date as ds

    etl_task = PythonOperator(
        task_id="run_etl",
        python_callable=run_etl
    )
