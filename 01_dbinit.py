import psycopg
import config
import os

with psycopg.connect(host=config.DB_HOST,
                     port=config.DB_PORT,
                     dbname=config.DB_BASE,
                     user=config.DB_USER,
                     password=config.DB_PASS) as conn:
    with conn.cursor() as cur:
        sql_init_path = os.path.join(os.path.dirname(__file__), '01_dbinit.sql')
        cur.execute(open(sql_init_path, "r").read())
        print('выполнено успешно')