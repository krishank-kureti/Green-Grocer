# screens/login.py
import customtkinter as ctk
from theme import apply_theme
from tkinter import messagebox
from main import run_app

apply_theme()

class LoginScreen(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Green-Grocer Login")
        self.geometry("420x320")
        self.resizable(False, False)

        ctk.CTkLabel(self, text="Welcome to Green-Grocer", font=("Arial", 18)).pack(pady=16)

        self.username = ctk.CTkEntry(self, placeholder_text="Username")
        self.password = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.username.pack(pady=8, padx=24, fill="x")
        self.password.pack(pady=8, padx=24, fill="x")

        ctk.CTkButton(self, text="Login as Admin", command=lambda: self.login("admin")).pack(pady=8, padx=24, fill="x")
        ctk.CTkButton(self, text="Login as Viewer", command=lambda: self.login("viewer")).pack(pady=4, padx=24, fill="x")

        ctk.CTkLabel(self, text="(Demo login — admin/viewer)", text_color="#666666").pack(pady=8)

    def login(self, role):
        # In an actual app you'd validate credentials. For demo we let the role selection suffice.
        self.destroy()
        run_app(role)
