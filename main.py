import customtkinter as ctk
from theme import apply_theme, PRIMARY
from screens.farmers import FarmersScreen
from screens.regions import RegionsScreen
from screens.orders import OrdersScreen
from screens.charts import ChartScreen

apply_theme()

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Green-Grocer Management System")
        self.geometry("900x600")

        sidebar = ctk.CTkFrame(self, width=180)
        sidebar.pack(side="left", fill="y")

        self.container = ctk.CTkFrame(self)
        self.container.pack(side="right", fill="both", expand=True)

        btns = [
            ("Farmers", self.show_farmers),
            ("Regions", self.show_regions),
            ("Orders", self.show_orders),
            ("Charts", self.show_charts),
        ]
        for text, cmd in btns:
            ctk.CTkButton(sidebar, text=text, command=cmd,
                          fg_color=PRIMARY).pack(pady=10, fill="x")

        self.current_screen = None
        self.show_farmers()

    def load_screen(self, screen_class):
        if self.current_screen:
            self.current_screen.destroy()
        self.current_screen = screen_class(self.container)
        self.current_screen.pack(fill="both", expand=True)

    def show_farmers(self): self.load_screen(FarmersScreen)
    def show_regions(self): self.load_screen(RegionsScreen)
    def show_orders(self): self.load_screen(OrdersScreen)
    def show_charts(self): self.load_screen(ChartScreen)

if __name__ == "__main__":
    App().mainloop()
