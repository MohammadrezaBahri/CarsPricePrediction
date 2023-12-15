import aiohttp
import asyncio
import json
import logging
import config   
import time
from datetime import datetime
import psycopg2 

logging.basicConfig(filename='logs/crawl_tokens_log.txt', 
                    level=logging.ERROR, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def insert_tokens_into_database(tokens):
    try:
        conn = psycopg2.connect(**config.db_params)
        cursor = conn.cursor()

        # Insert token into the 'tokens' table
        insert_query = 'INSERT INTO divar_cars_data.tokens ("token") VALUES '
        for i, token in enumerate(tokens):
            insert_query += f"{',' if i > 0 else ''}('{token}')"

        insert_query += ' ON CONFLICT DO NOTHING'

        cursor.execute(insert_query)

        conn.commit()

    except Exception as e:
        logging.error(f"Error inserting tokens into the database: {e}")

    finally:
        cursor.close()
        conn.close()

async def crawl_website(session, url, payload):
    tokens = []

    try:
        async with session.post(url=url, data=payload) as response:
            if response.status == 200:
                try:
                    # Extract tokens from the response JSON
                    post_list = (await response.json())['web_widgets']['post_list']
                    for post in post_list:
                        token = post['data'].get('token')
                        if token:
                            tokens.append(token)
                except KeyError as e:
                    error_message = f"Error extracting tokens: {e}. Check the structure of the response JSON."
                    logging.error(error_message)
            else:
                error_message = f"Request failed with status code {response.status}"
                logging.error(error_message)

    except Exception as e:
        error_message = f"Error during request: {e}"
        logging.error(error_message)

    return tokens

async def main():
    url = config.URL
    num_requests = config.PAGES_FOR_CRAWL_BATCH_QUANTITY  

    async with aiohttp.ClientSession() as session:
        tasks = []
        for page in range(1, num_requests + 1):
            payload = config.get_payload(page)
            tasks.append(crawl_website(session, url, payload))

        start_time = time.time()
        results = await asyncio.gather(*tasks)
        end_time = time.time()

        # Concatenate the tokens from all requests into a single list
        all_tokens = [token for tokens in results for token in tokens]

        # Insert tokens into the 'tokens' table in the PostgreSQL database
        insert_tokens_into_database(all_tokens)

        # Log the execution time
        execution_time = end_time - start_time
        logging.info(f"Total execution time: {execution_time} seconds")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
