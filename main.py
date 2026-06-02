import tkinter as tk
from database import DatabaseManager
from gui import TradeApp

def main():
    db = DatabaseManager("trade_sim.db")

    root = tk.Tk()
    root.title("Simulador Global de Comercio y Divisas")
    root.geometry("1000x700")
    
    app = TradeApp(root, db)

    root.mainloop()

    db.close()

if __name__ == "__main__":
    main()

