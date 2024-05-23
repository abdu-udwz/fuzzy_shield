from fastapi import FastAPI, WebSocket, Request, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.websockets import WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fuzzy_shield.config import Config

import asyncio
from redis import Redis as RedisBlocking
import redis.asyncio as redis
import json
import uuid
import time
import concurrent.futures
import logging

config = Config()
# print(config.model_dump())

logger = logging.getLogger("fuzzy_shield_app")

app = FastAPI()

# Redis connection
redis_pool = redis.ConnectionPool.from_url(
    "redis://localhost:6379", decode_responses=True)

# Redis channel for task updates
redis_channel = "task_updates"
# Process pool for tasks
process_pool = concurrent.futures.ProcessPoolExecutor(max_workers=4)

updates = asyncio.Queue()


@app.on_event('startup')
async def initialize_redis():
    logger.info('initializing redis update listener')
    # Subscribe to the Redis channel
    r = redis.Redis.from_pool(redis_pool)
    pubsub = r.pubsub()

    await pubsub.subscribe(redis_channel)
    future = asyncio.create_task(reader(pubsub))
    # await future


@app.on_event('shutdown')
async def process_shutdown():
    await redis_pool.disconnect()
    process_pool.shutdown()


async def reader(channel: redis.client.PubSub):
    while True:
        # timeout=None is required here to avoid loops running eagerly for messages
        message = await channel.get_message(ignore_subscribe_messages=True, timeout=None)
        if message and message["type"] == "message":
            # Received a task update
            print('task updated from redis queue')
            update = json.loads(message["data"])
            updates.put_nowait(update)


@app.post("/api/submit_task/")
async def submit_task(request: Request, background_task: BackgroundTasks):
    data = await request.json()
    text = data.get("text")
    if not text:
        raise HTTPException(
            status_code=400, detail="Missing 'text' in request body")

    task_id = str(uuid.uuid4())
    r = redis.Redis.from_pool(redis_pool)

    # Store the task in Redis
    await r.hset(task_id, "status", "queued")
    await r.hset(task_id, "text", text)

    # Submit the task to the process pool
    background_task.add_task(schedule_task, task_id, text)

    return JSONResponse({"task_id": task_id})


def schedule_task(task_id, text):
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    # future = loop.run_in_executor(None, _process_task, task_id, text)
    # return future.result()

    _process_task(task_id, text)


def _process_task(task_id, text):
    with RedisBlocking.from_url("redis://localhost:6379") as r:

        # This is a dummy worker for now - it will be replaced with your algorithms later
        print(f"Processing task {task_id}...")
        time.sleep(3)  # Simulate some work
        print(f"Task {task_id} completed.")
        r.hset(task_id, "status", "completed")

        # Publish the task update on Redis channel
        r.publish(redis_channel, json.dumps(
            {"task_id": task_id, "status": "completed"}))

        # ... [Here's where you'll call your fuzzy matching algorithms] ...


@app.websocket("/api/ws/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        await websocket.send_text("Connection established!")

        while True:
            # print(f"received text from websocket {data}")
            update = await updates.get()
            await websocket.send_text(json.dumps(update))
            updates.task_done()

    except WebSocketDisconnect:
        print("WebSocket connection closed")


@app.get("/api/tasks/{task_id}")
async def get_results(task_id: str):
    print(task_id, type(task_id))
    task_data = r.hgetall(task_id)

    if not task_data:
        raise HTTPException(status_code=404, detail="Task not found")

    return JSONResponse(task_data)


class SPAStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope):
        response = await super().get_response(path, scope)
        if response.status_code == 404:
            response = await super().get_response('.', scope)
        return response


app.mount('/app/', SPAStaticFiles(directory='public',
          html=True), name='whatever')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9090)
