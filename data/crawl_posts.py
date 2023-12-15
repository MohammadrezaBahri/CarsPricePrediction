import traceback
import aiohttp
import asyncio
import logging
import psycopg2
import config
import utils
from datetime import datetime
from psycopg2 import IntegrityError

logging.basicConfig(filename='logs/crawl_posts_log.txt', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')


# Function to insert post data into the 'posts' table
def insert_post_into_database(token, usage, third_party_insurance_deadline, production_year, price,
                               motor_status, brand_model, color, body_status, chassis_status, fuel_type, gearbox):
    try:
        conn = psycopg2.connect(**config.db_params)
        cursor = conn.cursor()

        # Insert post data into the 'posts' table
        cursor.execute("""
            INSERT INTO divar_cars_data.posts
            (token, usage, third_party_insurance_deadline, production_year, price,
            motor_status, brand_model, color, body_status, chassis_status, fuel_type, gearbox, insert_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (token, usage, third_party_insurance_deadline, production_year, price,
              motor_status, brand_model, color, body_status, chassis_status, fuel_type, gearbox, datetime.now()))

        conn.commit()

    except Exception as e:
        raise e  # You may want to log or handle the exception according to your requirements

    finally:
        cursor.close()
        conn.close()

def handle_deleted_token(token:str) -> None:
    try:
        conn = psycopg2.connect(**config.db_params)
        cursor = conn.cursor()

        # Update 'is_deleted' status in the 'divar_cars_data.tokens' table
        cursor.execute(f"""
            UPDATE divar_cars_data.tokens
            SET is_deleted = TRUE
            WHERE token = '{token}'""")

        conn.commit()
    except Exception as e:
        # Log the error
        logging.error(f"Error updating 'is_deleted' status for token {token}: {e}")
    finally:
        cursor.close()
        conn.close()

# Function to get post details from the API for a given token
async def get_post_details(session, token):
    post_url = config.POSTS_URL + token  

    try:
        async with session.get(url=post_url) as response:
            if response.status == 200:
                post_json = await response.json()
                return post_json
            else:
                logging.error(f"Failed to get post details for token {token}. Status code: {response.status}")
                if response.status == 404: handle_deleted_token(token=token)
                return None
    except Exception as e:
        logging.error(f"Error during request for token {token}: {e}")
        return None

# Function to process tokens and insert post data into the database
async def process_tokens(session, tokens):
    for token in tokens:
        post_json = await get_post_details(session, token)
        if post_json:

            post_data = post_json['widgets']['list_data'][0]['items']

            post_data = post_json['widgets']['list_data'][0]['items'] + post_json['widgets']['list_data'][1:]

            items = {item['title']:item['value'] for item in post_data}

            if post_data is not None:
                try:
                    # Extract relevant information from the post_data
                    usage = utils.clean_integer(items.get(config.PostAttributes.usage.value))
                    third_party_insurance_deadline = utils.clean_integer(items.get(config.PostAttributes.third_party_insurance_deadline.value)) if items.get(config.PostAttributes.third_party_insurance_deadline.value) is not None else None
                    production_year = utils.clean_integer(items.get(config.PostAttributes.production_year.value))
                    price = utils.clean_integer(items.get(config.PostAttributes.price.value))
                    motor_status = items.get(config.PostAttributes.motor_status.value)
                    brand_model = items.get(config.PostAttributes.brand_model.value)
                    color = items.get(config.PostAttributes.color.value)
                    body_status = items.get(config.PostAttributes.body_status.value)
                    chassis_status = items.get(config.PostAttributes.chassis_status.value)
                    fuel_type = items.get(config.PostAttributes.fuel_type.value)
                    gearbox = items.get(config.PostAttributes.gearbox.value)

                    # Insert post data into the 'posts' table
                    insert_post_into_database(token, usage, third_party_insurance_deadline, production_year, price,
                                            motor_status, brand_model, color, body_status, chassis_status, fuel_type, gearbox)
                except IntegrityError as e:
                    # Handle duplicate key violation (token already exists in the table)
                    logging.warning(f"Skipping duplicate post data for token {token}")
                except Exception as e:
                    logging.error(f"Error inserting post data for token {token} into the database: {e}")
                    logging.error(traceback.format_exc())

# Main function
async def main():
    # Query the 'tokens' table to retrieve tokens
    tokens_query = "SELECT token FROM divar_cars_data.tokens WHERE is_crawled = FALSE AND is_deleted = FALSE"
    try:
        conn = psycopg2.connect(**config.db_params)
        cursor = conn.cursor()

        cursor.execute(tokens_query)
        tokens = [row[0] for row in cursor.fetchall()]

    except Exception as e:
        logging.error(f"Error querying tokens from the database: {e}")
        return

    finally:
        cursor.close()
        conn.close()

    async with aiohttp.ClientSession() as session:
        await process_tokens(session, tokens)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
