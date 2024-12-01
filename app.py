import requests
import os
from dotenv import load_dotenv

load_dotenv()

URL_TO_SCRAPE = os.getenv('URL_TO_SCRAPE')

def fetch_page(url: str) -> str:
    """
    Alguma docstring
    """
    response = requests.get(url)
    return response.text

if __name__ == "__main__": 
    page_content = fetch_page(URL_TO_SCRAPE)
    print(page_content)