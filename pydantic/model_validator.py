from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator, model_validator
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):
    name: str
    email: EmailStr
    age: int
    weight: float
    married: bool
    contact: Dict[str, str]

    @model_validator(mode='after')
    def emergency_contact(cls, model):
        if model.age > 60 and 'emergency' not in model.contact:
            raise ValueError('patient older than 60 must have emergency contact')
        return model


def update(patient: Patient):
    print(patient.name)
    print(patient.age)
    print('updated')

patient_data = {'name': 'Roman', 'email': 'abc@green.com', 'age': 64, 'weight': 72.5, 'married': True, 'contact': {'phone': '016000', 'emergency': '077'}}
validated_data = Patient(**patient_data)

update(validated_data)
