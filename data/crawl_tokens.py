import asyncio
import timeit
import aiohttp

from config import PAGES_FOR_CRAWL_BATCH_QUANTITY
from crawling_logger import tokens_info_logger as logger
from database import insert_tokens_into_database
from process_requests import crawl_page


async def main():
    num_requests = PAGES_FOR_CRAWL_BATCH_QUANTITY  

    logger.info(f"crawling {num_requests} pages\n{'-'*50}")

    async with aiohttp.ClientSession() as session:
        tasks = [crawl_page(session, page) for page in range(1, num_requests + 1)]

        start_time = timeit.default_timer()
        results = await asyncio.gather(*tasks)
        end_time = timeit.default_timer()

        # Concatenate the tokens from all requests into a single list
        all_tokens = [token for tokens in results for token in tokens]

        logger.info(f"Total requests time: {end_time - start_time} seconds")
        logger.info(f"{len(all_tokens)} results was found\n{'-'*50}")

        # Insert tokens into the 'tokens' table in the PostgreSQL database
        logger.info(f'inserting {len(all_tokens)} tokens into the database')
        start_time = timeit.default_timer()
        insert_tokens_into_database(all_tokens)
        end_time = timeit.default_timer()
        logger.info(f"Total insertion time: {end_time - start_time} seconds for {len(all_tokens)} tokens\n{'-'*50}")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
