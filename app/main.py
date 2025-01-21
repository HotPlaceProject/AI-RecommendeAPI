# app/main.py
import os
from fastapi import FastAPI

# config.py에서 환경 변수를 로드 (미리 import하는 순간 .env도 로드)
from app.core.config import settings
from app.api.vi.routers.recommend import router as recommend_router

# 실제로 .env의 내용을 os.environ에 세팅
os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY
os.environ["TAVILY_API_KEY"] = settings.TAVILY_API_KEY

# FastAPI 인스턴스 생성
app = FastAPI(
    title="My Recommendation API",
    version="1.0.0",
    description="LangChain + FastAPI를 활용한 맛집 추천 API"
)

# 라우터 등록
app.include_router(recommend_router, prefix="/api/v1", tags=["recommend"])

@app.get("/")
async def root():
    return {"message": "Hello! This is a recommendation API."}
