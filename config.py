from pydantic import BaseSettings


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URI: str
    TEST_SQLALCHEMY_DATABASE_URI: str

settings = Settings()
