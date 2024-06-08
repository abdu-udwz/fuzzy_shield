from typing import Literal, Optional
from typing_extensions import Annotated
from uuid import uuid4
from datetime import datetime
from pydantic import BaseModel, Field, UUID4, PastDatetime, field_serializer, StringConstraints

TASK_STATUS = Literal["queued", "partial", "completed"]


class Task(BaseModel):
    task_id: str = Field(default_factory=lambda: uuid4().hex, frozen=True)
    text: str
    status: TASK_STATUS = "queued"

    """Keep track for false-positive and false-negative"""
    designated_result: bool = False

    @field_serializer("designated_result", when_used="always")
    def serialize_designated_result(self, designated_result: bool):
        return int(designated_result)

    collection: str = Field(
        min_length=1, strip_white_space=True, default="main")

    created_at: Annotated[PastDatetime, Field(
        default_factory=datetime.now, frozen=True)]

    # redis cannot accept a datetime object
    @field_serializer('created_at', when_used='always')
    def serialize_created_at(self, created_at: datetime):
        return created_at.isoformat()

    sqli: int = 1
    xss: int = 1

    hamming: int = 1
    hamming_sqli_score: float = -1
    hamming_sqli_time: float = -1
    hamming_sqli_cpu: float = -1
    hamming_sqli_memory: float = -1

    hamming_xss_score: float = -1
    hamming_xss_time: float = -1
    hamming_xss_cpu: float = -1
    hamming_xss_memory: float = -1

    naive: int = 1
    naive_sqli_score: float = -1
    naive_sqli_time: float = -1
    naive_sqli_cpu: float = -1
    naive_sqli_memory: float = -1

    naive_xss_score: float = -1
    naive_xss_time: float = -1
    naive_xss_cpu: float = -1
    naive_xss_memory: float = -1

    levenshtein_ratio: int = 1
    levenshtein_ratio_sqli_score: float = -1
    levenshtein_ratio_sqli_time: float = -1
    levenshtein_ratio_sqli_cpu: float = -1
    levenshtein_ratio_sqli_memory: float = -1

    levenshtein_ratio_xss_score: float = -1
    levenshtein_ratio_xss_time: float = -1
    levenshtein_ratio_xss_cpu: float = -1
    levenshtein_ratio_xss_memory: float = -1

    levenshtein_sort: int = 1
    levenshtein_sort_sqli_score: float = -1
    levenshtein_sort_sqli_time: float = -1
    levenshtein_sort_sqli_cpu: float = -1
    levenshtein_sort_sqli_memory: float = -1

    levenshtein_sort_xss_score: float = -1
    levenshtein_sort_xss_time: float = -1
    levenshtein_sort_xss_cpu: float = -1
    levenshtein_sort_xss_memory: float = -1


class TaskCollectionResponse(BaseModel):
    tasks: list[Task]
    count: int
