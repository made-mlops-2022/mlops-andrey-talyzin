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
        }
        for x in range(row_num)
    ]

    return rows
