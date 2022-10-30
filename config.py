from pydantic import BaseSettings


class Settings(BaseSettings):
    SQL: str

settings = Settings()
