import pytest
from airflow.models import DagBag


@pytest.fixture()
def dagbag():
    return DagBag()


def test_generate(dagbag):
    dag = dagbag.get_dag(dag_id='generate_data')
    assert dagbag.import_errors == {}
    assert dag is not None
    assert len(dag.tasks) == 1


def test_train(dagbag):
    dag = dagbag.get_dag(dag_id='train')
    assert dagbag.import_errors == {}
    assert dag is not None
    assert len(dag.tasks) == 5

    content = {
        "data-availability-sensor": ["docker-airflow-preprocess"],
        "docker-airflow-preprocess": ["docker-airflow-split"],
        "docker-airflow-split": ['docker-airflow-train'],
        "docker-airflow-train": ["docker-airflow-validate"],
        "docker-airflow-validate": []
    }
    for name, task in dag.task_dict.items():
        assert set(content[name]) == task.downstream_task_ids


def test_predict(dagbag):
    dag = dagbag.get_dag(dag_id='predict')
    assert dagbag.import_errors == {}
    assert dag is not None
    assert len(dag.tasks) == 2

    content = {
        "docker-airflow-predict_preprocess": ["docker-airflow-predict"],
        "docker-airflow-predict": []
    }
    for name, task in dag.task_dict.items():
        assert set(content[name]) == task.downstream_task_ids
