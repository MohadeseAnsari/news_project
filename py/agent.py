import os

from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

from py.models import GeneratedNews


load_dotenv()


API_KEY = os.getenv("AVALAI_API_KEY")

if not API_KEY:
    raise RuntimeError("AVALAI_API_KEY is not configured.")


provider = OpenAIProvider(
    base_url="https://api.avalai.ir/v1",
    api_key=API_KEY,
)


model = OpenAIChatModel(
    "gpt-5.6-luna",
    provider=provider,
)


news_agent = Agent(
    model,
    output_type=GeneratedNews,
    system_prompt="""
You are a professional news editor.

Your task is to transform the user's abstract into a professional
news article.

The output must contain:
- title: a clear and professional news headline
- lead: a concise summary of the most important information
- body: a well-structured news article

Do not invent facts that are not supported by the input abstract.
Write in a professional journalistic style.
""",
)


def generate_news(abstract: str) -> GeneratedNews:
    result = news_agent.run_sync(abstract)
    return result.output
