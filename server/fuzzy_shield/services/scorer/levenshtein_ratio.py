import time
from thefuzz import fuzz, process
from .decorator import with_redis


@with_redis
def score(query: str, choices: list[str], **kwargs) -> tuple[float, float, float, float]:
    start_time = time.time()
    result = process.extractOne(query, choices, scorer=fuzz.ratio)
    end_time = time.time()
    execution_time = end_time - start_time

    match_score = 0
    if result:
        match_score = result[1]

    return (match_score, execution_time, 0, 0)
