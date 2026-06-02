import sqlite3 as sql
import pandas as pd
from pandas._typing import Scalar
from typing import Literal, Any

class DatabaseManager:
    def __init__(self, db_name: str = "trade_sim.db") -> None:
        self.conn: sql.Connection = sql.connect(db_name)
        self.cursor: sql.Cursor = self.conn.cursor()
        self.initialize_database()

    def initialize_database(self) -> None:
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS countries (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE,
                currency TEXT,
                exchange_rate_usd REAL
            );
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE,
                base_price_usd REAL
            );
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS trade_flows (
                id INTEGER PRIMARY KEY,
                source_country TEXT,
                dest_country TEXT,
                product TEXT,
                volume INTEGER,
                tariff_rate REAL,
                freight_cost_usd REAL
            );
        ''')
        self.conn.commit()
        self._seed_data()

    def _seed_data(self) -> None:
        self.cursor.execute("SELECT COUNT(*) FROM countries")
        if self.cursor.fetchone()[0] == 0:
            countries: list[tuple[str, str, float]] = [
                ('Mexico', 'MXN', 17.50), ('USA', 'USD', 1.0),
                ('Brazil', 'BRL', 5.10), ('China', 'CNY', 7.20)
            ]
            self.cursor.executemany("INSERT INTO countries (name, currency, exchange_rate_usd) VALUES (?, ?, ?)", countries)
            
            products: list[tuple[str, float]] = [('Electrónica', 500.0), ('Agricultura', 50.0), ('Vehículos', 25000.0)]
            self.cursor.executemany("INSERT INTO products (name, base_price_usd) VALUES (?, ?)", products)
            
            flows: list[tuple[str,str,str,int,float,float]] = [
                ('China', 'USA', 'Electrónica', 10000, 0.15, 20.0),
                ('Mexico', 'USA', 'Vehículos', 500, 0.0, 500.0),
                ('USA', 'Mexico', 'Agricultura', 50000, 0.05, 5.0),
                ('Brazil', 'China', 'Agricultura', 100000, 0.10, 8.0)
            ]
            self.cursor.executemany("INSERT INTO trade_flows (source_country, dest_country, product, volume, tariff_rate, freight_cost_usd) VALUES (?, ?, ?, ?, ?, ?)", flows)
            self.conn.commit()

    def get_dataframe(self, query: str, params: tuple[Scalar] | list[Scalar] | dict[str, Scalar] = []) -> pd.DataFrame:
        """Retorna un DataFrame basado en un query de SQL."""
        return pd.read_sql_query(query, self.conn, params=params)

    def update_variable(self, table: Literal["countries", "products", "trade_flows"], column: str, value: Any, condition_col: str, condition_val: Any) -> None:
        """Actualiza variables dinámicas como aranceles o tipos de cambio."""

        self.cursor.execute(f"PRAGMA table_info({table});")
        valid_columns: list[str] = [row[1] for row in self.cursor.fetchall()]

        if column not in valid_columns or condition_col not in valid_columns: raise ValueError(f"ERROR! Columna ingresada no válida para la tabla {table}.")

        query: str = f"UPDATE {table} SET {column} = ? WHERE {condition_col} = ?"
        self.cursor.execute(query, (value, condition_val))
        self.conn.commit()

    def close(self):
        self.conn.close()