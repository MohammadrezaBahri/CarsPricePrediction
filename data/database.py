from datetime import datetime
import traceback

import psycopg2

from crawling_logger import posts_error_logger, tokens_error_logger
from database_config import db_params



def get_tokens_from_database():
    tokens_query = "SELECT token FROM divar_cars_data.tokens WHERE is_crawled = FALSE AND is_deleted < 3"
    
    try:
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cursor:
                cursor.execute(tokens_query)
                tokens = [row[0] for row in cursor.fetchall()]
                return tokens

    except psycopg2.Error as e:
        posts_error_logger.error(f"Error querying tokens from the database: {e}")
        return None

def insert_posts_into_database(posts):
    try:
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cursor:
                values = [
                    (
                        post['token'],
                        post.get('usage', None),
                        post.get('third_party_insurance_deadline', None),
                        post.get('production_year', None),
                        post.get('price', None),
                        post.get('motor_status', None),
                        post.get('brand_model', None),
                        post.get('color', None),
                        post.get('body_status', None),
                        post.get('chassis_status', None),
                        post.get('fuel_type', None),
                        datetime.now()
                    ) for post in posts
                ]

                # Perform insert using executemany
                cursor.executemany("""
                    INSERT INTO divar_cars_data.posts
                    (token, usage, third_party_insurance_deadline, production_year, price,
                    motor_status, brand_model, color, body_status, chassis_status, fuel_type, insert_date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, values)

                conn.commit()

    except Exception as e:
        posts_error_logger.error(f"Error inserting posts into the database: {e}")
        posts_error_logger.error(traceback.format_exc())


def handle_deleted_token(tokens):
    try:
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cursor:
                # Update 'is_deleted' status in the 'divar_cars_data.tokens' table
                cursor.executemany("""
                    UPDATE divar_cars_data.tokens
                    SET is_deleted = is_deleted + 1
                    WHERE token = %s
                """, [(token,) for token in tokens])

                conn.commit()

    except Exception as e:
        posts_error_logger.error(f"Error handling deleted tokens: {e}")
        posts_error_logger.error(traceback.format_exc())

        conn.close()


def insert_tokens_into_database(tokens):
    try:

        with psycopg2.connect(**db_params) as conn, conn.cursor() as cursor:
            cursor.executemany('INSERT INTO divar_cars_data.tokens ("token") VALUES (%s) ON CONFLICT DO NOTHING', 
                               [(token,) for token in tokens])
            conn.commit()

    except Exception as e:
        tokens_error_logger.error(f"Error inserting tokens into the database: {e}")

