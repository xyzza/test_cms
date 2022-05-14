from fastapi import APIRouter, HTTPException
from app.models import article

router = APIRouter(
    prefix="/v1/articles",
    tags=["Articles V1"],
)


# TODO: implement OUTPUT model, connect it to swagger
# TODO: implement other than REST view


@router.get("/")
async def read_articles():
    return await article.get_many()


@router.get(
    "/{article_id}",
    responses={
        404: {"description": "Not found"},
    },
)
async def read_article(article_id: int):
    try:
        row, _ = await article.get_one(article_id=article_id)
    except (IndexError, ValueError):
        raise HTTPException(status_code=404, detail="Article not found")
    return row


@router.patch(
    "/{article_id}",
    responses={
        404: {"description": "Not found"},
    },
)
async def update_article(article_id: int, title: str, body: str):
    # TODO: implement patch
    return article_id


@router.delete(
    "/{article_id}",
    responses={
        404: {"description": "Not found"},
    },
)
async def delete_article(article_id: int):
    # TODO: implement delete
    return article_id
