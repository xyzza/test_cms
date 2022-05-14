from fastapi import Depends, FastAPI

from .dependencies import get_token_header
from .routers import article

app = FastAPI(
    dependencies=[Depends(get_token_header)],
    responses={
        403: {"description": "Operation forbidden"},
    },
)


app.include_router(article.router)
