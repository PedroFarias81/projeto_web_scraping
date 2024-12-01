from dotenv import load_dotenv
import bs4
from bs4 import BeautifulSoup
import requests
import os
import time

load_dotenv()

URL_TO_SCRAPE = os.getenv('URL_TO_SCRAPE')

def fetch_page(url: str) -> str:
    """
    Alguma docstring
    """
    response = requests.get(url)
    return response.text

def fix_prices_from_html(price_tag: bs4.element.Tag) -> int:
    """
    Alguma docstring
    """
    price = price_tag.get_text().replace(".", "")
    return int(price)

def parse_page(html: str) -> str:
    """
    Alguma docstring
    """
    soup = BeautifulSoup(html, "html.parser")
    product_name = soup.find('h1', class_="ui-pdp-title").get_text()
    prices = soup.find_all('span', class_="andes-money-amount__fraction")

    #Getting all the multiple types of price from list of prices
    old_price = fix_prices_from_html(prices[0])
    new_price = fix_prices_from_html(prices[1])
    installment_price = fix_prices_from_html(prices[2])

    return {
        "product_name": product_name,
        "old_price": old_price,
        "new_price": new_price,
        "installment_price": installment_price
    }

if __name__ == "__main__":
    while True:
        page_content = fetch_page(URL_TO_SCRAPE)
        product_info = parse_page(page_content)
        print(product_info)
        time.sleep(10)