import os
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
import joblib
from data.model import HeartRequest
import urllib.request
import pandas as pd

app = FastAPI()
model = None


@app.on_event("startup")
def load_model():
    model_path = os.getenv("MODEL_PATH")
    # model_path = "data/model.joblib"
    model_url = os.getenv("MODEL_URL")
    # model_url = 'https://s-dt2.cloud.gcore.lu/data/model.joblib'
    if not os.path.exists(model_path):
        urllib.request.urlretrieve(model_url, model_path)
    global model
    model = joblib.load(model_path)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)


@app.post("/predict")
async def predict(data: HeartRequest):
    request = pd.DataFrame([data.dict()])
    result = model.predict(request)
    condition = 'sick' if result[0] else 'healthy'

    return {"condition": condition}


@app.get("/health", status_code=200)
async def health():
    global model
    if model is None:
        raise HTTPException(status_code=404, detail="Model not found")
    return {"status": "ok"}
