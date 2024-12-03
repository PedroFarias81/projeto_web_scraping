import sqlite3
import pandas as pd

def create_connection(db_name: str) -> sqlite3.Connection:
    """
    Função responsável por criar a conexão com o banco de dados
    sqlite3

    Args:
        db_name (str): Nome do banco no qual vai ser criado

    Returns:
        sqlite3.Connection: Conexão com o banco de dados sqlite3
    """
    conn = sqlite3.connect(db_name)
    return conn

def setup_database(conn: sqlite3.Connection) -> None:
    """
    Função responsável por realizar a inicialização do 
    banco de dados a partir de um schema

    Args:
        conn (sqlite3.Connection): Conexão com o banco de dados sqlite3
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
    Função responsável por salvar as informações dentro do banco de dados

    Args:
        product_info (dict): Dicionário contendo os dados a serem inseridos
        conn (sqlite3.Connection): Conexão com o banco de dados sqlite3
    """
    new_row = pd.DataFrame([product_info])
    new_row.to_sql('prices', conn, if_exists='append', index=False)

def get_max_prices(conn: sqlite3.Connection) -> tuple:
    """
    Função responsável por pegar o preço máximo e data cadastrados até então
    """
    cursor = conn.cursor()
    cursor.execute(
        '''
        SELECT MAX(new_price), created_at FROM prices
        '''
    )
    result = cursor.fetchone()
    return result[0], result[1]