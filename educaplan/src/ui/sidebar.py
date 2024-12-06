import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttkb

class Sidebar(ttk.Frame):
    def __init__(self, parent, user_role, allowed_categories, on_category_select, **kwargs):
        super().__init__(parent, **kwargs)
        self.user_role = user_role
        self.allowed_categories = allowed_categories
        self.on_category_select = on_category_select
        self.setup_ui()

    def setup_ui(self):
        style = ttkb.Style()
        style.configure("Sidebar.TFrame", background="white")
        self.configure(style="Sidebar.TFrame")

        ttk.Label(self, text="Menu", font=("Helvetica", 16, "bold")).pack(pady=(20, 10))

        self.create_menu_buttons()

    def create_menu_buttons(self):
        for category in self.allowed_categories:
            btn = ttk.Button(self, text=category, style="Sidebar.TButton", command=lambda c=category: self.category_click(c))
            btn.pack(pady=5, padx=10, fill=tk.X)

    def category_click(self, category):
        self.on_category_select(category)

