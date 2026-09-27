"""if we need to validate a combination of fields, then model validator is used. field validator is used to validate a single field.E.g. if age >60, contact_details should have an emergency contact."""

from pydantic import BaseModel, EmailStr, AnyUrl, Field, model_validator
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):
    name: str
    email: EmailStr 
    linked_in_url: AnyUrl 
    age: int= Field(gt=16, lt=60) 
    weight: float = Field(gt=0) 
    allergies: List[str] = Field(max_length=5)
    contact_details: Dict[str, str]

    @model_validator(mode='after') #no field name passed as this is applied on the whole pydantic object.
    def validate_emergency_contact(cls, model):
        """
        cls is the class Patient and model is the pydantic model. cls is passed to so that that class's other methods can also be used if needed inside this function. 
        """
        if model.age>60 and 'emergency' not in model.contact_details:
            raise ValueError("expectede emergency contact")
        return model

def insert_patient_data(patient: Patient):
    # operations needed to push data to datawarehouse
    print(patient.name)
    print(patient.email)
    print(patient.linked_in_url)
    print(patient.age)
    print(patient.weight)
    print(patient.allergies)
    print(patient.contact_details)
    print("inserted data into database")

patient_info={'name':'temp','email':'temp@hdfc.com' ,'linked_in_url':'http://temp.com','age':30, 'weight':60.5, 'allergies':['dust', 'ac'],'contact_details':{'mob': '8578574954'} }
patient1=Patient(**patient_info)
insert_patient_data(patient1)

"""field validator operates in two modes- before and after. Before means- it gets the value before type coersion. default is after"""