import json
import traceback

import aiohttp

from crawling_logger import posts_error_logger, tokens_error_logger
import config
import utils


async def get_post_details(session, token):
    post_url = config.POSTS_URL + token

    try:
        async with session.get(url=post_url) as response:
            if response.status == 200:
                try:
                    post_data = await response.json()
                    return response.status, post_data
                except json.JSONDecodeError:
                    posts_error_logger.error(f"Error decoding JSON for token {token}")
                    return None, None

            elif response.status == 404:
                return response.status, {'token': token}

            else:
                posts_error_logger.error(f"Failed to get post details for token {token}. Status code: {response.status}")
                return response.status, None

    except aiohttp.ClientError as e:
        posts_error_logger.error(f"Error during request for token {token}: {e}")
        posts_error_logger.error(traceback.format_exc())
        return None, None


async def process_token(session, token):
    try:
        status_code, post_data = await get_post_details(session, token)

        if status_code == 404:
            return status_code, post_data
        
        elif status_code == 200 and post_data:
            post_data = post_data['widgets']['list_data'][0]['items'] + post_data['widgets']['list_data'][1:]
            items = {item['title']: item['value'] for item in post_data}

            if items[config.PostAttributes.brand_model.value].startswith('ون'):
                return None, None

            post_dict = {
                'token': token,
                'usage': utils.clean_integer(items.get(config.PostAttributes.usage.value, None)),
                'third_party_insurance_deadline': utils.clean_integer(items.get(config.PostAttributes.third_party_insurance_deadline.value, None)),
                'production_year': utils.clean_integer(items.get(config.PostAttributes.production_year.value, None)),
                'price': utils.clean_integer(items[config.PostAttributes.price.value]),
                'motor_status': items.get(config.PostAttributes.motor_status.value, None),
                'brand_model': items[config.PostAttributes.brand_model.value],
                'color': items.get(config.PostAttributes.color.value, None),
                'body_status': items.get(config.PostAttributes.body_status.value, None),
                'chassis_status': items.get(config.PostAttributes.chassis_status.value, None),
                'fuel_type': items.get(config.PostAttributes.fuel_type.value, None),
            }

            # post_description = {'token': token, 'description': post_data['widgets']['description']}

            return status_code, post_dict

        else:
            return status_code, None

    except Exception as e:
        posts_error_logger.error(f"Error processing token {token}: {e}")
        posts_error_logger.error(traceback.format_exc())
        return None, None


async def crawl_page(session, page):
    tokens = []
    url = config.URL

    try:
        async with session.post(url=url, data=config.get_payload(page)) as response:
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
                    tokens_error_logger.error(error_message)
            else:
                error_message = f"Request failed with status code {response.status}"
                tokens_error_logger.error(error_message)

    except Exception as e:
        tokens_error_logger.error(f"Error during request: {e}")

    return tokens