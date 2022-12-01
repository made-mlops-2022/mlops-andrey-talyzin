import os

import click
import pandas as pd
import mlflow.pyfunc


@click.command('predict')
@click.option('--input-dir', type=click.Path())
@click.option('--output-dir', type=click.Path())
def predict(input_dir: str, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    data = pd.read_csv(os.path.join(input_dir, 'train_data.csv'))  # processed data

    mlflow.set_tracking_uri("http://localhost:6969")
    model = mlflow.pyfunc.load_model(
        model_uri='models:/rf_model/Production'
    )

    pred = model.predict(data)
    pd.DataFrame(pred).to_csv(os.path.join(output_dir, 'output.csv'), index=False)


if __name__ == '__main__':
    predict()
