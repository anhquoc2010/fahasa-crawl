from fastapi import APIRouter
from config.db import conn
from models.product import products
from schemas.schemas import Product
import config.openapi as openapi
from models.category import categories
import pandas as pd

product = APIRouter()

def create_product(product: Product):
    new_product = {"id": product["id"],
                   "product_name": product["product_name"],
                   "product_finalprice": product["product_finalprice"],
                   "product_price": product["product_price"],
                   "type_id": product["type_id"],
                   "type": product["type"],
                   "rating_html": product["rating_html"],
                   "soon_release": product["soon_release"],
                   "product_url": product["product_url"],
                   "image_src": product["image_src"],
                   "discount": product["discount"],
                   "discount_label_html": product["discount_label_html"],
                   "episode": product["episode"],
                   "item_code": product["item_code"] if "item_code" in product else "",
                   "author": product["author"] if "author" in product else "",
                   "publisher": product["publisher"] if "publisher" in product else "",
                   "publish_year": product["publish_year"] if "publish_year" in product else -1,
                   "weight": product["weight"] if "weight" in product else -1,
                   "size": product["size"] if "size" in product else "",
                   "page_number": product["page_number"] if "page_number" in product else -1,
                   "material": product["material"] if "material" in product else "",
                   "specification": product["specification"] if "specification" in product else "",
                   "warning_info": product["warning_info"] if "warning_info" in product else "",
                   "use_guide": product["use_guide"] if "use_guide" in product else "",
                   "translator": product["translator"] if "translator" in product else "",
                   "category_id": product["category_id"]}
    result = conn.execute(products.insert().values(new_product))
    conn.begin()
    return conn.execute(products.select().where(products.c.id == result.lastrowid)).first()

def get_products():
    return conn.execute(products.select()).fetchall()

@product.get("/products", tags=["Product"], response_model=list[Product])
async def get_products_endpoint():
    product_tuples = get_products()
    products = []
    for product_tuple in product_tuples:
        product_dict = {"id": product_tuple[0], "product_name": product_tuple[1], "product_finalprice": product_tuple[2], "product_price": product_tuple[3], "type_id": product_tuple[4], "type": product_tuple[5], "rating_html": product_tuple[6], "soon_release": product_tuple[7], "product_url": product_tuple[8], "image_src": product_tuple[9], "discount": product_tuple[10], "discount_label_html": product_tuple[11], "episode": product_tuple[12],
            "item_code": product_tuple[13], "author": product_tuple[14], "publisher": product_tuple[15], "publish_year": product_tuple[16], "weight": product_tuple[17], "size": product_tuple[18], "page_number": product_tuple[19], "material": product_tuple[20], "specification": product_tuple[21], "warning_info": product_tuple[22], "use_guide": product_tuple[23], "translator": product_tuple[24], "category_id": product_tuple[25]}
        products.append(product_dict)
    return products

def get_product_by_name(name: str):
    return conn.execute(products.select().where(products.c.product_name.like(f"%{name}%"))).fetchall()

@product.get("/products/{name}", tags=["Product"], response_model= list[Product])
def get_product_endpoint(name: str):
    product_tuples = get_product_by_name(name)
    products = []
    for product_tuple in product_tuples:
        product_dict = {"id": product_tuple[0], "product_name": product_tuple[1], "product_finalprice": product_tuple[2], "product_price": product_tuple[3], "type_id": product_tuple[4], "type": product_tuple[5], "rating_html": product_tuple[6], "soon_release": product_tuple[7], "product_url": product_tuple[8], "image_src": product_tuple[9], "discount": product_tuple[10], "discount_label_html": product_tuple[11], "episode": product_tuple[12], "item_code": product_tuple[13], "author": product_tuple[14], "publisher": product_tuple[15], "publish_year": product_tuple[16], "weight": product_tuple[17], "size": product_tuple[18], "page_number": product_tuple[19], "material": product_tuple[20], "specification": product_tuple[21], "warning_info": product_tuple[22], "use_guide": product_tuple[23], "translator": product_tuple[24], "category_id": product_tuple[25]}
        products.append(product_dict)
    return products

def get_products_by_price(min: float, max: float):
    return conn.execute(products.select().where(products.c.product_finalprice.between(min, max))).fetchall()

@product.get("/products/price/", tags=["Product"], response_model=list[Product])
def get_products_by_price_endpoint(min: float, max: float):
    product_tuples = get_products_by_price(min, max)
    products = []
    for product_tuple in product_tuples:
        product_dict = {"id": product_tuple[0], "product_name": product_tuple[1], "product_finalprice": product_tuple[2], "product_price": product_tuple[3], "type_id": product_tuple[4], "type": product_tuple[5], "rating_html": product_tuple[6], "soon_release": product_tuple[7], "product_url": product_tuple[8], "image_src": product_tuple[9], "discount": product_tuple[10], "discount_label_html": product_tuple[11], "episode": product_tuple[12], "item_code": product_tuple[13], "author": product_tuple[14], "publisher": product_tuple[15], "publish_year": product_tuple[16], "weight": product_tuple[17], "size": product_tuple[18], "page_number": product_tuple[19], "material": product_tuple[20], "specification": product_tuple[21], "warning_info": product_tuple[22], "use_guide": product_tuple[23], "translator": product_tuple[24], "category_id": product_tuple[25]}
        products.append(product_dict)
    return products

def get_youngest_child_categories():
    return conn.execute(categories.select().where(categories.c.id.notin_(categories.select().with_only_columns(categories.c.parent_category)))).fetchall()

@product.get("/crawl-products", tags=["Crawl"])
def crawl_products_endpoint(max_qty: int):
    cate_child_id = [i[0] for i in get_youngest_child_categories()]

    old_product_id = [i[0] for i in get_products()]

    new_product_id = []

    new_products = []

    def get_data_product(category_id):
        if max_qty <= len(new_products):
            return "crawl max!"
        try:
            url = openapi.data_url + str(category_id)
            res = openapi.get_data_from_api(url)

            total = res['total_products']
            url = openapi.url_product_list.format(category_id, total)
            df = pd.DataFrame(res['product_list'])
            df.fillna(value=0, inplace=True)
            df['category_id'] = category_id
            df['product_price'] =  [int(str(p).replace('.', '')) for p in df['product_price']]
            df['product_finalprice'] =  [int(str(p).replace('.', '')) for p in df['product_finalprice']]
            df.rename(columns = {'product_id':'id'}, inplace=True)
            df['id'] = pd.to_numeric(df['id'])
            new_data = [row for row in df.to_dict('records') if row['id'] not in old_product_id and row['id'] not in new_product_id]

            qty = max_qty - len(new_products)
            new_products.extend(new_data[:qty])

            cur_ids = df['id'].values.tolist()
            new_ids = [i for i in cur_ids if i not in new_product_id]
            new_product_id.extend(new_ids)
            return "cate_id: {} | product qty of this id: {} | crawl count: {}".format(category_id,total,len(new_products))
        except:
            print("Crawl product error!")

    openapi.runner(cate_child_id, get_data_product)
    openapi.runner(new_products, create_product)

    return {
        "currentProducts": len(old_product_id),
        "new": len(new_products),
        "data": new_products
    }

@product.get("/products/count/", tags=["Product"], response_model= int)
def get_products_count_endpoint():
    return len(get_products())
