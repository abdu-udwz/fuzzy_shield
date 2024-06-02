from fastapi import APIRouter
from fuzzy_shield.dependencies.redis import RedisDep, RedisSetsDep

router = APIRouter(prefix='/collections')


@router.get('/')
async def get_collections(r: RedisDep, sets: RedisSetsDep):
    collections: list[str] = await r.keys(f'{sets.collection_prefix}*')

    collections = list(filter(lambda col: not (col.endswith(
        '_incomplete') or col.endswith('_completed')), collections))
    return [collection.replace(sets.collection_prefix, '') for collection in collections]
