from fastapi.testclient import TestClient
from server.app import app
from data.fake_data import gen_dataset
import json

client = TestClient(app)


def test_predict():
    for data in gen_dataset(10):
        response = client.post("/predict", content=json.dumps(data))

        assert response.status_code == 200
        assert "condition" in response.json()

    data = {
        'age': 69,
        'sex': 1,
        'cp': 0,
        'trestbps': 170,
        'chol': 288,
        'fbs': 0,
        'restecg': 2,
        'thalach': 159,
        'exang': 0,
        'oldpeak': 1.2,
        'slope': 1,
        'ca': 0,
        'thal': 2
    }
    response = client.post('/predict', content=json.dumps(data))
    assert response.status_code == 200
    assert response.json() == {'condition': 'sick'}


def test_predict_validation():
    data = gen_dataset(1)[0]
    data['sex'] = -69
    response = client.post('/predict', content=json.dumps(data))
    assert response.status_code == 400


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

