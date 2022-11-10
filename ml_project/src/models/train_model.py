import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from omegaconf import MISSING
import hydra
from loguru import logger
import joblib

from dataclasses import dataclass
from hydra.core.config_store import ConfigStore

from sklearn.pipeline import Pipeline

from src.features.transformers import SqrTransformer


@dataclass
class ModelType:
    model_type: str


@dataclass
class LogReg(ModelType):
    model_type: str = "logreg"
    C: float = 0.01


@dataclass
class RF(ModelType):
    model_type: str = "rf"
    max_depth: int = 3


@dataclass
class Config:
    model: ModelType
    sqr_feat: list = MISSING
    model_name: str = 'model.joblib'
    dataset: str = 'heart_cleveland_upload.csv'


cs = ConfigStore.instance()
cs.store(name='base_config', node=Config)
cs.store(group='model', name="logreg", node=LogReg)
cs.store(group='model', name="rf", node=RF)


@hydra.main(version_base=None, config_path='conf', config_name="config")
def main(cfg: Config) -> None:
    logger.info('Reading data')
    df = pd.read_csv('data/raw/' + cfg.dataset)

    X = df.drop('condition', axis=1)
    y = df['condition']

    if cfg.model.model_type == 'logreg':
        model = LogisticRegression(C=cfg.model.C, max_iter=10000)
        logger.info("Using Logistic Regression as model")
    elif cfg.model.model_type == 'rf':
        model = RandomForestClassifier(max_depth=cfg.model.max_depth)
        logger.info("Using Random Forest as model")

    sqr_feat = cfg.sqr_feat

    pipe = Pipeline(
        [
            ('transformer', SqrTransformer(sqr_feat)),
            ('model', model)
        ])

    logger.info('Start training')

    pipe.fit(X, y)

    logger.info('Finished training')

    logger.info('Saving model')

    #     with open('models/'+cfg.model_name, 'wb') as file:
    #         pickle.dump(pipe, file)
    #         logger.info('Model saved')

    joblib.dump(
        pipe,
        'models/' + cfg.model_name,
    )
    logger.info('Model saved')


if __name__ == "__main__":
    main()
