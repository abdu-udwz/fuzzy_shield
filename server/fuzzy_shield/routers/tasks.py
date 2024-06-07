from typing import Optional
from fastapi import Request, HTTPException, BackgroundTasks, Query
from fastapi import APIRouter

from fuzzy_shield.services import schedule_task
from fuzzy_shield.data import bulk_schedule_sample
from fuzzy_shield.dependencies.redis import RedisDep, RedisSetsDep
from fuzzy_shield.task import Task, TaskCollectionResponse, TASK_STATUS

router = APIRouter(prefix="/tasks", tags=['tasks'])


@router.get("/", response_model=TaskCollectionResponse)
async def get_tasks(r: RedisDep, sets: RedisSetsDep, limit: Optional[int] = Query(default=10, maximum=100),
                    page: Optional[int] = Query(default=0),
                    status: Optional[TASK_STATUS] = None,
                    collection: Optional[str] = None) -> TaskCollectionResponse:

    lstart = page * limit
    lend = lstart + limit

    task_set = sets.main if not collection else sets.collection(collection)
    if status is not None and status != "completed":
        task_set = sets.main_incomplete if not collection else sets.collection_incomplete(
            collection)
    elif status == 'completed':
        task_set = sets.main_completed if not collection else sets.collection_completed(
            collection)

    ids = await r.zrange(task_set, desc=True, start=lstart, end=lend)
    tasks: list[Task] = []
    for task_id in ids:
        task_raw = await r.hgetall(task_id)
        task = Task(**task_raw)
        tasks.append(task)

    task_count = await r.zcount(task_set, '-inf', '+inf')

    return TaskCollectionResponse(tasks=tasks, count=task_count)


@router.get("/{task_id}")
async def get_task(task_id: str, r: RedisDep) -> Task:
    task_data = await r.hgetall(task_id)

    if not task_data:
        raise HTTPException(status_code=404, detail="Task not found")

    task = Task(**task_data)
    return task


@router.post("/")
async def submit_task(request: Request, background_task: BackgroundTasks, r: RedisDep, sets: RedisSetsDep) -> Task:
    data = await request.json()
    text = data.get("text")
    collection = data.get("collection")
    if not text:
        raise HTTPException(
            status_code=400, detail="Missing 'text' in request body")

    task = Task(text=text,
                sqli=data.get("sqli", 1), xss=data.get("xss", 1),
                hamming=data.get("hamming", 1),
                naive=data.get("naive", 1),
                levenshtein_ratio=data.get("levenshtein_ratio", 1),
                levenshtein_sort=data.get("levenshtein_sort", 1))
    if collection:
        task.collection = collection

    # Submit the task to the process pool
    background_task.add_task(schedule_task, task)

    return task


# bulk submit sample tasks

@router.post('/bulk')
async def schedule_sample() -> None:
    bulk_schedule_sample()
