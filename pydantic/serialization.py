from pydantic import BaseModel

class Address(BaseModel):
    house: str
    village: str
    postal_code: str

class Patient(BaseModel):
    name: str
    gender: str = 'Male'
    age: int
    address: Address

address = {'house': '45/d', 'village': 'choto gadairchar', 'postal_code': 'madhabdi 1604'}

validate_address = Address(**address)

patient = {'name': 'Roman', 'age': 24, 'address': validate_address}

validate_patient = Patient(**patient)

# export
# dictionary_ = validate_patient.model_dump(include=['name', 'age'])
# dictionary_ = validate_patient.model_dump(exclude=['name', 'age'])
# dictionary_ = validate_patient.model_dump(include={'address':['village', 'postal_code']})
# dictionary_ = validate_patient.model_dump(exclude={'address':['village']})
# dictionary_ = validate_patient.model_dump(exclude_unset=True)
dictionary_ = validate_patient.model_dump()
json_ = validate_patient.model_dump_json()

print(dictionary_)
print(type(dictionary_))

print(json_)
print(type(json_))
