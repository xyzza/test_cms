"""
Initial migration
"""

from yoyo import step

__depends__ = {"__init__"}

steps = [
    step(
        apply="""
        CREATE TABLE article (
            id serial primary key,
            title varchar(256) not null,
            body text not null,
            created_at timestamp default now() not null,
            modified_at timestamp default now() not null,
        );
        """,
        rollback="""
        DROP TABLE article;
        """,
    )
]
