"""
Article model
"""
from db.repo.utils import select_articles

# TODO: pydantic class with attached methods?
# TODO: create_or_update_method ?
# TODO: delete method


async def get_one(article_id):
    return await select_articles(article_id=article_id)


async def get_many():
    return await select_articles(offset=0, limit=10)
