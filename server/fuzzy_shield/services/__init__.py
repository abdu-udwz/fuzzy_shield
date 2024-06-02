import time
import json
import concurrent.futures

from redis import Redis as RedisBlocking
from fastapi import FastAPI
from fuzzy_shield import RedisSets
from fuzzy_shield.task import Task
from fuzzy_shield.config import Config
from fuzzy_shield.services import status_updater

config = Config()
# Process pool for tasks
process_pool = concurrent.futures.ProcessPoolExecutor(max_workers=4)


def on_startup(app: FastAPI):
    status_updater.initialize()


def on_shutdown(app: FastAPI):
    status_updater.uninitialize()
    process_pool.shutdown()


def schedule_task(task_id):
    process_pool.submit(_process_task, task_id)
    # _process_task(task_id)


def _process_task(task_id):
    with RedisBlocking.from_url(str(config.redis_url), decode_responses=True) as r:
        task_raw = r.hgetall(task_id)
        # This is a dummy worker for now - it will be replaced with your algorithms later
        print(f"Processing task {task_id}...")
        time.sleep(20)  # Simulate some work
        print(f"Task {task_id} completed.")

        # Publish the task update on Redis channel
        r.publish("task_updates", json.dumps(
            {"task_id": task_id, "status": "completed"}))

        # ... [Here's where you'll call your fuzzy matching algorithms] ...
