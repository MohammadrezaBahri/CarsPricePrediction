import asyncio
import timeit
import aiohttp

from crawling_logger import posts_info_logger as logger
from database import get_tokens_from_database, insert_posts_into_database, handle_deleted_token
from process_requests import process_token


async def main():
    tokens = get_tokens_from_database()
    logger.info(f"{len(tokens)} posts found to crawl\n{'-'*50}")

    async with aiohttp.ClientSession() as session:
        def process_token_wrapper(token):
            return process_token(session, token)

        start_time = timeit.default_timer()
        tasks = [process_token_wrapper(token) for token in tokens]
        results = await asyncio.gather(*tasks)
        end_time = timeit.default_timer()
        logger.info(f"Total requests time: {end_time - start_time} seconds")
        logger.info(f"{len(results)} results was found\n{'-'*50}")

    posts = []
    deleted_tokens = []

    if results:
        for status_code, post_data in results:
            if status_code == 200 and post_data:
                posts.append(post_data)
            elif status_code == 404:
                deleted_tokens.append(post_data.get('token'))

    if posts:
        logger.info(f'Inserting {len(posts)} new posts to the database')
        start_time = timeit.default_timer()
        insert_posts_into_database(posts)
        logger.info(f"Total insertion time: {timeit.default_timer() - start_time} seconds for {len(posts)} posts\n{'-'*50}")

    if deleted_tokens:
        logger.info(f'Handling {len(deleted_tokens)} deleted tokens')
        start_time = timeit.default_timer()
        handle_deleted_token(deleted_tokens)
        logger.info(f"Total handling time: {timeit.default_timer() - start_time} seconds for {len(deleted_tokens)} tokens\n{'-'*50}")
    

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
