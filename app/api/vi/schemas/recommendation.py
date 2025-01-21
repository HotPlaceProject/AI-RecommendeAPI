# app/api/v1/schemas/recommendation.py
from pydantic import BaseModel, Field
from typing import List

class Restaurant(BaseModel):
    name: str = Field(description="식당 이름")
    description: str = Field(description="식당 설명")
    reason: str = Field(description="추천 이유")

class Recommendation(BaseModel):
    msg: str
    restaurants: List[Restaurant]
