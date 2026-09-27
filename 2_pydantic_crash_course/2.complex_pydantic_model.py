
from pydantic import BaseModel
from typing import List, Dict

"""1. data type validation"""

class Patient(BaseModel):
    name: str
    age: int
    weight: float
    allergies: List[str] #list of str
    contact_details: Dict[str, str] #key, value both are str (mob, email etc. keys)
    """
    We don;t use list(), dict() instead List[str] because list() can only validate that allergies shoult be a list but can't validate the entries in the list as str.
    """

def insert_patient_data(patient: Patient):
    # operations needed to push data to datawarehouse
    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print(patient.allergies)
    print(patient.contact_details)
    print("inserted data into database")

patient_info={'name':'temp', 'age':30, 'weight':60.5, 'allergies':['dust', 'ac'],'contact_details':{'mob': '8578574954', 'email':'asteh@gmail.com'} }
patient1=Patient(**patient_info)
insert_patient_data(patient1)

"""2. By default, all the fields inside pydantic model are required. We can make some of these fields as optional as well. need to give the optional field a default value- None"""
from typing import List, Dict, Optional
class Patient(BaseModel):
    name: str
    age: int
    weight: Optional[float]= None #this will be an optional field now
    allergies: List[str] #list of str
    contact_details: Dict[str, str]
patient_info={'name':'temp', 'age':30, 'allergies':['dust', 'ac'],'contact_details':{'mob': '8578574954', 'email':'asteh@gmail.com'} }
patient1=Patient(**patient_info)
insert_patient_data(patient1)    

"""3. Data Validation- constraints on data"""
from pydantic import BaseModel, EmailStr, AnyUrl

class Patient(BaseModel):
    name: str
    email: EmailStr # this will validate that email has @ and has '.' after @ somewhere
    linked_in_url: AnyUrl # this will ensure that the entry has http: and .
    age: int
    weight: float
    allergies: List[str] #list of str
    contact_details: Dict[str, str]

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

patient_info={'name':'temp','email':'temp@temp.p' ,'linked_in_url':'http://temp.com','age':30, 'weight':60.5, 'allergies':['dust', 'ac'],'contact_details':{'mob': '8578574954'} }
patient1=Patient(**patient_info)
insert_patient_data(patient1)

"""4. custom data validation"""

from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import Annotated

class Patient(BaseModel):
    name: str
    email: EmailStr # this will validate that email has @ and has '.' after @ somewhere
    linked_in_url: AnyUrl # this will ensure that the entry has http: and .
    age: int= Field(gt=16, lt=60) # age between 0 and 60 
    weight: float = Field(gt=0) # this will ensure that value is greated than 0
    allergies: List[str] = Field(max_length=5) #list of str, <=5 len
    contact_details: Dict[str, str]

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

patient_info={'name':'temp','email':'temp@temp.p' ,'linked_in_url':'http://temp.com','age':30, 'weight':60.5, 'allergies':['dust', 'ac'],'contact_details':{'mob': '8578574954'} }
patient1=Patient(**patient_info)
insert_patient_data(patient1)

# we can aslo add metadata to the fields using Annotated
class Patient(BaseModel):
    name: str
    email: Annotated[EmailStr, Field(max_length=50, title='email of patient', description='provide email address', example=['temp@gmail.com'])] # adding metadata
    linked_in_url: AnyUrl 
    age: Annotated[int, Field(default=0, gt=16, lt=60, strict=True)] #adding default value. strict will not allow type conversion from '30' to 30. 
    weight: float = Field(gt=0) # this will ensure that value is greated than 0
    allergies: List[str] = Field(max_length=5) #list of str, <=5 len
    contact_details: Dict[str, str]


