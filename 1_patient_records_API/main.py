from fastapi import FastAPI, Path, HTTPException, Query
import json

app= FastAPI()

@app.get("/")
def hello():
    return {'message':"Patient Management System API"}

@app.get("/about")
def about():
    return {'message': 'A functional API to manage patients'}

def load_data():
    with open('/Users/ashutosh.verma1/Desktop/fastAPI/1_patient_records_API/patients_db.json', 'r') as f:
        data=json.load(f)

    return data

@app.get("/view")
def view():
    data=load_data()
    return data

@app.get("/patient/{patient_id}") #patient id is a dynamic path parameter. Path parameter is a dynamic value in the url used to identify specific resource (patient in this case)
def view_patient(patient_id: str=Path(..., description="ID of patient in the DB", example="P001")): 
    """
    Path() func is used for adding description, validation, type hint etc. about the path parameter so that it is easier for the client to understand what to input. When we go to /docs endpoint, these details will be shown there. three dots at the start means this is mandatory parameter
    """
    data=load_data()
    if patient_id in data:
        return data[patient_id]
    # return {'message':"Patient not found"}
    """ when data is not found, the status code should be 404. But the above return statement returns 202 (means request processed successfully) with the message- Patient not found. But the status code should be 404. Therefore, we use HTTPException to raise exception with appropriate code and message when something goes wrong. These details about code etc can be checked in /docs while trying out inputs.
    """
    raise HTTPException(status_code=404, detail='Patient not found')

    
@app.get("/sort")
def sort_patient(sort_by: str= Query(..., description="sort patients by either height, weight, bmi"), order: str=Query('asc', description="decide whether to sort in asc or desc order. Default is asc")):
    """
    Query() function is used to pass query parameters. three dots parameter means this parameter is mandatory to pass. 
    """
    valid_field= ['height', 'weight', 'bmi']
    if sort_by not in valid_field:
        raise HTTPException(status_code=400, detail=f"invalid field. select from {valid_field}") 

    if order not in ('asc', 'desc'):
        raise HTTPException(status_code=400, detail="invalid order, select from 'asc', 'desc' ")
    data=load_data()

    sorted_data=sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse='asc'!=order)
    return sorted_data

