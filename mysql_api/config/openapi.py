import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

data_url = 'https://www.fahasa.com/fahasa_catalog/product/loadCatalog?category_id='
url_product_list = 'https://www.fahasa.com/fahasa_catalog/product/loadCatalog?category_id={}&currentPage=1&limit={}&order=num_orders&series_type=0&fbclid=IwAR0rrA5ALIcS4Jq5koZ2mPkQ8zInC7Yp-9TWCYzAxT9b3nwT79pMePv1-ds'

#lấy dữ liệu từ api
def get_data_from_api(url):
    headers = requests.utils.default_headers()
    headers.update(
        {
            'User-Agent': 'My User Agent 1.0',
        }
    )
    response = requests.get(url, headers=headers)
    return response.json()

#bat dong bo
def runner(data, func, max_workers = 1):
    threads= []
    with ThreadPoolExecutor(max_workers) as executor:
        for i in data:
            threads.append(executor.submit(func, i))
        for task in as_completed(threads):
            print(task.result())