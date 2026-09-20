"""
مقایسه پرامپت v1 و v2 روی سه ورودی ثابت.
اجرا: python -m scripts.compare_prompts
"""

import json
from pathlib import Path

from py.agent import generate_news

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "docs" / "comparison_outputs"
OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

INPUT_FILES = [
    DATA_DIR / "sample_input_1.json",
    DATA_DIR / "sample_input_2.json",
    DATA_DIR / "sample_input_3.json",
]


def main():
    all_results = []

    for input_file in INPUT_FILES:
        if not input_file.exists():
            print(f" پیدا نشد: {input_file}")
            continue

        data = json.loads(input_file.read_text(encoding="utf-8"))
        abstract = data["abstract"]
        name = input_file.stem

        print(f"\n{'=' * 60}")
        print(f" {name}")
        print("=" * 60)

        print(" اجرای v1...")
        v1 = generate_news(abstract, version="v1").model_dump()

        print("  اجرای v2...")
        v2 = generate_news(abstract, version="v2").model_dump()

        result = {
            "input_file": name,
            "input_abstract": abstract,
            "v1": v1,
            "v2": v2,
        }
        all_results.append(result)

        out = OUTPUT_DIR / f"{name}_comparison.json"
        out.write_text(
            json.dumps(result, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f" ذخیره شد: {out}")

    all_out = OUTPUT_DIR / "all_comparisons.json"
    all_out.write_text(
        json.dumps(all_results, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"\n همه نتایج: {all_out}")


if __name__ == "__main__":
    main()
