import sqlite3

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