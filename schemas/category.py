from pydantic import BaseModel


class CategoryBase(BaseModel):
    title: str


class CategoryCreate(CategoryBase):
    user_id: int


class Category(CategoryBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
