from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.user import User
from schemas.statistics import Statistics


def get_user_statistics(db: Session, user_id: int, year_month: str = None):
    user = db.query(User).filter_by(id=user_id).one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    number_purchases = len(user.items)
    list_categories = []
    for category in user.categories:
        list_categories.append(category.title)
    details_dict = {category: 0 for category in list_categories}
    number_purchases_category = {category: 0 for category in list_categories}
    all_costs = 0
    if year_month is not None:
        count_items_month = 0
    for item in user.items:
        if year_month is not None:
            if (
                    item.time.strftime("%Y-%m") == year_month
            ):
                details_dict[item.category.title] += item.price
                all_costs += item.price
                number_purchases_category[item.category.title] += 1
                count_items_month += 1
        else:
            details_dict[item.category.title] += item.price
            all_costs += item.price
            number_purchases_category[item.category.title] += 1
    user_stats = Statistics
    user_stats.email = user.email
    user_stats.costs = all_costs
    if year_month is not None:
        user_stats.number_purchases = count_items_month
    else:
        user_stats.number_purchases = number_purchases
    user_stats.details = details_dict
    user_stats.number_purchases_category = number_purchases_category
    return user_stats
