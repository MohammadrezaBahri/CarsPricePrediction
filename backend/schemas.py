from typing import Union

from pydantic import BaseModel

class Post(BaseModel):
    usage: int
    third_party_insurance_deadline: int
    production_year: int
    motor_status: str
    color: str
    body_status: str
    chassis_status: str
    fuel_type: str
    brand_model_level1: str
    brand_model_level2: Union[str, None] = None
    brand_model_level3: Union[str, None] = None

class Prediction(BaseModel):
    predicted_price: int