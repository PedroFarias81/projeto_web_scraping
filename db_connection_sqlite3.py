import sqlite3
import pandas as pd

def create_connection(db_name: str) -> sqlite3.Connection:
    """
    Alguma docstring
    """
    conn = sqlite3.connect(db_name)
    return conn

def setup_database(conn: sqlite3.Connection) -> None:
    """
    Alguma Docstring
    """
    cursor = conn.cursor()
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT,
            old_price INTEGER,
            new_price INTEGER,
            installment_price FLOAT,
            created_at TEXT
        ) 
        '''
    )

def save_to_database(product_info: dict, conn: sqlite3.Connection) -> None:
    """
    Alguma docstring
    """
    new_row = pd.DataFrame([product_info])
    new_row.to_sql('prices', conn, if_exists='append', index=False)

def get_max_prices(conn: sqlite3.Connection) -> tuple:
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