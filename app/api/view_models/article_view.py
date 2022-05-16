import datetime
from typing import List

from pydantic.main import BaseModel

from .base import AllOptional


class NonExistingArticle(BaseModel):
    title: str
    body: str


class NonExistingArticleOptional(NonExistingArticle, metaclass=AllOptional):
    pass


class ExistingArticle(NonExistingArticle):
    id: int
    created_at: datetime.datetime
    modified_at: datetime.datetime


class PluralArticle(BaseModel):
    items: List[ExistingArticle]
