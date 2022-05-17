from typing import Any
from typing import Dict
from typing import List
from typing import Optional

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import create_async_engine

database_meta = sa.MetaData()


class Repo:
    def __init__(self):
        self._engine = None

    def start(self, dsn):
        if self._engine is None:
            self._engine = create_async_engine(dsn)

    @property
    def engine(self):
        return self._engine

    async def stop(self):
        if self._engine is not None:
            await self._engine.dispose()

    async def select_with_filters(
        self,
        table: str,
        connection: sa.engine.Connection,
        columns: Optional[List[str]] = None,
        filters: Optional[List[Any]] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        order_by: Optional[Any] = None,
    ) -> List[sa.engine.Row]:
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

    async def insert_row(
        self, table: str, connection, values: Dict[str, Any], returning: List[sa.column]
    ) -> Optional[sa.engine.Row]:
        expression = sa.insert(table).values(**values)
        if returning:
            expression = expression.returning(*returning)
        result = await connection.execute(expression)
        await connection.commit()
        if result:
            return [x for x in result][0]

    async def update_rows(
        self,
        table: str,
        connection: sa.engine.Connection,
        values: Dict[str, Any],
        where: sa.sql.expression,
        returning: List[sa.column],
    ) -> List[sa.engine.Row]:
        expression = sa.update(table).values(**values)
        if where:
            expression = expression.where(where)
        if returning:
            expression = expression.returning(*returning)
        result = await connection.execute(expression)
        await connection.commit()
        return [x for x in result]

    async def delete_rows(
        self,
        table: str,
        connection: sa.engine.Connection,
        where: sa.sql.expression,
        returning: List[sa.column],
    ) -> List[sa.engine.Row]:
        expression = sa.delete(table).where(where)
        if returning:
            expression = expression.returning(*returning)
        result = await connection.execute(expression)
        await connection.commit()
        return result.fetchall()

    def text_filter(self, column_name: str, column_value: str) -> sa.sql.expression:
        return sa.column(column_name).ilike(f"%{column_value}%")


repo = Repo()
