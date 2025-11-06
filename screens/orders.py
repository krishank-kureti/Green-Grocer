# screens/orders.py
import customtkinter as ctk
from tkinter import ttk, simpledialog
from db import get_connection
from utils import show_success, show_error

class OrdersScreen(ctk.CTkFrame):
    def __init__(self, master, role="viewer"):
        super().__init__(master)
        self.role = role
        ctk.CTkLabel(self, text="Orders", font=("Arial", 16)).pack(pady=8)

        cols = ("Order_ID", "Buyer_ID", "Farmer_Produce_ID", "Quantity_Purchased", "Contracted")
        self.tree = ttk.Treeview(self, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=120)
        self.tree.pack(fill="both", expand=True, padx=8, pady=8)

        # Both admin and viewer can place orders
        form = ctk.CTkFrame(self)
        form.pack(pady=6, padx=8, fill="x")
        self.buyer = ctk.CTkEntry(form, placeholder_text="Buyer ID")
        self.fpid = ctk.CTkEntry(form, placeholder_text="Farmer Produce ID")
        self.qty = ctk.CTkEntry(form, placeholder_text="Quantity")
        for w in (self.buyer, self.fpid, self.qty):
            w.pack(side="left", padx=6, pady=6, expand=True, fill="x")

        ctk.CTkButton(self, text="Place Order (calls sp_place_order)", command=self.place).pack(pady=6)

        # Admin can Update/Delete orders; viewer cannot
        if self.role == "admin":
            btn_frame = ctk.CTkFrame(self)
            btn_frame.pack(pady=4)
            ctk.CTkButton(btn_frame, text="Delete Selected", command=self.delete_record).pack(side="left", padx=6)
            ctk.CTkButton(btn_frame, text="Update Qty", command=self.update_quantity).pack(side="left", padx=6)

        self.load()

    def load(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT Order_ID, Buyer_ID, Farmer_Produce_ID, Quantity_Purchased, Contracted FROM Orders")
            rows = cur.fetchall()
            self.tree.delete(*self.tree.get_children())
            for r in rows:
                self.tree.insert("", "end", values=r)
        except Exception as e:
            show_error(str(e))
        finally:
            try: conn.close()
            except: pass

    def place(self):
        try:
            buyer = int(self.buyer.get().strip())
            fpid = int(self.fpid.get().strip())
            qty = int(self.qty.get().strip())

            conn = get_connection()
            cur = conn.cursor()
            args = [buyer, fpid, qty, 0, 0]
            cur.callproc("sp_place_order", args)
            conn.commit()
            conn.close()
            show_success("Order placed successfully. Database triggers executed.")
            self.load()
        except Exception as e:
            show_error(str(e))

    def delete_record(self):
        if self.role != "admin":
            show_error("Only admins can delete orders.")
            return
        try:
            sel = self.tree.selection()
            if not sel:
                show_error("Select an order to delete")
                return
            item = self.tree.item(sel[0])["values"]
            oid = item[0]
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM Orders WHERE Order_ID=%s", (oid,))
            conn.commit()
            conn.close()
            show_success("Order deleted")
            self.load()
        except Exception as e:
            show_error(str(e))

    def update_quantity(self):
        if self.role != "admin":
            show_error("Only admins can update orders.")
            return
        try:
            sel = self.tree.selection()
            if not sel:
                show_error("Select an order to update")
                return
            item = self.tree.item(sel[0])["values"]
            oid = item[0]
            new_qty = simpledialog.askinteger("Update", "New Quantity:", initialvalue=item[3], parent=self)
            if new_qty is None:
                return
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("UPDATE Orders SET Quantity_Purchased=%s WHERE Order_ID=%s", (new_qty, oid))
            conn.commit()
            conn.close()
            show_success("Order quantity updated")
            self.load()
        except Exception as e:
            show_error(str(e))
