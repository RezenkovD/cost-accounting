from pydantic import BaseModel


class GroupBase(BaseModel):
    title: str


class GroupCreate(GroupBase):
    group_password: str


class Group(GroupBase):
    id: int

    class Config:
        orm_mode = True
