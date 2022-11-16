from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import extract
from sqlalchemy import and_
from pydantic.schema import datetime

from models.user import User
from models.item import Item
from schemas.statistics import Statistics


def get_user_statistics(db: Session, user_id: int, year_month: datetime = None):
    user = db.query(User).filter_by(id=user_id).one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if year_month is not None:
        items = (
            db.query(Item)
            .filter(
                and_(
                    Item.user_id == user_id,
                    extract("year", Item.time) == year_month.year,
                    extract("month", Item.time) == year_month.month,
                )
            )
            .all()
        )
    else:
        items = (
            db.query(Item)
            .filter(
                Item.user_id == user_id,
            )
            .all()
        )
    list_categories = []
    for category in user.categories:
        list_categories.append(category.title)
    details_dict = {category: 0 for category in list_categories}
    number_purchases_category = {category: 0 for category in list_categories}
    all_costs = 0
    number_purchases = 0
    for item in items:
        details_dict[item.category.title] += item.price
        all_costs += item.price
        number_purchases_category[item.category.title] += 1
        number_purchases += 1
    user_stats = Statistics
    user_stats.email = user.email
    user_stats.costs = all_costs
    user_stats.number_purchases = number_purchases
    user_stats.details = details_dict
    user_stats.number_purchases_category = number_purchases_category
    return user_stats
