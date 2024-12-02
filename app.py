from db_connection_postgres import *
from telegram_connection import *
from dotenv import load_dotenv
from bs4 import BeautifulSoup
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

def parse_page(html: str) -> dict:
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

async def main():
    
    #Criando a conexão com o banco de dados
    conn = create_connection()
    setup_database(conn)

    #Criando a conexão com o Telegram
    bot = configure_telegram_session()
    
    try:
        while True:
            #Carregando, tratando e salvando o dado no banco de dados
            page_content = fetch_page(URL_TO_SCRAPE, USER_AGENT)
            product_info = parse_page(page_content)

            #Pegando o preço e data do valor máximo até então no banco de dados
            max_price, max_timestamp = get_max_price(conn)
            current_price = product_info["new_price"]
            current_timestamp = product_info["created_at"]

            #Caso o preço atual for maior que o maior preço até então mandar uma mensagem pelo telegram
            if max_price is None or current_price > max_price:
                message = f"Preço maior encontrado!: {current_price} em {current_timestamp}" 
                print(message)
                max_price = current_price
                max_timestamp = current_timestamp
            else:
                message = f"O maior preço registrado é {max_price} em {max_timestamp}"
                print(message)

            await send_telegram_message(bot, message=message)

            save_to_database(product_info)
            print(f"Dados Salvo no Banco de Dados!, {product_info}")
            await asyncio.sleep(20)

    except KeyboardInterrupt:
        print("Parando a execução...")

    finally:
        conn.close()

asyncio.run(main=main())