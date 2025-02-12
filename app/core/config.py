# app/core/config.py
import os
import secrets
from typing import Annotated, Any, Literal, ClassVar
from pathlib import Path

from pydantic import AnyUrl, BeforeValidator, computed_field, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# parse_cors 유틸 함수
def parse_cors(v: Any) -> list[str] | str:
    """
    CORS 원본 문자열 또는 리스트를 파싱해 list[str]으로 변환.
    예) "http://localhost:3000, https://example.com"
        -> ["http://localhost:3000", "https://example.com"]
    """
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(f"Invalid CORS format: {v}")


class Settings(BaseSettings):
    """
    Pydantic v2의 BaseSettings & SettingsConfigDict를 활용한 설정 정의.
    .env 파일에서 환경 변수를 자동으로 로드하며, 
    속성에 대한 기본값 / 타입 검증 로직을 제공한다.
    """
    BASE_DIR: ClassVar[Path] = Path(__file__).resolve().parent.parent
    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env")
    )

    # === 일반 설정 ===
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = Field(default_factory=lambda: secrets.token_urlsafe(32))
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 60 minutes * 24 hours * 8 days

    # === FastAPI / CORS 설정 ===
    FRONTEND_HOST: str = "http://localhost:5173"
    BACKEND_CORS_ORIGINS: Annotated[list[AnyUrl] | str, BeforeValidator(parse_cors)] = []

    @computed_field
    @property
    def all_cors_origins(self) -> list[str]:
        """
        FRONTEND_HOST와 BACKEND_CORS_ORIGINS를 합쳐서 
        최종적으로 CORS 허용 origin 리스트를 반환.
        """
        # 각 origin을 문자열로 변환 후, 마지막 '/'를 제거
        base = [str(origin).rstrip("/") for origin in self.BACKEND_CORS_ORIGINS]
        base.append(self.FRONTEND_HOST.rstrip("/"))
        return base

    # === API 키 설정 ===
    OPENAI_API_KEY: str = Field(default="asd", env="OPENAI_API_KEY")
    TAVILY_API_KEY: str = Field(default="qwe", env="TAVILY_API_KEY")

    # 필요한 추가 환경 변수가 있다면 여기에 선언하면 됨

# 실제 인스턴스
settings = Settings()

print("config Loaded:", settings.OPENAI_API_KEY)