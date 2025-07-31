from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):
    name: str
    email: EmailStr
    age: int
    weight: float
    married: bool
    contact: Dict[str, str]

    @field_validator('email', mode='after') # using 'mode='after'' means getting value after type coercion
    @classmethod
    def email_val(cls, value):
        valid_dom = ['green.com']
        domain = value.split('@')[-1]
        
        if domain not in valid_dom:
            raise ValueError('Not valid domain')
        return value
    
    @field_validator('name', mode='before') # using 'mode='before'' means getting value before type coercion
    @classmethod
    def transform_name(cls, value):
        return value.upper()

def update(patient: Patient):
    print(patient.name)
    print(patient.age)
    print('updated')

patient_data = {'name': 'Roman', 'email': 'abc@green.com', 'age': 24, 'weight': 72.5, 'married': True, 'contact': {'phone': '016000'}}
validated_data = Patient(**patient_data)

update(validated_data)
