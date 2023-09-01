import requests
import config
import asyncio
import aiohttp
import datetime
import pandas as pd
import psycopg
import warnings
import json
warnings.simplefilter(action='ignore', category=UserWarning) # чтобы пандас не предупреждал о коннекте


async def parse(id, cur):
    try:
        url = f'https://card.wb.ru/cards/detail?nm={int(id)}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url,  proxy=config.PROXY, timeout=10) as response:
                html = await response.text()
                if response.status != 200:
                    print(response.status, 'некорректный код ответа')
                    return None

                subject_top_product_feedbacks = json.loads(html)['data']['products'][0]['feedbacks']
                sql = f"UPDATE subject SET subject_top_product_feedbacks=(%s) WHERE subject_top_product_id = (%s)"
                cur.execute(sql, [subject_top_product_feedbacks, id])
                # print(id, 'успех')
    except Exception as e:
        pass
        # print(id, 'ошибка', e)


async def main():
    with psycopg.connect(host=config.DB_HOST,
                         port=config.DB_PORT,
                         dbname=config.DB_BASE,
                         user=config.DB_USER,
                         password=config.DB_PASS) as conn:
        with conn.cursor() as cur:
            # определим какие еще остались
            df = pd.read_sql_query('select subject_top_product_id from subject where subject_top_product_feedbacks is NULL ', con=conn)
            df = df.sort_values('subject_top_product_id')  # только там, где еще не заданы данные
            product_ids = list(df.subject_top_product_id)
            product_ids = [int(item) for item in product_ids if item > 0] # для форматирования в дальнейшем
            print(datetime.datetime.now(), 'Осталось заполнить продуктов:',  len(product_ids))

            async with asyncio.TaskGroup() as tg:
                for id in product_ids:
                    tg.create_task(parse(id, cur))


while True:
    asyncio.run(main())
    print(datetime.datetime.now(), 'сбор завершен - сводка')

