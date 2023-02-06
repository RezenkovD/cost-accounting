from pydantic import BaseModel
from pydantic.schema import datetime


class InvitationBase(BaseModel):
    recipient_id: str


class InvitationCreate(InvitationBase):
    pass


class Invitation(InvitationBase):
    id: int
    status: str
    sender_id: int
    recipient_id: int
    group_id: int
    time: datetime

    class Config:
        orm_mode = True
