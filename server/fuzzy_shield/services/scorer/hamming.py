import time
from .decorator import with_redis


@with_redis
def score(query: str, choices: list[str], **kwargs) -> tuple[float, float, float, float]:
    start_time = time.time()
    time.sleep(13)
    end_time = time.time()
    execution_time = end_time - start_time

    return (0, execution_time, 0, 0)
