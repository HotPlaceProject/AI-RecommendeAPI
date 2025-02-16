# app/api/v1/schemas/recommendation.py
from pydantic import BaseModel, Field
from typing import List


class Restaurant(BaseModel):
    name: str = Field(description="식당 이름")
    description: str = Field(description="식당 설명")
    reason: str = Field(description="추천 이유")
    url: str = Field(description="식당 URL")


class Recommendation(BaseModel):
    msg: str
    restaurants: List[Restaurant]


class User(BaseModel):
    age: int = Field(description="나이")
    gender : str = Field(description="성별")


class RecommendationRequest(BaseModel):
    user: User
    region: str = Field(description="지역")
    category: str = Field(description="선호유형")

    class Config:
        schema_extra = {
            "example": {
                "user": {
                    "age": 20,
                    "gender": "남성"
                },
                "region": "대치동",
                "category": "국밥"
            }
        }
