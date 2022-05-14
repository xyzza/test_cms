import datetime

from .base import database_meta
from .base import sa


# article table
Article = sa.Table(
    "article",
    database_meta,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("title", sa.String(256), nullable=False),
    sa.Column("body", sa.Text(), nullable=False),
    sa.Column(
        "created_at", sa.DateTime(), nullable=False, default=datetime.datetime.now
    ),
    sa.Column(
        "modified_at", sa.DateTime(), nullable=False, default=datetime.datetime.now
    ),
)
