import os
import click
import pandas as pd
from faker import Faker


def gen_dataset(row_num: int):
    fake = Faker()
    rows = [
        {
            "age": fake.random_int(min=29, max=77),
            "sex": fake.random_int(min=0, max=1),
            "cp": fake.random_int(min=0, max=4),
            "trestbps": fake.random_int(min=94, max=200),
            "chol": fake.random_int(min=126, max=564),
            "fbs": fake.random_int(min=0, max=1),
            "restecg": fake.random_int(min=0, max=2),
            "thalach": fake.random_int(min=71, max=202),
            "exang": fake.random_int(min=0, max=1),
            "oldpeak": fake.pyfloat(min_value=0, max_value=6.2),
            "slope": fake.random_int(min=0, max=2),
            "ca": fake.random_int(min=0, max=4),
            "thal": fake.random_int(min=0, max=2),
            "condition": fake.random_int(min=0, max=1)
        }
        for x in range(row_num)
    ]
    return rows


@click.command('generate')
@click.option('--output-dir', type=click.Path())
def generate_data(output_dir):
    os.makedirs(output_dir, exist_ok=True)
    columns = list(gen_dataset(1)[0].keys())
    fake_data = pd.DataFrame([list(gen_dataset(1)[0].values())], columns=columns)
    for data in gen_dataset(10):
        fake_data = fake_data.append(data, ignore_index=True)

    conditions = fake_data.columns[-1]
    fake_data.drop(conditions, axis=1).to_csv(os.path.join(output_dir, 'data.csv'), index=False)
    fake_data[conditions].to_csv(os.path.join(output_dir, 'target.csv'), index=False)


if __name__ == '__main__':
    generate_data()
