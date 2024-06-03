import asyncio
import json
from redis.asyncio import Redis

from fuzzy_shield import RedisSets, ALGORITHMS
from fuzzy_shield.dependencies.redis import redis_pool
from fuzzy_shield.task import Task, TASK_STATUS
from .queues import INTERNAL_UPDATES_QUEUE, EXTERNAL_UPDATES_QUEUE

_app_running = False


loop_task = None


def initialize():
    global _app_running
    _app_running = True

    global loop_task
    loop_task = asyncio.create_task(loop())


def uninitialize():
    global _app_running
    _app_running = False

    if loop_task and not (loop_task.done() or loop_task.cancelled()):
        loop_task.cancel()


async def loop():
    r = Redis.from_pool(redis_pool)
    while True and _app_running:
        try:
            update = await INTERNAL_UPDATES_QUEUE.get()
            print('Internal status updater', update)
            task_id = update["task_id"]

            await r.hset(task_id, mapping=update)

            task_raw = await r.hgetall(task_id)
            task = Task(**task_raw)
            EXTERNAL_UPDATES_QUEUE.put_nowait(update)

            new_status = compute_task_status(task)
            await r.hset(task_id, "status", new_status)

            if new_status == 'completed':
                r.zrem(RedisSets.main_incomplete, task_id)
                r.zadd(RedisSets.main_completed, {
                    task_id: task.created_at.timestamp()})

                if task.collection:
                    r.zrem(
                        RedisSets.collection_incomplete(task.collection), task_id)
                    r.zadd(RedisSets.collection_completed(task.collection), {
                        task_id: task.created_at.timestamp()})

            if new_status != task.status:
                EXTERNAL_UPDATES_QUEUE.put_nowait(json.dumps({
                    "task_id": task_id,
                    "status": new_status
                }))

            INTERNAL_UPDATES_QUEUE.task_done()
        except Exception as exc:
            print("Something went wrong while handling internal status updates")
            print(exc)


def compute_task_status(task: Task) -> TASK_STATUS:
    algos = ALGORITHMS.keys()

    enabled_algo = set()

    for algo in algos:
        algo_enabled = getattr(task, algo)
        if algo_enabled:
            enabled_algo.add(algo)

    algo_state = {}
    one_done = False
    for algo in enabled_algo:
        algo_state[algo] = {
            "sqli": not task.sqli,
            "xss": not task.xss
        }

        if task.sqli and getattr(task, f"{algo}_sqli_time"):
            one_done = True
            algo_state[algo]['sqli'] = True

        if task.sqli and getattr(task, f"{algo}_xss_time"):
            one_done = True
            algo_state[algo]['xss'] = True

    all_done = True
    for algo, algo_state in algo_state.items():
        if (task.xss and not algo_state["xss"]) or (task.sqli and not algo_state["sqli"]):
            all_done = False
            break

    if all_done:
        return 'completed'
    elif one_done:
        return 'partial'

    return 'queued'
