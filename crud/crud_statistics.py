from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.user import User
from schemas.statistics import Statistics


def get_user_statistics(db: Session, user_id: int):
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
    for x in range(number_purchases):
        details_dict[user.items[x].category.title] += user.items[x].price
        all_costs += user.items[x].price
        number_purchases_category[user.items[x].category.title] += 1
    user_stats = Statistics
    user_stats.email = user.email
    user_stats.costs = all_costs
    user_stats.number_purchases = number_purchases
    user_stats.details = details_dict
    user_stats.number_purchases_category = number_purchases_category
    return user_stats
