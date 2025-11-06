# screens/queries.py
import customtkinter as ctk
from tkinter import ttk
from db import get_connection
from utils import show_error

class QueriesScreen(ctk.CTkFrame):
    def __init__(self, master, role="viewer"):
        super().__init__(master)
        self.role = role
        ctk.CTkLabel(self, text="Advanced SQL Queries", font=("Arial", 16)).pack(pady=10)

        # Frame for buttons
        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(pady=6)

        ctk.CTkButton(btn_frame, text="Join Query", command=self.join_query).pack(side="left", padx=6)
        ctk.CTkButton(btn_frame, text="Nested Query", command=self.nested_query).pack(side="left", padx=6)
        ctk.CTkButton(btn_frame, text="Aggregate Query", command=self.aggregate_query).pack(side="left", padx=6)

        # Treeview for results
        self.tree = ttk.Treeview(self)
        self.tree.pack(fill="both", expand=True, padx=8, pady=8)

        # Label to show explanation text
        self.message_label = ctk.CTkLabel(self, text="", text_color="#444", wraplength=800, justify="center")
        self.message_label.pack(pady=10)

    def run_query(self, query):
        """Executes the given SQL query and displays results in the Treeview."""
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(query)
            rows = cur.fetchall()
            headers = [desc[0] for desc in cur.description] if cur.description else []

            self.tree["columns"] = headers
            self.tree["show"] = "headings"

            # Clear previous headings and data
            for col in headers:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=140)
            self.tree.delete(*self.tree.get_children())

            # Insert new rows
            for r in rows:
                self.tree.insert("", "end", values=r)

            conn.close()
        except Exception as e:
            show_error(str(e))

    def join_query(self):
        q = """
        SELECT f.Farmer_Name AS Farmer, r.Region_Name AS Region
        FROM Farmer f
        JOIN Region r ON f.Region_ID = r.Region_ID
        """
        self.run_query(q)
        self.message_label.configure(
            text="Join Query → Displays each farmer and the region they belong to."
        )

    def nested_query(self):
        q = """
        SELECT Farmer_Name
        FROM Farmer
        WHERE Farmer_ID IN (
            SELECT Farmer_ID
            FROM Farmer_Produce
            WHERE Quantity_Available > 100
        )
        """
        self.run_query(q)
        self.message_label.configure(
            text="Nested Query → Lists farmers whose produce quantity exceeds 100, determined by a subquery."
        )

    def aggregate_query(self):
        q = """
        SELECT r.Region_Name AS Region, COUNT(f.Farmer_ID) AS FarmerCount
        FROM Region r
        LEFT JOIN Farmer f ON r.Region_ID = f.Region_ID
        GROUP BY r.Region_Name
        """
        self.run_query(q)
        self.message_label.configure(
            text="Aggregate Query → Shows each region and the total number of farmers in it."
        )
