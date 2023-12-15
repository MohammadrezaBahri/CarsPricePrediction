import aiohttp
import asyncio
import config as c
import time

results = []  

def get_tasks(session):
    tasks = [session.post(url=c.URL, data=c.get_payload(i)) for i in range (5)]
    return tasks

async def main():
    start_time = time.time()
    
    async with aiohttp.ClientSession() as session:
        tasks = get_tasks(session=session)
        responses = await asyncio.gather(*tasks)
        for response in responses:
            results.append(await response.json())


    print('execution time: ', time.time() - start_time)

if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()