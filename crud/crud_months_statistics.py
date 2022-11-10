from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.user import User
from schemas.statistics import Statistics


def get_user_statistics(db: Session, user_id: int, month: int):
    if month <= 0:
        raise HTTPException(status_code=404, detail="Enter a positive number")
    if month > 12:
        raise HTTPException(status_code=404, detail="There is no such month number")
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    number_purchases = len(user.items)
    count_items_month = 0
    number_categories = len(user.categories)
    list_categories = []
    for x in range(number_categories):
        list_categories.append(user.categories[x].title)
    details_dict = {category: 0 for category in list_categories}
    number_purchases_category = {category: 0 for category in list_categories}
    all_costs = 0
    for x in range(number_purchases):
        if int(user.items[x].time.strftime("%m")) == month:
            details_dict[user.items[x].category.title] += user.items[x].price
            all_costs += user.items[x].price
            number_purchases_category[user.items[x].category.title] += 1
            count_items_month += 1
    user_stats = Statistics
    user_stats.email = user.email
    user_stats.costs = all_costs
    user_stats.number_purchases = count_items_month
    user_stats.details = details_dict
    user_stats.number_purchases_category = number_purchases_category
    return user_stats
