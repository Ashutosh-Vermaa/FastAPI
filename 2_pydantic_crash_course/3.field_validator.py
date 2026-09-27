"""there can be cases where we want to identify if the email belongs to a specific company employee- e.g. they get a discount at the hospital etc. Or we want to ensure that the name is in capital letters- we use field validator to transform

We need to create a class method for this using the field_validator decorator"""


from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):
    name: str
    email: EmailStr 
    linked_in_url: AnyUrl 
    age: int= Field(gt=16, lt=60) 
    weight: float = Field(gt=0) 
    allergies: List[str] = Field(max_length=5)
    contact_details: Dict[str, str]

    @field_validator('email') #applying field validation on email field
    @classmethod
    def email_validator(cls, value):
        """
        cls is the class Patient and value is the value of the email field. cls is passed to so that that class's other methods can also be used if needed inside this function. 
        """
        valid_domains=['hdfc.com', 'icici.com']
        domain_name=value.split("@")[-1]

        if domain_name not in valid_domains:
            raise ValueError('not valid domain')
        return value

    @field_validator('name')
    @classmethod
    def transform_name(cls, name):
        return name.upper()


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