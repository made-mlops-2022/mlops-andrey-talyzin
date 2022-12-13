import os
from datetime import timedelta
from airflow.utils.email import send_email_smtp

MOUNT_DIR = "/Users/Andrey/Downloads/made-mlops-2022/airflow_ml_dags/data"
DATA_PATH = "/opt/airflow/data/raw/{{ ds }}/data.csv"
TARGET_PATH = "/opt/airflow/data/raw/{{ ds }}/target.csv"
RAW_DATA = "/data/raw/{{ ds }}"
PROCESSED_DATA = "/data/processed/{{ ds }}"
SPLITTED_DATA = "/data/split/{{ ds }}"
MODELS = "/data/models/{{ ds }}"
METRICS = "/data/metrics/{{ ds }}"
PREDICTED = "/data/predictions/{{ ds }}"
MLRUNS_DIR = "/Users/Andrey/Downloads/made-mlops-2022/airflow_ml_dags/mlruns"


def check_data_exist(filenames: list):
    for filename in filenames:
        if not os.path.exists(filename):
            return False
    return True


def failure_callback(context):
    dag_run = context.get('dag_run')
    msg = "DAG has failed!"
    subject = f'FAIL!: DAG {dag_run}'
    send_email_smtp(to=default_args['email'], subject=subject, html_content=msg)


default_args = {
    'owner': 'airflow',
    'email': ['amadey.developer@gmail.com'],
    # 'email_on_failure': True,
    # 'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(seconds=300),
    'on_failure_callback': failure_callback
}
