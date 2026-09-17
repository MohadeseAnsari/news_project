"""
مدل‌های Pydantic برای API.
این‌ها ورودی/خروجی HTTP هستن.
"""

from pydantic import BaseModel, Field, field_validator


class NewsRequest(BaseModel):
    """بدنه ورودی JSON — مطابق json_input.md."""

    shared_Secret: str = Field(min_length=1)

    username:          str = Field(min_length=1, max_length=100)
    title:             str = Field(min_length=5, max_length=200)
    abstract:          str = Field(min_length=1, max_length=5000)
    field:             str = Field(min_length=1, max_length=200)
    university:        str = Field(min_length=1, max_length=200)
    table_of_contents: str = Field(min_length=1, max_length=5000)
    author:            str = Field(min_length=1, max_length=200)
    supervisor:        str = Field(min_length=1, max_length=200)

    @field_validator(
        "username", "title", "abstract", "field",
        "university", "table_of_contents", "author", "supervisor",
    )
    @classmethod
    def not_blank(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("field cannot be empty or whitespace")
        return v.strip()


class NewsResponse(BaseModel):
    id:      int
    status:  str
    message: str


class HealthResponse(BaseModel):
    status: str
    db:     str
