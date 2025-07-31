from fastapi import FastAPI, Path, HTTPException, Query
# using Path function we can add additional information in the path params
# using HTTPException we can send custom http error responses
# using Query we can send additional information in the url for specific actions like sorting or searching

import json

app = FastAPI()

@app.get('/')
def home():
    return {'message': 'Patient Management System'}

@app.get('/about')
def about():
    return {'message': 'An API to manage the patient records'}

# To load the data from the json file
def load_data():
    with open('project_1/patients.json', 'r') as f:
        data = json.load(f)
    return data

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