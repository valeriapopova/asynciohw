import asyncio
import time
import aiohttp
import more_itertools
from typing import Iterable

import config
from config import DSN
import asyncpg

API_ENDPOINT = 'https://swapi.dev/api/people/'
MAX_CHUCK = 10


# async def task_test():
#     while True:
#         print('работа')
#
#         await asyncio.sleep(1)


async def get_people(id_range: Iterable[int]):
    for id_range_chunk in more_itertools.chunked(id_range, MAX_CHUCK):
        yield await asyncio.gather(*[get_person(i) for i in id_range_chunk])


async def get_person(person_id: int) -> dict:
    async with aiohttp.client.ClientSession() as session:
        async with session.get(f'{API_ENDPOINT}/{person_id}') as response:
            response = await response.json()
            # print(response)
            return response


# async def main():
#     task = asyncio.create_task(task_test())
#     print(task)
#     async for people in get_people(range(1, 100)):
#         print(len(people))
#         print(people)
#
#     await task


async def insert_people(pool: asyncpg.Pool, people_list):
    for key, values_list in people_list.items():
        query = f'INSERT INTO people VALUES ({values_list})'
        async with pool.acquire() as conn:
            async with conn.transaction():
                await conn.executemany(query, people_list)


async def main():
    pool = await asyncpg.create_pool(config.DSN)
    tasks = []

    for i in range(84):
        get_person_task = asyncio.create_task(get_person(i))
        tasks.append(get_person_task)

    for task in tasks:
        await task
        await insert_people(pool, task.result())
        print(task.result())


start = time.time()
asyncio.run(main())
print(time.time() - start)

