import asyncio
from fastapi import FastAPI
from . import redis


async def on_startup(app: FastAPI):
    await redis.initialize_redis()


async def on_shutdown(app: FastAPI):
    await redis.uninitialize_redis()
