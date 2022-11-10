from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import schemas.item
import crud.crud_item
import schemas.user
import crud.crud_user
import schemas.category
import crud.crud_category
import schemas.statistics
import crud.crud_statistics
import crud.crud_months_statistics
from db.database import SessionLocal


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.user.User)
def create_user(user: schemas.user.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.crud_user.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.user.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.crud_user.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.user.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.crud_user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/item/", response_model=schemas.item.Item)
def create_item_for_user(
    user_id: int, item: schemas.item.ItemCreate, db: Session = Depends(get_db)
):
    return crud.crud_item.create_user_item(db=db, item=item, user_id=user_id)


@app.post("/users/category/", response_model=schemas.category.Category)
def create_category_for_user(
    category: schemas.category.CategoryCreate,
    db: Session = Depends(get_db),
):
    return crud.crud_category.create_user_category(db=db, category=category)


@app.get(
    "/users/{user_id}/statistics", response_model=schemas.statistics.Statistics
)
def get_stats(user_id: int, db: Session = Depends(get_db)):
    statistics = crud.crud_statistics.get_user_statistics(db, user_id=user_id)
    if statistics is None:
        raise HTTPException(status_code=404, detail="User not found")
    return statistics


@app.get(
    "/users/{user_id}/statistics/{month}",
    response_model=schemas.statistics.Statistics,
)
def get_stats_month(user_id: int, month: int, db: Session = Depends(get_db)):
    statistics_month = crud.crud_months_statistics.get_user_statistics(
        db, user_id=user_id, month=month
    )
    if statistics_month is None:
        raise HTTPException(status_code=404, detail="User not found")
    return statistics_month
