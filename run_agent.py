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
