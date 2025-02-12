# app/api/v1/routers/recommend.py
from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse

from app.services.recommendation_service import recommend_restaurant

router = APIRouter()

@router.post("/recommend")
async def recommend(user_query: str = Body(..., example="대치동 맛집")):
    """
    POST /recommend

    LangChain & Tavily Search를 활용하여 맛집을 추천해주는 REST API.
    """
    # 추천 로직 호출
    recommendation_dict = recommend_restaurant(user_query)

    # JSON 형식의 문자열을 그대로 반환
    # todo : json.loads(json_str)를 거쳐 Python dict로 만든 뒤 반환

    return JSONResponse(content={"result": recommendation_dict})