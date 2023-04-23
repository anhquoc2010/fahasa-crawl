from fastapi import APIRouter
from config.db import conn
from models.category import categories
from schemas.schemas import Category
import config.openapi as openapi
import pandas as pd

category = APIRouter()

def get_categories():
    return conn.execute(categories.select()).fetchall()

def create_category(category: Category):
    new_category = {"id": category['id'],
                    "name": category['name'],
                    "path": category['path'],
                    "title": category['title'],
                    "description": category['description'],
                    "keywords": category['keywords'],
                    "parent_category": category['parent_category']}
    result = conn.execute(categories.insert().values(new_category))
    conn.begin()
    return conn.execute(categories.select().where(categories.c.id == result.lastrowid)).first()

def crawl_categories():
    old_categories = [i[0] for i in get_categories()]
    new_categories = []
    all_cate_ids = [2]

    def get_cate(data):
        _id, parent_id = data
        response = openapi.get_data_from_api(openapi.data_url + str(_id))
        new_cate = response['category']
        new_cate['parent_category'] = int(parent_id)
        new_cate['id'] = int(new_cate['id'])
        if(new_cate['id'] not in old_categories):
            new_categories.append(new_cate)
            print(new_cate)

        df = pd.DataFrame(response['children_categories'])
        if(not 'id' in df.columns):
            return

        cur_cate_ids = df['id'].values.tolist()
        new_cate_ids = [i for i in cur_cate_ids if i not in all_cate_ids]

        if(new_cate_ids == []):
            return
        all_cate_ids.extend(new_cate_ids)
        next_cate = [[i, _id] for i in new_cate_ids]
        openapi.runner(next_cate, get_cate)

        return

    get_cate([2, 2])
    return new_categories

def insert_multi_categories(categories: list[Category]):
    openapi.runner(categories, create_category)

@category.get("/crawl-categories", tags=["Crawl"])
def crawl_categories_endpoint():
    result = crawl_categories()
    insert_multi_categories(result)
    return result

@category.get("/categories/count/", tags=["Category"], response_model= int)
def get_categories_count_endpoint():
    return len(get_categories())
