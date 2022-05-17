from typing import Callable

from fastapi import Depends
from fastapi import FastAPI

from db.repo.crud import ArticleRepo
from db.repo.crud import article_repo

from .api.routers import article_router
from .config import settings
from .dependencies import get_token_header


def init_app(dsn: str, repo: ArticleRepo):
    app = FastAPI(
        # dependencies=[Depends(get_token_header)],
        responses={
            403: {"description": "Operation forbidden"},
        },
    )
    app.add_event_handler("startup", create_start_app_handler(dsn=dsn, repository=repo))
    app.add_event_handler("shutdown", create_stop_app_handler(repository=repo))
    app.include_router(article_router.router)
    return app


def create_start_app_handler(dsn: str, repository: ArticleRepo) -> Callable:
    async def start_app() -> None:
        repository.start(dsn=dsn)

    return start_app


def create_stop_app_handler(repository: ArticleRepo) -> Callable:
    async def stop_app() -> None:
        await repository.stop()

    return stop_app


app = init_app(dsn=settings.db_dsn, repo=article_repo)
