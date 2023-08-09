import requests
import time
import aiohttp
import asyncio
from models import Session, SwapiPeople, Base, engine
from more_itertools import chunked

MAX_CHUNK_SIZE = 10

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

def get_titles(list_: list):
    titles = ''
    for link in list_:
        dict_with_info = requests.get(link).json()
        title = dict_with_info.get('title', dict_with_info.get('name'))
        titles += title + ', '
    return titles[:-2]


async def get_info_person(person_id):
    async with aiohttp.ClientSession() as session:
    # session = aiohttp.ClientSession()
        URL = f'https://swapi.dev/api/people/{person_id}/'
        response = await session.get(URL)
        dict_data = await response.json()
        # if dict_data == {'detail': 'Not found'}:
        #     return dict_data

        try:
            del dict_data['created']
            del dict_data['edited']
            del dict_data['url']
        except KeyError:
            return {'detail': 'Not found'}

        dict_data['films'] = get_titles(dict_data['films'])
        dict_data['species'] = get_titles(dict_data['species'])
        dict_data['vehicles'] = get_titles(dict_data['vehicles'])
        dict_data['starships'] = get_titles(dict_data['starships'])
    return dict_data


async def insert_to_db(people_json_list):
    async with Session() as session:
        swapi_people_list = [SwapiPeople(**json_data) for json_data in people_json_list]
        session.add_all(swapi_people_list)
        await session.commit()


async def get_people():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    for ids_chunk in chunked(range(1, 83), MAX_CHUNK_SIZE):
        print(ids_chunk)
        coros = []
        for id_ in ids_chunk:
            info_person = asyncio.create_task(get_info_person(id_))
            print(info_person)
            coros.append(info_person)
        print(coros)
        people_data = await asyncio.gather(*coros)
        # await insert_to_db(people_data)
        task = asyncio.create_task(insert_to_db(people_data))
    curret_task = asyncio.current_task()
    tasks_sets = asyncio.all_tasks()
    tasks_sets.remove(curret_task)
    await asyncio.gather(*tasks_sets)
    await engine.dispose()

start = time.time()
asyncio.run(get_people())
# print(asyncio.run(get_info_person(17)))
end = time.time()
print(end - start)
