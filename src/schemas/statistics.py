from pydantic import BaseModel


class Statistics(BaseModel):
    email: str
    costs: float
    number_purchases: int
    details: dict
    number_purchases_category: dict

    class Config:
        orm_mode = True
