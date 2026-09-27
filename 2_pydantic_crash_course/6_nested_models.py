"""using 1 pydantic model inside anther pydantic model as a field. E.g. if we set address as a string datatype in the model, fetching the city, pincode etc. will be challenging from it. Address is a complex datatype- combination of other datatypes. For such cases, we should create a model for adddress separately and use that model as the data type for address. """

from pydantic import BaseModel, EmailStr, AnyUrl, Field, model_validator, computed_field
from typing import List, Dict, Optional, Annotated

class Address(BaseModel):
    city: str
    state: str
    pincode: str

class Patient(BaseModel):
    name: str
    gender: str 
    address: Address
    age: int= Field(gt=16, lt=60) 

address_dict= {'city':'Gurgaon', 'state':'haryana', 'pincode':'12432'}
address1=Address(**address_dict)

patient_info={'name':'temp','age':30,'gender': "male", 'address':address1 }
patient1=Patient(**patient_info)

print(patient1.name)
print(patient1.address.city)