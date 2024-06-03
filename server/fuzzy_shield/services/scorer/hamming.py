import time
from .decorator import with_redis


@with_redis
def score(query: str, choices: list[str], **kwargs) -> tuple[float, float, float, float]:
    time.sleep(23)

    return (0, 0, 0, 0)
