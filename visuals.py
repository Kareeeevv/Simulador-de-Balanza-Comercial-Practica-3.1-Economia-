import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pandas import DataFrame, Series
from tkinter.ttk import Frame

class ChartManager:
    def __init__(self, frame: Frame) -> None:
        self.frame = frame
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(6, 8))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def update_charts(self, trade_flows_df: DataFrame, balance_df: DataFrame) -> None:
        self.ax1.clear()
        self.ax2.clear()

        # -- Gráfico 1: Balanza comercial -- #

        if not balance_df.empty:
            colors: list[str] = ['green' if x > 0 else 'red' for x in balance_df['trade_balance']]
            self.ax1.bar(balance_df['country'], balance_df['trade_balance'], color=colors)
            self.ax1.set_title('Balanza Comercial por País (USD)')
            self.ax1.set_ylabel('Balanza (Exp - Imp)')
            self.ax1.axhline(0, color='black', linewidth=1)

        # -- Gráfico 2: Impacto del costo total de IPP -- #

        if not trade_flows_df.empty:
            imports_by_country: Series = trade_flows_df.groupby('dest_country')['total_trade_value_usd'].sum()
            self.ax2.pie(imports_by_country, labels=imports_by_country.index, autopct='%1.1f%%', startangle=90)
            self.ax2.set_title('Distribución de Importaciones por País')

        self.fig.tight_layout()
        self.canvas.draw()
