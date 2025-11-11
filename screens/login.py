# screens/login.py
import customtkinter as ctk
from theme import apply_theme
from tkinter import messagebox
from main import run_app
from db import get_connection
from screens.UserCreateWindow import UserCreateWindow  # ✅ use the correct class
import hashlib

apply_theme()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

class LoginScreen(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Green-Grocer Login")
        self.geometry("420x380")
        self.resizable(False, False)

        ctk.CTkLabel(self, text="Login", font=("Arial", 20)).pack(pady=16)

        self.username = ctk.CTkEntry(self, placeholder_text="Username")
        self.password = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.username.pack(pady=8, padx=24, fill="x")
        self.password.pack(pady=8, padx=24, fill="x")

        ctk.CTkButton(self, text="Login", command=self.login).pack(pady=8)
        ctk.CTkButton(self, text="Create New User", command=self.open_user_create).pack(pady=8)

        ctk.CTkLabel(self, text="(Admin can manage users)", text_color="#666666").pack(pady=8)

    def login(self):
        uname = self.username.get().strip()
        pwd = self.password.get().strip()

        if not uname or not pwd:
            messagebox.showerror("Error", "Please enter username and password")
            return

        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT Password, Role FROM Users WHERE Username=%s", (uname,))
            row = cur.fetchone()
            conn.close()

            if not row:
                messagebox.showerror("Error", "User not found")
                return

            stored_hash, role = row
            if hash_password(pwd) != stored_hash:
                messagebox.showerror("Error", "Incorrect password")
                return

            self.destroy()
            run_app(role)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def open_user_create(self):
        # ✅ open the proper dialog; giving parent helps with window focus/centering
        UserCreateWindow(parent=self)
