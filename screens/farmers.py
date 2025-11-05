import customtkinter as ctk
from tkinter import ttk
from db import get_connection
from utils import show_success, show_error

class FarmersScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        self.tree = ttk.Treeview(self, columns=("id", "name", "size", "contact", "region"))
        self.tree.heading("#0", text="")
        for col,name in zip(("id","name","size","contact","region"),
                            ("ID","Name","Farm Size","Contact","Region")):
            self.tree.heading(col, text=name)
            self.tree.column(col, width=120)
        self.tree.pack(fill="both", expand=True)

        form = ctk.CTkFrame(self)
        form.pack(pady=10)

        self.name = ctk.CTkEntry(form, placeholder_text="Name")
        self.size = ctk.CTkEntry(form, placeholder_text="Farm Size")
        self.contact = ctk.CTkEntry(form, placeholder_text="Contact")
        self.region = ctk.CTkEntry(form, placeholder_text="Region ID")

        for widget in (self.name, self.size, self.contact, self.region):
            widget.pack(pady=5, padx=5, side="left")

        ctk.CTkButton(self, text="Add Farmer", command=self.add_farmer).pack()
        self.load()

    def load(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Farmer")
        rows = cur.fetchall()
        self.tree.delete(*self.tree.get_children())
        for row in rows:
            self.tree.insert("", "end", values=row)
        conn.close()

    def add_farmer(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO Farmer VALUES (%s, %s, %s, %s, %s)",
                (None, self.name.get(), self.size.get(), self.contact.get(), self.region.get())
            )
            conn.commit()
            conn.close()
            show_success("Farmer added!")
            self.load()
        except Exception as e:
            show_error(str(e))
