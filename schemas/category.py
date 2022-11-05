from pydantic import BaseModel


class CategoryBase(BaseModel):
    title: str


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
