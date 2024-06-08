from typing import Callable
import functools
import json

import time
import tracemalloc
import psutil

from redis import Redis
from fuzzy_shield.config import Config
from fuzzy_shield import RedisSets

config = Config()

redis_instance = Redis.from_url(str(config.redis_url))


def scorer_profiler(func: Callable):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        task_id = kwargs["task_id"]
        is_sqli = kwargs["is_sqli"]
        algo = kwargs["algo"]

        score, execution_time, cpu, memory = run_and_profile_scorer(
            func, *args)
        execution_time = execution_time * 1000

        type_slug = 'sqli' if is_sqli else 'xss'
        redis_instance.publish(RedisSets.updates_channel, json.dumps(
            {
                "task_id": task_id,
                f"{algo}_{type_slug}_score": score,
                f"{algo}_{type_slug}_time": execution_time,
                f"{algo}_{type_slug}_cpu": cpu,
                f"{algo}_{type_slug}_memory": memory
            }))

    return wrapper


def run_and_profile_scorer(scorer: Callable, text: str, choice: list[str]) -> tuple[float, float, float, float]:
    ps = psutil.Process()

    tracemalloc.start()
    # Record the CPU times before execution
    cpu_before_time = ps.cpu_times()
    before_time = time.time()

    # call the real score function
    result = scorer(text, choice)
    cpu_after_time = ps.cpu_times()
    after_time = time.time()

    score = 0
    if result:
        score = result[1]

    current_mem, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    user_cpu_usage = cpu_after_time.user - cpu_before_time.user
    system_cpu_usage = cpu_after_time.system - cpu_before_time.system

    execution_time = user_cpu_usage + system_cpu_usage
    real_execution_time = after_time - before_time
    cpu_percentage = execution_time / real_execution_time * 100

    if cpu_percentage <= 1:
        # zero-percentage is caused by a so small "cpu time" or cache so
        # `execution_time` is zero

        # print(execution_time, real_execution_time, score, result[0])
        cpu_percentage = 100

    return score, real_execution_time, cpu_percentage, peak_mem
