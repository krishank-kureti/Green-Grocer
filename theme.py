# theme.py
import customtkinter as ctk

PRIMARY = "#8B6F47"      # Brown earthy accent
SECONDARY = "#D9CBB3"    # Sand beige
BG = "#F8F5F0"            # Off-white
TEXT = "#3B3024"

def apply_theme():
    ctk.set_appearance_mode("light")
    # you can give a custom theme name to ctk; we'll keep default and use PRIMARY color for buttons
