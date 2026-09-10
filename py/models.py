from enum import Enum

from pydantic import BaseModel, Field


class NewsField(str, Enum):
    SCIENCE = "science"
    TECHNOLOGY = "technology"
    MEDICAL = "medical"
    OTHER = "other"


class NewsInput(BaseModel):
    shared_Secret: str = Field(min_length=1)
    username: str = Field(min_length=1, max_length=100)
    title: str = Field(min_length=5, max_length=200)
    abstract: str = Field(min_length=1, max_length=5000)
    field: NewsField
    university: str = Field(min_length=1, max_length=200)
    table_of_contents: str = Field(min_length=1, max_length=5000)
    author: str = Field(min_length=1, max_length=200)
    supervisor: str = Field(min_length=1, max_length=200)


class GeneratedNews(BaseModel):
    title: str = Field(min_length=5, max_length=200)
    lead: str = Field(min_length=1, max_length=1000)
    body: str = Field(min_length=1, max_length=10000)
