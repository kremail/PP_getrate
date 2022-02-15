"""Request exchange rate from cbr.ru"""

from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup

enddate = datetime.now() + timedelta(days=1)
enddate = enddate.strftime('%d.%m.%Y')
startdate = input("Please enter start date (dd.mm.yyyy): ")
URL = ("https://cbr.ru/currency_base/dynamics/?UniDbQuery.Posted=True&UniDbQuery"
       ".so=1&UniDbQuery.mode=1&UniDbQuery.date_req1=&UniDbQuery.date_req2"
       "=&UniDbQuery.VAL_NM_RQ=R01235&UniDbQuery.From="+startdate+"&UniDbQuery.To="
       + enddate)
r = requests.get(url=URL)
data = []
table = BeautifulSoup(r.text, 'html.parser').find(
    'table', attrs={'class': 'data'})
rows = table.find_all('tr')
for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    data.append(cols)
data = data[2:]
for row in data:
    row[0] = datetime.strptime(row[0], '%d.%m.%Y')
    del row[1]
    row[1] = row[1].replace(",", ".")
    row[1] = float(row[1])
    print(datetime.strftime(row[0], '%d.%m.%y'), " ", row[1])
