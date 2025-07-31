from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator, model_validator, computed_field
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):
    name: str
    email: EmailStr
    age: int
    weight: float # kg
    height: float # mtr

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2), 2)
        return bmi


def update(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.bmi)
    print('updated')

patient_data = {'name': 'Roman', 'email': 'abc@green.com', 'age': 64, 'weight': 72.5, 'height': 1.62}
validated_data = Patient(**patient_data)

update(validated_data)