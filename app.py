from bs4 import BeautifulSoup
from dotenv import load_dotenv
from db_connection import *
from telegram_connection import *
import pandas as pd
import numpy as np
import requests
import asyncio
import time
import bs4
import os

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

def get_max_prices(conn: sqlite3.Connection):
    """
    Alguma docstring
    """
    cursor = conn.cursor()
    cursor.execute(
        '''
        SELECT MAX(new_price), created_at FROM prices
        '''
    )
    result = cursor.fetchone()
    return result[0], result[1]

async def main():
    
    #Criando a conexão com o banco de dados
    conn = create_connection('iphone_prices.db')
    setup_database(conn)

    #Criando a conexão com o Telegram
    bot = configure_telegram_session()

    while True:

        #Carregando, tratando e salvando o dado no banco de dados
        page_content = fetch_page(URL_TO_SCRAPE, USER_AGENT)
        product_info = parse_page(page_content)
        save_to_database(product_info, conn)

        #Pegando o preço e data do valor máximo até então no banco de dados
        max_price, max_timestamp = get_max_prices(conn)
        current_price = product_info["new_price"]
        current_timestamp = product_info["created_at"]

        #Caso o preço atual for maior que o maior preço até então mandar uma mensagem pelo telegram
        if current_price > max_price:
            print(f"Preço maior encontrado!: {current_price} em {current_timestamp}")
            await send_telegram_message(bot, message=f"Preço maior encontrado!: {current_price} em {current_timestamp}")
            max_price = current_price
            max_timestamp = current_timestamp
        else:
            print(f"O maior preço registrado é {max_price} em {max_timestamp}")
            await send_telegram_message(bot, message=f"O maior preço registrado é {max_price} em {max_timestamp}")

        print(f"Dados Salvo no Banco de Dados!, {product_info}")
        await asyncio.sleep(20)

asyncio.run(main=main())