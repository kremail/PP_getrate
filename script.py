import requests
from bs4 import BeautifulSoup

URL = "https://cbr.ru"
data = {}
r = requests.get(url=URL)
if r.status_code == 200:
    soup = BeautifulSoup(r.text, 'html.parser')

exchange_rate = soup.select_one(
    'div[class^="col-md-2 col-xs-9 _right mono-num"]').text
exchange_rate = exchange_rate[0:exchange_rate.find(" ")]
print(exchange_rate)
