# database.py
import streamlit as st
import psycopg2
from psycopg2 import sql
from database_config import db_params

@st.cache_data
def fetch_distinct_values(field_name):
    with psycopg2.connect(**db_params) as conn:
        with conn.cursor() as cursor:
            query = sql.SQL("SELECT DISTINCT field_value FROM divar_cars_data.field_values WHERE field_name = {}").format(sql.Literal(field_name))
            cursor.execute(query)

            values = [value[0] for value in cursor.fetchall()]

            return values


@st.cache_data
def fetch_distinct_brand_models(**kwargs):
    with psycopg2.connect(**db_params) as conn:
        with conn.cursor() as cursor:
            if kwargs.get('brand_model_level2') and kwargs.get('brand_model_level1'):
                # Return brand_model_level3_options based on brand_model_level2
                query = """
                    SELECT DISTINCT brand_model_level3
                    FROM divar_cars_data.brand_models
                    WHERE brand_model_level1 = %s AND brand_model_level2 = %s
                """
                cursor.execute(query, (kwargs['brand_model_level1'], kwargs.get('brand_model_level2')))
                brand_model_level3_options = [row[0] for row in cursor.fetchall()]
                return brand_model_level3_options

            elif kwargs.get('brand_model_level1'):
                # Return brand_model_level2_options based on brand_model_level1
                query = """
                    SELECT DISTINCT brand_model_level2
                    FROM divar_cars_data.brand_models
                    WHERE brand_model_level1 = %s
                """
                cursor.execute(query, (kwargs['brand_model_level1'],))
                brand_model_level2_options = [row[0] for row in cursor.fetchall()]
                return brand_model_level2_options

            else:
                # Return brand_model_level1_options
                query = """
                    SELECT DISTINCT brand_model_level1
                    FROM divar_cars_data.brand_models
                """
                cursor.execute(query)
                brand_model_level1_options = [row[0] for row in cursor.fetchall()]
                return brand_model_level1_options
