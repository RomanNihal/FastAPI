from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal
import pickle
import pandas as pd

# import the ml model
with open('project_2\model.pkl', 'rb') as file:
    model = pickle.load(file)

app = FastAPI()

tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
tier_2_cities = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
    "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
    "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
    "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
    "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
    "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
]

# pydantic model to validate inputs
class u_input(BaseModel):
    age: Annotated[int, Field(..., gt=0, lt=80, description='Age of the user')]
    weight: Annotated[float, Field(..., gt=0, description='Weight of the user in kg')]
    height: Annotated[float, Field(..., gt=0, lt=2.5, description='Height of the user in mtr')]
    income: Annotated[float, Field(..., gt=0, description='Salary of the usere in lpa')]
    smoker: Annotated[bool, Field(..., description='Is user a smoker')]
    city: Annotated[str, Field(..., description='City in which the user lives')]
    occupation: Annotated[Literal['retired', 'freelancer', 'student', 'government_job',
       'business_owner', 'unemployed', 'private_job'], Field(..., description='Occupation of the user lives')]
    
    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight/(self.height**2)
    
    @computed_field
    @property
    def life_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return 'high'
        elif self.smoker and self.bmi < 18:
            return 'high'
        elif self.smoker and self.bmi >= 18:
            return 'medium'
        else:
            return 'Normal'
        
    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return 'young'
        elif self.age < 45:
            return 'adult'
        elif self.age < 60:
            return 'middle aged'
        else:
            return 'senior'
        
    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3
        
@app.post('/predict')
def predict_premium(data: u_input):
    model_input = pd.DataFrame([{
        'income_lpa': data.income,
        'occupation': data.occupation,
        'age_group': data.age_group,
        'city_tier': data.city_tier, 
        'bmi': data.bmi,
        'life_risk': data.life_risk
    }])

    pred = model.predict(model_input)[0]

    return JSONResponse(status_code=200, content={'predicted category': pred})