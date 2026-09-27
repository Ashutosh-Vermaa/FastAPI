"""these fields are computed from the used input data but not directly entered by the user. E.g. we have height and weight and we want to get BMI"""

from pydantic import BaseModel, EmailStr, AnyUrl, Field, model_validator, computed_field
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):
    name: str
    email: EmailStr 
    linked_in_url: AnyUrl 
    age: int= Field(gt=16, lt=60) 
    weight: float = Field(gt=0) 
    height: float = Field(gt=0) 
    allergies: List[str] = Field(max_length=5)
    contact_details: Dict[str, str]

    @computed_field
    @property 
    def bmi(self)->float: #it gets class instance as the input to the function
        bmi=round(self.weight/(self.height**2), 2)
        return bmi

def update_client_data(patient: Patient):
    print(patient.name)
    print(patient.email)
    print(patient.age)
    print("BMI", patient.bmi)


patient_info={'name':'temp','email':'temp@hdfc.com' ,'linked_in_url':'http://temp.com','age':30,'height':1.7 ,'weight':60.5, 'allergies':['dust', 'ac'],'contact_details':{'mob': '8578574954'} }
patient1=Patient(**patient_info)
update_client_data(patient1)

"""field validator operates in two modes- before and after. Before means- it gets the value before type coersion. default is after"""
    