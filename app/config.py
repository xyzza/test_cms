from pydantic import BaseSettings


class Settings(BaseSettings):
    db_dsn: str


settings = Settings()
