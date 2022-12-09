from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from datetime import datetime, date
import logging

from app import schemas
from app.crud import crud_statistics
from app.crud.crud_user import get_current_active_user
from app.db import get_db


router = APIRouter(
    prefix="/users",
    tags=["statistics"],
)


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


@router.get("/read-statistics/", response_model=schemas.Statistics)
def read_stats(
    current_user: schemas.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    statistics = crud_statistics.get_user_statistics(db, current_user.id)
    return statistics


@router.get(
    "/read-statistics/{filter_date}/",
    response_model=schemas.Statistics,
)
def read_stats_month(
    filter_date: str,
    current_user: schemas.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    date_ = transform_date_or_422(filter_date)
    statistics_month = crud_statistics.get_user_statistics(
        db, user_id=current_user.id, filter_date=date_
    )
    return statistics_month
