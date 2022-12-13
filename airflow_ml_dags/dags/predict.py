import airflow
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount
from variables import *


with DAG(
    'predict',
    default_args=default_args,
    schedule_interval='@daily',
    start_date=airflow.utils.dates.days_ago(5)
) as dag:
    preprocess = DockerOperator(
        image='airflow-preprocess',
        command=f'--input-dir {RAW_DATA} --output-dir {PROCESSED_DATA}',
        network_mode='bridge',
        task_id='docker-airflow-predict_preprocess',
        do_xcom_push=False,
        auto_remove=True,
        mounts=[Mount(source=MOUNT_DIR, target='/data', type='bind')]
        )

    predict = DockerOperator(
        image='airflow-predict',
        command=f'--input-dir {PROCESSED_DATA} --output-dir {PREDICTED}',
        network_mode='host',
        task_id='docker-airflow-predict',
        do_xcom_push=False,
        auto_remove=True,
        mounts=[Mount(source=MOUNT_DIR, target='/data', type='bind'),
                Mount(source=MLRUNS_DIR, target='/mlruns', type='bind')]
    )

    preprocess >> predict
