import os
import mlflow
import click
import pickle
import pandas as pd
from sklearn.ensemble import RandomForestClassifier


@click.command('train')
@click.option('--input-dir', type=click.Path())
@click.option('--output-dir', type=click.Path())
def train(input_dir, output_dir):
    mlflow.set_tracking_uri("http://localhost:6969")
    with mlflow.start_run(run_name='train'):
        run = mlflow.active_run()

        os.makedirs(output_dir, exist_ok=True)
        data = pd.read_csv(os.path.join(input_dir, 'x_train.csv'))
        target = pd.read_csv(os.path.join(input_dir, 'y_train.csv'))

        rf = RandomForestClassifier(max_depth=3)
        rf.fit(data, target)

        params = rf.get_params()
        for param in params:
            mlflow.log_param(param, params[param])

        with open(os.path.join(output_dir, f'rf_model_{run.info.run_id}.pkl'), 'wb') as f:
            pickle.dump(rf, f)

        mlflow.sklearn.log_model(
            sk_model=rf,
            artifact_path="random_forest_model",
            registered_model_name='rf_model')


if __name__ == '__main__':
    train()
