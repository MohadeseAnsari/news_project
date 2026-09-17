"""
Agent تولید خبر با PydanticAI و AvalAI.

هر دو پرامپت v1 و v2 از فایل‌های متنی خونده می‌شن.
پیش‌فرض: v2 (پرامپت بهبودیافته).

Usage:
    from py.agent import generate_news, generate_news_v1

    result = generate_news(abstract)        # با v2
    result = generate_news_v1(abstract)     # با v1
"""

import os
from pathlib import Path
from functools import lru_cache

from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

from py.models import GeneratedNews

# ---------------- Environment ----------------
load_dotenv()

API_KEY = os.getenv("AVALAI_API_KEY")
if not API_KEY:
    raise RuntimeError("AVALAI_API_KEY is not configured.")

# ---------------- مسیرها ----------------
BASE_DIR = Path(__file__).parent.parent
PROMPTS_DIR = BASE_DIR / "docs"

PROMPT_FILES = {
    "v1": PROMPTS_DIR / "prompt_v1.txt",
    "v2": PROMPTS_DIR / "prompt_v2.txt",
}

DEFAULT_PROMPT_VERSION = "v2"


# ---------------- Model + Provider ----------------
provider = OpenAIProvider(
    base_url="https://api.avalai.ir/v1",
    api_key=API_KEY,
)

model = OpenAIChatModel(
    "gpt-5.6-luna",
    provider=provider,
)


# ---------------- Prompt loader ----------------
@lru_cache(maxsize=None)
def load_prompt(version: str) -> str:
    """
    متن پرامپت رو از فایل می‌خونه.
    نتیجه cache می‌شه تا هر بار فایل خونده نشه.

    Args:
        version: "v1" یا "v2"

    Returns:
        متن پرامپت
    """
    if version not in PROMPT_FILES:
        raise ValueError(
            f"نسخه پرامپت نامعتبر: {version}. "
            f"مقادیر مجاز: {list(PROMPT_FILES.keys())}"
        )

    path = PROMPT_FILES[version]
    if not path.exists():
        raise FileNotFoundError(f"فایل پرامپت پیدا نشد: {path}")

    return path.read_text(encoding="utf-8").strip()


# ---------------- Agent factory ----------------
def build_agent(version: str = DEFAULT_PROMPT_VERSION) -> Agent:
    """
    یه Agent با پرامپت مشخص می‌سازه.
    هر بار صدا زده بشه، یه Agent جدید با پرامپت اون نسخه می‌ده.
    """
    system_prompt = load_prompt(version)
    return Agent(
        model,
        output_type=GeneratedNews,
        system_prompt=system_prompt,
    )


# ---------------- Public API ----------------
def generate_news(
    abstract: str,
    version: str = DEFAULT_PROMPT_VERSION,
) -> GeneratedNews:
    """
    تولید خبر از چکیده با نسخه پرامپت مشخص.

    Args:
        abstract: چکیده پایان‌نامه
        version:  "v1" یا "v2" (پیش‌فرض: v2)

    Returns:
        GeneratedNews
    """
    agent = build_agent(version)
    result = agent.run_sync(abstract)
    return result.output


def generate_news_v1(abstract: str) -> GeneratedNews:
    """تولید خبر با پرامپت v1 (برای مقایسه)."""
    return generate_news(abstract, version="v1")


def generate_news_v2(abstract: str) -> GeneratedNews:
    """تولید خبر با پرامپت v2 (نسخه پیش‌فرض)."""
    return generate_news(abstract, version="v2")


"""
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
    system_prompt=
You are a professional news editor.

Your task is to transform the user's abstract into a professional
news article.

The output must contain:
- title: a clear and professional news headline
- lead: a concise summary of the most important information
- body: a well-structured news article

Do not invent facts that are not supported by the input abstract.
Write in a professional journalistic style.
,
)


def generate_news(abstract: str) -> GeneratedNews:
    result = news_agent.run_sync(abstract)
    return result.output
"""
