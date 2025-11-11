import customtkinter as ctk
from theme import apply_theme, PRIMARY

# Screens
from screens.farmers import FarmersScreen
from screens.regions import RegionsScreen
from screens.orders import OrdersScreen
from screens.charts import ChartScreen
from screens.queries import QueriesScreen
from screens.produce import ProduceScreen
from screens.users import UsersScreen  # ✅ added


apply_theme()

class App(ctk.CTk):
    def __init__(self, role="viewer"):
        super().__init__()
        self.role = role  # "admin" or "viewer"
        self.title("Green-Grocer Management System")
        self.geometry("1100x700")
        self.configure(fg_color="#FFFFFF")

        # Sidebar
        sidebar = ctk.CTkFrame(self, width=200)
        sidebar.pack(side="left", fill="y", padx=8, pady=8)

        # Main container where screens load
        self.container = ctk.CTkFrame(self)
        self.container.pack(side="right", fill="both", expand=True, padx=8, pady=8)

        # Sidebar Navigation Buttons
        self.buttons = [
            ("Farmers", self.show_farmers),
            ("Regions", self.show_regions),
            ("Produce", self.show_produce),
            ("Orders", self.show_orders),
            ("Charts", self.show_charts),
            ("Queries", self.show_queries),
        ]

        # Add Users Management screen only for admin
        if self.role == "admin":
            self.buttons.append(("Users", self.show_users))

        # Create Sidebar Buttons
        for text, cmd in self.buttons:
            ctk.CTkButton(sidebar, text=text, command=cmd, fg_color=PRIMARY).pack(pady=8, fill="x")

        # Role Label
        if self.role == "admin":
            ctk.CTkLabel(sidebar, text="Admin Mode", text_color="#ff3b30").pack(side="bottom", pady=10)
        else:
            ctk.CTkLabel(sidebar, text="Viewer Mode", text_color="#333333").pack(side="bottom", pady=10)

        # Track current screen
        self.current_screen = None

        # Show initial screen
        self.show_farmers()

    # Helper to load new screens
    def load_screen(self, screen_class):
        if self.current_screen:
            self.current_screen.destroy()

        # Instantiate screen with role
        self.current_screen = screen_class(self.container, role=self.role)
        self.current_screen.pack(fill="both", expand=True)

    # Screen handler methods
    def show_farmers(self): self.load_screen(FarmersScreen)
    def show_regions(self): self.load_screen(RegionsScreen)
    def show_produce(self): self.load_screen(ProduceScreen)
    def show_orders(self): self.load_screen(OrdersScreen)
    def show_charts(self): self.load_screen(ChartScreen)
    def show_queries(self): self.load_screen(QueriesScreen)
    def show_users(self): self.load_screen(UsersScreen)  # ✅ added


def run_app(role="viewer"):
    app = App(role)
    app.mainloop()


# Entry Point
if __name__ == "__main__":
    from screens.login import LoginScreen
    LoginScreen().mainloop()
