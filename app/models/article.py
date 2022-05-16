import datetime
from typing import Optional

from db.repo.utils import article_repo

# default pagination is turned off
DEFAULT_PAGINATION = 0


async def create_one(title: str, body: str):
    return await article_repo.insert_article(title=title, body=body)


async def get_one(article_id: int):
    return await article_repo.select_articles(article_id=article_id)


async def get_many(
    offset: Optional[int] = 0,
    limit: Optional[int] = DEFAULT_PAGINATION,
    title: Optional[str] = None,
    body: Optional[str] = None,
    created_at: Optional[datetime.datetime] = None,
    sort_asc: bool = False,
):
    return await article_repo.select_articles(
        title=title,
        body=body,
        created_at=created_at,
        offset=offset,
        limit=limit,
        sort_asc=sort_asc,
    )


async def update_one(article_id: int, title: str = None, body: str = None):
    return await article_repo.update_article(
        article_id=article_id, title=title, body=body
    )


async def delete_one(article_id: int):
    return await article_repo.delete_article(article_id=article_id)
