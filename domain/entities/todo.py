import datetime

from pydantic import BaseModel, fields
from uuid import UUID, uuid4


class Todo(BaseModel):
    id: UUID = fields.Field(default_factory=uuid4)
    text: str
    created_at: datetime.datetime = fields.Field(default_factory=datetime.datetime.now)
    is_done: bool = False
