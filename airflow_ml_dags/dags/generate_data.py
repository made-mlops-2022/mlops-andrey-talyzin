from airflow import DAG
import airflow
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount
from variables import MOUNT_DIR, default_args


with DAG(
    'generate_data',
    default_args=default_args,
    schedule_interval='@daily',
    start_date=airflow.utils.dates.days_ago(5)
) as dag:
    generate = DockerOperator(
        image='airflow-generate-data',
        command='--output-dir /data/raw/{{ ds }}',
        network_mode='bridge',
        task_id='docker-airflow-generate-data',
        do_xcom_push=False,
        auto_remove=True,
        mounts=[Mount(source=MOUNT_DIR, target='/data', type='bind')]
    )

    generate
