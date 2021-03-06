from locale import currency
from wsgiref.handlers import format_date_time
import requests
from bs4 import BeautifulSoup

# html = requests.get("https://m.ifin.kz/bank/alfabank/currency-rate/petropavlovsk?currencyId=RUB")
def currencies_format(cur):
    try:
        usd_buy = cur[0].text.strip()
        usd_sell = cur[1].text.strip()
        eur_buy = cur[2].text.strip()
        eur_sell = cur[3].text.strip()
        rub_buy = cur[4].text.strip()
        rub_sell = cur[5].text.strip()
    except:
        usd_buy = 'Не актуально, попроуйте позже...'
        usd_sell = 'Не актуально, попроуйте позже...'
        eur_buy = 'Не актуально, попроуйте позже...'
        eur_sell = 'Не актуально, попроуйте позже...'
        rub_buy = 'Не актуально, попроуйте позже...'
        rub_sell = 'Не актуально, попроуйте позже...'
    return [usd_buy, usd_sell, eur_buy, eur_sell, rub_buy, rub_sell]
def get_data():
    response = requests.get("https://ifin.kz/exchange/petropavlovsk?sort=sellingPrice3")
    soup = BeautifulSoup(response.text, "html.parser")
    messages = {}
    rows = soup.find_all('div', class_='tbl-row row-toggle company-row')
    for row in rows:
        name = row.find('a', class_='table-row-title')
        url = f'https://ifin.kz{name.get("href")}'
        currencies = row.find_all('div', class_=('tbl-td rate-value', 'tbl-td rate-value best'))
        formated_curs = currencies_format(currencies)
        msg = f"Обменник - {name.text}\n$ ДОЛЛАР $\nПокупка - {formated_curs[0]} тг. | Продажа - {formated_curs[1]} тг.\n€ ЕВРО €\nПокупка - {formated_curs[2]} тг. | Продажа - {formated_curs[3]} тг.\n₱ РУБЛЬ ₱\nПокупка - {formated_curs[4]} тг. | Продажа - {formated_curs[5]} тг.\n\n URL - {url}\nHINT: Перед тем идти обменивать валюту, позвоните в обменный пункт,чтобы уточнить курс. Когда вы окажетесь в обменном пункте, курсы могут измениться"
        messages[str(name.text)]=msg

    return messages
            