# def insert(name: str, age: int): # the name should be str and the age should be int
# # To solve this we can use type hinting (name: str, age: int)
# # but the problem with the typehinting is that it doesn't produce error

#     # print(name)
#     # print(age)
#     # print('inserted into the database')

# # another way to solve is adding condition
# # but it is not scalable
#     if type(name) == str and type(age) == int:
#         # data validation
#         if age < 0:
#             raise ValueError('age cant be negative')
#         else:
#             print(name)
#             print(age)
#             print('inserted into the database')
#     else:
#         print('incorrect data type')


# insert('Roman', 'twenty') # because of dynamic typing of python it will accept str

from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):
    name: str = Annotated[str, Field(max_length=20, title='name of the patient', description='name should be less than 20 char', examples=['Roman', 'Nahid'])]
    email: EmailStr
    linkedin: AnyUrl
    age: int = Field(gt=20, lt=40)
    weight: Annotated[float, Field(gt=0, strict=True)] # using 'strict = True' to turn of the automatic type coercion 
    married: bool = False
    # allergies: Optional[list[str]] = None # to make the field optional
    # allergies: list[str] = None
    # allergies: list[str] = Field(max_items=5)
    # allergies: Optional[List[str]] = Field(default=None, max_items=5)
    allergies: List[str] = Field(default=None, max_items=5)
    contact: Dict[str, str]

def insert(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.married)
    print(patient.allergies)
    print('inserted into the database')

patient_data = {'name': 'Roman', 'email': 'abc@gmail.com', 'linkedin': 'http://linkedin.com/roman', 'age': 24, 'weight': 72.5, 'married': True, 'allergies': ['a', 'b'], 'contact': {'phone': '016000'}}
validated_data = Patient(**patient_data) # '**' to unpack the dictonary

insert(validated_data)

# def update(patient: Patient):
#     print(patient.name)
#     print(patient.age)
#     print('updated')

# update(validated_data)