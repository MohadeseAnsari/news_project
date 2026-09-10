from pydantic import ValidationError

from py.models import GeneratedNews, NewsField, NewsInput


def valid_news_input() -> dict:
    return {
        "shared_Secret": "demo-secret",
        "username": "intern",
        "title": "AI Research Project",
        "abstract": (
            "A university research team has developed a new "
            "artificial intelligence method for scientific data analysis."
        ),
        "field": "technology",
        "university": "Example University",
        "table_of_contents": "Introduction, Method, Results",
        "author": "Research Team",
        "supervisor": "Internship Supervisor",
    }


def test_valid_news_input() -> None:
    news = NewsInput.model_validate(valid_news_input())

    assert news.username == "intern"
    assert news.field == NewsField.TECHNOLOGY

    print("PASS: valid NewsInput")


def test_missing_required_field() -> None:
    data = valid_news_input()
    data.pop("abstract")

    try:
        NewsInput.model_validate(data)
    except ValidationError:
        print("PASS: missing required field rejected")
    else:
        raise AssertionError("Missing abstract was accepted")


def test_invalid_field() -> None:
    data = valid_news_input()
    data["field"] = "Artificial Intelligence"

    try:
        NewsInput.model_validate(data)
    except ValidationError:
        print("PASS: invalid field rejected")
    else:
        raise AssertionError("Invalid field was accepted")


def test_title_too_long() -> None:
    data = valid_news_input()
    data["title"] = "A" * 201

    try:
        NewsInput.model_validate(data)
    except ValidationError:
        print("PASS: title longer than 200 characters rejected")
    else:
        raise AssertionError("Overly long title was accepted")


def test_generated_news() -> None:
    news = GeneratedNews(
        title="AI Research Project",
        lead="A research team has developed a new AI method.",
        body="The method could improve scientific data analysis.",
    )

    result = news.model_dump()

    assert result["title"] == "AI Research Project"
    assert "lead" in result
    assert "body" in result

    print("PASS: GeneratedNews and model_dump")


if __name__ == "__main__":
    test_valid_news_input()
    test_missing_required_field()
    test_invalid_field()
    test_title_too_long()
    test_generated_news()

    print()
    print("All model tests passed.")


""""
from py.models import NewsInput, GeneratedNews


news = NewsInput(
    shared_Secret="test-secret",
    username="mohadese",
    title="Artificial Intelligence Research",
    abstract="This is a test abstract about artificial intelligence.",
    field="technology",
    university="Example University",
    table_of_contents="Introduction, Method, Results",
    author="Test Author",
    supervisor="Test Supervisor",
)

print("NewsInput:")
print(news)

print("\nAs dictionary:")
print(news.model_dump())

print("\nAs JSON:")
print(news.model_dump_json())


generated = GeneratedNews(
    title="Artificial Intelligence in Modern Research",
    lead="Artificial intelligence is changing the way research is conducted.",
    body="This is the generated news body for testing the Pydantic model.",
)

print("\nGeneratedNews:")
print(generated)

print("\nGeneratedNews JSON:")
print(generated.model_dump_json())

"""


"""
from pydantic import ValidationError

from py.models import NewsInput, GeneratedNews


def create_valid_news():
    return NewsInput(
        shared_Secret="test-secret",
        username="mohadese",
        title="Artificial Intelligence Research",
        abstract="This is a test abstract about artificial intelligence.",
        field="technology",
        university="Example University",
        table_of_contents="Introduction, Method, Results",
        author="Test Author",
        supervisor="Test Supervisor",
    )


print("=" * 60)
print("TEST 1: Valid NewsInput")
print("=" * 60)

news = create_valid_news()

print("Validation successful!")
print(news)


print("\n" + "=" * 60)
print("TEST 2: Model -> Dictionary")
print("=" * 60)

news_dict = news.model_dump()

print(news_dict)


print("\n" + "=" * 60)
print("TEST 3: Model -> JSON")
print("=" * 60)

news_json = news.model_dump_json()

print(news_json)


print("\n" + "=" * 60)
print("TEST 4: Missing Required Field")
print("=" * 60)

try:
    NewsInput(
        shared_Secret="test-secret",
        username="mohadese",
        # title intentionally missing
        abstract="Test abstract",
        field="technology",
        university="Example University",
        table_of_contents="Introduction",
        author="Test Author",
        supervisor="Test Supervisor",
    )
except ValidationError as error:
    print("ValidationError caught successfully:")
    print(error)


print("\n" + "=" * 60)
print("TEST 5: Title Too Short")
print("=" * 60)

try:
    NewsInput(
        shared_Secret="test-secret",
        username="mohadese",
        title="AI",
        abstract="Test abstract",
        field="technology",
        university="Example University",
        table_of_contents="Introduction",
        author="Test Author",
        supervisor="Test Supervisor",
    )
except ValidationError as error:
    print("ValidationError caught successfully:")
    print(error)


print("\n" + "=" * 60)
print("TEST 6: Invalid Field")
print("=" * 60)

try:
    NewsInput(
        shared_Secret="test-secret",
        username="mohadese",
        title="Artificial Intelligence Research",
        abstract="Test abstract",
        field="invalid-field",
        university="Example University",
        table_of_contents="Introduction",
        author="Test Author",
        supervisor="Test Supervisor",
    )
except ValidationError as error:
    print("ValidationError caught successfully:")
    print(error)


print("\n" + "=" * 60)
print("TEST 7: GeneratedNews")
print("=" * 60)

generated_news = GeneratedNews(
    title="Artificial Intelligence in Modern Research",
    lead="Artificial intelligence is changing modern research.",
    body="This is the generated news body for testing.",
)

print("GeneratedNews validation successful!")
print(generated_news)
print(generated_news.model_dump_json())


print("\n" + "=" * 60)
print("ALL TESTS FINISHED")
print("=" * 60)

"""
