"""
اجرای agent روی یه فایل JSON.

Usage:
    python run_agent.py data/sample_input_1.json           # پیش‌فرض: v2
    python run_agent.py data/sample_input_1.json --v1      # با v1
"""

import json
import sys
from pathlib import Path

from py.agent import generate_news
from py.models import NewsInput


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python run_agent.py <input_json> [--v1|--v2]")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    version = "v1" if "--v1" in sys.argv else "v2"

    if not input_path.exists():
        print(f" فایل پیدا نشد: {input_path}")
        sys.exit(1)

    try:
        with input_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        news_input = NewsInput.model_validate(data)

        print(f" ورودی: {input_path.name}")
        print(f" نسخه پرامپت: {version}")
        print(f" عنوان: {news_input.title}")
        print()

        generated = generate_news(news_input.abstract, version=version)

        print("=" * 60)
        print(f"خروجی ({version})")
        print("=" * 60)
        print(f"\n Title:\n{generated.title}")
        print(f"\n Lead:\n{generated.lead}")
        print(f"\n Body:\n{generated.body}")

        # ذخیره خروجی با اسم نسخه
        output_path = input_path.with_name(
            f"{input_path.stem}_output_{version}.json"
        )
        with output_path.open("w", encoding="utf-8") as f:
            json.dump(
                generated.model_dump(),
                f,
                ensure_ascii=False,
                indent=2,
            )
        print(f"\n ذخیره شد: {output_path}")

    except Exception as error:
        print("=" * 60)
        print(" خطا در اجرا")
        print("=" * 60)
        print(f"نوع خطا: {type(error).__name__}")
        print(f"پیام: {error}")
        raise


if __name__ == "__main__":
    main()


"""
import json
import sys
from pathlib import Path

from py.agent import generate_news
from py.models import NewsInput


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python run_agent.py <input_json>")
        sys.exit(1)

    input_path = Path(sys.argv[1])

    if not input_path.exists():
        print(f"Input file not found: {input_path}")
        sys.exit(1)

    try:
        with input_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        news_input = NewsInput.model_validate(data)

        print("Input validation: OK")
        print(f"Title: {news_input.title}")
        print()

        generated_news = generate_news(news_input.abstract)

        print("=" * 60)
        print("Generated News")
        print("=" * 60)

        print("\nTitle:")
        print(generated_news.title)

        print("\nLead:")
        print(generated_news.lead)

        print("\nBody:")
        print(generated_news.body)

        output_path = input_path.with_name(
            f"{input_path.stem}_output.json"
        )

        with output_path.open("w", encoding="utf-8") as file:
            json.dump(
                generated_news.model_dump(),
                file,
                ensure_ascii=False,
                indent=2,
            )

        print()
        print(f"Output saved to: {output_path}")

    except Exception as error:
        print("=" * 60)
        print("Pipeline execution failed")
        print("=" * 60)
        print(f"Error type: {type(error).__name__}")
        print(f"Error message: {error}")

        raise


if __name__ == "__main__":
    main()
"""
