from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator
from extract import extraction
from transform import transformation
from load import loading
from main import main

with DAG(
    dag_id='stock_pipeline',
    start_date=datetime(2024, 1, 1),
    schedule='@daily',
    catchup=False
) as dag:
    
    extract_task = PythonOperator(
        task_id='main',
        python_callable=main
    )