import tkinter as tk
from tkinter import ttk, messagebox
from trade_logic import TradeSimulator
from database import DatabaseManager
from visuals import ChartManager

class TradeApp:
    def __init__(self, root: tk.Tk, db_manager: DatabaseManager):
        self.root = root
        self.db = db_manager
        self.simulator = TradeSimulator(self.db)
        
        self.setup_ui()
        self.__refresh_simulation()

    def setup_ui(self):
        #  - Paneles principales - #
        left_panel = ttk.Frame(self.root, padding="10", width=300)
        left_panel.pack(side="left", fill="y")
        
        right_panel = ttk.Frame(self.root, padding="10")
        right_panel.pack(side="right", fill="both", expand=True)

        # - Título - #
        ttk.Label(left_panel, text="Panel de Control", font=("Arial", 14, "bold")).pack(pady=10)

        # - Modificar Tipo de Cambio - #
        ttk.Label(left_panel, text="Modificar Tipo de Cambio (vs USD):").pack(anchor="w", pady=5)
        self.country_combo = ttk.Combobox(left_panel, values=self.__get_country_names())
        self.country_combo.pack(fill="x", pady=2)
        self.fx_entry = ttk.Entry(left_panel)
        self.fx_entry.pack(fill="x", pady=2)
        ttk.Button(left_panel, text="Actualizar T.C.", command=self.__update_fx).pack(fill="x", pady=5)

        ttk.Separator(left_panel, orient='horizontal').pack(fill='x', pady=10)

        # - Modificar Aranceles - #
        ttk.Label(left_panel, text="Modificar Arancel de Ruta:").pack(anchor="w", pady=5)
        self.flow_combo = ttk.Combobox(left_panel, values=self.__get_trade_routes())
        self.flow_combo.pack(fill="x", pady=2)
        self.tariff_entry = ttk.Entry(left_panel)
        self.tariff_entry.pack(fill="x", pady=2)
        ttk.Button(left_panel, text="Actualizar Arancel", command=self.__update_tariff).pack(fill="x", pady=5)

        ttk.Separator(left_panel, orient='horizontal').pack(fill='x', pady=10)

        # - Botón de Simulación General - #
        ttk.Button(left_panel, text="🔄 Ejecutar Simulación", command=self.__refresh_simulation).pack(fill="x", pady=20)

        # - Inicializar Gráficos en el panel derecho - #
        self.chart_manager = ChartManager(right_panel)

    def __get_country_names(self):
        df = self.db.get_dataframe("SELECT name FROM countries")
        return df['name'].tolist() if not df.empty else []

    def __get_trade_routes(self):
        df = self.db.get_dataframe("SELECT id, source_country, dest_country, product FROM trade_flows")
        return [f"{row['id']}: {row['source_country']}->{row['dest_country']} ({row['product']})" for _, row in df.iterrows()]

    def __update_fx(self):
        country: str = self.country_combo.get()
        try:
            new_fx = float(self.fx_entry.get())
            self.db.update_variable('countries', 'exchange_rate_usd', new_fx, 'name', country)
            messagebox.showinfo("Éxito", f"Tipo de cambio de {country} actualizado.")
            self.__refresh_simulation()
        except ValueError:
            messagebox.showerror("Error", "Ingrese un valor numérico válido.")

    def __update_tariff(self):
        route_info: str = self.flow_combo.get()
        if not route_info: return
        route_id = int(route_info.split(":")[0])
        try:
            new_tariff = float(self.tariff_entry.get())
            self.db.update_variable('trade_flows', 'tariff_rate', new_tariff, 'id', route_id)
            messagebox.showinfo("Éxito", "Arancel actualizado exitosamente.")
            self.__refresh_simulation()
        except ValueError:
            messagebox.showerror("Error", "Ingrese un arancel válido (ej. 0.15 para 15%).")

    def __refresh_simulation(self):
        flows_df, balance_df = self.simulator.calculate_trade_metrics()
        self.chart_manager.update_charts(flows_df, balance_df)
