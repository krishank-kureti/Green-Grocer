# screens/UserCreateWindow.py
import customtkinter as ctk
from tkinter import messagebox
from db import get_connection
import hashlib

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

class UserCreateWindow(ctk.CTkToplevel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.title("Create User")
        self.geometry("360x260")
        self.resizable(False, False)

        ctk.CTkLabel(self, text="Create Viewer User", font=("Arial", 16)).pack(pady=16)

        self.uname = ctk.CTkEntry(self, placeholder_text="Username")
        self.pwd = ctk.CTkEntry(self, placeholder_text="Password", show="*")

        self.uname.pack(pady=8, padx=20, fill="x")
        self.pwd.pack(pady=8, padx=20, fill="x")

        # ✅ no role dropdown
        # ✅ role always "viewer"
        ctk.CTkButton(self, text="Create User", command=self.create_user).pack(pady=12)

    def create_user(self):
        uname = self.uname.get().strip()
        pwd = self.pwd.get().strip()

        if not uname or not pwd:
            messagebox.showerror("Error", "Please fill all fields")
            return
        if len(pwd) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters")
            return

        try:
            conn = get_connection()
            cur = conn.cursor()

            # ✅ ALWAYS create viewer level users
            cur.execute(
                "INSERT INTO Users (Username, Password, Role) VALUES (%s, %s, %s)",
                (uname, hash_password(pwd), "viewer")
            )

            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Viewer user created!")
            self.destroy()

        except Exception as e:
            messagebox.showerror("Error", str(e))
