import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

PASSWORD_DB = os.getenv("PASSWORD_DB")
HOST = os.getenv("HOST")
DB_NAME = os.getenv("DB_NAME")
SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:{PASSWORD_DB}@{HOST}/{DB_NAME}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()