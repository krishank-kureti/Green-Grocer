import customtkinter as ctk
from tkinter import ttk
from db import get_connection

class RegionsScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.tree = ttk.Treeview(self, columns=("id","name","climate","soil"))
        for c,n in zip(("id","name","climate","soil"),
                       ("ID","Region","Climate","Soil")):
            self.tree.heading(c,text=n)
            self.tree.column(c,width=120)
        self.tree.pack(fill="both", expand=True)
        self.load()

    def load(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Region")
        rows = cur.fetchall()
        self.tree.delete(*self.tree.get_children())
        for r in rows:
            self.tree.insert("", "end", values=r)
        conn.close()
