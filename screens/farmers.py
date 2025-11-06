# screens/farmers.py
import customtkinter as ctk
from tkinter import ttk, simpledialog
from db import get_connection
from utils import show_success, show_error

class FarmersScreen(ctk.CTkFrame):
    def __init__(self, master, role="viewer"):
        super().__init__(master)
        self.role = role

        ctk.CTkLabel(self, text="Farmers", font=("Arial", 16)).pack(pady=8)

        cols = ("Farmer_ID", "Farmer_Name", "Farm_Size", "Contact_Info", "Region_ID")
        self.tree = ttk.Treeview(self, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=120)
        self.tree.pack(fill="both", expand=True, padx=8, pady=8)

        # Show Add/Edit/Delete only if admin
        if self.role == "admin":
            form = ctk.CTkFrame(self)
            form.pack(pady=6, padx=8, fill="x")

            self.name = ctk.CTkEntry(form, placeholder_text="Name")
            self.size = ctk.CTkEntry(form, placeholder_text="Farm Size")
            self.contact = ctk.CTkEntry(form, placeholder_text="Contact")
            self.region = ctk.CTkEntry(form, placeholder_text="Region ID")
            for w in (self.name, self.size, self.contact, self.region):
                w.pack(side="left", padx=6, pady=6, expand=True, fill="x")

            ctk.CTkButton(self, text="Add Farmer", command=self.add_farmer).pack(pady=6)

            btn_frame = ctk.CTkFrame(self)
            btn_frame.pack(pady=4)
            ctk.CTkButton(btn_frame, text="Update Selected", command=self.update_record).pack(side="left", padx=6)
            ctk.CTkButton(btn_frame, text="Delete Selected", command=self.delete_record).pack(side="left", padx=6)

        self.load()

    def load(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT Farmer_ID, Farmer_Name, Farm_Size, Contact_Info, Region_ID FROM Farmer")
            rows = cur.fetchall()
            self.tree.delete(*self.tree.get_children())
            for r in rows:
                self.tree.insert("", "end", values=r)
        except Exception as e:
            show_error(str(e))
        finally:
            try: conn.close()
            except: pass

    def add_farmer(self):
        try:
            name = self.name.get().strip()
            size = int(self.size.get().strip() or 0)
            contact = int(self.contact.get().strip())
            region = int(self.region.get().strip() or 0)

            conn = get_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO Farmer (Farmer_Name, Farm_Size, Contact_Info, Region_ID) VALUES (%s,%s,%s,%s)",
                        (name, size, contact, region))
            conn.commit()
            conn.close()
            show_success("Farmer added!")
            self.load()
        except Exception as e:
            show_error(str(e))

    def update_record(self):
        try:
            sel = self.tree.selection()
            if not sel:
                show_error("Select a farmer to update")
                return
            item = self.tree.item(sel[0])["values"]
            fid = item[0]

            new_name = simpledialog.askstring("Update", "Name:", initialvalue=item[1], parent=self)
            new_size = simpledialog.askinteger("Update", "Farm Size:", initialvalue=item[2], parent=self)
            new_contact = simpledialog.askinteger("Update", "Contact:", initialvalue=item[3], parent=self)
            new_region = simpledialog.askinteger("Update", "Region ID:", initialvalue=item[4], parent=self)

            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                UPDATE Farmer SET Farmer_Name=%s, Farm_Size=%s, Contact_Info=%s, Region_ID=%s
                WHERE Farmer_ID=%s
            """, (new_name, new_size, new_contact, new_region, fid))
            conn.commit()
            conn.close()
            show_success("Farmer updated")
            self.load()
        except Exception as e:
            show_error(str(e))

    def delete_record(self):
        try:
            sel = self.tree.selection()
            if not sel:
                show_error("Select a farmer to delete")
                return
            item = self.tree.item(sel[0])["values"]
            fid = item[0]
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM Farmer WHERE Farmer_ID=%s", (fid,))
            conn.commit()
            conn.close()
            show_success("Farmer deleted")
            self.load()
        except Exception as e:
            show_error(str(e))
