from fastapi import APIRouter
from . import tasks
from . import collections

api_router = APIRouter(prefix='/api')
api_router.include_router(tasks.router)
api_router.include_router(collections.router)
