import time
from .decorator import scorer_profiler


@scorer_profiler
def score(query: str, choices: list[str]):
    time.sleep(13)
    return None
