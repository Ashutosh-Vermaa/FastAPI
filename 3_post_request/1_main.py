from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, AnyUrl, Field, model_validator, computed_field
from fastapi.responses import JSONResponse
from typing import List, Dict, Optional, Annotated, Literal
import json


class Patient(BaseModel):
    id: Annotated[str, Field(...,description="id of the patient")]  
    name: Annotated[str, Field(...,description="name of the patient")]  
    gender: Annotated[Literal['male', 'female', 'others'], Field(...,description="gender of the patient"), ]  
    age: Annotated[int, Field(...,description="gender of the patient",gt=0, lt=120)] 
    city: Annotated[str, Field(...,description="city of the patient"), ]
    height: Annotated[float, Field(...,description="height of the patient"), ]
    weight: Annotated[float, Field(...,description="weight of the patient"), ] 

    @computed_field
    @property
    def bmi(self)->float:
        return round(self.weight/(self.height**2),2)

    @computed_field
    @property
    def verdict(self)->str:
        if self.bmi<18.5:
            return 'Underweight'
        elif self.bmi<30:
            return 'Normal'
        else:
            return 'Obese'

def save_data(data):
    with open('/Users/ashutosh.verma1/Desktop/fastAPI/1.patient_records_API/patients_db.json', 'w') as f:
        json.dump(data, f)

app=FastAPI()

@app.post("/create")
def create_patient(patient:Patient):
    #load existing data
    with open('/Users/ashutosh.verma1/Desktop/fastAPI/1.patient_records_API/patients_db.json', 'r') as f:
        data=json.load(f)
    #check the patient id doesn't exist    
    if patient.id in data:
        raise HTTPException(status_code=400,detail="patient alreay exists")

    #add patient to data
    data[patient.id]= patient.model_dump(exclude=['id'])

    #save the data
    save_data(data)

    return JSONResponse(status_code=201, content='patient created successfully')

    
    
