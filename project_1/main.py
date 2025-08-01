from fastapi import FastAPI, Path, HTTPException, Query
# using Path function we can add additional information in the path params
# using HTTPException we can send custom http error responses
# using Query we can send additional information in the url for specific actions like sorting or searching
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json

app = FastAPI()

class Patient(BaseModel):
    id: Annotated[str, Field(..., description='ID of the patient', examples=['p001', 'p002'])]
    name: Annotated[str, Field(..., description='Name of the patient')]
    city: Annotated[str, Field(..., description='City of the patient')]
    age: Annotated[int, Field(..., gt=0, lt=80, description='Age of the patient')]    
    gender: Annotated[Literal['Male', 'Female', 'Others'], Field(..., description='Gender of the patient')]
    height: Annotated[float, Field(..., gt=0, description='Height of the patient in mtrs')]
    weight: Annotated[float, Field(..., gt=0, description='Weight of the patient in kgs')]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi =  round(self.weight/(self.height**2))
        return bmi
    
# we need to build a new pydantic model for update
class P_Update(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None)]
    gender: Annotated[Optional[Literal['Male', 'Female', 'Others']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None)]
    weight: Annotated[Optional[float], Field(default=None)]

# to load the data from the json file
def load_data():
    with open('project_1/patients.json', 'r') as f:
        data = json.load(f)
    return data

# to save the data into the json file
def save_data(data):
    with open('project_1/patients.json', 'w') as f:
        json.dump(data, f)

@app.get('/')
def home():
    return {'message': 'Patient Management System'}

@app.get('/about')
def about():
    return {'message': 'An API to manage the patient records'}

@app.get('/view')
def view():
    data = load_data()
    return data

@app.get('/patient/{patient_id}')
def patient(patient_id: str = Path(..., description='Id of the patient', example='p001')): # "..." means required
    data = load_data()
    
    if patient_id in data:
        return data[patient_id]
    
    raise HTTPException(status_code=404, detail='patient not found')

@app.get('/sort')
def sort(sort_by: str = Query(..., description='sort on the basis of height or weight'), order: str = Query('asc', description='sorting order')):
    data =  load_data()

    valid_fields = ['height', 'weight']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail='invalid field. select from {valid_fields}')
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='invalid field. select from asc and desc')
    
    data = load_data()

    sort_order = True if order=='desc' else False

    sorted_data =  sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)

    return sorted_data

@app.post('/create')
def create(patient: Patient):
    # load existing data
    data = load_data()

    # check if the patient already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient already exists')

    # new patient add to the database
    # need to convert pydantic object to dictionary
    data[patient.id] = patient.model_dump(exclude=['id'])

    # save into the json file
    save_data(data)

    return JSONResponse(status_code=201, content={'message': 'Patient created successfully'})

@app.put('/update/{patient_id}')
def update(patient_id: str, p_update: P_Update):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient id not found')
    
    # extract the existing patient info
    existing_info = data[patient_id]
    
    # converting new info into dictionary
    new_info = p_update.model_dump(exclude_unset=True)

    # updating existing info with new info using loop
    for key, value in new_info.items():
        existing_info[key] = value

    # to update the computed fields we need to convert the existing info into pydantic object so that the computed values update accordingly
    existing_info['id'] = patient_id
    existing_info_pydantic = Patient(**existing_info)
    existing_info = existing_info_pydantic.model_dump(exclude='id')
    
    data[patient_id] = existing_info
    save_data(data)

    return JSONResponse(status_code=200, content={'message': 'Patient updated successfully'})

@app.delete('/delete/{patient_id}')
def delete(patient_id: str):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient id not found')
    
    del data[patient_id]
    save_data(data)

    return JSONResponse(status_code=200, content={'message': 'Patient deleted successfully'})
