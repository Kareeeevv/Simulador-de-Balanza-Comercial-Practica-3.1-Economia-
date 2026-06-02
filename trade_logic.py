import pandas as pd
from database import DatabaseManager

class TradeSimulator:
    def __init__(self, db_manager: DatabaseManager) -> None:
        self.db = db_manager

    def calculate_trade_metrics(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        """Calcula el costo final de los productos y la balanza comercial."""

        query: str = """
            SELECT t.source_country, t.dest_country, t.product, t.volume, 
                   t.tariff_rate, t.freight_cost_usd, p.base_price_usd,
                   cs.exchange_rate_usd as source_fx, cd.exchange_rate_usd as dest_fx
            FROM trade_flows t
            JOIN products p ON t.product = p.name
            JOIN countries cs ON t.source_country = cs.name
            JOIN countries cd ON t.dest_country = cd.name
        """
        df: pd.DataFrame = self.db.get_dataframe(query)
        
        if df.empty:
            return df, pd.DataFrame()

        # Costo final en USD = (Precio * (1 + Arancel)) + Flete
        df['final_unit_cost_usd'] = (df['base_price_usd'] * (1 + df['tariff_rate'])) + df['freight_cost_usd']
        df['total_trade_value_usd'] = df['final_unit_cost_usd'] * df['volume']

        # Costo final en moneda local = Costo final en USD * Tipo de cambio local
        df['price_in_dest_currency'] = df['final_unit_cost_usd'] * df['dest_fx']

        # Cálculo principal de la balanza comercial.
        exports: pd.DataFrame = df.groupby('source_country')['total_trade_value_usd'].sum().reset_index()
        exports.columns = ['country', 'total_exports']
        
        imports: pd.DataFrame = df.groupby('dest_country')['total_trade_value_usd'].sum().reset_index()
        imports.columns = ['country', 'total_imports']
        
        balance: pd.DataFrame = pd.merge(exports, imports, on='country', how='outer').fillna(0)
        balance['trade_balance'] = balance['total_exports'] - balance['total_imports']
        
        return df, balance
