import os
import logging
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, date

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 3000

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def transform_date_or_422(date_: str) -> date:
    """
    '2021-01' -> datetime.date(2021, 01, 01) else raise HTTP_422
    """
    try:
        transformed_date = datetime.strptime(date_, "%Y-%m").date().replace(day=1)
    except ValueError:
        logging.info(f"{date_} has incorrect date format")
        raise HTTPException(
            status_code=422,
            detail=f"{date_} has incorrect date format, but should be YYYY-MM",
        )
    return transformed_date
