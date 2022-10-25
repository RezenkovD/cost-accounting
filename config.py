from pydantic import BaseSettings


class Settings(BaseSettings):
    PASSWORD_DB: str
    HOST: str
    DB_NAME: str

settings = Settings()