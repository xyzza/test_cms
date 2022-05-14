import datetime

from .base import _select_with_filters
from .model import Article
from .base import engine
from .base import sa
from .base import text_filter


async def select_articles(
    article_id: int = None,
    title: str = None,
    body: str = None,
    created_at: datetime.datetime = None,
    offset: int = None,
    limit: int = None,
):
    filters = []
    if article_id:
        filters.append(sa.column("id") == article_id)

    if title:
        filters.append(text_filter("title", title))

    if body:
        filters.append(text_filter("body", body))

    if created_at:
        filters.append(sa.column("created_at") >= created_at)

    columns = [
        Article.c.id,
        Article.c.title,
        Article.c.body,
        Article.c.created_at,
    ]

    order_by = Article.c.created_at.desc()
    async with engine.connect() as conn:
        result = await _select_with_filters(
            table=Article,
            connection=conn,
            columns=columns,
            filters=filters,
            offset=offset,
            limit=limit,
            order_by=order_by,
        )
    await engine.dispose()  # TODO: is it needed? try finally?
    return result


async def insert_article():
    pass


async def delete_article():
    pass


async def update_article():
    pass
