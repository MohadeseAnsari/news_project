from py.agent import generate_news


abstract = """
A university research team has developed a new artificial intelligence
method that can help researchers analyze large scientific datasets more
efficiently. The researchers said the method may reduce the time required
for data analysis and could be useful in several scientific fields.
"""


try:
    result = generate_news(abstract)

    print("=" * 60)
    print("Generated News")
    print("=" * 60)

    print("\nTitle:")
    print(result.title)

    print("\nLead:")
    print(result.lead)

    print("\nBody:")
    print(result.body)

    print("\nJSON:")
    print(result.model_dump_json(indent=2))

except Exception as error:
    print("=" * 60)
    print("Agent execution failed")
    print("=" * 60)
    print(f"Error type: {type(error).__name__}")
    print(f"Error message: {error}")
