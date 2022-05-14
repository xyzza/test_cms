import os
from typing import Optional, List, Any, Tuple
from sqlalchemy.ext.asyncio import create_async_engine
import sqlalchemy as sa

database_meta = sa.MetaData()
engine = create_async_engine(os.getenv("DB_DSN"))


async def tear_down_engine():
    # FIXME:
    return await engine.dispose()


def text_filter(column_name, column_value):
    return sa.column(column_name).ilike(f"%{column_value}%")


async def _select_with_filters(
    table: str,
    connection,  # TODO: typing
    columns: Optional[List[str]] = None,
    filters: Optional[List[Any]] = None,
    offset: Optional[int] = None,
    limit: Optional[int] = None,
    order_by: Optional[Any] = None,
) -> Tuple[List[sa.engine.Row], Optional[int]]:
    if columns is None:
        columns = []

    expression = sa.select(columns).select_from(table)

    if filters:
        expression = expression.where(*filters)

    if order_by is not None:
        expression = expression.order_by(order_by)

    if limit:
        expression = expression.limit(limit)

    if offset:
        expression = expression.offset(offset)

    result = await connection.execute(expression)
    return result.fetchall()
