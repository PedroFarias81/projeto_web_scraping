from dotenv import load_dotenv
import psycopg2
from sqlalchemy import create_engine
import pandas as pd
import os

load_dotenv()

# Configurações do banco de dados PostgreSQL
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")

# Cria o engine do SQLAlchemy para o PostgreSQL
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
engine = create_engine(DATABASE_URL)

def create_connection() -> psycopg2.extensions.connection:
    """
    Alguma Docstring
    """
    conn = psycopg2.connect(
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT
    )
    return conn

def setup_database(conn: psycopg2.extensions.connection) -> None:
    """
    Alguma Docstring
    """
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS prices (
            id SERIAL PRIMARY KEY,
            product_name TEXT,
            old_price INTEGER,
            new_price INTEGER,
            installment_price INTEGER,
            created_at TIMESTAMP
        )
        """
    )
    conn.commit()
    cursor.close()

def save_to_database(data: dict, table_name='prices'):
    """
    Alguma docstring
    """
    df = pd.DataFrame([data])
    # Usa SQLAlchemy para salvar os dados no PostgreSQL
    df.to_sql(table_name, engine, if_exists='append', index=False)

def get_max_price(conn: psycopg2.extensions.connection) -> tuple:
    """
    Alguma docstring
    """
    cursor = conn.cursor()
    cursor.execute(
        '''
        SELECT 
            new_price, created_at 
        FROM 
            prices 
        WHERE 
            new_price = (SELECT MAX(new_price) FROM prices);
        '''
    )
    result = cursor.fetchone()
    cursor.close()
    #Se não houver dados já cadastrados, retornar None
    if result and result[0] is not None:
        return result[0], result[1]
    return None, None