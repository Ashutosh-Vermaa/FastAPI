from pydantic import BaseModel, Field, computed_field, field_validator
from typing import Literal , Annotated
from config.config import tier_1_cities, tier_2_cities


# pydantic model to validate incoming data
class Customer(BaseModel):
    age: int= Field(...,description='age of the person', gt=1, lt=90)	
    weight: float=Field(...,description='weight of the person in kg', gt=0)	
    height: float=Field(...,description='height of the person in meter', gt=0)	
    income_lpa: float=Field(...,description='income of the person', gt=0)	
    smoker: Annotated[bool, Field(...,description='does the person smoke')]
    city: str= Field(...,description='city of the person')
    occupation: Annotated[Literal['retired', 'freelancer', 'student', 'government_job',
       'business_owner', 'unemployed', 'private_job'], Field(...,description='occupation of the person')]

    @field_validator('city')
    @classmethod
    def normalize_city(cls, value):
        v=value.strip().title()
        return v
    
    @computed_field
    @property
    def bmi(self)->float: #it gets class instance as the input to the function
        bmi=round(self.weight/(self.height**2), 2)
        return bmi

    @computed_field
    @property
    def age_group(self)->str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        return "senior"

    @computed_field
    @property
    def lifestyle_risk(self)->str:
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker or self.bmi > 27:
            return "medium"
        else:
            return "low"

    @computed_field
    @property
    def city_tier(self)->int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3