import pandas as pd
import numpy as np
import os

from src.models.train_model import main as train
from src.models.predict_model import main as predict
from src.models.train_model import Config, LogReg

from click.testing import CliRunner

from faker import Faker


def gen_dataset(row_num: int):
    fake = Faker()

    rows = [
        {
            "sex": fake.random_int(min=0, max=1),
            "cp": fake.random_int(min=0, max=4),
            "fbs": fake.random_int(min=0, max=1),
            "restecg": fake.random_int(min=0, max=2),
            "exang": fake.random_int(min=0, max=1),
            "slope": fake.random_int(min=0, max=2),
            "ca": fake.random_int(min=0, max=4),
            "thal": fake.random_int(min=0, max=2),
            "age": fake.random_int(min=29, max=77),
            "trestbps": fake.random_int(min=94, max=200),
            "chol": fake.random_int(min=126, max=564),
            "thalach": fake.random_int(min=71, max=202),
            "oldpeak": fake.pyfloat(min_value=0, max_value=6.2),
            "condition": fake.random_int(min=0, max=1),
        }
        for x in range(row_num)
    ]

    return pd.DataFrame(rows)


def main() -> None:
    df_train = gen_dataset(300)

    df_train.to_csv('data/raw/gen_dataset.csv')

    config = Config(
        LogReg(C=1.0),
        ['trestbps'],
        'test_model.joblib',
        'gen_dataset.csv',
    )

    train(config)

    assert os.path.isfile('models/test_model.joblib')

    df_test = gen_dataset(100)

    df_test.to_csv('data/raw/gen_dataset.csv')

    runner = CliRunner()
    result = runner.invoke(predict,
                           [
                               "--dataset",
                               'data/raw/gen_dataset.csv',
                               '--model',
                               'models/test_model.joblib',
                               '--output',
                               'data/raw/gen_dataset.csv'
                           ])

    assert result.exit_code == 0

    y_pred = np.genfromtxt('data/raw/gen_dataset.csv', delimiter=',')

    assert y_pred.shape[0] == df_test.shape[0]

    assert set(y_pred) == {0, 1}


if __name__ == "__main__":
    main()
