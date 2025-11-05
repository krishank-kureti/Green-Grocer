import customtkinter as ctk
from tkinter import ttk
from db import get_connection
from utils import show_success, show_error

class OrdersScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.tree = ttk.Treeview(self, columns=("id","buyer","prod","qty","contract"))
        for c,n in zip(("id","buyer","prod","qty","contract"),
                       ("ID","Buyer","Farmer Produce","Qty","Contract")):
            self.tree.heading(c,text=n)
            self.tree.column(c,width=100)
        self.tree.pack(fill="both", expand=True)

        form = ctk.CTkFrame(self)
        form.pack(pady=10)
        self.buyer = ctk.CTkEntry(form, placeholder_text="Buyer ID")
        self.fpid = ctk.CTkEntry(form, placeholder_text="Farmer Produce ID")
        self.qty = ctk.CTkEntry(form, placeholder_text="Qty")

        for f in (self.buyer,self.fpid,self.qty):
            f.pack(side="left", padx=5)

        ctk.CTkButton(self, text="Place Order", command=self.place).pack(pady=5)

        self.load()

    def load(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Orders")
        rows = cur.fetchall()
        self.tree.delete(*self.tree.get_children())
        for r in rows:
            self.tree.insert("", "end", values=r)
        conn.close()

    def place(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            args = [int(self.buyer.get()), int(self.fpid.get()), int(self.qty.get()), None, None]
            cur.callproc("sp_place_order", args)
            conn.commit()
            conn.close()
            show_success("Order placed!")
            self.load()
        except Exception as e:
            show_error(str(e))
