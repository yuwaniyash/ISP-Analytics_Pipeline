from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'yuwi',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

PROJECT_DIR = '/opt/airflow/project'

with DAG(
    dag_id='isp_analytics_pipeline',
    default_args=default_args,
    description='End-to-end ISP data pipeline',
    schedule_interval='@daily',
    start_date=datetime(2026, 1, 1),
    catchup=False,
) as dag:

    generate_data = BashOperator(
        task_id='generate_data',
        bash_command=f'cd {PROJECT_DIR} && python Ingestion/generate_data.py',
    )

    ingest_data = BashOperator(
        task_id='ingest_data',
        bash_command=f'cd {PROJECT_DIR} && python Ingestion/ingest.py',
    )

    run_dbt = BashOperator(
        task_id='run_dbt',
        bash_command=f'cd {PROJECT_DIR}/dbt_project && dbt run --profiles-dir {PROJECT_DIR}',
    )

    generate_data >> ingest_data >> run_dbt