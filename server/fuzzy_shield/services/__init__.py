import time
import concurrent.futures
import pandas as pd
import pathlib

from redis import Redis as RedisBlocking
from fastapi import FastAPI
from fuzzy_shield import Algorithms, RedisSets as sets
from fuzzy_shield.task import Task
from fuzzy_shield.config import Config
from fuzzy_shield.services import status_updater
from fuzzy_shield.services import scorer

config = Config()
# Process pool for tasks
process_pool = concurrent.futures.ProcessPoolExecutor(max_workers=1)


sqli_set: list[str] | None = None
xss_set: list[str] | None = None


def on_startup(app: FastAPI):
    status_updater.initialize()

    sqli_path = pathlib.Path('./datasets/out/sqli-malicious.csv')
    xss_path = pathlib.Path('./datasets/out/xss-malicious.csv')

    if not sqli_path.exists():
        print(f"SQLi dataset file does not exists {sqli_path}")
        exit(1)

    if not xss_path.exists():
        print(f"XSS dataset file does not exists {xss_path}")
        exit(1)
    global sqli_set, xss_set

    sqli_set = pd.read_csv(sqli_path)["Query"]
    xss_set = pd.read_csv(xss_path)["Sentence"]


def on_shutdown(app: FastAPI):
    status_updater.uninitialize()
    process_pool.shutdown()


def schedule_task(task: Task):
    task_id = task.task_id
    print(f"Processing task {task_id}...")
    persist_task(task)

    algos = Algorithms.algorithms

    for algo in algos:
        algo_scorer_function: function = getattr(scorer, algo)

        if task.sqli and getattr(task, algo):
            f = process_pool.submit(
                algo_scorer_function, task.text, sqli_set, task_id=task_id, is_sqli=True, algo=algo)
            f.add_done_callback(handle_task_finished)

        if task.xss and getattr(task, algo):
            f = process_pool.submit(
                algo_scorer_function, task.text, xss_set, task_id=task_id, is_sqli=False, algo=algo)
            f.add_done_callback(handle_task_finished)


def persist_task(task: Task):
    with RedisBlocking.from_url(str(config.redis_url), decode_responses=True) as r:
        task_id = task.task_id
        r.hset(task_id, mapping=task.model_dump())
        r.zadd(sets.main, {task_id: task.created_at.timestamp()})
        r.zadd(sets.main_incomplete, {task_id: task.created_at.timestamp()})
        if task.collection is not None:
            r.zadd(sets.collection(task.collection), {
                   task_id: task.created_at.timestamp()})
            r.zadd(sets.collection_incomplete(task.collection),
                   {task_id: task.created_at.timestamp()})


def handle_task_finished(worker_future: concurrent.futures.Future):
    if worker_future.exception():
        raise worker_future.exception()
