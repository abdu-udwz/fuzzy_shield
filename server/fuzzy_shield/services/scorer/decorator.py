import functools
import json

from redis import Redis
from fuzzy_shield.config import Config
from fuzzy_shield import RedisSets

config = Config()

redis_instance = Redis.from_url(str(config.redis_url))


def with_redis(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        task_id = kwargs["task_id"]
        is_sqli = kwargs["is_sqli"]
        algo = kwargs["algo"]
        score, time, cpu, memory = func(*args, **kwargs)

        time = time * 1000

        type_slug = 'sqli' if is_sqli else 'xss'
        redis_instance.publish(RedisSets.updates_channel, json.dumps(
            {
                "task_id": task_id,
                f"{algo}_{type_slug}_score": score,
                f"{algo}_{type_slug}_time": time
            }))

    return wrapper
