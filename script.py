from datetime import datetime
import requests
from bs4 import BeautifulSoup

URL = "https://cbr.ru"
r = requests.get(url=URL)
if r.status_code == 200:
    soup = BeautifulSoup(r.text, 'html.parser')
    exchange_rate_t = soup.select_one(
        'div[class^="col-md-2 col-xs-9 _right mono-num"]').text
    exchange_rate_t = exchange_rate_t[0:exchange_rate_t.find(" ")]
    exchange_rate_t = exchange_rate_t.replace(",", ".")
    exchange_rate = float(exchange_rate_t)
    exchange_rate_date_t = soup.select_one(
        'div[class^="col-md-2 col-xs-7 _right"]').text
    exchange_rate_date = datetime.strptime(exchange_rate_date_t, '%d.%m.%Y')
    print(datetime.strftime(exchange_rate_date, '%d.%m.%y'), " ", exchange_rate)
else:
    print("Connection error")
