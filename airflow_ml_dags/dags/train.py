import airflow
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.sensors.python import PythonSensor
from docker.types import Mount
from variables import *


with DAG(
    'train',
    default_args=default_args,
    schedule_interval='@weekly',
    start_date=airflow.utils.dates.days_ago(5)
) as dag:
    data_check = PythonSensor(
        task_id='data-availability-sensor',
        python_callable=check_data_exist,
        op_args=[[DATA_PATH, TARGET_PATH]],
        timeout=6000,
        poke_interval=10,
        retries=100,
        mode="poke"
    )

    data_preprocess = DockerOperator(
        image='airflow-preprocess',
        command=f'--input-dir {RAW_DATA} --output-dir {PROCESSED_DATA}',
        network_mode='bridge',
        task_id='docker-airflow-preprocess',
        do_xcom_push=False,
        auto_remove=True,
        mounts=[Mount(source=MOUNT_DIR, target='/data', type='bind')]
    )

    data_split = DockerOperator(
        image='airflow-split',
        command=f'--input-dir {PROCESSED_DATA} --output-dir {SPLITTED_DATA}',
        network_mode='bridge',
        task_id='docker-airflow-split',
        do_xcom_push=False,
        auto_remove=True,
        mounts=[Mount(source=MOUNT_DIR, target='/data', type='bind')]
    )

    train = DockerOperator(
        image='airflow-train',
        command=f'--input-dir {SPLITTED_DATA} --output-dir {MODELS}',
        network_mode='host',
        task_id='docker-airflow-train',
        do_xcom_push=True,
        auto_remove=True,
        mounts=[Mount(source=MOUNT_DIR, target='/data', type='bind'),
                Mount(source=MLRUNS_DIR, target='/mlruns', type='bind')],
    )

    validate = DockerOperator(
        image='airflow-validate',
        command=f'--input-dir {SPLITTED_DATA} --model-dir {MODELS} --output-dir {METRICS}',
        network_mode='host',
        task_id='docker-airflow-validate',
        do_xcom_push=False,
        auto_remove=True,
        mounts=[Mount(source=MOUNT_DIR, target='/data', type='bind'),
                Mount(source=MLRUNS_DIR, target='/mlruns', type='bind')]
    )

    data_check >> data_preprocess >> data_split >> train >> validate
