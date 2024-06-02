import logging
import asyncio
import json
from typing_extensions import Annotated

import redis.asyncio as redis
from fastapi import Depends
from fuzzy_shield import RedisSets
from fuzzy_shield.config import Config

config = Config()


logger = logging.getLogger("redis#dependency")


# Redis channel for task updates
redis_channel = "task_updates"

_app_running = False

# Redis connection
redis_pool = redis.ConnectionPool.from_url(
    str(config.redis_url), decode_responses=True)

redis_instance = redis.Redis.from_pool(redis_pool)


async def initialize_redis():
    logger.info('initializing redis & update listener')
    global _app_running
    _app_running = True

    r = redis.Redis.from_pool(redis_pool)
    global redis_instance
    redis_instance = r
    pubsub = r.pubsub()

    await pubsub.subscribe(redis_channel)
    asyncio.create_task(reader(pubsub))


async def uninitialize_redis():
    logger.info('Stopping update listener and disconnecting')
    global _app_running
    _app_running = False
    await redis_pool.disconnect()

updates = asyncio.Queue()


async def reader(channel: redis.client.PubSub):
    while True and _app_running:
        # timeout=None is required here to avoid loops running eagerly for messages
        message = await channel.get_message(ignore_subscribe_messages=True, timeout=None)
        if message and message["type"] == "message":
            # Received a task update
            logger.info(
                f'Received update on task from queue {message["data"]}')
            update = json.loads(message["data"])
            updates.put_nowait(update)
    else:
        logger.info('')


def get_redis():
    return redis_instance


RedisDep = Annotated[redis.Redis, Depends(get_redis)]


def get_redis_sets():
    return RedisSets


RedisSetsDep = Annotated[RedisSets, Depends(get_redis_sets)]


def get_updates_queue():
    return updates


RedisUpdatesQueueDep = Annotated[asyncio.Queue, Depends(get_updates_queue)]
