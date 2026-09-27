from fastapi import FastAPI
import numpy as np
import pickle
import pandas as pd
from schemas.requests import Customer
from schemas.response import PredictionResponse
from ml.predict import predict_output, model, MODEL_VERSION
from fastapi.responses import JSONResponse

app=FastAPI()

if app is not None:
    print('API obj created')

@app.get('/')
def home():
    return {'message':"Insurance Premium prediction API"}    		

@app.get('/health')
def health_check():
    return {
        'status': 'OK',
        'version':MODEL_VERSION,
        'model_loaded': model is not None

    }

@app.post('/predict', response_model=PredictionResponse)
def predict(customer: Customer):
    X = {
    "bmi": customer.bmi,
    "age_group": customer.age_group,
    "lifestyle_risk": customer.lifestyle_risk,
    "city_tier": customer.city_tier,
    "income_lpa": customer.income_lpa,
    "occupation": customer.occupation
    }

    try:
        output=predict_output(X)
        #before returning the output, it will be validated using PredictionResponse
        return JSONResponse(status_code=200, content={'response': output})
    except Exception as e:
        return JSONResponse(status_code=500, content=str(e))
    