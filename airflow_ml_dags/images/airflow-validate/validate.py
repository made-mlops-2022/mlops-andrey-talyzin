import os
import click
import pickle
import mlflow
import json
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score


@click.command('validate')
@click.option('--input-dir', type=click.Path())
@click.option('--model-dir', type=click.Path())
@click.option('--output-dir', type=click.Path())
def validate(input_dir, model_dir, output_dir):

    mlflow.set_tracking_uri("http://localhost:6969")
    model_name = os.listdir(model_dir)[0]
    run_id = model_name[9:-4]

    with mlflow.start_run(run_id=run_id):
        os.makedirs(output_dir, exist_ok=True)
        data = pd.read_csv(os.path.join(input_dir, 'x_val.csv'))
        target = pd.read_csv(os.path.join(input_dir, 'y_val.csv'))

        with open(os.path.join(model_dir, model_name), 'rb') as model_file:
            model = pickle.load(model_file)
        pred = model.predict(data)

        metrics = {'accuracy': accuracy_score(target, pred), 'f1_score': f1_score(target, pred)}

        for metric in metrics:
            mlflow.log_metric(metric, metrics[metric])

        with open(os.path.join(output_dir, 'metric.json'), 'w') as metric_file:
            json.dump(metrics, metric_file)


if __name__ == '__main__':
    validate()
