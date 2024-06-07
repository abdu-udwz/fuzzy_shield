import time
import tracemalloc
from thefuzz import fuzz, process
from .decorator import with_redis


@with_redis
def score(query: str, choices: list[str], **kwargs) -> tuple[float, float, float, float]:
    tracemalloc.start()
    start_time = time.time()
    result = process.extractOne(query, choices, scorer=fuzz.ratio)
    end_time = time.time()
    current_mem, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    execution_time = end_time - start_time

    match_score = 0
    if result:
        match_score = result[1]

    return (match_score, execution_time, 0, peak_mem)
