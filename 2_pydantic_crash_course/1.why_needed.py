def insert_patient_data(name, age):
    # operations needed to push data to datawarehouse
    print(name)
    print(age)
    print("inserted data into database")

def insert_patient_data(name, age):
    if type(name)!=str and type(age)!=int:
        raise TypeError("Invalid type")

    if age<0:
        raise ValueError("age can't be negative")
    
    # operations needed to push data to datawarehouse
    print(name)
    print(age)
    print("inserted data into database")

"""
Imagine there is a function to insert data into database. A programer can call this function with insert_patient_data("temp", "thirty"). But the age was expected to be a numeric value. And it since python has dynamic typing, this code will work. So age can have numeric and str values. But we need to ensure that age is passed only as a numeric value (data validation). 
One thing that can be done is use type hints insert_patient_data(name: str, age: int). this will show what data type is expected while calling the function but it won't enforce data validation- the user can still enter invalid input and the code will work. Other way is to manually check the dtype which is not scalable and requires manuall coding for each function- makes the codebase messy.  

Pydantic solves this problem- 
1. data validation
2. Pydantic solves the other problem of putting constraints over the inputs e.g. age>0 
"""

from pydantic import BaseModel

# 1. creating pydantic model
class Patient(BaseModel):
    name: str
    age: int

# 2. instantiating the model- creating an object of the above clss
patient_info={'name':'temp', 'age':30}
patient=Patient(**patient_info)

# 3. if the data is correctly entered- patient object will be created. This is passed to the function.

def insert_patient_data(patient: Patient):
    # operations needed to push data to datawarehouse
    print(patient.name)
    print(patient.age)
    print("inserted data into database")

patient_info={'name':'temp', 'age':'thirty'}
patient1=Patient(**patient_info)
insert_patient_data(patient1)
