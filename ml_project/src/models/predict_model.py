import pandas as pd
import numpy as np
# from sklearn.linear_model import LogisticRegression
# from omegaconf import DictConfig, OmegaConf
from loguru import logger
import joblib
import click


# from dataclasses import dataclass
# from hydra.core.config_store import ConfigStore

# from sklearn.pipeline import Pipeline
# from src.features.transformers import SqrTransformer
# from omegaconf import DictConfig, OmegaConf, MISSING
# from src.models.train_model import Config, RF, LogReg, ModelType


@click.command()
@click.option(
    "--model",
    help="Pretrained model path.",
    type=click.Path(exists=True),
    required=True,
)
@click.option(
    "--dataset",
    help="Input dataset in csv format.",
    type=click.Path(exists=True),
    required=True,
)
@click.option(
    "--output",
    help="Output file with predicted labels.",
    type=click.Path(),
    required=True,
)
def main(model: str, dataset: str, output: str) -> None:
    logger.info('Reading data')

    df = pd.read_csv(dataset)

    if 'condition' in df.columns:
        df = df.drop(['condition'], axis=1)

    #     with open(model, 'rb') as file:
    #         model = pickle.load(file)
    #         logger.info('Model loaded')

    model = joblib.load(model)

    y_pred = model.predict(df)

    logger.info('Saving results')

    np.savetxt(output, y_pred, delimiter=",")


if __name__ == "__main__":
    main()
