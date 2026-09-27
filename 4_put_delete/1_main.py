from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, AnyUrl, Field, model_validator, computed_field
from fastapi.responses import JSONResponse
from typing import List, Dict, Optional, Annotated, Literal, Optional
import json


def save_data(data):
    with open('/Users/ashutosh.verma1/Desktop/fastAPI/1.patient_records_API/patients_db.json', 'w') as f:
        json.dump(data, f)

def load_data():
    with open('/Users/ashutosh.verma1/Desktop/fastAPI/1.patient_records_API/patients_db.json', 'r') as f:
        data=json.load(f)
    return data

class Patient(BaseModel):
    id: Annotated[str, Field(..., description='ID of the patient', examples=['P001'])]
    name: Annotated[str, Field(..., description='Name of the patient')]
    city: Annotated[str, Field(..., description='City where the patient is living')]
    age: Annotated[int, Field(..., gt=0, lt=120, description='Age of the patient')]
    gender: Annotated[Literal['male', 'female', 'others'], Field(..., description='Gender of the patient')]
    height: Annotated[float, Field(..., gt=0, description='Height of the patient in mtrs')]
    weight: Annotated[float, Field(..., gt=0, description='Weight of the patient in kgs')]

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


class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal['male', 'female']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]

"""
user can send any fields' data to update- that we don;t know
"""
@app.put("/update/{patient_id}")
def update_patient(patient_id:str, patient: PatientUpdate):
    data=load_data()
    if patient_id not in data:
        raise HTTPException(status_code= 404, detail='patient not found')

    patient_data=data.get(patient_id)
    for key, val in patient.model_dump(exclude_unset=True).items():
        # exclude_unset=True so that the default values don't overwrite
        patient_data[key]=val


    """the issue here is that if weight or height changes, bmi and verdict are not updated. Therefore, we convert this object to pydantic object first so that those fields will be calculated and convert back to dict and set it to patient id in database. """
    patient_data['id']=patient_id
    pydantic_obj=Patient(**patient_data)

    data[patient_id]=pydantic_obj.model_dump(exclude='id')

    save_data(data)

    return JSONResponse(status_code=200, content={'message':'patient data updated'})


@app.delete("/delete/{patient_id}")
def delete_patient(patient_id):
    data=load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail= 'patient not found')
    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200, content={'message':'patient deleted'})
