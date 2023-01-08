from bs4 import BeautifulSoup as BS
import requests
from config import PRICE_URL
import logging


HEADERS = headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def get_html(url: str) -> str:
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code != 200:
        logging.error(f"failed to get html | status code: {resp.status_code}")
        return
    
    return resp.text

def parse_html(html: str) -> list:
    prices = dict()

    soup = BS(html, "lxml")
    price_list = soup.find("div", class_="p-inner ru").select('div[class*="f-"]')
    for item in price_list:
        if not item.get("class"):
            break

        class_fuel_name = item.get("class")[-1]
        fuel_name = class_fuel_name.split("-")[-1]
        price = item.get_text(".", strip=True)
        if fuel_name == "95p":
            formatted_fuel_name = "95 Премиум"
        elif fuel_name == "dt":
            formatted_fuel_name = "ДТ"
        elif fuel_name == "dte":
            formatted_fuel_name = "ДТ Евро"
        else:
            formatted_fuel_name = fuel_name

        prices[formatted_fuel_name] = {"price": float(price), "compare": 0}
    
    return prices


def get_cost() -> dict:
    html = get_html(PRICE_URL)
    cost = parse_html(html)

    return cost
