import asyncio
import os

import psycopg2
import pytest
from httpx import AsyncClient
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from yoyo import get_backend
from yoyo import read_migrations

from app.config import settings
from app.server import init_app
from db import migrations
from db.repo.crud import article_repo

_MIGRATIONS_PATH = os.path.dirname(os.path.abspath(migrations.__file__))
_DRIVER_SYNC = "postgresql"
_DRIVER_ASYNC = f"{_DRIVER_SYNC}+asyncpg"
_TEST_DB_NAME = "test_db"

ORIGIN = settings.db_dsn
ORIGIN = ORIGIN.split("/")
ORIGIN[0] = "{driver}:"
ORIGIN[-1] = "{db_name}"
_TEMPLATE_DSN = "/".join(ORIGIN)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture()
def repo(setup_test_db):
    article_repo.start(dsn=setup_test_db)
    return article_repo


@pytest.fixture()
def app(setup_test_db, repo):
    return init_app(dsn=setup_test_db, repo=repo)


@pytest.fixture()
async def authorized_client(app):
    async with AsyncClient(
        app=app, base_url="http://test", headers={"x-auth-token": "some_token"}
    ) as ac:
        yield ac


@pytest.fixture()
async def not_authorized_client(app):
    async with AsyncClient(
        app=app,
        base_url="http://test",
    ) as ac:
        yield ac


@pytest.fixture(scope="session")
def setup_test_db():

    conn = psycopg2.connect(
        _TEMPLATE_DSN.format(driver=_DRIVER_SYNC, db_name="postgres")
    )
    try:
        with conn.cursor() as cursor:
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor.execute(f"DROP DATABASE IF EXISTS {_TEST_DB_NAME}")
            cursor.execute(f"CREATE DATABASE {_TEST_DB_NAME}")
    finally:
        conn.close()

    backend = get_backend(
        _TEMPLATE_DSN.format(driver=_DRIVER_SYNC, db_name=_TEST_DB_NAME)
    )
    migrations = read_migrations(_MIGRATIONS_PATH)
    with backend.lock():
        backend.apply_migrations(backend.to_apply(migrations))

    return _TEMPLATE_DSN.format(driver=_DRIVER_ASYNC, db_name=_TEST_DB_NAME)


@pytest.fixture(autouse=True)
async def truncate():
    yield
    with psycopg2.connect(
        _TEMPLATE_DSN.format(driver=_DRIVER_SYNC, db_name=_TEST_DB_NAME)
    ) as connection:
        with connection.cursor() as cursor:
            for table in [
                "article",
            ]:
                cursor.execute(f"TRUNCATE TABLE {table}")


@pytest.fixture()
async def article(repo):
    article = await repo.insert_article(
        title="Does android dream of electric sheep?", body="They do..."
    )
    return article


@pytest.fixture()
async def articles(repo):
    article1 = await repo.insert_article(
        title="Does android dream of electric sheep?", body="They do..."
    )
    article2 = await repo.insert_article(
        title="Ghost in the Shell", body="...written and illustrated by Masamune Shirow"
    )
    return [article1, article2]
