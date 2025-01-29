# app/services/recommendation_service.py
from typing import Optional
import os

# LangChain, OpenAI 관련 임포트
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnableConfig, chain
# from langchain_openai import ChatOpenAI
from langchain_deepseek import ChatDeepSeek

# Pydantic 모델
from app.api.vi.schemas.recommendation import Recommendation
from app.core.config import settings

# 검색 툴
from app.langchain_tools.search_web import search_web

os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY

# 예시: 사용자 특성
# todo: 실제 사용자 입력을 받아서 feature 변수에 할당
feature = "남성/20대/술집"

# 1) ChatPromptTemplate 구성
# todo: 사용자 입력을 받아서 user_input 변수에 할당
# todo: 프롬프트 수정 - 참고한 소스 제공
prompt_template = ChatPromptTemplate([
  ("system", f"""
      당신은 사용자의 나이, 성별, 선호하는 스타일을 기반으로 맞춤형 식당을 추천하는 어시스턴트입니다.

      아래 사용자의 특성을 반영해서 맞춤형 맛집을 추천해주세요
      {feature}

    """),
  ("user", "#Format: {format_instructions}\n\n#user_input: {user_input}"),
  ("placeholder", "{messages}")
])

# 2) JsonOutputParser
output_parser = JsonOutputParser(pydantic_object=Recommendation)
prompt = prompt_template.partial(
    format_instructions=output_parser.get_format_instructions())

# 3) OpenAI 모델 초기화
# llm = ChatOpenAI(model="gpt-4o-mini")
llm = ChatDeepSeek(
    model="...",
    temperature=0.4,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)

# 4) LLM + Tool 바인딩
llm_with_tools = llm.bind_tools(tools=[search_web])

# 5) 최종 체인
llm_chain = prompt | llm_with_tools


@chain
def web_search_chain(user_input: str, config: RunnableConfig):
  """
  LangChain 체인을 통한 검색 + LLM 호출 함수.
  """
  input_ = {"user_input": user_input}
  ai_msg = llm_chain.invoke(input_, config=config)
  tool_msgs = search_web.batch(ai_msg.tool_calls, config=config)

  return llm_chain.invoke({**input_, "messages": [ai_msg, *tool_msgs]},
                          config=config)


def recommend_restaurant(user_query: str) -> str:
  """
  외부에서 호출되는 추천 로직.
  """
  response = web_search_chain.invoke(user_query)
  json_str = response.content.replace("```json\n", "").replace("\n```", "")
  return json_str
