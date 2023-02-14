import requests
import json
import pandas as pd
import config as c
import traceback
from datetime import datetime

start = datetime.today()

tokens = []
posts = [] 

for page in range(1, 51):
    
    payload = {
        "json_schema": {
            "category": {"value": c.category},
            "price": {"max": c.max_price,"min": c.min_price},
            "usage": {"max": c.max_usage,"min": c.min_usage},
            "production-year": {"min": c.min_production_year}
            }, 
    "last-post-date":c.last_post_date,
    "page":page}

    try:
        response = requests.post(url = c.url, json = payload)
        data = json.loads(response.content)
        tokens = tokens + ([widget['data']['token'] for widget in data['web_widgets']['post_list']])
    except:
        with open('log.txt', 'a') as f:
            msg = f"{str(datetime.today())}\npage: {page}\n{traceback.format_exc()}{'-'*60}\n"
            f.write(msg)
    if page%5 == 0: print(f"page {page} done.")

missed = []
for token in tokens:

    url = f'https://api.divar.ir/v5/posts/{token}'
    response = requests.get(url)

    try:
        data = json.loads(response.content)
    except:
        with open('log.txt', 'a') as f:
            msg = f"{str(datetime.today())}\ntoken: {token}\n{traceback.format_exc()}{'-'*60}\n"
            f.write(msg)
        missed.append(token)

    try:
        s = [{e['title']: e['value']} for e in data['widgets']['list_data'][0]['items']] + \
            [{e['title']: e['value']} for e in data['widgets']['list_data'][1:]]
        keys = [list(i.keys())[0] for i in s]
        values = [list(i.values())[0] for i in s]

        posts.append([token, dict(zip(keys,values)), data['widgets']['description']])
    
    except KeyError:
        with open('log.txt', 'a') as f:
            msg = f"{str(datetime.today())}\ntoken: {token}\n{traceback.format_exc()}{'-'*60}\n"
            f.write(msg)
        missed.append(token)


try:
    with open('data_new.json', encoding='utf-8') as f:
        data = json.load(f)
        posts = data + posts
except:
    pass

with open('data_new.json', 'w', encoding='utf-8') as f:
    json.dump(posts, f, ensure_ascii=False, indent=4)

print(f"last run: {str(datetime.today())}\nduration: {((datetime.today() - start).seconds)/60} mins")
