import datetime
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from db.repo.crud import article_repo

# default pagination is turned off
DEFAULT_PAGINATION = 0


class DoesNotExists(Exception):
    """Article doesn't exists"""


async def create_one(title: str, body: str) -> Dict[str, Any]:
    result = await article_repo.insert_article(title=title, body=body)
    # TODO: DTO
    return dict(result)


async def get_one(article_id: int) -> Dict[str, Any]:
    try:
        row, *_ = await article_repo.select_articles(article_id=article_id)
    except (IndexError, ValueError):
        raise DoesNotExists
    # TODO: DTO
    return dict(row)


async def get_many(
    offset: Optional[int] = 0,
    limit: Optional[int] = DEFAULT_PAGINATION,
    title: Optional[str] = None,
    body: Optional[str] = None,
    created_at: Optional[datetime.datetime] = None,
    sort_asc: bool = False,
) -> List[Dict[str, Any]]:
    result = await article_repo.select_articles(
        title=title,
        body=body,
        created_at=created_at,
        offset=offset,
        limit=limit,
        sort_asc=sort_asc,
    )
    # TODO: DTO
    return [dict(x) for x in result]


async def update_one(
    article_id: int, title: str = None, body: str = None
) -> Dict[str, Any]:
    result = await article_repo.update_article(
        article_id=article_id, title=title, body=body
    )
    # TODO: DTO
    if not result:
        raise DoesNotExists
    return dict(**result)


async def delete_one(article_id: int):
    result = await article_repo.delete_article(article_id=article_id)
    if not result:
        raise DoesNotExists
