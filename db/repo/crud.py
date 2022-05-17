import datetime
from typing import Any
from typing import Dict
from typing import List

from .base import Repo
from .base import sa
from .tables import Article


class ArticleRepo(Repo):

    columns = [
        Article.c.id,
        Article.c.title,
        Article.c.body,
        Article.c.created_at,
        Article.c.modified_at,
    ]

    async def insert_article(self, title: str, body: str) -> Dict[str, Any]:
        async with self.engine.connect() as conn:
            result = await self.insert_row(
                table=Article,
                connection=conn,
                values={"title": title, "body": body},
                returning=self.columns,
            )
        return result

    async def update_article(
        self, article_id: int, title: str = None, body: str = None
    ) -> sa.engine.Row:
        values = {}
        # TODO: DTO might be a better idea
        if title:
            values["title"] = title
        if body:
            values["body"] = body
        async with self.engine.connect() as conn:
            result = await self.update_rows(
                table=Article,
                connection=conn,
                values=values,
                where=(Article.c.id == article_id),
                returning=self.columns,
            )
        result = [x for x in result]
        if result:
            return result[0]

    async def select_articles(
        self,
        article_id: int = None,
        title: str = None,
        body: str = None,
        created_at: datetime.datetime = None,
        offset: int = None,
        limit: int = None,
        sort_asc: bool = False,
    ) -> List[sa.engine.Row]:
        filters = []
        if article_id:
            filters.append(sa.column("id") == article_id)

        if title:
            filters.append(self.text_filter("title", title))

        if body:
            filters.append(self.text_filter("body", body))

        if created_at:
            filters.append(sa.column("created_at") >= created_at)

        order_by = Article.c.created_at.desc()
        if sort_asc:
            order_by = Article.c.created_at.asc()

        async with self.engine.connect() as conn:
            result = await self.select_with_filters(
                table=Article,
                connection=conn,
                columns=self.columns,
                filters=filters,
                offset=offset,
                limit=limit,
                order_by=order_by,
            )
        return result

    async def delete_article(self, article_id: int) -> List[sa.engine.Row]:
        async with self.engine.connect() as conn:
            result = await self.delete_rows(
                table=Article,
                connection=conn,
                where=(Article.c.id == article_id),
                returning=[Article.c.id],
            )
        return result


# repository instance
article_repo = ArticleRepo()
