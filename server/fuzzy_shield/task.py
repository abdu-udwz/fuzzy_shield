from typing import Literal
from typing_extensions import Annotated
from uuid import uuid4
from datetime import datetime
from pydantic import BaseModel, Field, UUID4, PastDatetime, field_serializer


class Task(BaseModel):
    task_id: UUID4 = Field(default_factory=lambda: uuid4().hex, frozen=True)
    text: str
    status: Literal["queued", "completed", "cancelled"] = "queued"

    created_at: Annotated[PastDatetime, Field(
        default_factory=datetime.now, frozen=True)]

    # redis cannot accept a datetime object
    @field_serializer('created_at', when_used='always')
    def serilize_created_at(self, created_at: datetime):
        return created_at.isoformat()
