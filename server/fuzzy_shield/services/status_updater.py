import asyncio
from redis.asyncio import Redis

from fuzzy_shield import RedisSets
from fuzzy_shield.dependencies.redis import redis_pool
from fuzzy_shield.task import Task
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

            task_id = update["task_id"]
            update_status = update["task_status"]

            r.hset(task_id, "status", update_status)

            task_raw = r.hgetall(task_id)
            task = Task(**task_raw)

            r.zrem(RedisSets.main_incomplete, task_id)
            r.zadd(RedisSets.main_completed, {
                task_id: task.created_at.timestamp()})

            if task.collection:
                r.zrem(
                    RedisSets.collection_incomplete(task.collection), task_id)
                r.zadd(RedisSets.collection_completed(task.collection), {
                    task_id: task.created_at.timestamp()})

            EXTERNAL_UPDATES_QUEUE.put_nowait(update)
            INTERNAL_UPDATES_QUEUE.task_done()
        except:
            print("something went wrong")
