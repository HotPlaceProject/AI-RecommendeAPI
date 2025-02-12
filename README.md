# FastAPI 맛집 추천 AI API

## 📌 프로젝트 개요
FastAPI를 사용하여 사용자의 취향에 맞는 맛집을 추천하는 AI API 서버입니다.

## 🚀 실행 방법
### 1. Poetry 가상 환경 설정
Poetry를 사용하여 가상 환경을 설정합니다.
```bash
poetry install
```

### 2. 환경 변수 설정
`.env` 파일을 생성하고 다음 내용을 추가하세요.
```env
OPENAI_API_KEY=your_openai_api_key_here
```
이 API 키가 없으면 OpenAI 관련 기능이 동작하지 않습니다.

### 3. 서버 실행
아래 명령어로 FastAPI 서버를 실행할 수 있습니다.
```bash
poetry run uvicorn app.main:app --port 8080
```

### 4. API 접근 경로
| 기능 | 경로 |
|------|------|
| API 문서 (Swagger UI) | [http://localhost:8080/docs](http://localhost:8080/docs) |
| API 문서 (ReDoc) | [http://localhost:8080/redoc](http://localhost:8080/redoc) |

## 📡 API 사용 방법
### 🔹 맛집 추천 API
- **엔드포인트:** `/api/v1/recommend`
- **메서드:** `POST`
- **요청 형식:** JSON
  ```json
  {
    "user_preferences": "20, 남성, 서울, 매운 음식"
  }
  ```
- **응답 형식:** JSON
  ```json
  {
    "recommendations": [
      "신촌 맛집 - 매운 닭갈비",
      "강남 맛집 - 매운 곱창",
      "홍대 맛집 - 얼큰한 부대찌개"
    ]
  }
  ```

## ⚙️ 폴더 구조
```
app/
│── main.py          # FastAPI 서버 메인 파일
│── api/
│   │── v1/
│   │   │── routers/
│   │   │   │── recommend.py  # 맛집 추천 API 라우터
│   │   │── schemas/
│   │   │   │── recommendation.py  # 데이터 모델
│── core/
│   │── config.py  # 환경 변수 설정
│── langchain_tools/
│   │── search_web.py  # 웹 검색 기능
│── services/
│   │── .env  # 환경 변수 파일
```

## 📌 기타 사항
- 서버 실행 시 `--reload` 옵션을 사용하면 코드 변경 시 자동으로 재시작됩니다.
  ```bash
  poetry run uvicorn app.main:app --port 8080 --reload
  ```
- `.env` 파일을 사용하여 API 키 등의 환경 변수를 관리할 수 있습니다.

