import requests
import config
import asyncio
import aiohttp
import datetime
import pandas as pd
import psycopg
import warnings
warnings.simplefilter(action='ignore', category=UserWarning) # чтобы пандас не предупреждал о коннекте


async def get_subject_summary(id, cur):
    try:
        url = f'https://mpstats.io/api/wb/get/subject?d1={config.DATE_BEGIN}&d2={config.DATE_END}&path={id}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url,  cookies=config.MPSTATS_COOKIES, proxy=config.PROXY, timeout=10) as response:
                html = await response.text()
                if response.status != 200:
                    # pass
                    print(response.status, 'некорректный код ответа')
                else:
                    sql = f"UPDATE subject SET subject_products_raw=(%s) WHERE subject_id = (%s)"
                    cur.execute(sql, [html, id])
    except:
        pass


async def main():
    with psycopg.connect(host=config.DB_HOST,
                         port=config.DB_PORT,
                         dbname=config.DB_BASE,
                         user=config.DB_USER,
                         password=config.DB_PASS) as conn:
        with conn.cursor() as cur:
            # определим какие еще остались
            df = pd.read_sql_query('select subject_id from subject where subject_products_raw is NULL', con=conn)
            df = df.sort_values('subject_id')  # только там, где еще не заданы данные
            subject_ids = list(df.subject_id)
            print(datetime.datetime.now(), 'Осталось заполнить:',  len(subject_ids))

            async with asyncio.TaskGroup() as tg:
                for id in subject_ids[:10]:
                    tg.create_task(get_subject_summary(id, cur))


while True:
    try:
        asyncio.run(main())
        print(datetime.datetime.now(), 'сбор завершен - товары')
    except Exception as e:
        print('Ошибка', e)
