# utils.py
from tkinter import messagebox

def show_success(msg):
    messagebox.showinfo("Success", msg)

def show_error(msg):
    messagebox.showerror("Error", msg)