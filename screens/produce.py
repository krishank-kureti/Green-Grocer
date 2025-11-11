# screens/produce.py
import customtkinter as ctk
from tkinter import ttk
from db import get_connection
from utils import show_success, show_error

class ProduceScreen(ctk.CTkFrame):
    """
    Handles:
      - Produce (master list): Produce_ID, Category, Produce_Name, Shelf_Life
      - Farmer_Produce (harvest): Farmer_Produce_ID, Farmer_ID, Produce_ID, Quantity_Available, Harvest_Date
      - Lookups: fn_get_latest_price, fn_get_available_qty
    Role:
      - admin: full CRUD
      - viewer: view-only + add harvest + lookups
    """
    def __init__(self, master, role="viewer"):
        super().__init__(master)
        self.role = role
        ctk.CTkLabel(self, text="Produce & Harvest Management", font=("Arial", 16)).pack(pady=8)

        # Parent container for the two tables
        top_frame = ctk.CTkFrame(self)
        top_frame.pack(fill="both", expand=True, padx=8, pady=8)

        # ===================== LEFT: PRODUCE =====================
        produce_frame = ctk.CTkFrame(top_frame)
        produce_frame.pack(side="left", fill="both", expand=True, padx=6, pady=6)

        pcols = ("Produce_ID", "Category", "Produce_Name", "Shelf_Life")
        self.produce_tree = ttk.Treeview(produce_frame, columns=pcols, show="headings")
        for c in pcols:
            self.produce_tree.heading(c, text=c)
            self.produce_tree.column(c, width=140)
        self.produce_tree.pack(fill="both", expand=True, padx=6, pady=6)

        # Admin controls for Produce
        if self.role == "admin":
            prod_controls = ctk.CTkFrame(produce_frame)
            prod_controls.pack(pady=6, padx=6, fill="x")

            # Optional explicit Produce ID (if your table expects manual IDs)
            self.p_id = ctk.CTkEntry(prod_controls, placeholder_text="Produce ID (optional)")
            self.p_category = ctk.CTkEntry(prod_controls, placeholder_text="Category")
            self.p_name = ctk.CTkEntry(prod_controls, placeholder_text="Produce Name")
            self.p_shelf = ctk.CTkEntry(prod_controls, placeholder_text="Shelf Life (days)")
            for w in (self.p_id, self.p_category, self.p_name, self.p_shelf):
                w.pack(side="left", padx=6, pady=6, expand=True, fill="x")

            ctk.CTkButton(prod_controls, text="Add Produce", command=self.add_produce).pack(side="left", padx=6)

            btn_frame = ctk.CTkFrame(produce_frame)
            btn_frame.pack(pady=4)
            ctk.CTkButton(btn_frame, text="Update Selected", command=self.update_produce).pack(side="left", padx=6)
            ctk.CTkButton(btn_frame, text="Delete Selected", command=self.delete_produce).pack(side="left", padx=6)

        # ===================== RIGHT: FARMER_PRODUCE =====================
        farmprod_frame = ctk.CTkFrame(top_frame)
        farmprod_frame.pack(side="right", fill="both", expand=True, padx=6, pady=6)

        fpcols = ("Farmer_Produce_ID", "Farmer_ID", "Produce_ID", "Quantity_Available", "Harvest_Date")
        self.fp_tree = ttk.Treeview(farmprod_frame, columns=fpcols, show="headings")
        for c in fpcols:
            self.fp_tree.heading(c, text=c)
            self.fp_tree.column(c, width=140)
        self.fp_tree.pack(fill="both", expand=True, padx=6, pady=6)

        # Add harvest controls (available to all roles)
        hp_frame = ctk.CTkFrame(farmprod_frame)
        hp_frame.pack(pady=6, padx=6, fill="x")

        # Optional explicit Farmer_Produce_ID (if not auto-increment)
        self.hp_id = ctk.CTkEntry(hp_frame, placeholder_text="Farmer_Produce_ID (optional)")
        self.hp_farmer = ctk.CTkEntry(hp_frame, placeholder_text="Farmer ID")
        self.hp_produce = ctk.CTkEntry(hp_frame, placeholder_text="Produce ID")
        self.hp_qty = ctk.CTkEntry(hp_frame, placeholder_text="Quantity")
        self.hp_date = ctk.CTkEntry(hp_frame, placeholder_text="Harvest Date (YYYY-MM-DD, optional)")
        for w in (self.hp_id, self.hp_farmer, self.hp_produce, self.hp_qty, self.hp_date):
            w.pack(side="left", padx=6, pady=6, expand=True, fill="x")
        ctk.CTkButton(hp_frame, text="Add Harvest", command=self.add_harvest).pack(side="left", padx=6)

        # Admin controls for Farmer_Produce (update and delete). Update uses dedicated fields below.
        if self.role == "admin":
            fp_btns = ctk.CTkFrame(farmprod_frame)
            fp_btns.pack(pady=4)
            ctk.CTkButton(fp_btns, text="Delete Harvest", command=self.delete_harvest).pack(side="left", padx=6)

        # Dedicated update fields for harvest (so admin can type new values)
        update_frame = ctk.CTkFrame(farmprod_frame)
        update_frame.pack(pady=6, padx=6, fill="x")
        # These fields are used by admin to update the selected harvest row
        self.upd_qty = ctk.CTkEntry(update_frame, placeholder_text="New Quantity (leave blank to skip)")
        self.upd_date = ctk.CTkEntry(update_frame, placeholder_text="New Harvest Date (YYYY-MM-DD)")
        for w in (self.upd_qty, self.upd_date):
            w.pack(side="left", padx=6, pady=6, expand=True, fill="x")
        if self.role == "admin":
            ctk.CTkButton(update_frame, text="Update Harvest (for selected)", command=self.update_harvest).pack(side="left", padx=6)

        # ===================== BOTTOM SECTION: LOOKUPS =====================
        bottom = ctk.CTkFrame(self)
        bottom.pack(fill="x", padx=8, pady=8)

        # Latest price lookup
        lookup_frame = ctk.CTkFrame(bottom)
        lookup_frame.pack(side="left", fill="x", expand=True, padx=6)
        self.lp_produce = ctk.CTkEntry(lookup_frame, placeholder_text="Produce ID for price")
        self.lp_region = ctk.CTkEntry(lookup_frame, placeholder_text="Region ID for price")
        self.lp_produce.pack(side="left", padx=6, pady=6)
        self.lp_region.pack(side="left", padx=6, pady=6)
        ctk.CTkButton(lookup_frame, text="Get Latest Price", command=self.get_latest_price).pack(side="left", padx=6)

        # Availability lookup
        avail_frame = ctk.CTkFrame(bottom)
        avail_frame.pack(side="left", fill="x", expand=True, padx=6)
        self.av_produce = ctk.CTkEntry(avail_frame, placeholder_text="Produce ID for availability")
        self.av_produce.pack(side="left", padx=6, pady=6)
        ctk.CTkButton(avail_frame, text="Get Available Qty", command=self.get_available_qty).pack(side="left", padx=6)

        # Aggregate availability
        ctk.CTkButton(bottom, text="Show Total Available per Produce", command=self.show_total_available).pack(side="right", padx=6)

        # Message label for feedback
        self.msg = ctk.CTkLabel(self, text="", text_color="#444")
        self.msg.pack(pady=6)

        # Load tables
        self.load_produce()
        self.load_fp()

    # ===================== PRODUCE CRUD =====================
    def load_produce(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT Produce_ID, Category, Produce_Name, Shelf_Life FROM Produce")
            rows = cur.fetchall()
            self.produce_tree.delete(*self.produce_tree.get_children())
            for r in rows:
                self.produce_tree.insert("", "end", values=r)
        except Exception as e:
            show_error(str(e))
        finally:
            try: conn.close()
            except: pass

    def add_produce(self):
        if self.role != "admin":
            show_error("Only admins can add produce.")
            return
        try:
            pid_text = self.p_id.get().strip()
            cat = self.p_category.get().strip()
            name = self.p_name.get().strip()
            life = self.p_shelf.get().strip()

            conn = get_connection()
            cur = conn.cursor()
            if pid_text:
                # explicit ID provided
                cur.execute("INSERT INTO Produce (Produce_ID, Category, Produce_Name, Shelf_Life) VALUES (%s,%s,%s,%s)",
                            (int(pid_text), cat, name, life))
            else:
                # let DB assign ID (AUTO_INCREMENT) or use schema default
                cur.execute("INSERT INTO Produce (Category, Produce_Name, Shelf_Life) VALUES (%s,%s,%s)",
                            (cat, name, life))
            conn.commit()
            conn.close()
            show_success("Produce added successfully.")
            # clear inputs
            try: self.p_id.delete(0, "end")
            except: pass
            self.p_category.delete(0, "end")
            self.p_name.delete(0, "end")
            self.p_shelf.delete(0, "end")
            self.load_produce()
        except Exception as e:
            show_error(str(e))

    def update_produce(self):
        if self.role != "admin":
            show_error("Only admins can update produce.")
            return
        try:
            sel = self.produce_tree.selection()
            if not sel:
                show_error("Select a produce row to update.")
                return
            item = self.produce_tree.item(sel[0])["values"]
            pid = item[0]

            # use a small inline input approach: reuse the admin inputs if filled, otherwise prompt for missing
            new_cat = self.p_category.get().strip() or item[1]
            new_name = self.p_name.get().strip() or item[2]
            new_life = self.p_shelf.get().strip() or item[3]

            conn = get_connection()
            cur = conn.cursor()
            cur.execute("UPDATE Produce SET Category=%s, Produce_Name=%s, Shelf_Life=%s WHERE Produce_ID=%s",
                        (new_cat, new_name, new_life, pid))
            conn.commit()
            conn.close()
            show_success("Produce updated.")
            self.load_produce()
        except Exception as e:
            show_error(str(e))

    def delete_produce(self):
        if self.role != "admin":
            show_error("Only admins can delete produce.")
            return
        try:
            sel = self.produce_tree.selection()
            if not sel:
                show_error("Select a produce row to delete.")
                return
            item = self.produce_tree.item(sel[0])["values"]
            pid = item[0]
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM Produce WHERE Produce_ID=%s", (pid,))
            conn.commit()
            conn.close()
            show_success("Produce deleted.")
            self.load_produce()
        except Exception as e:
            show_error(str(e))

    # ===================== FARMER_PRODUCE =====================
    def load_fp(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT Farmer_Produce_ID, Farmer_ID, Produce_ID, Quantity_Available, Harvest_Date FROM Farmer_Produce")
            rows = cur.fetchall()
            self.fp_tree.delete(*self.fp_tree.get_children())
            for r in rows:
                self.fp_tree.insert("", "end", values=r)
        except Exception as e:
            show_error(str(e))
        finally:
            try: conn.close()
            except: pass

    def add_harvest(self):
        try:
            fpid_text = self.hp_id.get().strip()
            farmer = int(self.hp_farmer.get().strip())
            produce = int(self.hp_produce.get().strip())
            qty = float(self.hp_qty.get().strip())
            date_text = self.hp_date.get().strip()  # optional, expected YYYY-MM-DD

            conn = get_connection()
            cur = conn.cursor()
            if fpid_text:
                # explicit Farmer_Produce_ID provided
                if date_text:
                    cur.execute("INSERT INTO Farmer_Produce (Farmer_Produce_ID, Farmer_ID, Produce_ID, Quantity_Available, Harvest_Date) VALUES (%s,%s,%s,%s,%s)",
                                (int(fpid_text), farmer, produce, qty, date_text))
                else:
                    cur.execute("INSERT INTO Farmer_Produce (Farmer_Produce_ID, Farmer_ID, Produce_ID, Quantity_Available, Harvest_Date) VALUES (%s,%s,%s,%s,NOW())",
                                (int(fpid_text), farmer, produce, qty))
            else:
                # let DB assign ID or use auto increment
                if date_text:
                    cur.execute("INSERT INTO Farmer_Produce (Farmer_ID, Produce_ID, Quantity_Available, Harvest_Date) VALUES (%s,%s,%s,%s)",
                                (farmer, produce, qty, date_text))
                else:
                    cur.execute("INSERT INTO Farmer_Produce (Farmer_ID, Produce_ID, Quantity_Available, Harvest_Date) VALUES (%s,%s,%s,NOW())",
                                (farmer, produce, qty))
            conn.commit()
            conn.close()
            show_success("Harvest added successfully.")
            # clear inputs
            try: self.hp_id.delete(0, "end")
            except: pass
            self.hp_farmer.delete(0, "end")
            self.hp_produce.delete(0, "end")
            self.hp_qty.delete(0, "end")
            self.hp_date.delete(0, "end")
            self.load_fp()
        except Exception as e:
            show_error(str(e))

    def update_harvest(self):
        if self.role != "admin":
            show_error("Only admins can update harvests.")
            return
        try:
            sel = self.fp_tree.selection()
            if not sel:
                show_error("Select a harvest record to update.")
                return
            item = self.fp_tree.item(sel[0])["values"]
            fpid = item[0]

            # prefer explicit values from update fields; if left blank, keep existing
            new_qty_text = self.upd_qty.get().strip()
            new_date_text = self.upd_date.get().strip()

            # if both blank, nothing to do
            if not new_qty_text and not new_date_text:
                show_error("Enter new quantity and/or new harvest date in the update fields.")
                return

            conn = get_connection()
            cur = conn.cursor()
            if new_qty_text and new_date_text:
                cur.execute("UPDATE Farmer_Produce SET Quantity_Available=%s, Harvest_Date=%s WHERE Farmer_Produce_ID=%s",
                            (float(new_qty_text), new_date_text, fpid))
            elif new_qty_text:
                cur.execute("UPDATE Farmer_Produce SET Quantity_Available=%s WHERE Farmer_Produce_ID=%s",
                            (float(new_qty_text), fpid))
            else:  # only date provided
                cur.execute("UPDATE Farmer_Produce SET Harvest_Date=%s WHERE Farmer_Produce_ID=%s",
                            (new_date_text, fpid))
            conn.commit()
            conn.close()
            show_success("Harvest updated.")
            # clear update fields after update
            self.upd_qty.delete(0, "end")
            self.upd_date.delete(0, "end")
            self.load_fp()
        except Exception as e:
            show_error(str(e))

    def delete_harvest(self):
        if self.role != "admin":
            show_error("Only admins can delete harvests.")
            return
        try:
            sel = self.fp_tree.selection()
            if not sel:
                show_error("Select a harvest record to delete.")
                return
            item = self.fp_tree.item(sel[0])["values"]
            fpid = item[0]
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM Farmer_Produce WHERE Farmer_Produce_ID=%s", (fpid,))
            conn.commit()
            conn.close()
            show_success("Harvest deleted.")
            self.load_fp()
        except Exception as e:
            show_error(str(e))

    # ===================== LOOKUPS =====================
    def get_latest_price(self):
        try:
            pid = int(self.lp_produce.get().strip())
            rid = int(self.lp_region.get().strip())
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT fn_get_latest_price(%s,%s)", (pid, rid))
            row = cur.fetchone()
            conn.close()
            val = row[0] if row else None
            self.msg.configure(text=f"Latest price for Produce {pid} in Region {rid}: {val}")
        except Exception as e:
            show_error(str(e))

    def get_available_qty(self):
        try:
            pid = int(self.av_produce.get().strip())
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT fn_get_available_qty(%s)", (pid,))
            row = cur.fetchone()
            conn.close()
            val = row[0] if row else None
            self.msg.configure(text=f"Available quantity for Produce {pid}: {val}")
        except Exception as e:
            show_error(str(e))

    def show_total_available(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT p.Produce_ID, p.Produce_Name, IFNULL(SUM(fp.Quantity_Available),0) AS TotalAvailable
                FROM Produce p
                LEFT JOIN Farmer_Produce fp ON p.Produce_ID = fp.Produce_ID
                GROUP BY p.Produce_ID, p.Produce_Name
            """)
            rows = cur.fetchall()
            conn.close()

            text = "Total available per produce:\n"
            for r in rows:
                text += f"{r[1]} (ID {r[0]}): {r[2]}\n"
            self.msg.configure(text=text)
        except Exception as e:
            show_error(str(e))