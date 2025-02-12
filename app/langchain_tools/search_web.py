# app/langchain_tools/search_web.py
import os
from langchain_community.tools import TavilySearchResults
from langchain_core.tools import tool

from dotenv import load_dotenv

load_dotenv()


@tool
def search_web(query: str) -> str:
    """
    Searches the internet for information that does not exist
    in the database or for the latest information.
    """
    os.environ[
        "TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")

    tavily_search = TavilySearchResults(max_results=5,
                                        include_domains=[
                                            "https://www.tistory.com/",
                                            "https://blog.naver.com/",
                                            "https://www.daum.net/",
                                            "https://brunch.co.kr/"])
    docs = tavily_search.invoke(query)

    if not docs:
        return "관련 정보를 찾을 수 없습니다."

    formatted_docs = "\n---\n".join(
        [
            f'<Document href="{doc["url"]}"/>\n{doc["content"]}\n</Document>'
            for doc in docs
        ]
    )

    return formatted_docs
