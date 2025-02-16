# app/api/v1/routers/recommend.py
from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse

from app.api.vi.schemas.recommendation import RecommendationRequest
from app.services.recommendation_service import recommend_restaurant

router = APIRouter()

@router.post("/recommend")
async def recommend(req: RecommendationRequest = Body(..., example={
    "user": {
        "age": 20,
        "gender": "남성"
    },
    "region": "대치동",
    "category": "국밥"
})):
    """
    POST /recommend

    LangChain & Tavily Search를 활용하여 맛집을 추천해주는 REST API.
    """
    # 추천 로직 호출
    recommendation_dict = recommend_restaurant(req)

    return JSONResponse(content={"result": recommendation_dict})