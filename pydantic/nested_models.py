from pydantic import BaseModel

class Address(BaseModel):
    house: str
    village: str
    postal_code: str

class Patient(BaseModel):
    name: str
    gender: str
    age: int
    address: Address

address = {'house': '45/d', 'village': 'choto gadairchar', 'postal_code': 'madhabdi 1604'}

validate_address = Address(**address)

patient = {'name': 'Roman', 'gender': 'male', 'age': 24, 'address': validate_address}

validate_patient = Patient(**patient)

print(validate_patient)
print(validate_patient.address.postal_code)