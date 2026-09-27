from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Literal , Annotated
from .config import tier_1_cities, tier_2_cities
import numpy as np
import pickle
import pandas as pd

# import ML model
def load_model():
    with open(
        '/Users/ashutosh.verma1/Desktop/fastAPI/5_ml_model_serving/model.pkl',
        'rb') as f:
        model = pickle.load(f)
    return model


app=FastAPI()

# pydantic model to validate incoming data
class Customer(BaseModel):
    age: int= Field(...,description='age of the person', gt=1, lt=90)	
    weight: float=Field(...,description='weight of the person in kg', gt=0)	
    height: float=Field(...,description='height of the person in meter', gt=0)	
    income_lpa: float=Field(...,description='income of the person', gt=0)	
    smoker: Annotated[bool, Field(...,description='does the person smoke')]
    city: str= Field(...,description='city of the person')
    occupation: Annotated[Literal['retired', 'freelancer', 'student', 'government_job',
       'business_owner', 'unemployed', 'private_job'], Field(...,description='occupation of the person')]
 
    @computed_field
    @property
    def bmi(self)->float: #it gets class instance as the input to the function
        bmi=round(self.weight/(self.height**2), 2)
        return bmi

    @computed_field
    @property
    def age_group(self)->str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        return "senior"

    @computed_field
    @property
    def lifestyle_risk(self)->str:
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker or self.bmi > 27:
            return "medium"
        else:
            return "low"

    @computed_field
    @property
    def city_tier(self)->int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3
    		

@app.post('/predict')
def predict(customer: Customer):
    X = pd.DataFrame([{
    "bmi": customer.bmi,
    "age_group": customer.age_group,
    "lifestyle_risk": customer.lifestyle_risk,
    "city_tier": customer.city_tier,
    "income_lpa": customer.income_lpa,
    "occupation": customer.occupation
    }])



    model=load_model()

    output=model.predict(X)[0]

    return JSONResponse(status_code=200, content={'predicted category is': output})



    