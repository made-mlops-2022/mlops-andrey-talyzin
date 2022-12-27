import json
import logging
import requests
from data.fake_data import gen_dataset

logger = logging.getLogger('Requests')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
logger.addHandler(handler)

response = requests.get("http://localhost:8080/health")

logger.info(f"Health: {response.json()}")
logger.info(f"Status code: {response.status_code}")

for data in gen_dataset(10):
    print(data)
    response = requests.post("http://localhost:8080/predict", json.dumps(data))

    logger.info(f"Response: {response.json()}")
    logger.info(f"Status code: {response.status_code}")

