import customtkinter as ctk
from db import get_connection
import matplotlib.pyplot as plt

class ChartScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        ctk.CTkButton(self, text="Farmers per Region", command=self.chart).pack(pady=20)

    def chart(self):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT Region.Region_Name, COUNT(Farmer.Farmer_ID)
            FROM Region LEFT JOIN Farmer
            ON Region.Region_ID = Farmer.Region_ID
            GROUP BY Region.Region_ID
        """)

        data = cur.fetchall()
        conn.close()

        labels = [r[0] for r in data]
        values = [r[1] for r in data]

        plt.bar(labels, values, color="#8B6F47")
        plt.title("Farmers per Region")
        plt.show()
