import time
import json
import concurrent.futures

from redis import Redis as RedisBlocking

from fuzzy_shield import RedisSets
from fuzzy_shield.task import Task
from fuzzy_shield.config import Config

config = Config()

# Process pool for tasks
process_pool = concurrent.futures.ProcessPoolExecutor(max_workers=4)


# @app.on_event('shutdown')
# async def process_shutdown():
#     process_pool.shutdown()


def schedule_task(task_id):
    process_pool.submit(_process_task, task_id)
    # _process_task(task_id)


def _process_task(task_id):
    with RedisBlocking.from_url(str(config.redis_url), decode_responses=True) as r:
        task_raw = r.hgetall(task_id)
        task = Task(**task_raw)
        # This is a dummy worker for now - it will be replaced with your algorithms later
        print(f"Processing task {task_id}...")
        time.sleep(20)  # Simulate some work
        print(f"Task {task_id} completed.")
        r.hset(task_id, "status", "completed")

        r.zrem(RedisSets.main_incomplete, task_id)
        r.zadd(RedisSets.main_completed, {
               task_id: task.created_at.timestamp()})

        if task.collection:
            r.zrem(
                RedisSets.collection_incomplete(task.collection), task_id)
            r.zadd(RedisSets.collection_completed(task.collection), {
                task_id: task.created_at.timestamp()})

        # Publish the task update on Redis channel
        r.publish("task_updates", json.dumps(
            {"task_id": task_id, "status": "completed"}))

        # ... [Here's where you'll call your fuzzy matching algorithms] ...
