from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from app import schemas
from app.crud import crud_statistics
from app.crud.crud_user import get_current_active_user
from app.db import get_db
from app.utils import transform_date_or_422

router = APIRouter(
    prefix="/users",
    tags=["statistics"],
)


@router.get("/statistics/", response_model=schemas.Statistics)
def read_stats(
    current_user: schemas.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    statistics = crud_statistics.get_user_statistics(db, current_user.id)
    return statistics


@router.get(
    "/statistics/{filter_date}/",
    response_model=schemas.Statistics,
)
def read_stats_month(
    filter_date: str,
    current_user: schemas.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    date_ = transform_date_or_422(filter_date)
    statistics_month = crud_statistics.get_user_statistics(db, current_user.id, date_)
    return statistics_month
