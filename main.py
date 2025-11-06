# main.py
import customtkinter as ctk
from theme import apply_theme, PRIMARY
from screens.farmers import FarmersScreen
from screens.regions import RegionsScreen
from screens.orders import OrdersScreen
from screens.charts import ChartScreen
from screens.queries import QueriesScreen

apply_theme()

class App(ctk.CTk):
    def __init__(self, role="viewer"):
        super().__init__()
        self.role = role  # "admin" or "viewer"
        self.title("Green-Grocer Management System")
        self.geometry("1000x650")
        self.configure(fg_color="#FFFFFF")

        # Sidebar
        sidebar = ctk.CTkFrame(self, width=180)
        sidebar.pack(side="left", fill="y", padx=8, pady=8)

        # Main container
        self.container = ctk.CTkFrame(self)
        self.container.pack(side="right", fill="both", expand=True, padx=8, pady=8)

        # Buttons
        btns = [
            ("Farmers", self.show_farmers),
            ("Regions", self.show_regions),
            ("Orders", self.show_orders),
            ("Charts", self.show_charts),
            ("Queries", self.show_queries),
        ]
        for text, cmd in btns:
            ctk.CTkButton(sidebar, text=text, command=cmd, fg_color=PRIMARY).pack(pady=8, fill="x")

        # Role label
        if self.role == "admin":
            ctk.CTkLabel(sidebar, text="Admin Mode", text_color="#ff3b30").pack(side="bottom", pady=10)
        else:
            ctk.CTkLabel(sidebar, text="Viewer Mode", text_color="#333333").pack(side="bottom", pady=10)

        self.current_screen = None
        self.show_farmers()

    def load_screen(self, screen_class):
        if self.current_screen:
            self.current_screen.destroy()
        self.current_screen = screen_class(self.container, role=self.role)
        self.current_screen.pack(fill="both", expand=True)

    def show_farmers(self): self.load_screen(FarmersScreen)
    def show_regions(self): self.load_screen(RegionsScreen)
    def show_orders(self): self.load_screen(OrdersScreen)
    def show_charts(self): self.load_screen(ChartScreen)
    def show_queries(self): self.load_screen(QueriesScreen)


def run_app(role="viewer"):
    app = App(role)
    app.mainloop()


if __name__ == "__main__":
    # Launch the login screen which will call run_app(role)
    from screens.login import LoginScreen
    LoginScreen().mainloop()
