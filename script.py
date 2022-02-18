"""Request exchange rate from cbr.ru"""

from datetime import datetime as dt
from datetime import timedelta as td
import sqlite3
import requests as rq
from bs4 import BeautifulSoup as bs

conn = sqlite3.connect('data/database.db')
c = conn.cursor()

enddate = dt.now() + td(days=1)
enddate = enddate.strftime('%d.%m.%Y')
c.execute("SELECT date FROM exchangerate")
if c.fetchone() is None:
    startdate = input("Please enter start date (dd.mm.yyyy): ")
else:
    startdate = dt.strftime(dt.strptime(
        c.fetchone()[0], '%Y-%m-%d %X') + td(days=1), '%d.%m.%Y')

if dt.strptime(startdate, '%d.%m.%Y') + td(days=1) < dt.strptime(enddate, '%d.%m.%Y'):
    URL = ("https://cbr.ru/currency_base/dynamics/?UniDbQuery.Posted=True&UniDbQuery"
           ".so=1&UniDbQuery.mode=1&UniDbQuery.date_req1=&UniDbQuery.date_req2"
           "=&UniDbQuery.VAL_NM_RQ=R01235&UniDbQuery.From="+startdate+"&UniDbQuery.To="
           + enddate)
    r = rq.get(url=URL)
    data = []
    table = bs(r.text, 'html.parser').find(
        'table', attrs={'class': 'data'})
    rows = table.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append(cols)
    data = data[2:]
    data.reverse()
    for row in data:
        row[0] = dt.strptime(row[0], '%d.%m.%Y')
        del row[1]
        row[1] = row[1].replace(",", ".")
        row[1] = row[1].replace(" ", "")
        row[1] = float(row[1])
        c.execute("INSERT INTO exchangerate VALUES (:date,:rate)",
                  {'date': row[0], 'rate': row[1]})
        print(dt.strftime(row[0], '%d.%m.%y'), " ", row[1])
conn.commit()
conn.close()
