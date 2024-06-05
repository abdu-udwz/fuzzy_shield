import time
from thefuzz import fuzz, process
from .decorator import with_redis


@with_redis
def score(query: str, choices: list[str], **kwargs) -> tuple[float, float, float, float]:
    start_time = time.time()
    result = process.extractOne(query, choices, scorer=fuzz.token_sort_ratio)
    end_time = time.time()

    execution_time = end_time - start_time

    if result:
        return (result[1], execution_time, 0, 0)

    return (0, 0, 0, 0)
