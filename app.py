import bs4
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from db_connection import *
import requests
import pandas as pd
import numpy as np
import os
import time

load_dotenv()

URL_TO_SCRAPE = os.getenv('URL_TO_SCRAPE')
USER_AGENT = os.getenv("USER_AGENT")

def fetch_page(url: str, user_agent: str) -> str:
    """
    Alguma docstring
    """
    response = requests.get(url, headers={"User-Agent": user_agent})
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

    #Sometimes, installment prices is not in the html
    try:
        installment_price = fix_prices_from_html(prices[2])
    except:
        installment_price = np.nan

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    return {
        "product_name": product_name,
        "old_price": old_price,
        "new_price": new_price,
        "installment_price": installment_price,
        "created_at": timestamp
    }

def save_to_database(product_info: dict, conn: sqlite3.Connection) -> None:
    """
    Alguma docstring
    """
    new_row = pd.DataFrame([product_info])
    new_row.to_sql('prices', conn, if_exists='append', index=False)
    

if __name__ == "__main__":
    
    conn = create_connection('iphone_prices.db')
    setup_database(conn)

    while True:
        #Fetch, parse and save the product to a datafrane
        page_content = fetch_page(URL_TO_SCRAPE, USER_AGENT)
        product_info = parse_page(page_content)
        save_to_database(product_info, conn)

        print(f"Dados Salvo no Banco de Dados!, {product_info}")
        time.sleep(10)