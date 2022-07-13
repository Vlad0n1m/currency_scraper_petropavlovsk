from locale import currency
from wsgiref.handlers import format_date_time
import requests
from bs4 import BeautifulSoup

# html = requests.get("https://m.ifin.kz/bank/alfabank/currency-rate/petropavlovsk?currencyId=RUB")
response = requests.get("https://ifin.kz/exchange/petropavlovsk")
soup = BeautifulSoup(response.text, "html.parser")
def currencies_format(cur):
    usd_buy = cur[0].text.strip()
    usd_sell = cur[1].text.strip()
    eur_buy = cur[2].text.strip()
    eur_sell = cur[3].text.strip()
    rub_buy = cur[4].text.strip()
    rub_sell = cur[5].text.strip()
    return [usd_buy, usd_sell, eur_buy, eur_sell, rub_buy, rub_sell]

rows = soup.find_all('div', class_='tbl-row row-toggle company-row')
for row in rows:
    name = row.find('a', class_='table-row-title')
    url = f'https://ifin.kz{name.get("href")}'
    currencies = row.find_all('div', class_=('tbl-td rate-value', 'tbl-td rate-value best'))
    formated_curs = currencies_format(currencies)
    msg = f"Обменник - {name.text}\n$ ДОЛЛАР $\nКупить - {formated_curs[0]} тг. | Продать - {formated_curs[1]} тг.\n€ ЕВРО €\nКупить - {formated_curs[2]} тг. | Продать - {formated_curs[3]} тг.\n₱ РУБЛЬ ₱\nКупить - {formated_curs[4]} тг. | Продать - {formated_curs[5]} тг.\n\n URL - {url}"
    print(msg)
    