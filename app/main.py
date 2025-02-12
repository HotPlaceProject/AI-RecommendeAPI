# app/main.py
from fastapi import FastAPI
from app.api.vi.routers.recommend import router as recommend_router


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
