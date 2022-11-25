FROM python:3.9-slim-buster

WORKDIR /online_inference

COPY ./requirements.txt /online_inference/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /online_inference/requirements.txt

COPY ./app /online_inference

ENV MODEL_PATH="data/model.joblib"
ENV MODEL_URL="https://s-dt2.cloud.gcore.lu/data/model.joblib"

CMD ["python3", "main.py"]
