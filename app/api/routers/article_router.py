from typing import Union

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from app.api.view_models.article_view import ExistingArticle
from app.api.view_models.article_view import NonExistingArticle
from app.api.view_models.article_view import NonExistingArticleOptional
from app.api.view_models.article_view import PluralArticle
from app.dependencies import get_token_header
from app.models import article as article_model

router = APIRouter(
    prefix="/v1/articles",
    tags=["Articles V1"],
)

# 404 case warning message
NOT_FOUND = "Article not found"


@router.post(
    "/",
    response_model=ExistingArticle,
    status_code=201,
    dependencies=[Depends(get_token_header)],
)
async def create_article(article: NonExistingArticle):
    return await article_model.create_one(**article.dict())


@router.get("/", response_model=PluralArticle)
async def read_articles(
    offset: Union[int, None] = None,
    limit: Union[int, None] = None,
    title: Union[str, None] = None,
    body: Union[str, None] = None,
    sort_asc: bool = False,
):
    return {
        "items": await article_model.get_many(
            offset=offset, limit=limit, title=title, body=body, sort_asc=sort_asc
        )
    }


@router.get(
    "/{article_id}",
    responses={
        404: {"description": NOT_FOUND},
    },
    response_model=ExistingArticle,
)
async def read_article(article_id: int):
    try:
        row = await article_model.get_one(article_id=article_id)
    except article_model.DoesNotExists:
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    return row


@router.patch(
    "/{article_id}",
    responses={
        404: {"description": NOT_FOUND},
    },
    response_model=ExistingArticle,
    dependencies=[Depends(get_token_header)],
)
async def update_article(article_id: int, article: NonExistingArticleOptional):
    try:
        row = await article_model.update_one(article_id=article_id, **article.dict())
    except article_model.DoesNotExists:
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    return row


@router.delete(
    "/{article_id}",
    responses={
        404: {"description": NOT_FOUND},
    },
    status_code=204,
    dependencies=[Depends(get_token_header)],
)
async def delete_article(article_id: int):
    try:
        await article_model.delete_one(article_id=article_id)
    except article_model.DoesNotExists:
        raise HTTPException(status_code=404, detail=NOT_FOUND)
