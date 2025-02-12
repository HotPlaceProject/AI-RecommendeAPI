# app/services/recommendation_service.py
import json
from typing import Optional
import os

from langchain.chains.llm import LLMChain
from langchain_core.messages import BaseMessage
# LangChain, OpenAI 관련 임포트
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnableConfig, chain, RunnableSerializable
from langchain_openai import ChatOpenAI
from typing import Any, List

# Pydantic 모델
from app.api.vi.schemas.recommendation import Recommendation, User, RecommendationRequest

# config.py에서 환경 변수를 로드
from app.core.config import settings
os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY
os.environ["TAVILY_API_KEY"] = settings.TAVILY_API_KEY

# 검색 툴
from app.langchain_tools.search_web import search_web


def create_prompt_template(feature: str) -> ChatPromptTemplate:
    """
    ChatPromptTemplate을 생성하는 함수
    """
    prompt_template = ChatPromptTemplate([
        ("system", f"""
          당신은 사용자의 나이, 성별, 희망 카테고리을 기반으로 맞춤형 식당을 추천하는 어시스턴트입니다.

          아래 사용자의 특성을 반영해서 맞춤형 맛집을 추천해주세요
          {feature}

        """),
        ("user", "#Format: {format_instructions}\n\n#user_input: {user_input}"),
        ("placeholder", "{messages}")
    ])
    output_parser = JsonOutputParser(pydantic_object=Recommendation) # output parser JsonOutputParser로 설정
    prompt = prompt_template.partial(format_instructions=output_parser.get_format_instructions())

    return prompt


def initialize_llm() -> ChatOpenAI:
    """
    LLM을 호출하는 함수
    """
    return ChatOpenAI(model="gpt-4o-mini")


def execute_web_search_chain(prompt: ChatPromptTemplate) -> Any:
    """
    LLM과 웹 검색 툴을 연결한 체인을 생성하여 반환
    """
    llm = initialize_llm()
    llm_with_tools = llm.bind_tools(tools=[search_web])
    llm_chain = prompt | llm_with_tools

    return llm_chain  # 🔹 체인만 반환 (invoke 실행 X)


def recommend_restaurant(req: RecommendationRequest) -> dict:
    """
    추천 요청을 받아서 맛집을 추천하는 함수
    """
    feature = f"나이: {req.user.age}, 성별: {req.user.gender}, 카테고리: {req.category}"
    prompt = create_prompt_template(feature)

    # 체인 생성
    llm_with_chain = execute_web_search_chain(prompt)

    # invoke 실행 (1차 호출 -> Tool 호출)
    ai_msg = llm_with_chain.invoke({"user_input": req.region}, config=RunnableConfig())
    print("Tool Calling:", ai_msg)

    # search_web 호출하여 추가 데이터 가져오기
    tool_msgs = search_web.batch(ai_msg.tool_calls, config=RunnableConfig())

    # LLM에게 검색 결과를 다시 전달하여 최종 응답 생성 (2차 호출)
    final_response = llm_with_chain.invoke({"user_input": req.region, "messages": [ai_msg, *tool_msgs]}, config=RunnableConfig())
    print("Final AI Response:", final_response)

    # JSON 파싱
    json_str = final_response.content.replace("```json\n", "").replace("\n```", "")
    return json.loads(json_str, strict=False)



