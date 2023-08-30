import requests


url = 'https://static-basket-01.wb.ru/vol0/data/subject-base.json'
r  = requests.get(url)
print(r.text)