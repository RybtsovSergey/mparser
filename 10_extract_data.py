import requests
import config
import pandas as pd
import psycopg
import warnings

warnings.simplefilter(action='ignore', category=UserWarning)  # чтобы пандас не предупреждал о коннекте

def extract(subject_id, summary_raw, cur):
    try:
        subject_top_product_id = summary_raw['top_products']['leaders']['days30'][0]['sku']
        subject_top_product_revenue = summary_raw['top_products']['leaders']['days30'][0]['revenue']
        subject_hhi = int(summary_raw['summary']['monopolization']['hhi'])
        subject_revenue = int(summary_raw['summary']['revenue']['value'])
        revenue_sum = 0
        sales_count = 0
        for seller in summary_raw['top_sellers']:
            revenue_sum += int(seller['revenue'])
            sales_count += int(seller['sales'])
        subject_price_mean = int(revenue_sum / sales_count)



        sql = f"UPDATE subject SET subject_top_product_id=(%s),  subject_top_product_revenue=(%s), subject_hhi=(%s), subject_price_mean=(%s), subject_revenue=(%s) WHERE subject_id = (%s)"
        cur.execute(sql, [subject_top_product_id, subject_top_product_revenue, subject_hhi, subject_price_mean, subject_revenue, subject_id])
        print(subject_id)
    except:
        print(subject_id, 'ошибка')

def main():
    with psycopg.connect(host=config.DB_HOST,
                         port=config.DB_PORT,
                         dbname=config.DB_BASE,
                         user=config.DB_USER,
                         password=config.DB_PASS) as conn:
        with conn.cursor() as cur:
            # определим какие еще остались
            sql = 'select subject_id, subject_summary_raw from subject where subject_summary_raw is NOT NULL ORDER BY subject_id'
            df = pd.read_sql_query(sql, con=conn)
            subject_ids = list(df.subject_id)
            summaries_raw = list(df.subject_summary_raw)
            for i in range(len(summaries_raw)):
                extract(subject_ids[i], summaries_raw[i], cur)


            print('готово')


main()
