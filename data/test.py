import aiohttp
import asyncio
import config as c

import time


async def crawl_website(session, url, payload):
    tokens = []

    async with session.post(url=url, data=payload) as response:
        if response.status == 200:
            post_list = (await response.json())['web_widgets']['post_list']
            for post in post_list:
                token = post['data'].get('token')
                if token:
                    tokens.append(token)
          
    return tokens

async def main():
    url = c.URL
    num_requests = 50

    async with aiohttp.ClientSession() as session:
        tasks = []
        for page in range(1, num_requests + 1):
            payload = f"""{{
                "json_schema": {{
                    "brand_model_manufacturer_origin": {{
                        "value": "{c.BRAND_MODEL_MANUFACTURER_ORIGIN}"
                    }},
                    "category": {{
                        "value": "{c.CATEGORY}"
                    }},
                    "business-type": {{
                        "value": "{c.BUSINESS_TYPE}"
                    }},
                    "cities": {c.CITIES},
                    "price": {{
                        "min": {c.MIN_PRICE},
                        "max": {c.MAX_PRICE}
                    }},
                    "production-year": {{
                        "min": {c.MIN_PRODUCTION_YEAR}
                    }}
                }},
                "last-post-date": {c.LAST_POST_DATE},
                "page": {page}
            }}"""
            tasks.append(crawl_website(session, url, payload))

        start_time = time.time()
        results = await asyncio.gather(*tasks)
        end_time = time.time()

        execution_time = end_time - start_time
        print(f"Total execution time: {execution_time} seconds")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    #loop.run_until_complete(main())


