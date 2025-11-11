# screens/regions.py
import customtkinter as ctk
from tkinter import ttk, simpledialog
from db import get_connection
from utils import show_success, show_error

class RegionsScreen(ctk.CTkFrame):
    def __init__(self, master, role="viewer"):
        super().__init__(master)
        self.role = role
        ctk.CTkLabel(self, text="Regions", font=("Arial", 16)).pack(pady=8)

        cols = ("Region_ID", "Region_Name", "Climate", "Soil_Type")
        self.tree = ttk.Treeview(self, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=140)
        self.tree.pack(fill="both", expand=True, padx=8, pady=8)

        # Only Admin can Add / Update / Delete regions
        if self.role == "admin":
            form = ctk.CTkFrame(self)
            form.pack(pady=6, padx=8, fill="x")
            self.rid = ctk.CTkEntry(form, placeholder_text="Region ID")
            self.rname = ctk.CTkEntry(form, placeholder_text="Region Name")
            self.climate = ctk.CTkEntry(form, placeholder_text="Climate")
            self.soil = ctk.CTkEntry(form, placeholder_text="Soil Type")
            for w in (self.rid, self.rname, self.climate, self.soil):
                w.pack(side="left", padx=6, pady=6, expand=True, fill="x")
            ctk.CTkButton(self, text="Add Region", command=self.add_region).pack(pady=6)

            btn_frame = ctk.CTkFrame(self)
            btn_frame.pack(pady=4)
            ctk.CTkButton(btn_frame, text="Update Selected", command=self.update_record).pack(side="left", padx=6)
            ctk.CTkButton(btn_frame, text="Delete Selected", command=self.delete_record).pack(side="left", padx=6)

        self.load()

    def load(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT Region_ID, Region_Name, Climate, Soil_Type FROM Region")
            rows = cur.fetchall()
            self.tree.delete(*self.tree.get_children())
            for r in rows:
                self.tree.insert("", "end", values=r)
        except Exception as e:
            show_error(str(e))
        finally:
            try: conn.close()
            except: pass

    def add_region(self):
        try:
            rid = int(self.rid.get().strip())
            name = self.rname.get().strip()
            climate = self.climate.get().strip()
            soil = self.soil.get().strip()

            conn = get_connection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO Region (Region_ID, Region_Name, Climate, Soil_Type) VALUES (%s,%s,%s,%s)",
                (rid, name, climate, soil)
            )
            conn.commit()
            conn.close()
            show_success("Region added")
            self.load()

            # clear fields
            self.rid.delete(0, "end")
            self.rname.delete(0, "end")
            self.climate.delete(0, "end")
            self.soil.delete(0, "end")

        except Exception as e:
                show_error(str(e))


    def update_record(self):
        try:
            sel = self.tree.selection()
            if not sel:
                show_error("Select a region to update")
                return
            item = self.tree.item(sel[0])["values"]
            rid = item[0]
            new_name = simpledialog.askstring("Update", "Region Name:", initialvalue=item[1], parent=self)
            new_climate = simpledialog.askstring("Update", "Climate:", initialvalue=item[2], parent=self)
            new_soil = simpledialog.askstring("Update", "Soil Type:", initialvalue=item[3], parent=self)

            conn = get_connection()
            cur = conn.cursor()
            cur.execute("UPDATE Region SET Region_Name=%s, Climate=%s, Soil_Type=%s WHERE Region_ID=%s",
                        (new_name, new_climate, new_soil, rid))
            conn.commit()
            conn.close()
            show_success("Region updated")
            self.load()
        except Exception as e:
            show_error(str(e))

    def delete_record(self):
        try:
            sel = self.tree.selection()
            if not sel:
                show_error("Select a region to delete")
                return
            item = self.tree.item(sel[0])["values"]
            rid = item[0]
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM Region WHERE Region_ID=%s", (rid,))
            conn.commit()
            conn.close()
            show_success("Region deleted")
            self.load()
        except Exception as e:
            show_error(str(e))
