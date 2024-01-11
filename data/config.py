from enum import Enum

CITIES = """[
			"1",
			"1706",
			"1707",
			"1708",
			"1709",
			"1710",
			"1711",
			"1712",
			"1713",
			"1714",
			"1715",
			"1716",
			"1717",
			"1718",
			"1719",
			"1720",
			"1721",
			"1722",
			"1738",
			"1739",
			"1740",
			"1751",
			"1752",
			"1753",
			"1754",
			"1758",
			"1759",
			"1760",
			"1761",
			"1762",
			"1763",
			"1764",
			"1765",
			"1766",
			"1767",
			"1768",
			"1769",
			"1770",
			"1771",
			"1772",
			"2",
			"29",
			"774",
			"781",
			"782",
			"783",
			"784",
			"850"
		]"""
CATEGORY = 'light'
LAST_POST_DATE = 0
MIN_PRICE = 10000000
MAX_PRICE = 10000000000
MIN_USAGE = 1
MAX_USAGE = 10000000
MIN_PRODUCTION_YEAR = 1389
BRAND_MODEL_MANUFACTURER_ORIGIN = "domestic"
BUSINESS_TYPE = "personal"
URL = f'https://api.divar.ir/v8/web-search/1/{CATEGORY}'
POSTS_URL = 'https://api.divar.ir/v5/posts/'
PAGES_FOR_CRAWL_BATCH_QUANTITY = 50

def get_payload(page):
    return f"""{{
                "json_schema": {{
                    "brand_model_manufacturer_origin": {{
                        "value": "{BRAND_MODEL_MANUFACTURER_ORIGIN}"
                    }},
                    "category": {{
                        "value": "{CATEGORY}"
                    }},
                    "business-type": {{
                        "value": "{BUSINESS_TYPE}"
                    }},
                    "cities": {CITIES},
                    "price": {{
                        "min": {MIN_PRICE},
                        "max": {MAX_PRICE}
                    }},
                    "production-year": {{
                        "min": {MIN_PRODUCTION_YEAR}
                    }}
                }},
                "last-post-date": {LAST_POST_DATE},
                "page": {page}
            }}"""


class PostAttributes(Enum):
    usage = 'کارکرد'
    third_party_insurance_deadline = 'مهلت بیمهٔ شخص ثالث'
    production_year = 'مدل (سال تولید)'
    price = 'قیمت پایه'
    motor_status = 'وضعیت موتور'
    brand_model = 'برند و تیپ'
    color = 'رنگ'
    body_status = 'وضعیت بدنه'
    chassis_status = 'وضعیت شاسی‌ها'
    fuel_type = 'نوع سوخت'
    gearbox = 'نوع گیربکس'