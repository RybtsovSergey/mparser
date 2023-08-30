import requests
import config
import psycopg

url = 'https://static-basket-01.wb.ru/vol0/data/subject-base.json'
r = requests.get(url)
subjects = []

for parent in r.json():
    for child in parent['childs']:
        item = {
            'subject_id': child['id'],
            'subject_name': child['name'],
            'subject_full_name': f"{parent['name']} \ {child['name']}",
            'subject_parent_name': parent['name'],
        }
        subjects.append(item)

cols = ', '.join(list(subjects[0].keys()))
placeholders = ', '.join(['%s' for item in list(subjects[0].keys())])
i = 0

with psycopg.connect(host=config.DB_HOST,
                     port=config.DB_PORT,
                     dbname=config.DB_BASE,
                     user=config.DB_USER,
                     password=config.DB_PASS) as conn:
    with conn.cursor() as cur:
        for subject in subjects:
            values = list(subject.values())
            sql = f'INSERT INTO subject ({cols}) VALUES ({placeholders}) ON CONFLICT DO NOTHING'
            cur.execute(sql, values)
            i += 1
            print(i, 'выполнено успешно')

