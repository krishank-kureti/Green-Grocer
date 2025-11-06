# screens/charts.py
import customtkinter as ctk
from db import get_connection
import matplotlib.pyplot as plt

class ChartScreen(ctk.CTkFrame):
    def __init__(self, master, role="viewer"):
        super().__init__(master)
        self.role = role
        ctk.CTkLabel(self, text="Charts", font=("Arial", 16)).pack(pady=8)
        ctk.CTkButton(self, text="Farmers per Region", command=self.chart_farmers_per_region).pack(pady=12)

    def chart_farmers_per_region(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT Region.Region_Name, COUNT(Farmer.Farmer_ID) AS cnt
                FROM Region LEFT JOIN Farmer ON Region.Region_ID = Farmer.Region_ID
                GROUP BY Region.Region_ID
            """)
            data = cur.fetchall()
            conn.close()

            labels = [r[0] for r in data]
            values = [r[1] for r in data]

            plt.figure(figsize=(8,5))
            plt.bar(labels, values, color="#8B6F47")
            plt.title("Farmers per Region")
            plt.tight_layout()
            plt.show()
        except Exception as e:
            # avoid calling tk functions here because charts triggered from UI thread
            import tkinter as tk
            tk.messagebox.showerror("Error", str(e))
