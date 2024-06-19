from typing_extensions import Optional
from fastapi import APIRouter, BackgroundTasks, HTTPException, Query
from fuzzy_shield.dependencies.redis import RedisDep, RedisSetsDep
from fuzzy_shield.data.stats import compute_stats
from fuzzy_shield.task import CollectionStatsConfig, Task

router = APIRouter(prefix='/collections')


@router.get('/')
async def get_collections(r: RedisDep, sets: RedisSetsDep):
    collections: list[str] = await r.keys(f'{sets.collection_prefix}*')

    collections = list(filter(lambda col: not (col.endswith(
        '_incomplete') or col.endswith('_completed')), collections))
    return [collection.replace(sets.collection_prefix, '') for collection in collections]


@router.get("/{collection}/stats", status_code=201)
async def get_collection_stats(
    background_tasks: BackgroundTasks,
    collection: str,
    r: RedisDep, sets: RedisSetsDep,
    sqli:  Optional[int] = Query(1),
    xss:  Optional[int] = Query(1),

    hamming:  Optional[int] = Query(1),
    hamming_sqli: Optional[float] = Query(50),
    hamming_xss: Optional[float] = Query(50),

    naive:  Optional[int] = Query(1),
    naive_sqli: Optional[float] = Query(50),
    naive_xss: Optional[float] = Query(50),

    levenshtein_ratio:  Optional[int] = Query(1),
    levenshtein_ratio_sqli: Optional[float] = Query(50),
    levenshtein_ratio_xss: Optional[float] = Query(50),

    levenshtein_sort:  Optional[int] = Query(1),
    levenshtein_sort_sqli: Optional[float] = Query(50),
    levenshtein_sort_xss: Optional[float] = Query(50),
):
    task_collection = sets.collection_completed(collection)

    ids = await r.zrange(task_collection, desc=True, start=0, end=-1)
    tasks: list = []
    for task_id in ids:
        task_raw = await r.hgetall(task_id)
        task = Task(**task_raw)
        tasks.append(task.model_dump())

    if len(ids) == 0:
        raise HTTPException(
            status_code=400, detail="Empty or non-existing collection")

    config = CollectionStatsConfig(collection=collection,
                                   sqli=sqli,
                                   xss=xss,
                                   hamming=hamming,
                                   hamming_sqli=hamming_sqli,
                                   hamming_xss=hamming_xss,

                                   naive=naive,
                                   naive_sqli=naive_sqli,
                                   naive_xss=naive_xss,

                                   levenshtein_ratio=levenshtein_ratio,
                                   levenshtein_ratio_sqli=levenshtein_ratio_sqli,
                                   levenshtein_ratio_xss=levenshtein_ratio_xss,

                                   levenshtein_sort=levenshtein_sort,
                                   levenshtein_sort_sqli=levenshtein_sort_sqli,
                                   levenshtein_sort_xss=levenshtein_sort_xss
                                   )

    background_tasks.add_task(compute_stats, tasks, config)
